import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

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
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.route("/")
@login_required
def index():
    """Show history of last five places saved"""
    
    rows = db.execute(
        "SELECT name, description, price, location FROM entries WHERE id = ? ORDER BY record desc LIMIT 5", session["user_id"])
        
    if len(rows) == 0:
        return render_template("newuser.html")
    else:
        username = db.execute(
            "SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        places=[]
        for row in rows:
            places.append({
                "name": row["name"],
                "description": row["description"],
                "location": row["location"],
                "price": row["price"]
            })
            
        return render_template("index.html", username=username, places=places)
        
        
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add an entry to user's own records"""
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        name = (request.form.get("name")).lower()
        location = request.form.get("location")
        description = request.form.get("description")
        price = request.form.get("price")
        
        # Ensure fields are not blank
        if not name:
            return apology("must provide name", 400)
        elif not location:
            return apology("must provide location", 400)
        elif not description:
            return apology("must provide description", 400)
            
        # Ensure name does not already exist
        row = db.execute("SELECT * FROM entries WHERE id = ? AND name = ?", session["user_id"], name)
        if len(row) == 1:
            return apology("you've already added this place", 400)
            
        # Ensure valid price entered
        try:
            price = int(price)
        except ValueError:
            return apology("price must be a positive integer", 400)
            
        # Update database with new entry
        db.execute("INSERT INTO entries (id, name, location, description, price) VALUES (?, ?, ?, ?, ?)", session["user_id"], name, location, description, int(price))
        
        # Success!
        flash("Yum! Record has been added.")
        return redirect("/")
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("add.html")
        
        
@app.route("/pick")
@login_required
def pick():
    """Randomly generate a place to eat from user's records"""
    
    selection = db.execute(
        "SELECT name, description, price, location FROM entries WHERE id = ? ORDER BY RANDOM() LIMIT 1", session["user_id"]
        )
    name = selection[0]["name"]
    location = selection[0]["location"]
    description = selection[0]["description"]
    price = selection[0]["price"]
    
    return render_template("pick.html", name=name, location=location, description=description, price=price)
    

@app.route("/explore")
@login_required
def explore():
    """Show up to 10 places saved by other users"""
    
    rows = db.execute(
        "SELECT name, description, price, location FROM entries WHERE id != ? ORDER BY RANDOM() LIMIT 10", session["user_id"])
        
    places=[]
    for row in rows:
        places.append({
            "name": row["name"],
            "location": row["location"],
            "description": row["description"],
            "price": row["price"]
        })
            
    return render_template("explore.html", places=places)

    
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

    # Redirect user to login form
    return redirect("/")
    
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
            
        # Ensure password matches confirmation
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)
            
        # Ensure username does not already exist
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) == 1:
            return apology("username already exists", 400)
            
        # Access form data (from user's submission)
        username = request.form.get("username")
        pwhash = generate_password_hash(request.form.get("password"))
        
        # Insert data into database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, pwhash)
        
        # Redirect user to homepage
        return redirect("/")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
        
        
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)