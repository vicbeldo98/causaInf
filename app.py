from flask import Flask, request, render_template, session
from flask_session import Session
from causal_effect import estimate_effect_with_estimand, estimate_with_variables, compute_estimands
import json


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
    causal_effect = estimate_with_variables(session['csv_content'], request.form['graph'], request.form['treatment'], request.form['outcome'], request.form['adjusted'])
    return {'treatment' : request.form['treatment'], 'outcome' : request.form['outcome'], 'effect' : causal_effect}


@app.route('/retrieve-estimands', methods=['POST'])
def retrieve_estimands():
    session['treatment'] = request.form['treatment']
    session['outcome'] = request.form['outcome']
    causal_estimands, session['model'], session['identified_estimand'] = compute_estimands(session['csv_content'], request.form['graph'], request.form['treatment'], request.form['outcome'])
    return json.dumps(dict(causal_estimands), default=str)


@app.route('/compute-effect-with-estimand', methods=['POST'])
def compute_effect_with_estimand():
    causal_effect = estimate_effect_with_estimand(session['model'], session['identified_estimand'], request.form['estimand_name'])
    return {'treatment' : session['treatment'], 'outcome' : session['outcome'], 'effect' : causal_effect}


@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    session['csv_content'] = request.form['file-content']
    print('In UploadCSV')
    return '', 200


app.run(debug=False)
