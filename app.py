from flask import Flask, request, render_template

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/")
def main_page():
    return render_template('dags.html')


@app.route('/compute-causal-effect', methods=['POST'])
def compute():
    print(request.form['graph'])
    print('In ComputeCausalEffect')
    return '', 200


@app.route('/upload-csv', methods=['POST'])
def uploadCSV():
    print(request.files)
    if 'file' not in request.files:
        print('No file part')
    else:
        print(request.files['file'])
    print('In UploadCSV')
    return '', 200


app.run(debug=True)
