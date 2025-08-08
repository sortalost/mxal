from functools import wraps
from flask import session, request, jsonify, flash, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "message": "Login required"}), 401
            else:
                flash("Please login to access this page.", "error")
                return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function