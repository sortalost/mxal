from .main import app
from flask import jsonify, session, request
from .modules import imap_client
from .modules import utils

@app.route("/api/inbox")
def api_inbox():
    if not session.get('email_user'):
        return jsonify({'error':'not logged in'}), 401
    start = int(request.args.get("start", 0))
    limit = int(request.args.get("limit", 10))
    messages, _ = imap_client.fetch_inbox(
        session["email_user"],
        session["email_pass"],
        start=start,
        limit=limit
    )
    return jsonify(messages)
