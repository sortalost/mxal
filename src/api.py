from .main import app
from flask import jsonify

@app.route("/api/inbox")
def api_inbox():
    if "email_user" not in session:
        return jsonify({"error": "Not logged in"}), 401

    messages, _ = fetch_inbox(session["email_user"], session["email_pass"], start=0, limit=10)
    return jsonify(messages)
