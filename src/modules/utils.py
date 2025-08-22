import time
import requests
from functools import wraps
from datetime import datetime
from flask import session, request, jsonify, flash, redirect, url_for


cockblockmsg = {
    'id':0,
    'subject':'COCKBLOCKED 🚨 | you are cockblocked :(',
    'date':'now',
    'from':'God (real)',
}

troubleshootmsg = {
    'id':0,
    'subject':'ERROR!',
    'date':'now',
    'from':'God (real)',
    'body':f'''\
    Go back and see the subject, based on that, see below:

    1. "COCKBLOCKED 🚨"
        -> Your email is cockblocked, ie, you cannot send emails. Go to <a href="https://cock.li/unblock" target="_blank">cock.li</a> to unblock. However, you can still receive emails.
    
    2. "EMPTY INBOX 📤"
        -> The "Inbox" folder is empty, ie, you have not received any emails yet. That's sad (maybe).
    
    3. "NOTHING SENT👀"
        -> The "Sent" folder does not exist, so, you (probably) haven\'t sent any emails yet. Go send some emails. You must NOT be cockblocked by the way.

    If you see something unexpected, let <a href="//sortalost.is-a.dev/contact" target="_blank">me</a> know.
    Peace.
    '''
}


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "message": "Login required"}), 401
            else:
                flash(f"Login required", "danger")
                return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def fetch_commit():
    url = f"https://api.github.com/repos/sortalost/mxal/commits"
    try:
        res = requests.get(url, headers={} ,timeout=5)
        res.raise_for_status()
        latest = res.json()[0]
        dt_obj = datetime.fromisoformat(latest["commit"]["author"]["date"].replace("Z", "+00:00"))
        return {
            "message": latest["commit"]["message"],
            "sha": latest["sha"][:7],
            "author": latest["commit"]["author"]["name"],
            "date": dt_obj.strftime("%b %d, %Y @ %I:%M %p"),
            "url": latest["html_url"]
        }
    except Exception as e:
        flash(f"failed to fetch commit: {e}")
        return {"message":"failed to fetch.","sha":"none","author":"none","date":"none","url":"none"}
