import os

import pandas as pd
from flask import Flask, json, render_template, request, session

from causal_effect import (compute_identification_options, compute_estimation_methods,
                           estimate_effect_with_estimand_and_estimator,
                           refuting_tests)
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config.from_object(__name__)
app.secret_key = "i-want-to-do-causal-inference"
Session(app)


@app.route("/")
def main_page():
    return render_template("dags.html")


@app.route("/retrieve-identification-options", methods=["POST"])
def retrieve_estimands():
    check_required_variables(request.form["treatment"], request.form["outcome"])
    session["treatment"] = request.form["treatment"]
    session["outcome"] = request.form["outcome"]
    (
        identification_options,
        session["model"],
        session["identified_estimand"],
    ) = compute_identification_options(
        session["csv_content"],
        request.form["graph"],
        request.form["treatment"],
        request.form["outcome"],
    )
    return json.dumps(identification_options, default=str)


@app.route("/compute-effect-with-estimand-and-estimator", methods=["POST"])
def compute_effect_with_estimand_and_estimator():
    session["estimate"], session["p-value"] = estimate_effect_with_estimand_and_estimator(
        session["model"],
        session["identified_estimand"],
        request.form["estimand_name"],
        request.form["estimation_method"],
    )

    return {
        "treatment": session["treatment"],
        "outcome": session["outcome"],
        "effect": round(session["estimate"].value, 3),
    }


@app.route("/compute-estimation-methods", methods=["POST"])
def compute_available_estimation_methods():
    estimation_methods = compute_estimation_methods(request.form["estimand_name"])
    return dict(estimation_methods)


@app.route("/refutation-tests", methods=["POST"])
def refutation():
    return dict(
        refuting_tests(
            session["model"], session["identified_estimand"], session["estimate"], session['p-value']
        )
    )


@app.route("/upload-csv", methods=["POST"])
def upload_csv():
    all_data = request.form["file-content"]
    with open("user.csv", "w") as csvfile:
        csvfile.write(all_data)
    with open("user.csv", "r") as csvfile:
        session["csv_content"] = pd.read_csv(csvfile)
    os.remove("user.csv")
    return "", 200


'''@app.errorhandler(Exception)
def handle_exception(e):
    return str(e), 500'''


def check_required_variables(treatment, outcome):
    if "csv_content" not in session.keys():
        raise Exception("No csv file found. Please, upload one first.")
    if treatment == "":
        raise Exception("Create exposure variables on the graph")
    elif len(treatment.split(",")) > 1:
        raise Exception("Just one exposure variable allowed")

    if outcome == "":
        raise Exception("Create outcome variable on the graph")
    elif len(outcome.split(",")) > 1:
        raise Exception("Just one outcome variable allowed")


app.run(debug=True)
