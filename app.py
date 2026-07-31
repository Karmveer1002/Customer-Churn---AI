from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify
)

import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import os
from datetime import datetime

from model import predictor

# ==========================================================
# APPLICATION
# ==========================================================

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "CustomerChurnPrediction2026"
)

DATABASE = "database.db"

UPLOAD_FOLDER = "uploads"

DATASET_FOLDER = "dataset"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ==========================================================
# DATABASE
# ==========================================================

def get_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn

# ==========================================================
# LOGIN CHECK
# ==========================================================

def login_required():

    return "user" in session

# ==========================================================
# HOME
# ==========================================================

@app.route("/")

def home():

    if login_required():

        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))

# ==========================================================
# LOGIN
# ==========================================================

@app.route("/login", methods=["GET", "POST"])

def login():

    if request.method == "POST":

        username = request.form.get("username")

        password = request.form.get("password")

        conn = get_connection()

        cur = conn.cursor()

        cur.execute(

            "SELECT * FROM users WHERE username=?",

            (username,)

        )

        user = cur.fetchone()

        conn.close()

        if user and check_password_hash(
        user["password"],
        password):

            session["user"] = username

            flash(

                "Login Successful",

                "success"

            )

            return redirect(

                url_for("dashboard")

            )

        flash(

            "Invalid Username or Password",

            "danger"

        )

    return render_template(

        "login.html"

    )

# ==========================================================
# SIGNUP
# ==========================================================

@app.route("/signup", methods=["GET", "POST"])

def signup():

    if request.method == "POST":

        username = request.form.get("username")

        password = generate_password_hash(
            request.form.get("password")
        )

        conn = get_connection()

        cur = conn.cursor()

        try:

            cur.execute(

                """

                INSERT INTO users

                (username,password)

                VALUES(?,?)

                """,

                (

                    username,

                    password

                )

            )

            conn.commit()

            flash(

                "Account Created Successfully",

                "success"

            )

            return redirect(

                url_for("login")

            )

        except sqlite3.IntegrityError:

            flash(

                "Username Already Exists",

                "warning"

            )

        finally:

            conn.close()

    return render_template(

        "signup.html"

    )

# ==========================================================
# LOGOUT
# ==========================================================

@app.route("/logout")

def logout():

    session.clear()

    flash(

        "Logged Out Successfully",

        "success"

    )

    return redirect(

        url_for("login")

    )
# ==========================================================
# DASHBOARD
# ==========================================================

@app.route("/dashboard")
def dashboard():
    print("Dashboard Opened")

    if not login_required():

        return redirect(url_for("login"))

    dataset_path = os.path.join(
        DATASET_FOLDER,
        "Churn_Modelling.csv"
    )

    total_customers = 0
    churn_count = 0
    active_customers = 0
    churn_rate = 0

    columns = []
    data = []

    if os.path.exists(dataset_path):

        df = pd.read_csv(dataset_path)

        total_customers = len(df)

        churn_count = int(df["Exited"].sum())

        active_customers = total_customers - churn_count

        churn_rate = round(
            (churn_count / total_customers) * 100,
            2
        )

        columns = list(df.columns)

        data = df.head(10).values.tolist()

    return render_template(

        "dashboard.html",

        total_customers=total_customers,

        churn_count=churn_count,

        active_customers=active_customers,

        churn_rate=churn_rate,

        columns=columns,

        data=data

    )

# ==========================================================
# CUSTOMER TABLE
# ==========================================================

@app.route("/table")
def table():

    if not login_required():

        return redirect(url_for("login"))

    dataset_path = os.path.join(
        DATASET_FOLDER,
        "Churn_Modelling.csv"
    )

    columns = []

    data = []

    if os.path.exists(dataset_path):

        df = pd.read_csv(dataset_path)

        columns = list(df.columns)

        data = df.values.tolist()

    return render_template(

        "table.html",

        columns=columns,

        data=data

    )

# ==========================================================
# DATASET UPLOAD
# ==========================================================

@app.route("/upload", methods=["POST"])
def upload():

    if not login_required():

        return redirect(url_for("login"))

    file = request.files.get("file")

    if file:

        filepath = os.path.join(

            DATASET_FOLDER,

            "Churn_Modelling.csv"

        )

        file.save(filepath)

        flash(

            "Dataset Uploaded Successfully",

            "success"

        )

    else:

        flash(

            "Please Select Dataset",

            "warning"

        )

    return redirect(

        url_for("table")

    )

