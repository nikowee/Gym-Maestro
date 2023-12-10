import werkzeug

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required, apology, get_exercise, get_bmi

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///project.db")


@app.route("/")
@login_required
def index():
    bmi_data = db.execute("SELECT bmi, bmi_range FROM users WHERE id = ?", session["user_id"])[0]

    return render_template("index.html", bmi_data=bmi_data)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "" or password == "":
            return apology("Username/Password cannot be blank")
        elif len(db.execute("SELECT * FROM users WHERE username = ?", username)) > 0:
            return apology("Username already exists")

        # generate password as hash, and store username and password hash into the user database
        hash = werkzeug.security.generate_password_hash(password, method='pbkdf2', salt_length=16)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        return render_template("login.html")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # search for user's info from db
        query = db.execute("SELECT * FROM users WHERE username = ?", username)

        # check if username exists and if password is correct
        if len(query) != 1 or not werkzeug.security.check_password_hash(query[0]["hash"], password):
            return apology("Username/Password is invalid", 403)

        # remember id of user logged in
        session["user_id"] = query[0]["id"]

        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    # clear session info
    session.clear()

    return redirect("/")


@app.route("/workoutplanner", methods=["GET", "POST"])
def workoutplanner():
    if request.method == "POST":
        filter = request.form.get("filter")
        filter_options = request.form.get("filter_options")
        limit = request.form.get("limit")

        # generate exercises
        gendata = get_exercise(filter, filter_options, limit)
        print(gendata)
        # query bmi data
        bmi_data = db.execute("SELECT bmi, bmi_range FROM users WHERE id = ?", session["user_id"])[0]

        return render_template("index.html", data=gendata, bmi_data=bmi_data)
    else:
        return render_template("workoutplanner.html")


@app.route("/bmicalc", methods=["GET", "POST"])
@login_required
def bmicalc():
    if request.method == "POST":
        weight = request.form.get("weight")
        height = request.form.get("height")

        # calculate bmi
        bmi_data = get_bmi(weight, height)
        print(bmi_data)

        # insert bmi data into database
        db.execute("UPDATE users SET bmi = ?, bmi_range = ? WHERE id = ?", bmi_data["info"]["bmi"], bmi_data["info"]["health"], session["user_id"])

        return redirect("/")
    else:
        return render_template("bmicalc.html")
