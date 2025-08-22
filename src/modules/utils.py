import time
import requests
from functools import wraps
from datetime import datetime
from flask import session, request, jsonify, flash, redirect, url_for


cockblockmsg = {
    'id':0,
    'subject':'you are cockblocked :(',
    'date':'now',
    'from':'God (real)',
    'body':'Your email is cockblocked, ie, you cannot send emails. Go to <a href="https://cock.li/unblock">cock.li</a> to unblock. However, you can still receive emails. That\'s sad, maybe. Peace :)'
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
