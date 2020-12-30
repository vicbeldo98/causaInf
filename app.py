from flask import Flask, render_template

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/")
def main_page():
    return render_template('dags.html')


@app.route('/compute-causal-effect', methods=['POST'])
def compute():
    print('In ComputeCausalEffect')
    return "Nothing"


@app.route('/upload-csv', methods=['POST'])
def uploadCSV():
    print('In UploadCSV')
    return "Nothing"


app.run(debug=True)
