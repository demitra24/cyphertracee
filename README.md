CYPHERTRACE | Global Threat Intelligence
A threat intelligence platform designed to detect, capture, and visualize real-time cyber attacks using interactive decoy systems (Honeypots).
https://youtu.be/oupMFAQcVnU
Watch the Live Demonstration

Overview
CypherTrace emulates vulnerable SSH and Web services to deceive attackers, log their tactics, and visualize the attack data in real-time. The system captures everything from initial connection probes and brute-force login attempts to post-exploitation command execution, providing a complete kill-chain view of attacker behavior.

Architecture
The system is built on a decoupled Microservices Architecture to separate data ingestion from data analytics, ensuring high availability and scalability.

Decoy Layer:
decoy.server.py: A multi-threaded TCP socket server emulating an SSH terminal on Port 3333. It features a rule-based command parser that generates realistic Linux outputs to increase attacker dwell time.
web.decoy.py: A Flask application on Port 8080 serving fake login portals and admin panels to capture web-based attacks.
Ingestion Layer:
ingest_service.py: A REST API (Port 5000) that receives JSON payloads from the decoy layer, validates them, and writes them to the database.
Analytics Layer:
api_service.py: A REST API (Port 5001) that reads the database, aggregates the data (calculating top IPs, countries, and commands), enriches raw IPs with Geolocation data via ip-api.com, and serves it to the dashboard.
Visualization Layer:
index.html: A lightweight, single-page application using Vanilla JavaScript that polls the Analytics API to render maps, charts, and a live event stream.
Features
Interactive SSH Emulation: Over 30 mapped Linux commands (including ps aux, netstat, cat /etc/passwd, and attacker tools like wget and nmap) return dynamic, randomized outputs to trick automated scripts and human attackers.
Command Categorization: Automatically classifies executed commands into categories (Reconnaissance, Privilege Escalation, Persistence, Exfiltration).
Real-Time Geolocation: Enriches attacker IP addresses with latitude, longitude, and country data, plotting origins on an interactive world map.
Dynamic Dashboard: Visualizes attack volume timelines, event type distributions, and top threat metrics.
IP Filtering & Terminal View: Search the dashboard by specific IP addresses to view their unique attack footprint and a reconstructed terminal output of their session.
Tech Stack
Layer
Technologies
Backend	Python 3, Flask, SQLite3
Frontend	HTML5, CSS3, Vanilla JavaScript
Data Visualization	Chart.js, Leaflet.js
Libraries / APIs	Flask-CORS, Python socket / threading, ip-api.com

Local Setup
To run this project locally, follow these steps:

1.Clone the repository:
bash
:git clone https://github.com/YOUR_USERNAME/cyphertrace.git
cd cyphertrace

2.Install Python dependencies:
bash
pip install flask flask-cors requests

Start the services in separate terminal windows:
bash

# Terminal 1: Start the Ingestion API
python ingest_service.py

# Terminal 2: Start the Analytics API
python api_service.py

# Terminal 3: Start the SSH Honeypot
python decoy.server.py

# Terminal 4: Start the Web Honeypot
python web.decoy.py

Launch the Dashboard:
Open index.html in your web browser.

*Generate Traffic:
SSH Attack: In a new terminal, run ncat 127.0.0.1 3333 and attempt to log in and run commands.

Web Attack: Navigate to http://127.0.0.1:8080 or http://127.0.0.1:8080/admin and submit the fake login forms.

*Design Decisions & Production Roadmap
This project currently uses SQLite for local development and demonstration purposes. SQLite provides a zero-configuration, lightweight database perfect for rapid prototyping and local testing.

In a production environment, the database layer would be migrated to a persistent, cloud-hosted solution like MongoDB Atlas or PostgreSQL. This architecture change is necessary because:

Concurrency: SQLite locks the database on write, which would bottleneck under a high-volume, distributed botnet attack.
Persistence: Free-tier cloud platforms (like Render) use ephemeral file systems that wipe SQLite databases on server sleep/restart. A managed cloud database ensures historical trend analysis is preserved.
Centralization: A cloud database with a connection URI allows multiple distributed honeypot nodes (across different regions) to write to a central data lake.
