import random
import string
from datetime import datetime, timedelta

# ==============================================================================
#  DATA GENERATION FUNCTIONS
# ==============================================================================

def get_whoami():
    """Returns a fake username"""
    return "root"

def get_pwd():
    """Returns a fake current directory"""
    return "/root"

def get_hostname():
    """Returns a fake hostname"""
    return "cyphertrace-vm"

def get_arch():
    """Returns a fake architecture"""
    return "x86_64"

def get_uname():
    """Returns fake system information"""
    return "Linux cyphertrace-vm 5.4.0-42-generic #46-Ubuntu SMP Fri Jul 10 00:24:02 UTC 2020 x86_64 x86_64 GNU/Linux"

def get_id():
    """Returns fake user ID information"""
    return "uid=0(root) gid=0(root) groups=0(root)"

def get_uptime():
    """Returns a fake uptime"""
    return " 10:30:15 up 2 days, 15:20,  1 user,  load average: 0.08, 0.12, 0.18"

def get_w():
    """Returns a fake 'w' command output"""
    return """ 10:30:15 up 2 days, 15:20,  1 user,  load average: 0.08, 0.12, 0.18
USER     TTY      FROM           LOGIN@   IDLE   JCPU   PCPU WHAT
root     pts/0    192.168.1.105  10:00    5.00s  0.12s  0.02s -bash"""

def get_last():
    """Returns a fake 'last' command output"""
    return """root     pts/0        192.168.1.105  Thu Oct 26 10:00   still logged in
root     pts/0        192.168.1.105  Thu Oct 25 18:30 - 19:00  (00:30)
reboot   system boot  5.4.0-42-gener Thu Oct 25 18:00   still running
wtmp begins Thu Oct 25 18:00:00 2023"""

def get_lastlog():
    """Returns a fake 'lastlog' command output"""
    return "Username     Port     From             Latest\nroot         pts/0    192.168.1.105  Thu Oct 26 10:00:00 +0000 2023"

def get_ls():
    """Returns a fake directory listing"""
    return "Desktop  Documents  Downloads  Music  Pictures  Public  Templates  Videos"

def get_ls_la():
    """Returns a fake detailed directory listing"""
    return """total 64
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

def get_ps_aux():
    """Returns a fake process list"""
    processes = [
        "USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND",
        "root           1  0.0  0.2 168632 12260 ?        Ssl  09:00   0:01 /sbin/init",
        "root         234  0.0  0.1  76488  5680 ?        Ss   09:00   0:00 /usr/sbin/sshd -D",
        "root         456  0.0  0.3 190456 12400 ?        Sl   09:00   0:00 /usr/lib/accountsservice/accounts-daemon",
        "root         567  0.0  0.2  90480  9216 ?        Ss   09:00   0:00 /usr/sbin/cron -f",
        "mysql       1112  0.2  2.1 1123456 87656 ?        Sl   09:00   0:05 /usr/sbin/mysqld",
        "root        1223  0.0  0.1  10724  3424 pts/0    Ss   10:00   0:00 -bash",
        "root        1334  0.0  0.1  14180  3368 pts/0    R+   10:05   0:00 ps aux"
    ]
    for i in range(3):
        pid = random.randint(2000, 3000)
        cpu = round(random.uniform(0.0, 1.0), 1)
        mem = round(random.uniform(0.1, 2.0), 1)
        vsz = random.randint(10000, 50000)
        rss = random.randint(1000, 10000)
        processes.append(f"root        {pid}  {cpu}  {mem} {vsz} {rss} ?        S    09:00   0:00 /usr/lib/some_service")
    return "\n".join(processes)

def get_top():
    """Returns a fake 'top' command header and process list"""
    return """top - 10:30:15 up 2 days, 15:20,  1 user,  load average: 0.08, 0.12, 0.18
Tasks: 105 total,   1 running,  80 sleeping,   0 stopped,   0 zombie
%Cpu(s):  5.0 us,  2.5 sy,  0.0 ni, 92.5 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   1990.4 total,   1234.5 free,    400.2 used,    355.7 buff/cache
MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.   1390.2 avail Mem
""" + get_ps_aux()

def get_lscpu():
    """Returns fake CPU architecture information"""
    return """Architecture:        x86_64
CPU op-mode(s):      32-bit, 64-bit
Byte Order:          Little Endian
CPU(s):              2
On-line CPU(s) list: 0,1
Thread(s) per core:  1
Core(s) per socket:  2
Socket(s):           1
NUMA node(s):        1
Vendor ID:           GenuineIntel
CPU family:          6
Model:               142
Model name:          Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz
Stepping:            10
CPU MHz:             1800.000
BogoMIPS:            3600.00
Hypervisor vendor:   KVM
Virtualization type: full
L1d cache:           32K
L1i cache:           32K
L2 cache:            256K
L3 cache:            4096K
NUMA node0 CPU(s):   0,1"""

def get_df_h():
    """Returns fake disk usage in human-readable format"""
    return """Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        20G   5.5G   14G  29% /
