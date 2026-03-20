import socket
import threading
import json
import requests
from datetime import datetime, timezone, timedelta
import random
import time

# --- Configuration ---
HOST = '0.0.0.0'
PORT = 3333
FAKE_BANNER = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1\n"
FAKE_PROMPT = "root@cyphertrace-vm:~# "

# ==============================================================================
#  FAKE DATA GENERATION FUNCTIONS
# ==============================================================================

# --- Basic Info Commands ---
def get_whoami(): return "root"
def get_pwd(): return "/root"
def get_uname(): return "Linux cyphertrace-vm 5.4.0-42-generic #46-Ubuntu SMP Fri Jul 10 00:24:02 UTC 2020 x86_64 x86_64 GNU/Linux"
def get_hostname(): return "cyphertrace-vm"
def get_arch(): return "x86_64"
def get_id(): return "uid=0(root) gid=0(root) groups=0(root)"
def get_uptime(): return f" {time.strftime('%H:%M:%S')} up 3 days, 12:34, 1 user, load average: 0.08, 0.02, 0.01"

# --- Listing & File Commands ---
def get_ls(): return "Desktop  Documents  Downloads  Music  Pictures  Public  Templates  Videos  system_backup.tar.gz"
def get_ls_la():
    return """total 68
drwxr-xr-x 15 root root 4096 Oct 26 10:00 .
drwxr-xr-x  3 root root 4096 Oct 25 09:00 ..
-rw-------  1 root root  571 Oct 26 10:00 .bash_history
-rw-r--r--  1 root root 3106 Oct 25 09:00 .bashrc
drwxr-xr-x  3 root root 4096 Oct 25 09:00 .cache
drw-r--r--  1 root root  118 Oct 25 09:00 .profile
-rw-r--r--  1 root root  250 Oct 25 09:00 .ssh
drwxr-xr-x  2 root root 4096 Oct 26 10:00 Desktop
drwxr-xr-x  2 root root 4096 Oct 26 10:00 Documents
drwxr-xr-x  2 root root 4096 Oct 26 10:00 Downloads
-rw-r--r--  1 root root  8192 Oct 26 10:00 system_backup.tar.gz
-rw-------  1 root root  2560 Oct 26 10:00 .mysql_history"""
def get_cat_etc_passwd():
    return """root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
mysql:x:117:121:MySQL Server,,,:/nonexistent:/bin/false"""
def get_history():
    commands = ["ls -la", "cd /var/log", "cat auth.log", "ps aux | grep ssh", "systemctl status ssh", "cd /home", "ls", "whoami", "uname -a", "exit"]
    history = []
    now = datetime.now()
    for i, cmd in enumerate(commands):
        timestamp = now - timedelta(minutes=len(commands)-i)
        timestamp_str = timestamp.strftime("%m/%d/%y %H:%M:%S")
        history.append(f"  {timestamp_str}: {cmd}")
    return "\n".join(history)

# --- System & Process Commands ---
def get_ps_aux():
    return """USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.2 168632 12260 ?        Ssl  09:00   0:01 /sbin/init
root         234  0.0  0.1  76488  5680 ?        Ss   09:00   0:00 /usr/sbin/sshd -D
root        1223  0.0  0.1  10724  3424 pts/0    Ss   10:00   0:00 -bash
root        1334  0.0  0.1  14180  3368 pts/0    R+   10:05   0:00 ps aux
mysql       1112  0.2  2.1 1123456 87656 ?        Sl   09:00   0:05 /usr/sbin/mysqld"""
def get_w():
    return f" 10:30:15 up 3 days, 12:34, 1 user, load average: 0.08, 0.02, 0.01\nUSER     TTY      FROM           LOGIN@   IDLE   JCPU   PCPU WHAT\nroot     pts/0    192.168.1.105  10:00    5.00s  0.12s  0.02s -bash"
