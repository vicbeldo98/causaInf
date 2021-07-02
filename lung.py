from __future__ import division

import math

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import PolynomialFeatures

from dowhy import CausalModel
from dowhy.causal_refuters import CausalRefuter


def load_lucas_0():
    return pd.read_csv("LUCAS-EXAMPLE/lucas.csv")


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
    node[id "Presion_Grupo" label "Presion_Grupo"] \
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
    edge[source "Presion_Grupo" target "Fumar"] \
    edge[source "Toser" target "Fatiga"]]'


model = CausalModel(
    data=data,
    treatment=["Fumar"],
    outcome=["Cancer_Pulmon"],
    graph=graph
)

# Identify causal effect and return target estimands
print("\nIDENTIFYING ESTIMAND\n")
identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)
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

print(dml_estimate.test_stat_significance())
print(dml_estimate.value)

# print(res_random.test_significance(estimate=dml_estimate, simulations=['random_common_cause'], test_type='auto', significance_level=0.05))
"""Bootstrap"""
'''res_bootstrap = model.refute_estimate(
    identified_estimand,
    dml_estimate,
    method_name="dummy_outcome_refuter",
    placebo_type="permute",
)
print(res_bootstrap)
print(res_bootstrap[0].new_effect)
'''
