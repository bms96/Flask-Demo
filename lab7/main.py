"""
Bryan Santini
3/2/2022
SDEV 300 Spring

This flask application generates a website with three different pages.
Each page of the website is built off of a template (index.html). The
styling is from bootstrap. Each page displays something different and
the date/time comes from the python datetime module where the date
information is fed into render_template() and displayed in the html
using {{variable}}.
"""

from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash
from passlib.hash import sha256_crypt


app = Flask(__name__)
app.secret_key = "a!@#WFD123wfsw/.e"
app.permanent_session_lifetime = timedelta(minutes=10)


@app.route("/home", methods=["POST", "GET"])
def home():
    """First page using datetime module"""
    if session.get("user") is None:
        return redirect(url_for("user_login"))
    today = date.today()
    current_date = today.strftime("%d/%m/%Y")
    current_time = datetime.now()
    return render_template(
        "index.html", date=current_date, hour=current_time.strftime("%I"),
        minute=current_time.minute, second=current_time.second)


def password_validation(p):
    """Function that tests the strength of a password"""

    symbols = ["!", "@", "#", "$", "%", "^", "&", "*"]

    if len(p) < 12:
        return False

    if not any(char.isdigit() for char in p):
        return False

    if not any(char.isupper() for char in p):
        return False

    if not any(char.islower() for char in p):
        return False

    if not any(char in symbols for char in p):
        return False

    return True


def username_validation(u):
    """Function that tests the validity of a username
       This is a simplified version of password_validity"""


    if len(u) < 6:
        return False

    if not any(char.islower() for char in u):
        return False

    return True


@app.route("/register", methods=["POST", "GET"])
def register_user():
    """Page that registers user"""
    if request.method == "POST":
        user = request.form["nm"]
        password = request.form["pass"]
        repeat_password = request.form["pass_check"]

        # logic for correct username and password

        if not password_validation(password):
            flash("Password must be 12 characters long with "
                  "at least 1 uppercase character, 1 special "
                  "character and one number")
            return redirect(url_for("register_user"))

        if not username_validation(user):
            flash("Username must contain at least 6 characters "
                  "with at least one lowercase letter")
            return redirect(url_for("register_user"))

        if password != repeat_password:
            flash("Passwords need to match")
            return redirect(url_for("register_user"))

        hashed_password = sha256_crypt.hash(password)

        with open("passfile", "a") as f:
            f.writelines(user + hashed_password + "\n")
        # print(user + "" + hashed_password)
        return redirect(url_for("user_login"))
    else:
        return render_template("register.html")


@app.route("/", methods=["POST", "GET"])
def user_login():
    """User login page"""
    if request.method == "POST":
        user = request.form["nm"]
        password = request.form["pass"]

        if user == "" or password == "":
            flash("Incorrect username or password", "error")
            return redirect(url_for("user_login"))

        # Verifying username and password is in text file

        with open("passfile", "r") as f:
            f_contents = f.readlines()
            for i in f_contents:
                # Getting rid of white space and user
                i = i.strip()
                i = i.replace(user, "")
                try:
                    if sha256_crypt.verify(password, i):
                        print("user found")
                        session["user"] = user
                        # return f"<h1>{user}</h1>"
                        flash("You have logged in successfully", "info")
                        return redirect(url_for("home"))
                except ValueError:
                    continue
        flash("Incorrect username or password", "error")
        return redirect(url_for("user_login"))
        # with open("passfile", "r") as f:
        #     print(f.name)
        #     f_contents = f.readline()
        #     # print(f_contents)
        # for line in f:
        #     print(line, end="")
        #     print("bryan : santini" in f_contents)

    return render_template("login.html")


@app.route("/secondPage")
def second_page():
    """Second page built from index.html"""
    if session.get("user") is None:
        return redirect(url_for("user_login"))

    return render_template("secondPage.html")


@app.route("/thirdPage")
def third_page():
    """Third page also built from index.html"""
    if session.get("user") is None:
        return redirect(url_for("user_login"))

    return render_template("thirdPage.html")


if __name__ == "__main__":
    app.run(debug=True)