def get_last():
    return """root     pts/0        192.168.1.105   Tue Oct 26 10:00   still logged in
reboot   system boot  5.4.0-42-generi Tue Oct 23 09:00   still running
root     pts/0        192.168.1.105   Mon Oct 25 22:15 - 23:45  (01:30)
root     tty1         :1               Mon Oct 25 09:00 - 09:01  (00:01)"""
def get_top():
    return """top - 10:30:15 up 3 days, 12:34,  1 user,  load average: 0.08, 0.02, 0.01
Tasks:  98 total,   1 running,  97 sleeping,   0 stopped,   0 zombie
%Cpu(s):  5.0 us,  2.5 sy,  0.0 ni, 92.5 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   1980.1 total,    250.5 free,    950.8 used,    778.8 buff/cache
MiB Swap:   2048.0 total,   1845.2 free,    202.8 used.    827.3 avail Mem

    PID USER      PR  NI VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   1334 root      20   0  14180   3368   2840 R   5.0   0.2   0:00.05 ps
   1112 mysql     20   0 1123456 87656  15456 S   2.0   4.3   0:05.12 mysqld
    234 root      20   0  76488   5680   5256 S   0.0   0.3   0:00.10 sshd"""
def get_lscpu():
    return """Architecture:        x86_64
CPU op-mode(s):      32-bit, 64-bit
Byte Order:          Little Endian
CPU(s):              2
On-line CPU(s) list: 0,1
Thread(s) per core:  1
Core(s) per socket:  2
Socket(s):           1
..."""
def get_df_h():
    return """Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        20G   5.5G   14G  29% /
tmpfs           478M     0  478M   0% /dev/shm
/dev/sdb1       100G   12G   88G  12% /var/data"""
def get_free_h():
    return """              total        used        free      shared  buff/cache   available
Mem:          1.9Gi       950Mi       250Mi       15Mi       778Mi       827Mi
Swap:         2.0Gi       202Mi       1.8Gi"""

# --- Network Commands ---
def get_ip_a():
    return """1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:a1:b2:c3 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.50/24 brd 192.168.1.255 scope global eth0
       valid_lft forever preferred_lft forever"""
def get_ifconfig():
    return """eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.50  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::a00:27ff:fea1:b2c3  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:a1:b2:c3  txqueuelen 1000  (Ethernet)
        RX packets 12345  bytes 1152345 (1.1 MB)
        TX packets 9876  bytes 987654 (987.6 KB)
lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0"""
def get_netstat(): return get_ss_tulpn() # Re-use the same output
def get_ss_tulpn():
    return """Netid State  Recv-Q Send-Q Local Address:Port   Peer Address:Port
tcp   LISTEN 0      128          0.0.0.0:22        0.0.0.0:*
tcp   LISTEN 0      50         127.0.0.1:3306      0.0.0.0:*
tcp   LISTEN 0      5          127.0.0.1:631       0.0.0.0:*
tcp   LISTEN 0      40             :::80           :::*
tcp   LISTEN 0      128             :::22           :::*
udp   UNCONN 0      0          0.0.0.0:68          0.0.0.0:*
udp   UNCONN 0      0          0.0.0.0:631         0.0.0.0:*"""
def get_arp_a():
    return """? (192.168.1.1) at 0a:1b:2c:3d:4e:5f [ether] on eth0
? (192.168.1.105) at ff:ee:dd:cc:bb:aa [ether] on eth0"""
def get_route():
    return """Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.1.1     0.0.0.0         UG    100    0        0 eth0
192.168.1.0     0.0.0.0         255.255.255.0   U     100    0        0 eth0"""

# --- Privilege Escalation & Persistence Commands ---
def get_sudo_l():
    return "Sorry, user root may not run sudo on cyphertrace-vm."
def get_sudo_su():
    return "[sudo] password for root: "
