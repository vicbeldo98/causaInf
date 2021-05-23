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
    return pd.read_csv("LUCAS-EXAMPLE/lucas.csv")


def load_lucas_1():
    data = pd.read_csv("lucas1_matlab/lucas1_test.csv")
    results = pd.read_csv("lucas1_matlab/lucas1_train.targets", header=None)
    data["Lung_Cancer"] = results
    data["Lung_Cancer"] = data["Lung_Cancer"].replace(-1, 0)
    return data


data = load_lucas_0()

model = CausalModel(
    data=data,
    treatment=["Smoking"],
    outcome=["Lung_Cancer"],
    graph='graph[directed 1 node[id "Smoking" label "Smoking"] \
    node[id "Yellow_Fingers" label "Yellow_Fingers"] \
    node[id "Anxiety" label "Anxiety"] \
    node[id "Peer_Pressure" label "Peer_Pressure"] \
    node[id "Genetics" label "Genetics"] \
    node[id "Attention_Disorder" label "Attention_Disorder"] \
    node[id "Born_an_Even_Day" label "Born_an_Even_Day"] \
    node[id "Car_Accident" label "Car_Accident"] \
    node[id "Fatigue" label "Fatigue"] \
    node[id "Allergy" label "Allergy"] \
    node[id "Coughing" label "Coughing"] \
    node[id "Lung_Cancer" label "Lung_Cancer"] \
    edge[source "Anxiety" target "Smoking"] \
    edge[source "Peer_Pressure" target "Smoking"] \
    edge[source "Smoking" target "Yellow_Fingers"] \
    edge[source "Smoking" target "Lung_Cancer"] \
    edge[source "Genetics" target "Lung_Cancer"] \
    edge[source "Genetics" target "Attention_Disorder"] \
    edge[source "Allergy" target "Coughing"] \
    edge[source "Coughing" target "Fatigue"] \
    edge[source "Attention_Disorder" target "Car_Accident"] \
    edge[source "Fatigue" target "Car_Accident"] \
    edge[source "Lung_Cancer" target "Coughing"] \
    edge[source "Lung_Cancer" target "Fatigue"]]',
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

print(res_random)
