import pandas as pd
from dowhy.causal_model import CausalModel
from io import StringIO
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LassoCV
from sklearn.ensemble import GradientBoostingRegressor
import json

CANNOT_FIND_SUITABLE_ESTIMAND = 'Sorry, we can not find a suitable estimand for the adjusted graph variables. To check for the available ones, click on "Compute with options".'
EMPTY_CSV = 'No data found on the uploaded csv. Please, select another.'
PARSE_ERROR_CSV = 'Error parsing the csv. Please, select another.'
CSV_ERROR = 'Something went wrong with the csv loading. Please, select another.'
PROBLEM_CAUSAL_MODEL_GRAPH = 'Something went wrong when estimating the Causal Model. Please, make sure that all nodes in the graph have a corresponding csv column, that the graph is directed and acyclic and that treatment and outcome variables are correctly marked on the graph.'
PROBLEM_CAUSAL_MODEL_MANUAL = 'Something went wrong when estimating the Causal Model.'


def load_csv(csv_content):
    try:
        data = StringIO(csv_content)
        dataframe = pd.read_csv(data, sep=",", engine='c', skipinitialspace=True)
        return dataframe
    except pd.errors.EmptyDataError:
        raise Exception('{}'.format(EMPTY_CSV))
    except pd.errors.ParserError:
        raise Exception('{}'.format(PARSE_ERROR_CSV))
    except Exception:
        raise Exception('{}'.format(CSV_ERROR))


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
    if iv_estimands == []:
        del result['iv']
    else:
        result['iv']['related_variables'] = iv_estimands
    for b in backdoor_dict.keys():
        result[b]['related_variables'] = backdoor_dict[b]
    return result, model, identified_estimand


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
    try:
        data = load_csv(csv_content)
        model = CausalModel(
            data=data,
            treatment=treatment.split(","),
            outcome=outcome.split(','),
            graph=graph,
            proceed_when_unidentifiable=True)
        identified_estimand = model.identify_effect()
        estimand_name = retrieveCorrespondingEstimand(identified_estimand, treatment, outcome, adjusted)
        if estimand_name is None:
            raise Exception(CANNOT_FIND_SUITABLE_ESTIMAND)
        causal_effect = estimate_effect_with_estimand(model, identified_estimand, estimand_name, True)
        return causal_effect
    except Exception as e:
        raise Exception('{}'.format(e))


def estimate_effect_with_estimand(model, identified_estimand, estimand_name, from_graph=False):
    try:
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
    except Exception:
        if from_graph:
            exception_msg = PROBLEM_CAUSAL_MODEL_GRAPH
        else:
            exception_msg = PROBLEM_CAUSAL_MODEL_MANUAL
        raise Exception('{}'.format(exception_msg))