def get_cat_crontab():
    return """# /etc/crontab: system-wide crontab
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
# Fake hidden job
*/15 * * * * root /root/.hidden/backup.sh > /dev/null 2>&1"""
def get_systemctl_list():
    return """UNIT                        LOAD   ACTIVE SUB     DESCRIPTION
accounts-daemon.service     loaded active running   Accounts Service
cron.service                loaded active running   Regular background program processing daemon
mysql.service               loaded active running   MySQL Community Server
networkd-dispatcher.service loaded active running   Dispatcher daemon for systemd-networkd
ssh.service                 loaded active running   OpenSSH SSH server daemon
systemd-resolved.service    loaded active running   Network Name Resolution"""

# --- Attacker Tool & Script Commands ---
def get_wget(url):
    return f"--2023-10-26 10:30:15--  {url}\nResolving {url.split('//')[1]}... 127.0.0.1\nConnecting to {url.split('//')[1]}|127.0.0.1|:80... connected.\nHTTP request sent, awaiting response... 200 OK\nLength: 12345 (12K) [application/x-sh]\nSaving to: ‘malware.sh’\n\nmalware.sh             [ <=>                ]  12.34K  --.-KB/s    in 0.001s\n\n2023-10-26 10:30:15 (12.3 MB/s) - ‘malware.sh’ saved [12345/12345]"
def get_curl(url):
    return f"  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current\n                                 Dload  Upload   Total   Spent    Left  Speed\n100 12345  100 12345    0     0  12.3M      0 --:--:-- --:--:-- --:--:-- 12.3M"
def get_nc_l():
    return "Ncat: Listening on 0.0.0.0:4444"
def get_nc_exfil():
    return "Connection to 10.10.10.10 1234 port [tcp/*] succeeded!"
def get_apt_install(tool):
    return f"Reading package lists... Done\nBuilding dependency tree... Done\nReading state information... Done\nThe following NEW packages will be installed:\n  {tool}\n0 upgraded, 1 newly installed, 0 to remove and 5 not upgraded.\nNeed to get 1234 kB of archives.\nAfter this operation, 5678 kB of additional disk space will be used.\nGet:1 http://archive.ubuntu.com/ubuntu focal/main amd64 {tool} amd64 1.2.3-4 [1234 kB]\nFetched 1234 kB in 0s (1234 kB/s)\nSelecting previously unselected package {tool}.\n(Reading database ... 12345 files and directories currently installed.)\nPreparing to unpack .../{tool}_1.2.3-4_amd64.deb ...\nUnpacking {tool} (1.2.3-4) ...\nSetting up {tool} (1.2.3-4) ...\nProcessing triggers for man-db (2.9.1-1) ..."

# --- Destructive & Cleanup Commands ---
def get_rm_rf_root():
    return "rm: it is dangerous to operate recursively on '/'\nrm: use --no-preserve-root to override this failsafe"
def get_dd_wipe():
    return "dd: failed to open '/dev/sda': Permission denied"

# --- Misc & Error Commands ---
def get_help():
    return """GNU bash, version 5.0.17(1)-release (x86_64-pc-linux-gnu)
These shell commands are defined internally.  Type `help' to see this list."""
def get_echo_path():
    return "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"
def get_man_page(cmd):
    return f"No manual entry for {cmd}"
def get_find_conf():
    return "/etc/ssh/sshd_config\n/etc/mysql/my.cnf\n/etc/apache2/apache2.conf\n/var/www/html/config.php"
def get_find_suid():
    return "/usr/bin/passwd\n/usr/bin/chsh\n/usr/bin/gpasswd\n/bin/su\n/bin/mount\n/bin/umount"


# ==============================================================================
#  COMMAND PROCESSING LOGIC
# ==============================================================================

