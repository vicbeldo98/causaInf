from flask import Flask, request, render_template, session, json
from flask_session import Session
from causal_effect import estimate_effect_with_estimand_and_estimator, estimate_with_variables, compute_estimands, compute_estimation_methods, refuting_tests
import pandas as pd
import numpy as np


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(__name__)
app.secret_key = 'i-want-to-do-causal-inference'
Session(app)


@app.route("/")
def main_page():
    return render_template('dags.html')


@app.route('/compute-effect-from-graph', methods=['POST'])
def compute_effect_from_graph():
    '''
        If adjusted nodes is a valid adjustment set: 
            Given the graph and its adjusted nodes, it returns the computed causal effect (ATE) of the treatment on the outcome, 
            adjusting on the adjusted nodes and using econml gradient boosting.
    '''
    check_required_variables(request.form['treatment'], request.form['outcome'])
    causal_effect = estimate_with_variables(session['csv_content'], request.form['graph'], request.form['treatment'], request.form['outcome'], request.form['adjusted'])
    return {'treatment' : request.form['treatment'], 'outcome' : request.form['outcome'], 'effect' : round(causal_effect.value, 3)}


@app.route('/retrieve-estimands', methods=['POST'])
def retrieve_estimands():
    check_required_variables(request.form['treatment'], request.form['outcome'])
    session['treatment'] = request.form['treatment']
    session['outcome'] = request.form['outcome']
    causal_estimands, session['model'], session['identified_estimand'] = compute_estimands(session['csv_content'], request.form['graph'], request.form['treatment'], request.form['outcome'])
    return json.dumps(dict(causal_estimands), default=str)


@app.route('/compute-effect-with-estimand-and-estimator', methods=['POST'])
def compute_effect_with_estimand_and_estimator():
    estimate = estimate_effect_with_estimand_and_estimator(session['model'], session['identified_estimand'], request.form['estimand_name'], request.form['estimation_method'])
    session['estimate'] = estimate
    return {'treatment' : session['treatment'], 'outcome' : session['outcome'], 'effect' : round(estimate.value, 3)}


@app.route('/compute-estimation-methods', methods=['POST'])
def compute_available_estimation_methods():
    estimation_methods = compute_estimation_methods(request.form['estimand_name'])
    return dict(estimation_methods)


@app.route('/refutation-tests', methods=['POST'])
def refutation():
    return dict(refuting_tests(session['model'], session['identified_estimand'], session['estimate']))


@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    all_data = request.form['file-content'].split('\r\n')
    columns = all_data[0].split(',')
    data = []
    for row in all_data[1:-1]:
        data.append([np.nan if element == '' else float(element) for element in row.split(',')])
    df = pd.DataFrame(data, columns=columns)
    session['csv_content'] = df
    return '', 200


'''@app.errorhandler(Exception)
def handle_exception(e):
    return str(e), 500'''


def check_required_variables(treatment, outcome):
    if 'csv_content' not in session.keys():
        raise Exception('No csv file found. Please, upload one first.')
    if treatment == '':
        raise Exception('Create exposure variables on the graph')
    elif len(treatment.split(",")) > 1:
        raise Exception('Just one exposure variable allowed')

    if outcome == '':
        raise Exception('Create outcome variable on the graph')
    elif len(outcome.split(",")) > 1:
        raise Exception('Just one outcome variable allowed')


app.run(debug=True)
