from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

# Configure application
app = Flask(__name__)
 
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# @app.after_request
# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")
def after_request(response):
  """Ensure responses aren't cached"""
  response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
  response.headers["Expires"] = 0
  response.headers["Pragma"] = "no-cache"
  return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
   """Show portfolio of stocks"""
   if request.method == "POST":
       score = request.form.get("userscore")
       db.execute("INSERT INTO scores (user_id,score) VALUES(?,?)", session["user_id"],score)
       return render_template("index.html")
   else:
       return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
  """Log user in"""
  # Forget any user_id
  session.clear()
  # User reached route via POST (as by submitting a form via POST)
  if request.method == "POST":
      password = request.form.get("password")
      # Ensure username was submitted
      if not request.form.get("username"):
          return apology("must provide username", 403)
      # Ensure password was submitted
      elif not password:
          return apology("must provide password", 403)
      # Query database for username
      rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
      # Ensure username exists and password is correct
      if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
          return apology("invalid username and/or password", 403)
      # Remember which user has logged in
      session["user_id"] = rows[0]["id"]
      # Redirect user to home page
      return redirect("/")
  # User reached route via GET (as by clicking a link or via redirect)
  else:
      return render_template("login.html")

@app.route("/logout")
def logout():
  """Log user out"""
  # Forget any user_id
  session.clear()
  # Redirect user to main page
  return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
  """Register user"""
  # If the user presses submit and attempts to register, perform the following
  if request.method == "POST":
      # Store user input from form
      password = request.form.get("password")
      username = request.form.get("username")
      confirmation = request.form.get("confirmation")
      # Return an apology if the user does not input any of the required fields
      if not username or not password or not confirmation:
          return apology("Please fill in all the necessary information!")
      if len(password) < 8:
          return apology("Password should be at least 8 characters")
      if not any(char.isdigit() for char in password):
          return apology("Password should contain at least one number")
      # Return an apology if the passwords do not match
      if password != confirmation:
          return apology("Passwords do not match!")
      # Making sure the username is not repeated
      rows = db.execute("SELECT * FROM users WHERE username = ?", username)
      if len(rows) != 0:
          return apology("Username not available!")
      # Generating the users hash to store in table
      hash = generate_password_hash(password)
      db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, hash)
      return redirect('/login')
  else:
      # If arriving at the page not having submitted a registration form, then display the html page displaying the form
      return render_template("register.html")

@app.route("/progress", methods=["GET", "POST"])
def progress():
   """play game"""
   rows = db.execute("SELECT score,time FROM scores WHERE user_id = ?", session["user_id"])
   scores = []
   # Appends each column in row into a list of dictionaries
   for row in rows:
       scores.append({
           'scores': row['score'],
           'time': row['time'],
       })
   return render_template("/progress.html", scores =scores)

@app.route("/records", methods=["GET", "POST"])
def records():
   rows = db.execute("SELECT score,time,username FROM scores JOIN users on scores.user_id = users.id ORDER BY score DESC LIMIT 10")
   scores = []
   # Appends each column in row into a list of dictionaries
   for row in rows:
       scores.append({
           'scores': row['score'],
           'time': row['time'],
           'username': row['username']
       })
   return render_template("records.html", scores=scores)
   
@app.route("/game", methods=["GET", "POST"])
def game():
   return redirect('/')

@app.route("/aboutus", methods=["GET", "POST"])
def aboutus():
   return render_template("/aboutus.html")