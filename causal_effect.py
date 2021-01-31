import pandas as pd
from dowhy.causal_model import CausalModel
from io import StringIO
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LassoCV
from sklearn.ensemble import GradientBoostingRegressor
import json


def load_csv(csv_content):
    data = StringIO(csv_content)
    dataframe = pd.read_csv(data, sep=",", engine='c', skipinitialspace=True)
    return dataframe


def compute_estimands(csv_content, graph, treatment, outcome):
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


def compute_causal_effect(csv_content, graph, treatment, outcome, adjusted):
    data = load_csv(csv_content)
    model = CausalModel(
        data=data,
        treatment=treatment.split(','),
        outcome=outcome.split(','),
        graph=graph,
        proceed_when_unidentifiable=True)
    
    identified_estimand = model.identify_effect()
    adjusted = json.loads(adjusted)
    # Check which estimand is the one fitting the user
    estimand_name = None
    # Backdoor
    backdoor_dict = identified_estimand.backdoor_variables
    print(backdoor_dict)
    for key in backdoor_dict.keys():
        print('LALA')
        print(backdoor_dict[key])
        print(adjusted)

        if backdoor_dict[key] == adjusted:
            print('I ENTER HERE')
            estimand_name = key
            print(estimand_name)

    # Frontdoor
    frontdoor_var = identified_estimand.get_frontdoor_variables()
    print(frontdoor_var)
    print('FRONTDOOR DICT')
    if frontdoor_var != [] and frontdoor_var == adjusted:
        estimand_name = 'frontdoor'

    # IV
    print('iv')
    instr_var = identified_estimand.get_instrumental_variables()
    if instr_var != [] and instr_var == adjusted:
        estimand_name = 'iv'
    # TODO: GESTIONAR ERROR QUÉ HACER CUANDO ESTO PETA, ARREGLARLO

    print('ESTIMAND NAME')
    print(estimand_name)
    print('\n ESTIMATING')
    dml_estimate = model.estimate_effect(identified_estimand,
                                         method_name = estimand_name + ".econml.dml.DML",
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
