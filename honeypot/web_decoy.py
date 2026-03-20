import flask
from flask import Flask, request, jsonify
import requests
from datetime import datetime, timezone

# --- Configuration ---
INGESTION_URL = "http://127.0.0.1:5000/logs"
app = Flask(__name__)

# --- Fake HTML Pages ---
FAKE_LOGIN_PAGE = """
<!DOCTYPE html><html><head><title>Login</title></head><body>
<h1>Admin Login</h1>
<form method='post' action='/login'>
    User: <input type='text' name='username'><br>
    Pass: <input type='password' name='password'><br>
    <input type='submit' value='Login'>
</form>
</body></html>
"""

FAKE_ADMIN_PANEL = """
<!DOCTYPE html><html><head><title>Admin Panel</title></head><body>
<h1>Admin Panel</h1>
<p>Welcome, admin.</p>
<a href="/logs">View Logs</a>
</body></html>
"""

# --- Logging Function (reused from decoy_server) ---
def log_event(event_type, data):
    """Sends a structured log entry to the ingestion service."""
    timestamp = datetime.now(timezone.utc).isoformat()
    log_entry = {
        "timestamp": timestamp,
        "event_type": event_type,
        "source_ip": data.get("source_ip"),
        "details": data
    }
    try:
        requests.post(INGESTION_URL, json=log_entry, timeout=5)
        print(f"[+] Web log sent for event '{event_type}' from {data.get('source_ip')}")
    except requests.exceptions.RequestException as e:
        print(f"[-] Could not send web log to ingestion service: {e}")

# --- Web Routes ---
@app.route('/')
def index():
    source_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    log_event("web_probe", {"source_ip": source_ip, "path": "/"})
    return "<h1>Welcome to our website!</h1>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    source_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        log_event("web_login_attempt", {"source_ip": source_ip, "username": username, "password": password})
    return FAKE_LOGIN_PAGE

@app.route('/admin')
def admin():
    source_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    log_event("web_probe", {"source_ip": source_ip, "path": "/admin"})
    return FAKE_ADMIN_PANEL

# Catch-all to log any path traversal attempts
@app.route('/<path:path>')
def catch_all(path):
    source_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    log_event("web_probe", {"source_ip": source_ip, "path": f"/{path}"})
    return f"<h1>404 Not Found</h1><p>The path {path} was not found.</p>", 404

if __name__ == '__main__':
    # We run this on port 8080 so it doesn't conflict with other services
    app.run(host='0.0.0.0', port=8080, debug=True)