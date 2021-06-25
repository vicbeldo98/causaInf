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

graph = 'graph[directed 1 node[id "Alergia" label "Alergia"] \
    node[id "Ansiedad" label "Ansiedad"] \
    node[id "Cancer_Pulmon" label "Cancer_Pulmon"] \
    node[id "Dedos_Amarillos" label "Dedos_Amarillos"] \
    node[id "Deficit_Atencion" label "Deficit_Atencion"] \
    node[id "Fatiga" label "Fatiga"] \
    node[id "Fumar" label "Fumar"] \
    node[id "Genetica" label "Genetica"] \
    node[id "Nacido_Dia_Par" label "Nacido_Dia_Par"] \
    node[id "Presion_Social" label "Presion_Social"] \
    node[id "Toser" label "Toser"] \
    node[id "Accidente_Coche" label "Accidente_Coche"] \
    edge[source "Alergia" target "Toser"] \
    edge[source "Ansiedad" target "Fumar"] \
    edge[source "Cancer_Pulmon" target "Fatiga"] \
    edge[source "Cancer_Pulmon" target "Toser"] \
    edge[source "Fumar" target "Cancer_Pulmon"] \
    edge[source "Fumar" target "Dedos_Amarillos"] \
    edge[source "Genetica" target "Cancer_Pulmon"] \
    edge[source "Genetica" target "Deficit_Atencion"] \
    edge[source "Presion_Social" target "Fumar"] \
    edge[source "Toser" target "Fatiga"]]'

little_graph = 'graph[directed 1 node[id "A" label "A"] \
    node[id "B" label "B"] \
    node[id "C" label "C"] \
    node[id "D" label "D"] \
    edge[source "A" target "B"] \
    edge[source "B" target "C"] \
    edge[source "D" target "B"] \
    edge[source "D" target "C"]]'

model = CausalModel(
    data=data,
    treatment=["A"],
    outcome=["C"],
    graph=little_graph
)

# Identify causal effect and return target estimands
print("\nIDENTIFYING ESTIMAND\n")
identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)
print(identified_estimand)

'''print("\n ESTIMATING")
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

"""res_random = model.refute_estimate(
    identified_estimand, dml_estimate, method_name="random_common_cause"
)"""

"""Bootstrap"""
res_bootstrap = model.refute_estimate(
    identified_estimand,
    dml_estimate,
    method_name="dummy_outcome_refuter",
    placebo_type="permute",
)
print(res_bootstrap)
print(res_bootstrap[0].new_effect)
'''