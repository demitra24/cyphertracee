import sqlite3

# This will be our database file, stored in the main project folder
DB_FILE = "cyphertrace.db"

def setup_database():
    """Sets up the database and the 'logs' table."""
    print(f"[*] Setting up database: {DB_FILE}")
    
    # Connect to the database (this will create the file if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create the logs table
    # We use IF NOT EXISTS to prevent errors if we run the script multiple times
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            source_ip TEXT NOT NULL,
            details TEXT
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    print("[+] Database and table 'logs' created successfully.")

if __name__ == "__main__":
    setup_database()