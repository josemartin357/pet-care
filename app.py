#application configurations to go here
#routes to go here

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, send_from_directory
from flask_session import Session
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required


# FLASK AND DB CONFIG HERE
# FLASK AND DB CONFIG HERE
# FLASK AND DB CONFIG HERE

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use database
db = SQL("sqlite:///todolist.db")

# ROUTES HERE
# ROUTES HERE
# ROUTES HERE

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        # query database for username
        users = db.execute("SELECT * FROM users WHERE username = :username",
                           username=request.form.get("username"))
        # Ensure username exists and password is correct
        if len(users) != 1 or not check_password_hash(users[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        # Remember which user has logged in
        session["user_id"] = users[0]["id"]
        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")