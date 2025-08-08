import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from .modules.imap_client import fetch_inbox, test_login, fetch_email
from .modules.smtp_client import send_email
from .modules.utils import login_required

app = Flask(__name__)
app.secret_key = os.urandom(8)

from . import api

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
    # ?start
    start = int(request.args.get("start", 0))
    limit = 10
    messages, total_count = fetch_inbox(session["email_user"], session["email_pass"], start=start, limit=limit)
    next_start = start + limit if start + limit < total_count else None
    prev_start = start - limit if start - limit >= 0 else None
    return render_template(
        "inbox.html",
        messages=messages,
        next_start=next_start,
        prev_start=prev_start
    )

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

@app.route("/view/<email_id>")
@login_required
def view_email(email_id):
    if "email_user" not in session:
        return redirect(url_for("login"))    
    email_data = fetch_email(session["email_user"], session["email_pass"], email_id)
    return render_template("view_email.html", email=email_data)


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run()