def get_command_output(command):
    """Returns the appropriate output for a given command"""
    cmd_parts = command.split()
    cmd = cmd_parts[0].lower()
    
    # Basic Info
    if cmd == "whoami": return get_whoami()
    elif cmd == "pwd": return get_pwd()
    elif cmd == "hostname": return get_hostname()
    elif cmd == "arch": return get_arch()
    elif cmd == "id": return get_id()
    elif cmd == "uptime": return get_uptime()
    elif cmd == "uname":
        if "-a" in cmd_parts: return get_uname()
        elif "-m" in cmd_parts: return get_arch()
        else: return "Linux"
    elif cmd == "w": return get_w()
    elif cmd == "who": return "root     pts/0        2023-10-26 10:00 (192.168.1.105)"
    elif cmd == "last": return get_last()
    elif cmd == "lastlog": return "Username     Port     From             Latest\nroot         pts/0                     192.168.1.105  Thu Oct 26 10:00:00 +0000 2023"

    # Listing & Files
    elif cmd == "ls":
        if "-la" in cmd_parts: return get_ls_la()
        elif "-R" in cmd_parts: return get_ls() + "\n./Documents:\nfile1.txt file2.pdf\n./Downloads:\ninstaller.run"
        else: return get_ls()
    elif cmd == "dir": return get_ls()
    elif cmd == "cat":
        if len(cmd_parts) > 1:
            if "/etc/passwd" in command: return get_cat_etc_passwd()
            elif ".bash_history" in command: return get_history()
            elif "/etc/crontab" in command: return get_cat_crontab()
            else: return f"cat: {cmd_parts[1]}: No such file or directory"
        else: return "cat: missing file operand\nTry 'cat --help' for more information."
    elif cmd == "history": return get_history()
    elif cmd == "find":
        if "-name" in command and "*.conf" in command: return get_find_conf()
        elif "-perm" in command and "4000" in command: return get_find_suid()
        else: return "find: missing argument to `-name'"
        
    # System & Processes
    elif cmd == "ps":
        if "aux" in cmd_parts: return get_ps_aux()
        else: return "  PID TTY          TIME CMD\n 1234 pts/0    00:00:00 bash\n 5678 pts/0    00:00:00 ps"
    elif cmd == "top": return get_top()
    elif cmd == "lscpu": return get_lscpu()
    elif cmd == "df":
        if "-h" in cmd_parts: return get_df_h()
        else: return get_df_h() # Default to human readable
    elif cmd == "free":
        if "-h" in cmd_parts: return get_free_h()
        else: return get_free_h() # Default to human readable

    # Network
    elif cmd == "ip":
        if "a" in cmd_parts: return get_ip_a()
        else: return "Try 'ip --help' for more information."
    elif cmd == "ifconfig": return get_ifconfig()
    elif cmd == "netstat": return get_netstat()
    elif cmd == "ss":
        if "-tulpn" in cmd_parts: return get_ss_tulpn()
        else: return get_ss_tulpn() # Default to common options
    elif cmd == "arp":
        if "-a" in cmd_parts: return get_arp_a()
        else: return "Try 'arp --help' for more information."
    elif cmd == "route": return get_route()
    elif cmd == "iwconfig": return "lo        no wireless extensions.\neth0      no wireless extensions."

    # Privilege Escalation
    elif cmd == "sudo":
        if "-l" in cmd_parts: return get_sudo_l()
        elif "su" in cmd_parts: return get_sudo_su()
        else: return "sudo: a password is required"
    elif cmd == "su": return "Password:"
    elif cmd == "systemctl":
        if "list-units" in command: return get_systemctl_list()
        else: return "Try 'systemctl --help' for more information."

    # Attacker Tools
    elif cmd == "wget":
        if len(cmd_parts) > 1: return get_wget(cmd_parts[1])
        else: return "wget: missing URL"
    elif cmd == "curl":
        if len(cmd_parts) > 1: return get_curl(cmd_parts[1])
        else: return "curl: try 'curl --help' for more information"
    elif cmd == "nc" or cmd == "netcat":
        if "-l" in cmd_parts: return get_nc_l()
        elif len(cmd_parts) > 3: return get_nc_exfil()
        else: return "This is nc from the nmap project, not the traditional GNU netcat."
    elif cmd == "python" or cmd == "perl":
        # Just pretend the one-liner executed and gave no output
        return ""
    elif cmd == "apt" or cmd == "apt-get":
        if "install" in cmd_parts and len(cmd_parts) > 2: return get_apt_install(cmd_parts[2])
        else: return "apt 2.0.2 (amd64)\nUsage: apt [options] command"
    elif cmd == "chmod": return "" # Just accept it
    elif cmd == "tar": return "a/\na/file1.txt\na/file2.txt\nb/\nb/file3.txt" # Fake listing
    
    # Destructive / Cleanup
    elif cmd == "rm":
        if "-rf" in cmd_parts and "/" in command and "--no-preserve-root" not in command:
            return get_rm_rf_root()
        else: return "" # Pretend it worked
    elif cmd == "dd": return get_dd_wipe()
    elif cmd == "history": return get_history()
    elif cmd in ["clear", "cls"]: return "\n\n" # Simulate clearing the screen
    elif cmd == "man":
        if len(cmd_parts) > 1: return get_man_page(cmd_parts[1])
        else: return "What manual page do you want?"
    elif cmd == "echo":
        if "$PATH" in command: return get_echo_path()
        else: return " ".join(cmd_parts[1:]) # Echo back whatever they typed
    elif cmd == "help": return get_help()
    elif cmd == "exit": return "logout"
    
    # Default for unknown commands
    else:
        # Suggest corrections for common typos
        if cmd == "sl": return f"bash: {cmd}: command not found. Did you mean 'ls'?"
        elif cmd == "cd..": return f"bash: {cmd}: command not found. Did you mean 'cd ..'?"
        else: return f"bash: {cmd}: command not found"


