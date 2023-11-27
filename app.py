import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required  
import json

# default password for all test accounts abcd

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///clearview.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    # Query the database for latest 3 articles
    articles = db.execute(
        "SELECT id, image, title, name, SUBSTR(content, 1, 220) AS limited_content FROM post ORDER BY date_n_time DESC LIMIT 3"
    )
    return render_template("index.html", latest=articles)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", apology="must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", apology="must provide password")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template("login.html", apology="invalid username or password")

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
            return render_template("register.html", apology="must provide username")
        # Ensure name was submitted
        if not request.form.get("name"):
            return render_template("register.html", apology="must provide name")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("register.html", apology="must provide password")

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return render_template("register.html", apology="must provide confirmation")

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("register.html", apology="password not confirmed")
        # Query database for username
        check = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(check) == 0:
            db.execute(
                "INSERT INTO users (username, hash, name) VALUES(?, ?, ?)",
                request.form.get("username"),
                generate_password_hash(request.form.get("password")),
                request.form.get("name"),
            )
            rows = db.execute(
                "SELECT * FROM users WHERE username = ?", request.form.get("username")
            )
            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            # Redirect user to home page
            return redirect("/")
        else:
            # If username already exists
            return render_template("register.html", apology="username already exists")
    else:
        # When method == "POST"
        return render_template("register.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """ Generate Contact Us """
    return render_template("contact.html")


@app.route("/form_submit", methods=["POST"])
def form_submit():
    # Submit feedback form into database
    db.execute(
        "INSERT INTO feedback (name, email, feed) VALUES (?, ?, ?)",
        request.form.get("name"),
        request.form.get("email"),
        request.form.get("feed"),
    )
    return render_template("contact.html")


@app.route("/about_us", methods=["GET"])
def about_us():
    """ Generate About Us """
    return render_template("about_us.html")


@app.route("/account", methods=["GET"])
# Login required
@login_required
def account():
    # Query the database for articles written by the user
    articles = db.execute(
        "SELECT id, image, title, name, SUBSTR(content, 1, 220) AS limited_content FROM post WHERE user_id = ? ORDER BY date_n_time DESC",
        session["user_id"],
    )
    return render_template("account.html", art=articles)


@app.route("/new_post", methods=["GET", "POST"])
# Post the article written by the user
def new_post():
    if request.method == "POST":
        # Check if title provided
        if not request.form.get("title"):
            return render_template("account.html", apology="must have title")
        # Check if content provided
        elif not request.form.get("content"):
            return render_template("account.html", apology="must have content")
        name = db.execute("SELECT name FROM users WHERE id=?", session["user_id"])
        n_ = name[0]["name"]
        date = db.execute("SELECT DATETIME('NOW') AS current_date")
        d_ = date[0]["current_date"]
        # Add the article into database
        db.execute(
            "INSERT INTO post (name, image, date_n_time, content, title, user_id) VALUES(?, ?, ?, ?, ?, ?)",
            n_,
            request.form.get("image"),
            d_,
            request.form.get("content"),
            request.form.get("title"),
            session["user_id"],
        )
        return redirect("/account")

@app.route("/search", methods=["POST"])
def search():
    search = request.form.get("search")
    # Query the database for titles like entered in search
    articles = db.execute(
        "SELECT id, image, title, name, SUBSTR(content, 1, 220) AS limited_content FROM post WHERE title LIKE ? ORDER BY date_n_time DESC LIMIT 10",
        "%" + search + "%",
    )
    # if no articles found
    if not articles:
        return render_template("search.html", results="No results")
    return render_template("search.html", res=articles)


@app.route("/article", methods=["GET"])
def article():
    return render_template("article.html")

@app.route("/go_to_page", methods=["POST", "GET"])
def go_to_page():
    if request.method == "GET":
        # Query the database for the article
        rendering = db.execute(
            "SELECT image, title, name, date_n_time, content FROM post content WHERE id=?",
            request.args.get("article_id"),
        )
        render = rendering[0]
        ccc = json.dumps(render)
        # Query the database for comments on that article
        comment = db.execute(
            "SELECT name, date_n_time, content FROM comments WHERE post_id=? ORDER BY date_n_time DESC",
            request.args.get("article_id"),
        )
        return render_template(
            "article.html",
            cc=render,
            article_id=request.args.get("article_id"),
            ccc=ccc,
            comment=comment,
        )
    else:
        rendering = db.execute(
            "SELECT image, title, name, date_n_time, content FROM post content WHERE id=?",
            request.args.get("article_id"),
        )
        render = rendering[0]
        print(rendering)
        print(render)
        ccc = json.dumps(render)
        return render_template(
            "article.html",
            cc=render,
            article_id=request.form.get("article_id"),
            ccc=ccc,
        )


@app.route("/comment", methods=["POST"])
# Post the comment by the user
# Login in required to comment
@login_required
def comment():
    # Name from session
    name = db.execute("SELECT name FROM users WHERE id=?", session["user_id"])
    n_ = name[0]["name"]
    # Date and Time of posting
    date = db.execute("SELECT DATETIME('NOW') AS current_date")
    d_ = date[0]["current_date"]
    # Add the comment into database
    db.execute(
        "INSERT INTO comments (name, date_n_time, content, person_id, post_id) VALUES(?, ?, ?, ?, ?)",
        n_,
        d_,
        request.form.get("comment"),
        session["user_id"],
        request.form.get("article_id"),
    )
    ccc = json.loads(request.form.get("ccc"))
    ddd = json.dumps(ccc)
    comment = db.execute(
        "SELECT name, date_n_time, content FROM comments WHERE post_id=? ORDER BY date_n_time DESC",
        request.form.get("article_id"),
    )
    return render_template(
        "article.html",
        cc=ccc,
        article_id=request.form.get("article_id"),
        ccc=ddd,
        comment=comment,
    )
