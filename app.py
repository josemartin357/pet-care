#application configurations to go here
#routes to go here

from asyncio import tasks
import click
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, send_from_directory
from flask_session import Session
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, get_datetime


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

# LOGIN ROUTE
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

# LOGOUT ROUTE
@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


# REGISTER ROUTE
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Forget any user_id
        session.clear()
        # get values from form
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # conditions to display apology
        if not firstname:
            return apology("Must provide first name")
        elif not username:
            return apology("Must provide username")
        elif not email:
            return apology("Must provide email")
        elif not password:
            return apology("Must provide password")
        elif not confirmation:
            return apology("Must provide password confirmation")

        # condition if passwords do not match
        elif password != confirmation:
            return apology("Passwords do not match")

        # Hash password
        password = generate_password_hash(password)

        username_check = db.execute("SELECT * FROM users WHERE username = :username",
                                    username=username)
        # if variable above exists, then username already taken
        if username_check:
            return apology("The username is already taken. Choose another.")

        # Adding values from form into table users with a db query
        db.execute("INSERT INTO users (firstname, lastname, email, username, password, datetime) VALUES (:firstname, :lastname, :email, :username, :password, :datetime)",
                   firstname=firstname, lastname=lastname, email=email, username=username, password=password, datetime=get_datetime())

        # Logging user in
        users = db.execute("SELECT * FROM users WHERE username = :username",
                           username=username)

        # using variable to start session
        session["user_id"] = users[0]["id"]

        # Redirect to index.html
        return redirect("/")

    # get method provides route to register html
    else:
        return render_template("register.html")

# TASKS ROUTE (MAIN)
# main route and login required
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show tasks items"""
    # if there is a POST method request
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            db.execute("INSERT INTO reminders (name, user_id, datetime) VALUES (:task, :user_id, :datetime)",
                       task=task, user_id=session["user_id"], datetime=get_datetime())
        return redirect("/")
    # else if method request is GET
    else:
        tasks = db.execute("SELECT * FROM reminders WHERE user_id = :user_id",
                               user_id=session["user_id"])
        users = db.execute("SELECT * FROM users WHERE id = :user_id",
                           user_id=session["user_id"])
        firstname = users[0]["firstname"]
        return render_template("index.html", tasks=tasks, name=firstname)

# LONG TERM TASKS ROUTE
@app.route("/goals", methods=["GET", "POST"])
@login_required
def goals():
    """Show long term tasks"""
    if request.method == "POST":
        # take value from input in form at goals.html and store
        longTask = request.form.get("longTask")
        # if there is a value stored 
        if longTask:
            db.execute("INSERT INTO goals (name, user_id, datetime) VALUES (:longTask, :user_id, :datetime)",
                       longTask=longTask, user_id=session["user_id"], datetime=get_datetime())
        return redirect("/goals")
    # else if method request is GET
    else:
        longTasks = db.execute("SELECT * FROM goals WHERE user_id = :user_id",
                           user_id=session["user_id"])
        return render_template("goals.html", longTasks=longTasks)


# DELETE TASKS ROUTE
@app.route("/delete", methods=["POST"])
@login_required
def delete():
    """Delete tasks from index.html"""
    clicked_tasks = request.form.getlist("click_task")
    # we iterate thru list and define every item as checked_reminder
    for item in clicked_tasks:
        # define variable that holds query that gets the id for every checked item
        clicked_task = db.execute("SELECT * FROM reminders WHERE id = :clicked_task",
                             clicked_task=item)
        clicked_task = clicked_task[0]

        # deleting from table based on id obtained in variable above
        db.execute("DELETE FROM reminders WHERE id = :clicked_id",
                   clicked_id=clicked_task['id'])

    # rendering remaining tasks based on user_id
    tasks = db.execute("SELECT * FROM reminders WHERE user_id = :user_id",
                           user_id=session["user_id"])
    return (jsonify(tasks))
