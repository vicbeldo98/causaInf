from __future__ import division
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")
sns.set_palette("colorblind")
from dowhy import CausalModel
from io import StringIO


def load_csv(csv_content):
    data = StringIO(csv_content)
    dataframe = pd.read_csv(data, sep=",", engine='c', skipinitialspace=True)
    return dataframe


def compute_causal_effect(csv_content, graph, treatment, outcome, adjusted, unobserved):
    data = load_csv(csv_content)
    # TODO: CUANDO HAY MULTIPLES TRATAMIENTOS, FORMATEARLO A LISTA
    model = CausalModel(
        data=data,
        treatment=treatment,
        outcome=outcome,
        graph=graph)

    # TODO: AJUSTARLO A LOS NODOS AJUSTADOS
    # TODO: COMO TRATAR LOS NODOS NO OBSERVADOS
    print('SAVING GRAPH IMAGE\n')
    model.view_model()
    from IPython.display import Image, display
    display(Image(filename="causal_model.png"))
    # Identify causal effect and return target estimands
    print('\nIDENTIFYING ESTIMAND\n')
    identified_estimand = model.identify_effect()
    print(identified_estimand)

    print('\n ESTIMATING')
    estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression", test_significance= True)
    print(estimate)
    print("Causal Estimate is " + str(estimate.value))
    '''refute_result = model.refute_estimate(identified_estimand, estimate, method_name="random_common_cause")
    print('\n REFUTING RESULTS')

    print(refute_result)'''
