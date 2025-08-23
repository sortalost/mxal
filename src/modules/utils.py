import time
import requests
from functools import wraps
from datetime import datetime
from flask import session, request, jsonify, flash, redirect, url_for


cockblockmsg = {
    'id':'error',
    'subject':'COCKBLOCKED 🚨 | you are cockblocked :(',
    'date':'now',
    'from':'God (real)',
}

troubleshootmsg = {
    'id':'error',
    'subject':'ERROR!',
    'date':'now',
    'from':'God (real)',
    'body':f'''\
<pre style='white-space: pre-line;'>
<h2>Go back and see the subject, based on that, see below:</h2>
<h3>1. "COCKBLOCKED 🚨"</h3>
<p>-> Your email is cockblocked, ie, you cannot send emails. Go to <a href="https://cock.li/unblock" target="_blank">cock.li</a> to unblock. However, you can still receive emails.</p>
    
<h3>2. "EMPTY INBOX 📤"</h3>
<p>-> The "Inbox" folder is empty, ie, you have not received any emails yet. That's sad (maybe).</p>
    
<h3>3. "NOTHING SENT👀"</h3>
<p>-> The "Sent" folder does not exist, so, you (probably) haven't sent any emails yet. Go send some emails. You must NOT be cockblocked by the way.</p>
<hr>
<p>If you see something unexpected, let <a href="//sortalost.is-a.dev/contact" target="_blank">me</a> know.</p>
<p>Peace.</p>
</pre>
'''
}


doesnotexistmsg = {
    'id':'error_404',
    'subject':'Not found',
    'date':'now',
    'from':'God (real)',
    'body':f'''\
<pre style='white-space: pre-line;'>
<h3"not found"</h3>
<p>email not found.</p>
<hr>
<p>If you are seeing something unexpected, let <a href="//sortalost.is-a.dev/contact" target="_blank">me</a> know.</p>
<p>Peace.</p>
</pre>
'''
}

godmsg = {
    'id':'god',
    'subject':'God's emails',
    'date':'now',
    'from':'God (real)',
    'body':f'''\
<pre style='white-space: pre-line;'>
<h2>You are loved, never forget this.</h2>
<p>Peace.</p>
</pre>
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
            "url": latest["html_url"],
            "timestamp": dt_obj.timestamp()
        }
    except Exception as e:
        flash(f"failed to fetch commit: {e}")
        return {"message":"failed to fetch.","sha":"none","author":"none","date":"none","url":"none","timestamp":"0"}


