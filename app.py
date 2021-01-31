from flask import Flask, request, render_template, session
from flask_session import Session
from causal_effect import compute_causal_effect, compute_estimands, estimate_effect_with_estimand
import json


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(__name__)
app.secret_key = 'i-want-to-do-causal-inference'
Session(app)


@app.route("/")
def main_page():
    return render_template('dags.html')


@app.route('/compute-causal-effect', methods=['POST'])
def compute():
    print('ADJUSTED 2')
    print(request.form['adjusted'])
    causal_effect = compute_causal_effect(session['csv_content'], request.form['graph'], request.form['treatment'], request.form['outcome'], request.form['adjusted'])
    return 'The causal effect of ' + request.form['treatment'] + ' on ' + request.form['outcome'] + ' is ' + str(causal_effect)


@app.route('/print-estimands', methods=['POST'])
def print_estimands():
    session['treatment'] = request.form['treatment']
    session['outcome'] = request.form['outcome']
    causal_estimands, session['model'], session['identified_estimand'] = compute_estimands(session['csv_content'], request.form['graph'], request.form['treatment'], request.form['outcome'])
    return json.dumps(dict(causal_estimands), default=str)


@app.route('/estimate-with-estimand', methods=['POST'])
def estimate_with_estimand():
    causal_effect = estimate_effect_with_estimand(session['model'], session['identified_estimand'], request.form['estimand_name'])
    return 'The causal effect of ' + session['treatment'] + ' on ' + session['outcome'] + ' is ' + str(causal_effect)


@app.route('/upload-csv', methods=['POST'])
def uploadCSV():
    session['csv_content'] = request.form['file-content']
    print('In UploadCSV')
    return '', 200


app.run(debug=True)
