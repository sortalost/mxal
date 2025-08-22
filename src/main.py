import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from .modules.imap_client import fetch_folder, test_login, fetch_email
from .modules.smtp_client import send_email
from .modules.utils import login_required, fetch_commit
import smtplib


app = Flask(__name__)
app.secret_key = os.getenv("secret_key")
commit = fetch_commit()


@app.route("/")
def index():
    return render_template("index.html")


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
            flash("Wrong credentials", "danger")
    return render_template("login.html")


@app.route("/inbox")
@login_required
def inbox():
    start = int(request.args.get("start", 0))
    limit = 10
    try:
        messages, total_count = fetch_folder(session["email_user"], session["email_pass"], "inbox", start=start, limit=limit)
    except:
        flash("No emails.")
        messages = [
            {
                'id':0,
                'subject':'empty inbox :/',
                'date':'now',
                'from':'God (real)',
                'body':'You have not received any email yet. That\'s sad, maybe. Peace :)'
            }
        ]
        total_count = 1
    next_start = start + limit if start + limit < total_count else None
    prev_start = start - limit if start - limit >= 0 else None
    return render_template(
        "inbox.html",
        messages=messages,
        next_start=next_start,
        prev_start=prev_start,
        msglength = len(messages)
    )


@app.route("/sent")
@login_required
def sent():
    try:
        messages, total_count = fetch_folder(
            session["email_user"],
            session["email_pass"],
            "Sent"
        )
    except:
        flash("Nothing sent yet")
        messages = [
            {
                'id':0,
                'subject':'Nothing sent yet (?)',
                'date':'now',
                'from':'God (real)',
                'body':'You probably haven\'t sent any emails yet. (If you think this is an error, let <a href="mailto:sortalost@cock.li">me</a> know). Peace :)'
            }
        ]
        total_count = 1
    return render_template("sent.html", messages=messages, total_count=total_count)


@app.route("/compose", methods=["GET", "POST"])
@login_required
def compose():
    if request.method == "POST":
        to = request.form["to"]
        subject = request.form["subject"]
        body = request.form["body"]
        try:
            send_email(session["email_user"], session["email_pass"], to, subject, body)
            flash("Email sent!", "success")
            return redirect(url_for("inbox"))
        except smtplib.SMTPDataError:
            flash("COCKBLOCKED 🚨")
            messages = [
                {
                    'id':0,
                    'subject':'you are cockblocked :(',
                    'date':'now',
                    'from':'God (real)',
                    'body':'Your email is cockblocked, ie, you cannot send emails. Go to <a href="https://cock.li/unblock">cock.li</a> to unblock. However, you can still receive emails. That\'s sad, maybe. Peace :)'
                }
            ]
            total_count = 1
    return render_template("compose.html")


@app.route("/view/<folder>/<email_id>")
@login_required
def view_email(folder, email_id):
    folder=folder.title() 
    email_data = fetch_email(session["email_user"], session["email_pass"], email_id, folder)
    return render_template("view_email.html", email=email_data)


@app.route("/api/inbox")
@login_required
def api_inbox():
    start = int(request.args.get("start", 0))
    limit = int(request.args.get("limit", 10))
    messages, _ = fetch_folder(
        session["email_user"],
        session["email_pass"],
        "inbox",
        start=start,
        limit=limit
    )
    return jsonify(messages)


@app.route("/api/sent")
@login_required
def api_sent():
    start = int(request.args.get("start", 0))
    limit = int(request.args.get("limit", 10))
    messages, _ = fetch_folder(
        session["email_user"],
        session["email_pass"],
        "Sent",
        start=start,
        limit=limit
    )
    return jsonify(messages)


@app.route("/logout")
@login_required
def logout():
    flash("Logged out")
    session.clear()
    return redirect(url_for("index"))


@app.context_processor
def inject_commit():
    return dict(commit=commit)

if __name__ == "__main__":
    app.run(debug=False)
