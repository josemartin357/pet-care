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
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
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
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



# LOGOUT ROUTE
@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


# REGISTER ROUTE
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Post method to get data from form
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
        # query checks if input username is also stored in table users and stores as variable
        username_check = db.execute("SELECT * FROM users WHERE username = :username",
                                    username=username)
        # if variable above exists, then username already taken
        if username_check:
            return apology("The username is already taken. Choose another.")

        # Adding values from form into table users with a db query
        db.execute("INSERT INTO users (firstname, lastname, email, username, password, datetime) VALUES (:firstname, :lastname, :email, :username, :password, :datetime)",
                   firstname=firstname, lastname=lastname, email=email, username=username, password=password, datetime=get_datetime())

        # Logging user in
        # db query selects username and stores in variable
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
        # storing value from input form at index.html
        task = request.form.get("task")
        # if there is a data, execute db query to insert in table
        if task:
            db.execute("INSERT INTO reminders (name, user_id, datetime) VALUES (:task, :user_id, :datetime)",
                       task=task, user_id=session["user_id"], datetime=get_datetime())
        # if a note is not inserted, return and display / (index.html)
        return redirect("/")
    # else if method request is GET
    else:
        # variable holds query to get all tasks from user
        tasks = db.execute("SELECT * FROM reminders WHERE user_id = :user_id",
                               user_id=session["user_id"])
        # variable holds query to get user
        users = db.execute("SELECT * FROM users WHERE id = :user_id",
                           user_id=session["user_id"])
        # firstname takes value from column users in dictionary
        firstname = users[0]["firstname"]
        # render index.html and pass values from tasks and firstname to it
        return render_template("index.html", tasks=tasks, name=firstname)

# LONG TERM TASKS ROUTE
# route /goals has two methods and requires login
@app.route("/goals", methods=["GET", "POST"])
@login_required
def goals():
    """Show long term tasks"""
    # if method request is POST
    if request.method == "POST":
        # take value from input in form at goals.html and store
        longTask = request.form.get("longTask")
        # if there is a value stored 
        if longTask:
            # run db.query to insert in goals table
            db.execute("INSERT INTO goals (name, user_id, datetime) VALUES (:longTask, :user_id, :datetime)",
                       longTask=longTask, user_id=session["user_id"], datetime=get_datetime())
        # else if there is no value to store, redirect to page
        return redirect("/goals")
    # else if method request is GET
    else:
        # run query to get all tasks from user_id and store as variable
        longTasks = db.execute("SELECT * FROM goals WHERE user_id = :user_id",
                           user_id=session["user_id"])
        # render html and pass variable above
        return render_template("goals.html", longTasks=longTasks)


# DELETE TASKS ROUTE
# delete route for tasks has post method and requires login
@app.route("/delete", methods=["POST"])
@login_required
def delete():
    """Delete tasks from index.html"""
    # grabbing value from input in index.html and storing as variable
    # getlist return a list of items for the given key. we use this since multiple checkboxes can be clicked
    clicked_tasks = request.form.getlist("click_task")
    # we iterate thru list and define every item as item
    for item in clicked_tasks:
        # define variable that holds query that gets the id for every clicked item
        clicked_task = db.execute("SELECT * FROM reminders WHERE id = :clicked_task",
                             clicked_task=item)
        clicked_task = clicked_task[0]

        # deleting from table based on id obtained in variable above
        db.execute("DELETE FROM reminders WHERE id = :clicked_id",
                   clicked_id=clicked_task['id'])

    # rendering remaining tasks based on user_id
    tasks = db.execute("SELECT * FROM reminders WHERE user_id = :user_id",
                           user_id=session["user_id"])
    # returning data as json for url checked in ajax
    return (jsonify(tasks))


