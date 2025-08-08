import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from .modules.imap_client import fetch_inbox, test_login
from .modules.smtp_client import send_email
from .modules.utils import login_required


app = Flask(__name__)
app.secret_key = os.urandom(8)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if test_login(email, password):
            session["email_user"] = email
            session["email_pass"] = password
            session["logged_in"] = True
            return redirect(url_for("inbox"))
        else:
            flash("Login failed. Check your credentials.", "danger")
    return render_template("login.html")

@app.route("/")
@login_required
def inbox():
    if "email_user" not in session:
        return redirect(url_for("login"))
    messages = fetch_inbox(session["email_user"], session["email_pass"])
    return render_template("inbox.html", messages=messages)

@app.route("/compose", methods=["GET", "POST"])
@login_required
def compose():
    if "email_user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        to = request.form["to"]
        subject = request.form["subject"]
        body = request.form["body"]
        send_email(session["email_user"], session["email_pass"], to, subject, body)
        flash("Email sent!", "success")
        return redirect(url_for("inbox"))
    return render_template("compose.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run()