# ==============================================================================
#  HONEYPOT SERVER LOGIC
# ==============================================================================

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
        response = requests.post("http://127.0.0.1:5000/logs", json=log_entry, timeout=5)
        print(f"[+] Log sent for event '{event_type}' from {data.get('source_ip')}. Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[-] Could not send log to ingestion service: {e}")

def handle_client(client_socket, client_address):
    """Handles a client connection."""
    source_ip = client_address[0]
    log_event("connection_established", {"source_ip": source_ip, "source_port": client_address[1]})
    
    try:
        client_socket.send(FAKE_BANNER.encode('utf-8'))
        
        username = client_socket.recv(1024).decode('utf-8').strip()
        if username: log_event("login_attempt", {"source_ip": source_ip, "username": username})
        client_socket.send(b"Password: ")
        password = client_socket.recv(1024).decode('utf-8').strip()
        if password: log_event("login_attempt", {"source_ip": source_ip, "password": password})

        client_socket.send(b"Access granted. Welcome.\n")
        
        while True:
            client_socket.send(FAKE_PROMPT.encode('utf-8'))
            
            try:
                data = client_socket.recv(1024)
                if not data:
                    log_event("session_ended", {"source_ip": source_ip, "reason": "Client disconnected"})
                    break

                command = data.decode('utf-8', errors='ignore').strip()
                
                if not command: continue

                if command.lower() == "exit":
                    log_event("session_ended", {"source_ip": source_ip, "reason": "User typed 'exit'"})
                    break

                log_event("command_executed", {"source_ip": source_ip, "command": command})
                response = get_command_output(command)
                client_socket.send(response.encode('utf-8') + b'\n')

            except (ConnectionResetError, BrokenPipeError):
                log_event("connection_lost", {"source_ip": source_ip})
                break

    except (ConnectionResetError, BrokenPipeError):
        log_event("connection_lost", {"source_ip": source_ip})
    finally:
        client_socket.close()
        log_event("connection_closed", {"source_ip": source_ip})

def start_honeypot():
    """Starts the interactive honeypot server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"[*] ADVANCED HONEYPOT listening on {HOST}:{PORT}")

        while True:
            client_socket, client_address = server.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.daemon = True
            client_handler.start()
    except OSError as e:
        print(f"[!] ERROR: Could not start honeypot. {e}")
    except KeyboardInterrupt:
        print("\n[*] Honeypot is shutting down.")
    finally:
        if 'server' in locals() and server:
            server.close()

if __name__ == "__main__":
    start_honeypot()