# ==========================================================
# PREDICTION
# ==========================================================

@app.route("/predict", methods=["GET", "POST"])
def predict():

    if not login_required():

        return redirect(url_for("login"))

    prediction = None

    if request.method == "POST":

        customer = {

            "CreditScore": int(request.form["credit_score"]),

            "Geography": request.form["geography"],

            "Gender": request.form["gender"],

            "Age": int(request.form["age"]),

            "Tenure": int(request.form["tenure"]),

            "Balance": float(request.form["balance"]),

            "NumOfProducts": int(request.form["products"]),

            "HasCrCard": int(request.form["card"]),

            "IsActiveMember": int(request.form["active"]),

            "EstimatedSalary": float(request.form["salary"])

        }

        prediction = predictor.predict(customer)

        conn = get_connection()

        cur = conn.cursor()

        cur.execute("""

        INSERT INTO prediction_history(

        username,

        CreditScore,

        Geography,

        Gender,

        Age,

        Tenure,

        Balance,

        NumOfProducts,

        HasCrCard,

        IsActiveMember,

        EstimatedSalary,

        Prediction,

        Probability,

        Risk

        )

        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)

        """,

        (

            session["user"],

            customer["CreditScore"],

            customer["Geography"],

            customer["Gender"],

            customer["Age"],

            customer["Tenure"],

            customer["Balance"],

            customer["NumOfProducts"],

            customer["HasCrCard"],

            customer["IsActiveMember"],

            customer["EstimatedSalary"],

            prediction["prediction"],

            prediction["probability"],

            prediction["risk"]

        ))

        conn.commit()

        conn.close()

    return render_template(

        "predict.html",

        prediction=prediction

    )
# ==========================================================
# INSIGHTS
# ==========================================================

@app.route("/insights")
def insights():

    if not login_required():
        return redirect(url_for("login"))

    dataset_path = os.path.join(
        DATASET_FOLDER,
        "Churn_Modelling.csv"
    )

    stats = {}

    if os.path.exists(dataset_path):

        df = pd.read_csv(dataset_path)

        stats = {

            "total": len(df),

            "active": int((df["Exited"] == 0).sum()),

            "churn": int((df["Exited"] == 1).sum()),

            "rate": round(df["Exited"].mean() * 100, 2)

        }

    return render_template(

        "insights.html",

        stats=stats

    )

# ==========================================================
# ADMIN PANEL
# ==========================================================

@app.route("/admin")
def admin():

    if not login_required():
        return redirect(url_for("login"))

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        "SELECT * FROM users"

    )

    users = cur.fetchall()

    conn.close()

    return render_template(

        "admin.html",

        users=users

    )

# ==========================================================
# PREDICTION HISTORY
# ==========================================================

@app.route("/history")
def history():

    if not login_required():
        return redirect(url_for("login"))

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT *

        FROM prediction_history

        ORDER BY id DESC

    """)

    history = cur.fetchall()

    conn.close()

    return render_template(

        "prediction_history.html",

        history=history

    )

# ==========================================================
# CHART DATA API
# ==========================================================

@app.route("/chart-data")
def chart_data():

    dataset_path = os.path.join(

        DATASET_FOLDER,

        "Churn_Modelling.csv"

    )

    if not os.path.exists(dataset_path):

        return jsonify({})

    df = pd.read_csv(dataset_path)

    active = int((df["Exited"] == 0).sum())

    churn = int((df["Exited"] == 1).sum())

    countries = (

        df["Geography"]

        .value_counts()

        .to_dict()

    )

    age = (

        df.groupby("Age")["Exited"]

        .sum()

        .to_dict()

    )

    return jsonify({

        "active": active,

        "churn": churn,

        "countries": countries,

        "age": age

    })

# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.route("/health")
def health():

    return {

        "status": "running",

        "application": "Customer Churn AI",

        "time": datetime.now().strftime(

            "%d-%m-%Y %H:%M:%S"

        )

    }

# ==========================================================
# CONTEXT
# ==========================================================

@app.context_processor
def inject_data():

    return {

        "current_year": datetime.now().year,

        "project_name": "Customer Churn AI"

    }

# ==========================================================
# 404
# ==========================================================

@app.errorhandler(404)
def not_found(e):

    return render_template(

        "404.html"

    ), 404

# ==========================================================
# START
# ==========================================================

if __name__ == "__main__":

    app.run(

        debug=False,

        host="0.0.0.0",

        port=5000

    )