# DELETE LONG TERM TASKS ROUTE
# delete route for long term tasks has post method and requires login
@app.route("/delete_long_task", methods=["POST"])
@login_required
def delete_long_task():
    """Delete long term tasks from goals.html"""
    # grabbing value from input in goals.html and storing as variable
    # getlist return a list of items for the given key. we use this since multiple checkboxes can be clicked
    clicked_longTasks = request.form.getlist("click_longTask")
    # we iterate thru list and define every item as item
    for item in clicked_longTasks:
        # define variable that holds query that gets the id for every checked item
        clicked_longTask = db.execute("SELECT * FROM goals WHERE id = :clicked_longTask",
                             clicked_longTask=item)
        clicked_longTask = clicked_longTask[0]
        # deleting from table based on id obtained in variable above
        db.execute("DELETE FROM goals WHERE id = :longTask_id",
                   longTask_id=clicked_longTask['id'])
    # rendering remaining tasks based on user_id
    LongTasksLeft = db.execute("SELECT * FROM goals WHERE user_id = :user_id",
                       user_id=session["user_id"])
    # returning data as json for url checked in ajax
    return (jsonify(LongTasksLeft))


# ROUTE TO SEND TASKS TO ACCOMPLISHED PAGE
# route to insert checked items to completed table while deleting from reminders table. Front end is supported with ajax.
@app.route("/move_task", methods=["POST"])
@login_required
def checked():
    """moving completed items to accomplished page"""
    # grabbing value from input in index.html and storing as variable
    # getlist return a list of items for the given key. we use this since multiple checkboxes can be clicked
    clicked_tasks = request.form.getlist("click_task")
    # we iterate thru list and define every item as item
    for item in clicked_tasks:
        # define var that holds query to select the id of every clicked tasks
        clicked_task = db.execute("SELECT * FROM reminders WHERE id = :task",
                                      task=item)
        clicked_task = clicked_task[0]
        # insert clicked tasks to table
        db.execute("INSERT INTO completed (name, user_id, datetime) VALUES (:name, :user_id, :datetime)",
                   name=clicked_task['name'], user_id=session['user_id'], datetime=get_datetime())
        # removing clicked tasks from table
        db.execute("DELETE FROM reminders WHERE id = :task_id",
                   task_id=clicked_task['id'])

    # rendering all active tasks based on user_id
    tasks = db.execute("SELECT * FROM reminders WHERE user_id = :user_id",
                           user_id=session["user_id"])

    # returning data as json for url checked in ajax
    return (jsonify(tasks))

# ROUTE TO DISPLAY ACCOMPLISHED TASKS
# accomplished route requires login
@app.route("/accomplished", methods=["GET"])
@login_required
def finished_task():
    """display finished tasks"""
    # get routes displays all completed tasks from user
    if request.method == "GET":
        finished_tasks = db.execute("SELECT * FROM completed WHERE user_id = :user_id",
                               user_id=session["user_id"])
        return render_template("completed.html", finished_tasks=finished_tasks)

# ROUTE TO SEND LONG TERM GOALS TO ACCOMPLISHED
@app.route("/move_long_task", methods=["POST"])
@login_required
def move_long_task():
    """moving completed goals to accomplished page"""
    clicked_long_tasks = request.form.getlist("click_longTask")
    for item in clicked_long_tasks:
        clicked_long_task = db.execute("SELECT * FROM goals WHERE id = :item_id",
                                  item_id=item)
        clicked_long_task = clicked_long_task[0]

        # Insert checked item(s) to completed table
        db.execute("INSERT INTO completed (name, user_id, datetime) VALUES (:name, :user_id, :datetime)",
                   name=clicked_long_task['name'], user_id=session['user_id'], datetime=get_datetime())
        # deleting checked item(s) from goals table
        db.execute("DELETE FROM goals WHERE id = :task_id",
                   task_id=clicked_long_task['id'])

    # rendering all items based on user_id
    longTasks = db.execute("SELECT * FROM goals WHERE user_id = :user_id",
                       user_id=session["user_id"])

    return (jsonify(longTasks))