from flask import Flask, request, jsonify
import sqlite3
import json
import os

# --- Configuration ---
# Use the same path as api_service.py to ensure both services use the same database
DB_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cyphertrace.db')

# --- Initialize Flask App ---
app = Flask(__name__)

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DB_FILE)
    # This allows us to access columns by name (like a dictionary)
    conn.row_factory = sqlite3.Row
    return conn

# --- API Endpoint for Receiving Logs ---
@app.route('/logs', methods=['POST'])
def receive_log():
    """Receives a JSON log entry and saves it to the database."""
    
    # 1. Check if the request contains JSON data
    if not request.is_json:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

    log_data = request.get_json()

    # 2. Basic validation to ensure required fields are present
    required_fields = ['timestamp', 'event_type', 'source_ip', 'details']
    if not all(field in log_data for field in required_fields):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    try:
        # 3. Connect to the database and insert the log
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO logs (timestamp, event_type, source_ip, details) VALUES (?, ?, ?, ?)",
            (log_data['timestamp'], log_data['event_type'], log_data['source_ip'], json.dumps(log_data['details']))
        )
        
        conn.commit()
        conn.close()
        
        # 4. Print a confirmation to our terminal and return success
        print(f"[+] Log received from {log_data['source_ip']}: {log_data['event_type']}")
        return jsonify({"status": "success", "message": "Log received"}), 201

    except Exception as e:
        # If something goes wrong, return an error
        print(f"[-] Error saving log: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

# --- Main entry point to run the app ---
if __name__ == '__main__':
    # The host='0.0.0.0' makes the server accessible from other devices on your network
    app.run(host='0.0.0.0', port=5000, debug=True)