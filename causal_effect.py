import pandas as pd
from dowhy.causal_model import CausalModel
from io import StringIO
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LassoCV
from sklearn.ensemble import GradientBoostingRegressor
import json

CANNOT_FIND_SUITABLE_ESTIMAND = 'Sorry, we can not find a suitable estimand for the selected variables. To check the available ones, click on "Compute manually"'


def load_csv(csv_content):
    try:
        data = StringIO(csv_content)
        dataframe = pd.read_csv(data, sep=",", engine='c', skipinitialspace=True)
        return dataframe
    except BaseException as e:
        raise Exception('{}'.format(e))


def compute_estimands(csv_content, graph, treatment, outcome):
    try:
        data = load_csv(csv_content)
        model = CausalModel(
            data=data,
            treatment=treatment.split(','),
            outcome=outcome.split(','),
            graph=graph,
            proceed_when_unidentifiable=True
        )
        identified_estimand = model.identify_effect()
        result = dict(identified_estimand.estimands.items())
        backdoor_dict = identified_estimand.backdoor_variables
        frontdoor_dict = identified_estimand.get_frontdoor_variables()
        iv_estimands = identified_estimand.get_instrumental_variables()
        if result['frontdoor'] is None:
            del result['frontdoor']
        else:
            result['frontdoor']['related_variables'] = frontdoor_dict
        if iv_estimands != []:
            result['iv']['related_variables'] = iv_estimands
        for b in backdoor_dict.keys():
            result[b]['related_variables'] = backdoor_dict[b]
        return result, model, identified_estimand
    except BaseException as e:
        raise Exception('{}'.format(e))


def retrieveCorrespondingEstimand(identified_estimand, treatment, outcome, adjusted):
    estimand_name = None
    adjusted = json.loads(adjusted)
    backdoor_dict = identified_estimand.backdoor_variables
    for key in backdoor_dict.keys():
        if backdoor_dict[key] == adjusted:
            estimand_name = key
    if estimand_name is None:
        frontdoor_var = identified_estimand.get_frontdoor_variables()
        if frontdoor_var != [] and frontdoor_var == adjusted:
            estimand_name = 'frontdoor'
    if estimand_name is None:
        instr_var = identified_estimand.get_instrumental_variables()
        if instr_var != [] and instr_var == adjusted:
            estimand_name = 'iv'

    return estimand_name


def estimate_with_variables(csv_content, graph, treatment, outcome, adjusted):
    data = load_csv(csv_content)
    model = CausalModel(
        data=data,
        treatment=treatment.split(','),
        outcome=outcome.split(','),
        graph=graph,
        proceed_when_unidentifiable=True)

    identified_estimand = model.identify_effect()
    estimand_name = retrieveCorrespondingEstimand(identified_estimand, treatment, outcome, adjusted)
    if estimand_name is None:
        raise Exception(CANNOT_FIND_SUITABLE_ESTIMAND)
    causal_effect = estimate_effect_with_estimand(model, identified_estimand, estimand_name)

    return causal_effect


def estimate_effect_with_estimand(model, identified_estimand, estimand_name):
    dml_estimate = model.estimate_effect(identified_estimand,
                                         method_name=estimand_name + ".econml.dml.DML",
                                         control_value=0,
                                         treatment_value=1,
                                         target_units="ate",
                                         confidence_intervals=False,
                                         method_params={"init_params": {'model_y': GradientBoostingRegressor(),
                                                                        'model_t': GradientBoostingRegressor(),
                                                                        "model_final": LassoCV(fit_intercept=False),
                                                                        'featurizer': PolynomialFeatures(degree=1, include_bias=False)},
                                                        "fit_params": {}}
                                         )
    return round(dml_estimate.value, 3)
