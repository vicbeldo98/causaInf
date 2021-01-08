from flask import Flask, request, render_template, session
from flask_session import Session
from causal_effect import compute_causal_effect


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
    compute_causal_effect(session['csv_content'], request.form['graph'], request.form['treatment'], request.form['outcome'], request.form['adjusted'], request.form['unobserved'])
    print('In ComputeCausalEffect')
    print(session)
    return '', 200


@app.route('/upload-csv', methods=['POST'])
def uploadCSV():
    session['csv_content'] = request.form['file-content']
    print('In UploadCSV')
    return '', 200


app.run(debug=True)