tmpfs           492M     0  492M   0% /dev/shm
tmpfs           492M  6.8M  485M   2% /run
tmpfs           492M     0  492M   0% /sys/fs/cgroup
/dev/sdb1       100G   20G   80G  20% /mnt/data"""

def get_free_h():
    """Returns fake memory usage in human-readable format"""
    return """              total        used        free      shared  buff/cache   available
Mem:          1.9Gi       400Mi       1.2Gi       8.0Mi       355Mi       1.3Gi
Swap:         2.0Gi          0B       2.0Gi"""

def get_cat_etc_passwd():
    """Returns a fake /etc/passwd file"""
    return """root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
syslog:x:102:106::/home/syslog:/usr/sbin/nologin
messagebus:x:103:107::/nonexistent:/usr/sbin/nologin
uuidd:x:104:108::/run/uuidd:/usr/sbin/nologin
dnsmasq:x:105:109:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
usbmux:x:106:110:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
rtkit:x:107:111:RealtimeKit,,,:/proc:/usr/sbin/nologin
pulse:x:108:112:PulseAudio daemon,,,:/var/run/pulse:/usr/sbin/nologin
speech-dispatcher:x:109:113:Speech Dispatcher,,,:/var/run/speech-dispatcher:/usr/sbin/nologin
avahi:x:110:114:Avahi mDNS daemon,,,:/var/run/avahi-daemon:/usr/sbin/nologin
saned:x:111:115::/var/lib/saned:/usr/sbin/nologin
colord:x:112:116:colord colour management daemon,,,:/var/lib/colord:/usr/sbin/nologin
hplip:x:113:117:HPLIP system user,,,:/var/run/hplip:/usr/sbin/nologin
geoclue:x:114:118::/var/lib/geoclue:/usr/sbin/nologin
gnome-initial-setup:x:115:119::/run/gnome-initial-setup/:/bin/false
gdm:x:116:120:Gnome Display Manager:/var/lib/gdm3:/bin/false
mysql:x:117:121:MySQL Server,,,:/nonexistent:/bin/false"""

def get_netstat():
    """Returns a fake netstat output"""
    return """Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN     
tcp6       0      0 :::80                   :::*                    LISTEN     
tcp6       0      0 :::22                   :::*                    LISTEN     
tcp6       0      0 ::1:631                 :::*                    LISTEN     
udp        0      0 0.0.0.0:68              0.0.0.0:*                          
udp        0      0 0.0.0.0:631             0.0.0.0:*                          
udp6       0      0 fe80::a00:27ff:fe4e:546 :::*                               

