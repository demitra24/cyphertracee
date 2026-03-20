# api_service.py

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
import requests
import json
from collections import Counter

# --- Configuration ---
DB_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cyphertrace.db')
GEOLOCATION_API_URL = "http://ip-api.com/json/"

# --- Initialize Flask App ---
app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# --- Helper function to get location for an IP ---
def get_location_for_ip(ip):
    """Fetches geolocation data for a given IP."""
    if ip in ('127.0.0.1', 'localhost'):
        return {"lat": 37.7749, "lon": -122.4194, "country": "Localhost"} # Default to San Francisco
    try:
        response = requests.get(f"{GEOLOCATION_API_URL}{ip}")
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        pass
    return None

# --- Helper function to print log to terminal ---
def print_log_to_terminal(log):
    """Prints a formatted log entry to the terminal."""
    timestamp = log['timestamp']
    event_type = log['event_type'].upper().replace('_', ' ')
    source_ip = log['source_ip']
    country = log.get('country', 'N/A')
    
    try:
        details = json.loads(log['details'])
        details_str = ""
        
        if log['event_type'] == 'web_login_attempt' and details.get('username'):
            details_str = f" | USER: \"{details['username']}\" | STATUS: {details.get('status', 'N/A')}"
        elif log['event_type'] == 'login_attempt' and details.get('username'):
            details_str = f" | USER: \"{details['username']}\""
        elif log['event_type'] == 'command_executed' and details.get('command'):
            details_str = f" | CMD: \"{details['command']}\""
        
        print(f"[EVENT STREAM] [{timestamp}] {event_type} | {source_ip} | {country}{details_str}")
    except json.JSONDecodeError:
        print(f"[EVENT STREAM] [{timestamp}] {event_type} | {source_ip} | {country} | ERROR: Could not parse details")

# --- API Endpoint to Get Logs ---
@app.route('/api/logs', methods=['GET'])
def get_logs():
    limit = request.args.get('limit', 1000, type=int)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT ?", (limit,))
        logs = cursor.fetchall()
        conn.close()

        logs_list = []
        processed_ips = set()

        for log in logs:
            log_dict = dict(log)
            source_ip = log_dict['source_ip']

            if source_ip not in processed_ips:
                location = get_location_for_ip(source_ip)
                if location and location.get('status') != 'fail':
                    log_dict['lat'] = location.get('lat')
                    log_dict['lon'] = location.get('lon')
                    log_dict['country'] = location.get('country', 'Unknown')
                else:
                    log_dict['lat'], log_dict['lon'], log_dict['country'] = None, None, 'Unknown'
                processed_ips.add(source_ip)
            
            logs_list.append(log_dict)
            # Print each log to the terminal
            print_log_to_terminal(log_dict)
        
        print(f"\n[EVENT STREAM] --- Displayed {len(logs_list)} most recent events ---\n")
        
        return jsonify(logs_list)

    except Exception as e:
        print(f"[-] Error fetching logs: {e}")
        return jsonify({"status": "error", "message": "Could not fetch logs"}), 500

# --- New, Enhanced API Endpoint for Analysis ---
@app.route('/api/analysis', methods=['GET'])
def get_analysis():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all logs to perform analysis
        cursor.execute("SELECT source_ip, details, event_type FROM logs")
        all_logs_for_analysis = cursor.fetchall()
        conn.close()

        # --- Perform Calculations ---
        total_events = len(all_logs_for_analysis)
        unique_sources = len(set(log['source_ip'] for log in all_logs_for_analysis))
        
        # Top Source IP
        ip_counts = Counter(log['source_ip'] for log in all_logs_for_analysis)
        top_source_ip, _ = ip_counts.most_common(1)[0] if ip_counts else ("-", 0)

        # Most Common Command
        commands = []
        for log in all_logs_for_analysis:
            if log['event_type'] == 'command_executed':
                try:
                    details = json.loads(log['details'])
                    commands.append(details.get('command'))
                except json.JSONDecodeError:
                    continue
        command_counts = Counter(commands)
        most_common_command, _ = command_counts.most_common(1)[0] if command_counts else ("-", 0)
        
        # Top Source Country (This is the new part)
        # We need to fetch country data for all unique IPs
        country_counts = Counter()
        for ip in ip_counts:
            location = get_location_for_ip(ip)
            if location and location.get('status') != 'fail':
                country = location.get('country', 'Unknown')
                country_counts[country] += 1
        
        top_source_country, _ = country_counts.most_common(1)[0] if country_counts else ("-", 0)

        return jsonify({
            "total_events": total_events,
            "unique_sources": unique_sources,
            "top_source_ip": top_source_ip,
            "top_source_country": top_source_country,
            "most_common_command": most_common_command
        })
        
    except Exception as e:
        print(f"[-] Error fetching analysis: {e}")
        return jsonify({"status": "error", "message": "Could not fetch analysis"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)