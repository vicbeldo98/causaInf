from __future__ import division
import pandas as pd
from dowhy import CausalModel
from io import StringIO


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


def load_csv(csv_content):
    data = StringIO(csv_content)
    dataframe = pd.read_csv(data, sep=",", engine='c', skipinitialspace=True)
    return dataframe


def compute_causal_effect(csv_content, graph, treatment, outcome, adjusted, unobserved):
    data = load_csv(csv_content)
    model = CausalModel(
        data=data,
        treatment=treatment.split(','),
        outcome=outcome.split(','),
        graph=graph,
        proceed_when_unidentifiable=True)

    
    # TODO: COMO TRATAR LOS NODOS NO OBSERVADOS
    # Identify causal effect and return target estimands
    print('\nIDENTIFYING ESTIMAND\n')
    identified_estimand = model.identify_effect()
    backdoor_dict = identified_estimand.backdoor_variables
    identified_name = None
    for key in backdoor_dict.keys():
        if backdoor_dict[key] == adjusted.split(','):
            identified_name = key

    # TODO: QUÉ HACER CUANDO ESTO PETA, ARREGLARLO
    assert(identified_name is not None)

    print('\n ESTIMATING')
    estimate = model.estimate_effect(identified_estimand, method_name=identified_name + ".linear_regression", test_significance=True)
    return round(estimate.value , 3)
    '''refute_result = model.refute_estimate(identified_estimand, estimate, method_name="random_common_cause")
    print('\n REFUTING RESULTS')

    print(refute_result)'''
