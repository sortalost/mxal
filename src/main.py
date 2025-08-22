import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from .modules.imap_client import fetch_folder, test_login, fetch_email
from .modules.smtp_client import send_email
from .modules.utils import login_required, time_ago, fetch_commit


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
            flash("Login failed. Check your credentials.", "danger")
    return render_template("login.html")


@app.route("/inbox")
@login_required
def inbox():
    start = int(request.args.get("start", 0))
    limit = 10
    messages, total_count = fetch_folder(session["email_user"], session["email_pass"], "inbox", start=start, limit=limit)
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
    messages, total_count = fetch_folder(
        session["email_user"],
        session["email_pass"],
        "Sent"
    )
    return render_template("sent.html", messages=messages, total_count=total_count)


@app.route("/compose", methods=["GET", "POST"])
@login_required
def compose():
    if request.method == "POST":
        to = request.form["to"]
        subject = request.form["subject"]
        body = request.form["body"]
        send_email(session["email_user"], session["email_pass"], to, subject, body)
        flash("Email sent!", "success")
        return redirect(url_for("inbox"))
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
    session.clear()
    return redirect(url_for("index"))


@app.context_processor
def inject_commit():
    return dict(commit=commit)

if __name__ == "__main__":
    app.run(debug=False)
