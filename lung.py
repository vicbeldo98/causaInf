from __future__ import division

import math

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import PolynomialFeatures

import dowhy
from dowhy import CausalModel


def load_lucas_0():
    return pd.read_csv("LUCAS-EXAMPLE/lucas_little.csv")


def load_lucas_1():
    data = pd.read_csv("lucas1_matlab/lucas1_test.csv")
    results = pd.read_csv("lucas1_matlab/lucas1_train.targets", header=None)
    data["Lung_Cancer"] = results
    data["Lung_Cancer"] = data["Lung_Cancer"].replace(-1, 0)
    return data


data = load_lucas_0()

model = CausalModel(
    data=data,
    treatment=["E"],
    outcome=["D"],
    graph='graph[directed 1 node[id "E" label "E"] \
    node[id "D" label "D"] \
    edge[source "E" target "D"]]'
)

# Identify causal effect and return target estimands
print("\nIDENTIFYING ESTIMAND\n")
identified_estimand = model.identify_effect()
print(identified_estimand)

print("\n ESTIMATING")
dml_estimate = model.estimate_effect(
    identified_estimand,
    method_name="backdoor.econml.dml.DML",
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

print(round(dml_estimate.value, 3))

res_random = model.refute_estimate(
    identified_estimand, dml_estimate, method_name="random_common_cause"
)

print(res_random.new_effect)
