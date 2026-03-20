# cyphertrace/api/simple_backend.py

from flask import Flask, jsonify, request
import os

# --- CORRECT IMPORT ---
# Import the entire module named 'database'
import database
# --------------------

# Initialize Flask app
app = Flask(__name__)

# Make sure the database is initialized when the server starts
# The path is relative to where you run the script (from the 'api' folder)
db_path = os.path.join(os.getcwd(), 'cyphertrace.db')
if not os.path.exists(db_path):
    print("Database not found. Initializing new database...")
    database.init_db()
else:
    print("Database found. Connecting to existing database.")

# --- ADD THIS DEBUGGING LINE ---
# This will print when the server starts and the routes are registered
print("\n*** REGISTERING FLASK ROUTES ***")
print(" - Registered route: /")
print(" - Registered route: /api/logs")
print(" - Registered route: /api/analysis")
print("*** ROUTE REGISTRATION COMPLETE ***\n")
# ---------------------------------


@app.route('/')
def index():
    return jsonify({"message": "CypherTrace API is running!"})

@app.route('/api/logs')
def send_logs():
    try:
        limit = request.args.get('limit', 100, type=int)
        # Call the function from the imported 'database' module
        logs = database.get_logs(limit=limit)
        
        # --- DEBUGGING PRINT ---
        # This will print the data to your terminal
        print("\n>>> Dashboard requested logs...")
        print(logs)
        print("----------------------\n")
        # --- END DEBUGGING PRINT ---

        return jsonify(logs)
    except Exception as e:
        # Log the error for debugging
        print(f"!!! ERROR in /api/logs (GET): {e} !!!")
        # Return a proper error response to the client
        return jsonify({"error": "Failed to retrieve logs from the database."}), 500

@app.route('/api/analysis')
def send_analysis():
    try:
        # Call the function from the imported 'database' module
        analysis = database.get_analysis()
        
        # --- DEBUGGING PRINT ---
        # This will print the data to your terminal
        print("\n>>> Dashboard requested analysis...")
        print(analysis)
        print("-------------------------\n")
        # --- END DEBUGGING PRINT ---

        if not analysis:
            return jsonify({"message": "No analysis data available yet."}), 404
        return jsonify(analysis)
    except Exception as e:
        # Log the error for debugging
        print(f"!!! ERROR in /api/analysis (GET): {e} !!!")
        # Return a proper error response to the client
        return jsonify({"error": "Failed to retrieve analysis from the database."}), 500

if __name__ == '__main__':
    # Running on 0.0.0.0 makes it accessible from other devices on your network
    # debug=True allows the server to auto-reload when you save changes
    app.run(host='0.0.0.0', port=5000, debug=True)