Active UNIX domain sockets (servers and established)
Proto RefCnt Flags       Type       State         I-Node   Path
unix  2      [ ACC ]     STREAM     LISTENING     12345    /run/systemd/private
unix  2      [ ACC ]     STREAM     LISTENING     12346    /run/lvm/lvmetad.socket
unix  2      [ ACC ]     STREAM     LISTENING     12347    /run/udev/control
unix  2      [ ACC ]     STREAM     LISTENING     12348    /var/run/dbus/system_bus_socket"""

def get_ip_a():
    """Returns a fake 'ip a' command output"""
    return """1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:a1:b2:c3 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.100/24 brd 192.168.1.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fea1:b2c3/64 scope link
       valid_lft forever preferred_lft forever"""

def get_ifconfig():
    """Returns a fake 'ifconfig' command output"""
    return """eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::a00:27ff:fea1:b2c3  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:a1:b2:c3  txqueuelen 1000  (Ethernet)
        RX packets 12345  bytes 1234567 (1.2 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 54321  bytes 7654321 (7.6 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 123  bytes 45678 (45.6 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 123  bytes 45678 (45.6 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0"""

def get_ss_tulpn():
    """Returns a fake 'ss -tulpn' command output"""
    return """Netid State  Recv-Q Send-Q Local Address:Port   Peer Address:Port
tcp   LISTEN 0      128          0.0.0.0:22        0.0.0.0:*
tcp   LISTEN 0      50         127.0.0.1:3306      0.0.0.0:*
tcp   LISTEN 0      5          127.0.0.1:631       0.0.0.0:*
tcp   LISTEN 0      40             :::80           :::*
tcp   LISTEN 0      128             :::22           :::*
udp   UNCONN 0      0          0.0.0.0:68          0.0.0.0:*
udp   UNCONN 0      0          0.0.0.0:631         0.0.0.0:*"""

def get_arp_a():
    """Returns a fake 'arp -a' command output"""
    return """? (192.168.1.1) at 0a:1b:2c:3d:4e:5f [ether] on eth0
? (192.168.1.105) at ff:ee:dd:cc:bb:aa [ether] on eth0"""

def get_route():
    """Returns a fake 'route' command output"""
    return """Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.1.1     0.0.0.0         UG    100    0        0 eth0
192.168.1.0     0.0.0.0         255.255.255.0   U     100    0        0 eth0"""

def get_sudo_l():
    """Returns a fake 'sudo -l' command output"""
    return "Sorry, user root may not run sudo on cyphertrace-vm."

def get_sudo_su():
    """Returns a fake 'sudo su' command output"""
    return "[sudo] password for root: "

def get_cat_crontab():
    """Returns a fake /etc/crontab file with a hidden job"""
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
    """Returns a fake 'systemctl list-units' command output"""
    return """UNIT                        LOAD   ACTIVE SUB     DESCRIPTION
accounts-daemon.service     loaded active running   Accounts Service
cron.service                loaded active running   Regular background program processing daemon
mysql.service               loaded active running   MySQL Community Server
networkd-dispatcher.service loaded active running   Dispatcher daemon for systemd-networkd
ssh.service                 loaded active running   OpenSSH SSH server daemon
systemd-resolved.service    loaded active running   Network Name Resolution"""

def get_wget(url):
    """Returns a fake 'wget' command output"""
    return f"--2023-10-26 10:30:15--  {url}\nResolving {url.split('//')[1]}... 127.0.0.1\nConnecting to {url.split('//')[1]}|127.0.0.1|:80... connected.\nHTTP request sent, awaiting response... 200 OK\nLength: 12345 (12K) [application/x-sh]\nSaving to: ‘malware.sh’\n\nmalware.sh             [ <=>                ]  12.34K  --.-KB/s    in 0.001s\n\n2023-10-26 10:30:15 (12.3 MB/s) - ‘malware.sh’ saved [12345/12345]"

def get_curl(url):
    """Returns a fake 'curl' command output"""
    return f"  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current\n                                 Dload  Upload   Total   Spent    Left  Speed\n100 12345  100 12345    0     0  12.3M      0 --:--:-- --:--:-- --:--:-- 12.3M"

def get_nc_l():
    """Returns a fake 'nc -l' command output"""
    return "Ncat: Listening on 0.0.0.0:4444"

def get_nc_exfil():
    """Returns a fake 'nc' exfil command output"""
    return "Connection to 10.10.10.10 1234 port [tcp/*] succeeded!"

def get_apt_install(tool):
    """Returns a fake 'apt install' command output"""
    return f"Reading package lists... Done\nBuilding dependency tree... Done\nReading state information... Done\nThe following NEW packages will be installed:\n  {tool}\n0 upgraded, 1 newly installed, 0 to remove and 5 not upgraded.\nNeed to get 1234 kB of archives.\nAfter this operation, 5678 kB of additional disk space will be used.\nGet:1 http://archive.ubuntu.com/ubuntu focal/main amd64 {tool} amd64 1.2.3-4 [1234 kB]\nFetched 1234 kB in 0s (1234 kB/s)\nSelecting previously unselected package {tool}.\n(Reading database ... 12345 files and directories currently installed.)\nPreparing to unpack .../{tool}_1.2.3-4_amd64.deb ...\nUnpacking {tool} (1.2.3-4) ...\nSetting up {tool} (1.2.3-4) ...\nProcessing triggers for man-db (2.9.1-1) ..."

def get_rm_rf_root():
    """Returns the output for a dangerous 'rm -rf /' command"""
    return "rm: it is dangerous to operate recursively on '/'\nrm: use --no-preserve-root to override this failsafe"

def get_dd_wipe():
    """Returns the output for a disk wiping command"""
    return "dd: failed to open '/dev/sda': Permission denied"

def get_help():
    """Returns a fake help message"""
    return """GNU bash, version 5.0.17(1)-release (x86_64-pc-linux-gnu)
These shell commands are defined internally.  Type `help' to see this list.
Type `help name' to find out more about the function `name'.
Use `info bash' to find out more about the shell in general.
Use `man -k' or `info' to find out more about commands not in this list.

A star (*) next to a name means that the command is disabled.

 job_spec [&]                                                                              
 history [-c] [-d offset] [n] or history -anrw [filename] or history -ps arg [arg...]
 let arg [arg ...]                                                                        
 local [option] name[=value] ...                                                         
 logout [n]                                                                               
 mapfile [-d delim] [-n count] [-O origin] [-s count] [-t] [-u fd] [-C callback]        
 popd [-n] [+N | -N]                                                                      
 printf [-v var] format [arguments]                                                      
 pushd [-n] [+N | -N] [dir]                                                              
 pwd [-LP]                                                                                
 read [-ers] [-a array] [-d delim] [-i text] [-n nchars] [-N nsecs] [-p prompt] [-t timeout]
 [-u fd] [name ...]                                                                      
 readarray [-d delim] [-n count] [-O origin] [-s count] [-t] [-u fd] [-C callback]       
 readonly [-aAf] [name[=value] ...] or readonly -p                                       
 return [n]                                                                               
 select NAME [in WORDS ... ;] do COMMANDS; done                                          
 set [-abefhkmnptuvxBCHP] [-o option-name] [--] [arg ...]                                
 shift [n]                                                                                
 shopt [-pqsu] [-o] [optname ...]                                                        
 source filename [arguments]                                                              
 suspend [-f]                                                                             
 test [expr]                                                                              
 times                                                                                    
 trap [-lp] [[arg] signal_spec ...]                                                      
 type [-afptP] name [name ...]                                                            
 ulimit [-SHabcdefiklmnpqrstuvxPRT] [limit]                                              
 umask [-p] [-S] [mode]                                                                   
 unalias [-a] name [name ...]                                                             
 unset [-f] [-v] [-n] [name ...]                                                         
 wait [-n] [id ...]                                                                       
 wait [id]"""

def get_history():
    """Returns a fake command history"""
    commands = [
        "ls -la",
        "cd /var/log",
        "cat auth.log",
        "ps aux | grep ssh",
        "systemctl status ssh",
        "cd /home",
        "ls",
        "cd /root",
        "ls -la",
        "cat .bash_history",
        "whoami",
        "uname -a",
        "netstat -tulpn",
        "cat /etc/passwd",
        "find / -name '*.conf' 2>/dev/null",
        "cat /etc/ssh/sshd_config",
        "systemctl restart ssh",
        "exit"
    ]
    history = []
    now = datetime.now()
    for i, cmd in enumerate(commands):
        timestamp = now - timedelta(minutes=len(commands)-i)
        timestamp_str = timestamp.strftime("%m/%d/%y %H:%M:%S")
        history.append(f"  {timestamp_str}: {cmd}")
    return "\n".join(history)

def get_find_conf():
    """Returns fake output for 'find / -name \"*.conf\"'"""
    return "/etc/ssh/sshd_config\n/etc/mysql/my.cnf\n/etc/apache2/apache2.conf\n/var/www/html/config.php"

def get_find_suid():
    """Returns fake output for 'find / -perm 4000'"""
    return "/usr/bin/passwd\n/usr/bin/chsh\n/usr/bin/gpasswd\n/bin/su\n/bin/mount\n/bin/umount"

def get_echo_path():
    """Returns the fake $PATH variable"""
    return "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"

def get_man_page(cmd):
    """Returns a fake 'man page not found' error"""
    return f"No manual entry for {cmd}"

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
        return ""
    elif cmd == "apt" or cmd == "apt-get":
        if "install" in cmd_parts and len(cmd_parts) > 2: return get_apt_install(cmd_parts[2])
        else: return "apt 2.0.2 (amd64)\nUsage: apt [options] command"
    elif cmd == "chmod": return ""
    elif cmd == "tar": return "a/\na/file1.txt\na/file2.txt\nb/\nb/file3.txt"
    
    # Destructive / Cleanup
    elif cmd == "rm":
        if "-rf" in cmd_parts and "/" in command and "--no-preserve-root" not in command:
            return get_rm_rf_root()
        else: return ""
    elif cmd == "dd": return get_dd_wipe()
    elif cmd == "history": return get_history()
    elif cmd in ["clear", "cls"]: return "\n\n"
    elif cmd == "man":
        if len(cmd_parts) > 1: return get_man_page(cmd_parts[1])
        else: return "What manual page do you want?"
    elif cmd == "echo":
        if "$PATH" in command: return get_echo_path()
        else: return " ".join(cmd_parts[1:])
    elif cmd == "help": return get_help()
    elif cmd == "exit": return "logout"
    
    # Default for unknown commands
    else:
        if cmd == "sl": return f"bash: {cmd}: command not found. Did you mean 'ls'?"
        elif cmd == "cd..": return f"bash: {cmd}: command not found. Did you mean 'cd ..'?"
        else: return f"bash: {cmd}: command not found"