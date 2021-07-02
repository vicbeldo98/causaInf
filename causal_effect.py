from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import PolynomialFeatures
import copy
from dowhy.causal_model import CausalModel

CANNOT_FIND_SUITABLE_ESTIMAND = 'Sorry, we can not find a suitable estimand for the adjusted graph variables. To check for the available ones, click on "Compute with options".'
EMPTY_CSV = "No data found on the uploaded csv. Please, select another."
PARSE_ERROR_CSV = "Error parsing the csv. Please, select another."
CSV_ERROR = "Something went wrong with the csv loading. Please, select another."
PROBLEM_CAUSAL_MODEL_MANUAL = "Something went wrong when estimating the Causal Model. Please, make sure that all nodes in the graph have a corresponding csv column, that the graph is directed and acyclic and that treatment and outcome variables are correctly marked on the graph."
CANNOT_FIND_SUITABLE_ESTIMATOR = "Something went wrong with the computed estimator"


def compute_identification_options(data, graph, treatment, outcome):
    import re
    for node in re.findall(r'node\[id "(.*)" label "\1"]', graph):
        if node not in list(data.columns):
            print(data.columns)
            raise Exception('Node %s not found in data provided.' % node)
    data = data.dropna()
    data[treatment].apply(float)
    data[outcome].apply(float)
    if data[treatment].isin([0, 1]).all():
        data = data.astype({treatment: "bool"}, copy=False)
        print("BINARY TREATMENT...")
    else:
        print("NON-BINARY TREATMENT...")

    model = CausalModel(
        data=data,
        treatment=treatment,
        outcome=outcome,
        graph=graph,
        proceed_when_unidentifiable=True,
    )
    identified_estimand = model.identify_effect()
    result = dict(identified_estimand.estimands.items())
    backdoor_dict = identified_estimand.backdoor_variables
    frontdoor_dict = identified_estimand.get_frontdoor_variables()
    del result["iv"]
    if result["frontdoor"] is None:
        del result["frontdoor"]
    else:
        result["frontdoor"]["related_variables"] = frontdoor_dict
    for b in backdoor_dict.keys():
        result[b]["related_variables"] = backdoor_dict[b]
    return result, model, identified_estimand


def estimate_effect_with_estimand_and_estimator(
    model, identified_estimand, estimand_name, estimand_method
):
    try:
        if estimand_method == "econml.dml.DML":
            estimate = model.estimate_effect(
                identified_estimand,
                method_name=estimand_name + ".econml.dml.DML",
                control_value=0,
                treatment_value=1,
                target_units="ate",
                confidence_intervals=False,
                method_params={
                    "init_params": {
                        "model_y": GradientBoostingRegressor(),
                        "model_t": GradientBoostingRegressor(),
                        "model_final": LassoCV(fit_intercept=False),
                        "featurizer": PolynomialFeatures(degree=1, include_bias=False),
                    },
                    "fit_params": {},
                },
            )
            real_estimate = copy.deepcopy(estimate)
            p_value = estimate.test_stat_significance()
            return real_estimate, p_value["p_value"][1]

        elif estimand_method == "linear_regression":
            estimate = model.estimate_effect(
                identified_estimand,
                target_units="ate",
                method_name=estimand_name + "." + estimand_method,
            )
            p_value = estimate.test_stat_significance()["p_value"][0]
            return estimate, p_value

        elif estimand_method == "propensity_score_stratification":
            estimate = model.estimate_effect(
                identified_estimand,
                method_name=estimand_name + "." + estimand_method,
                target_units="ate",
            )
            stratification_estimate = copy.deepcopy(estimate)
            p_value = estimate.test_stat_significance()["p_value"][1]
            print(p_value)
            return stratification_estimate, p_value

        elif estimand_method == "propensity_score_matching":
            estimate = model.estimate_effect(
                identified_estimand,
                method_name=estimand_name + "." + estimand_method,
                target_units="ate",
            )
            matching_estimate = copy.deepcopy(estimate)
            p_value = estimate.test_stat_significance()["p_value"]
            return matching_estimate, p_value

        else:
            raise Exception(CANNOT_FIND_SUITABLE_ESTIMATOR)

    except Exception as e:
        exception_msg = PROBLEM_CAUSAL_MODEL_MANUAL
        raise Exception("{}".format(exception_msg + str(e)))


def compute_estimation_methods(estimand):
    estimation_options = {
        "linear_regression": "Linear Regression",
        "propensity_score_stratification": "Propensity Score Stratification",
        "propensity_score_matching": "Propensity Score Matching",
        "econml.dml.DML": "Double Machine Learning",
    }
    return estimation_options


def refuting_tests(model, identified_estimand, estimate, p_value):

    """Adding a random common cause variable"""
    res_random = model.refute_estimate(
        identified_estimand, estimate, method_name="random_common_cause"
    )

    """Replacing treatment with a random (placebo) variable"""
    res_treatment_placebo = model.refute_estimate(
        identified_estimand,
        estimate,
        method_name="placebo_treatment_refuter",
        placebo_type="permute",
    )

    """Removing a random subset of the data"""
    res_subset = model.refute_estimate(
        identified_estimand,
        estimate,
        method_name="data_subset_refuter",
        subset_fraction=0.9,
    )

    """Bootstrap"""
    res_bootstrap = model.refute_estimate(
        identified_estimand,
        estimate,
        method_name="bootstrap_refuter",
    )

    return {
        "<br>Random common cause</br>": [str(round(res_random.new_effect, 3)), 'Inserts a random common cause and recomputes the causal effect. The estimated effect should be close to the original effect.'],
        "<br>Placebo treatment</br>": [str(round(res_treatment_placebo.new_effect, 3)), 'Substitutes the treatment values with values ​​of a random independent variable. The estimated effect should be close to zero.'],
        "<br>Subset validation</br>": [str(round(res_subset.new_effect, 3)), 'Replaces the given dataset with a randomly selected subset. The estimated effect should be close to the original effect.'],
        "<br>Bootstrap Validation</br>": [str(round(res_bootstrap.new_effect, 3)), 'Replaces the given dataset with a randomly selected samples of the dataset. The estimated effect should be close to the original effect.'],
        "original": str(round(res_random.estimated_effect, 3)),
        "p-value": str(round(p_value, 5))
    }
