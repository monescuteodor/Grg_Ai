Networking Protocols & Implementation Complete Reference
CHAPTER 1: GETTING STARTED WITH NETWORKING
Remarks
Networking protocols define rules for communication between computers. The OSI model has 7 layers, TCP/IP has 4 layers. Key protocols: TCP (reliable), UDP (fast), HTTP (web), DNS (name resolution), TLS (security). Modern protocols: HTTP/2, HTTP/3, QUIC, WebSocket.
Tools: Python (socket programming), Wireshark (packet analysis), netcat (testing), curl (HTTP), tcpdump (capture).
Hello Network
# hello_network.py
import socket

# Simple TCP server
def start_server(host='localhost', port=8080):
    """TCP server that echoes messages."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")
    
    while True:
        conn, addr = server.accept()
        print(f"Connection from {addr}")
        data = conn.recv(1024).decode()
        print(f"Received: {data}")
        conn.send(f"Echo: {data}".encode())
        conn.close()

# Simple TCP client
def start_client(host='localhost', port=8080, message="Hello"):
    """TCP client that sends a message."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(message.encode())
    response = client.recv(1024).decode()
    print(f"Response: {response}")
    client.close()

# Usage:
# import threading
# threading.Thread(target=start_server, daemon=True).start()
# time.sleep(1)
# start_client()

CHAPTER 2: OSI MODEL AND TCP/IP STACK
OSI 7-Layer Model
# Layer 7: Application (HTTP, FTP, SMTP, DNS)
# Layer 6: Presentation (SSL/TLS, encoding)
# Layer 5: Session (session management)
# Layer 4: Transport (TCP, UDP)
# Layer 3: Network (IP, ICMP, routing)
# Layer 2: Data Link (Ethernet, WiFi, MAC addresses)
# Layer 1: Physical (cables, signals)

# TCP/IP 4-Layer Model (simplified):
# Application Layer (combines OSI 5-7)
# Transport Layer (TCP, UDP)
# Internet Layer (IP)
# Network Access Layer (combines OSI 1-2)

class NetworkPacket:
    """Represents a network packet with headers."""
    
    def __init__(self, data):
        self.data = data
        self.headers = {}
    
    def add_header(self, layer, header):
        """Add header for specific layer."""
        self.headers[layer] = header
    
    def encapsulate(self):
        """Encapsulate data with all headers."""
        packet = self.data
        for layer in sorted(self.headers.keys(), reverse=True):
            packet = self.headers[layer] + packet
        return packet

# Example: HTTP request encapsulation
http_request = b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"
tcp_header = b"[TCP: src=12345 dst=80 seq=1 ack=0]"
ip_header = b"[IP: src=192.168.1.100 dst=93.184.216.34]"
eth_header = b"[ETH: src=AA:BB:CC:DD:EE:FF dst=11:22:33:44:55:66]"

packet = NetworkPacket(http_request)
packet.add_header(7, http_request)
packet.add_header(4, tcp_header)
packet.add_header(3, ip_header)
packet.add_header(2, eth_header)

full_packet = packet.encapsulate()
print("Full packet:", full_packet[:100])

Port Numbers
# Well-known ports (0-1023):
# 20-21: FTP
# 22: SSH
# 23: Telnet
# 25: SMTP
# 53: DNS
# 80: HTTP
# 110: POP3
# 143: IMAP
# 443: HTTPS
# 3306: MySQL
# 5432: PostgreSQL

# Registered ports (1024-49151):
# 8080: HTTP alternate
# 8443: HTTPS alternate

# Dynamic/private ports (49152-65535):
# Used for ephemeral client connections

import socket

def scan_port(host, port, timeout=1):
    """Check if a port is open."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

# Example: Scan common ports
host = "localhost"
common_ports = [22, 80, 443, 8080, 3306]
for port in common_ports:
    if scan_port(host, port):
        print(f"Port {port}: OPEN")
    else:
        print(f"Port {port}: CLOSED")

CHAPTER 3: TCP (TRANSMISSION CONTROL PROTOCOL)
TCP Three-Way Handshake
# TCP establishes connection with 3-way handshake:
# 1. Client → Server: SYN (synchronize)
# 2. Server → Client: SYN-ACK (synchronize-acknowledge)
# 3. Client → Server: ACK (acknowledge)

import socket
import struct

class TCPHeader:
    """TCP header structure (20 bytes minimum)."""
    
    def __init__(self, src_port, dst_port, seq_num, ack_num, flags):
        self.src_port = src_port
        self.dst_port = dst_port
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.data_offset = 5  # 5 * 4 = 20 bytes (no options)
        self.flags = flags  # SYN, ACK, FIN, RST, PSH, URG
        self.window = 65535
        self.checksum = 0
        self.urgent_ptr = 0
    
    def to_bytes(self):
        """Pack TCP header into bytes."""
        # Flags: URG ACK PSH RST SYN FIN
        flag_bits = 0
        if 'FIN' in self.flags: flag_bits |= 0x01
        if 'SYN' in self.flags: flag_bits |= 0x02
        if 'RST' in self.flags: flag_bits |= 0x04
        if 'PSH' in self.flags: flag_bits |= 0x08
        if 'ACK' in self.flags: flag_bits |= 0x10
        if 'URG' in self.flags: flag_bits |= 0x20
        
        # Pack header (simplified, no checksum calculation)
        header = struct.pack(
            '!HHIIBBHHH',
            self.src_port,
            self.dst_port,
            self.seq_num,
            self.ack_num,
            (self.data_offset << 4),
            flag_bits,
            self.window,
            self.checksum,
            self.urgent_ptr
        )
        return header
    
    def __repr__(self):
        return f"TCP(src={self.src_port}, dst={self.dst_port}, seq={self.seq_num}, ack={self.ack_num}, flags={self.flags})"

# Simulate TCP handshake
def tcp_handshake_simulation():
    """Simulate TCP 3-way handshake."""
    print("=== TCP 3-Way Handshake ===")
    
    # Step 1: Client sends SYN
    client_seq = 1000
    syn = TCPHeader(src_port=12345, dst_port=80, seq_num=client_seq, ack_num=0, flags=['SYN'])
    print(f"1. Client → Server: {syn}")
    
    # Step 2: Server responds with SYN-ACK
    server_seq = 5000
    syn_ack = TCPHeader(src_port=80, dst_port=12345, seq_num=server_seq, ack_num=client_seq + 1, flags=['SYN', 'ACK'])
    print(f"2. Server → Client: {syn_ack}")
    
    # Step 3: Client sends ACK
    ack = TCPHeader(src_port=12345, dst_port=80, seq_num=client_seq + 1, ack_num=server_seq + 1, flags=['ACK'])
    print(f"3. Client → Server: {ack}")
    
    print("Connection established!")

tcp_handshake_simulation()

TCP Congestion Control
# TCP uses congestion control to avoid network overload.
# Algorithms: Slow Start, Congestion Avoidance, Fast Retransmit, Fast Recovery

class TCPCongestionControl:
    """TCP congestion control simulation."""
    
    def __init__(self, mss=1460):
        self.mss = mss  # Maximum Segment Size
        self.cwnd = 1 * mss  # Congestion window (starts at 1 MSS)
        self.ssthresh = 65535  # Slow start threshold
        self.rtt = 100  # Round-trip time (ms)
        self.dup_acks = 0
    
    def slow_start(self):
        """Exponential growth phase."""
        if self.cwnd < self.ssthresh:
            self.cwnd *= 2  # Double window each RTT
            print(f"Slow Start: cwnd = {self.cwnd} bytes")
    
    def congestion_avoidance(self):
        """Linear growth phase."""
        if self.cwnd >= self.ssthresh:
            self.cwnd += self.mss  # Add 1 MSS per RTT
            print(f"Congestion Avoidance: cwnd = {self.cwnd} bytes")
    
    def on_ack_received(self):
        """Handle ACK receipt."""
        if self.cwnd < self.ssthresh:
            self.slow_start()
        else:
            self.congestion_avoidance()
    
    def on_timeout(self):
        """Handle timeout (packet loss detected)."""
        self.ssthresh = max(self.cwnd // 2, 2 * self.mss)
        self.cwnd = 1 * self.mss  # Reset to 1 MSS
        print(f"Timeout! ssthresh = {self.ssthresh}, cwnd = {self.cwnd}")
    
    def on_triple_dup_ack(self):
        """Handle 3 duplicate ACKs (fast retransmit)."""
        self.ssthresh = max(self.cwnd // 2, 2 * self.mss)
        self.cwnd = self.ssthresh + 3 * self.mss  # Fast recovery
        print(f"Triple DUP ACK! ssthresh = {self.ssthresh}, cwnd = {self.cwnd}")

# Example
cc = TCPCongestionControl()
print("\n=== TCP Congestion Control ===")
for i in range(5):
    cc.on_ack_received()

cc.on_timeout()
for i in range(3):
    cc.on_ack_received()

cc.on_triple_dup_ack()

TCP Flow Control
# Flow control prevents sender from overwhelming receiver.
# Uses sliding window mechanism with receiver's advertised window.

class TCPFlowControl:
    """TCP flow control with sliding window."""
    
    def __init__(self, buffer_size=65535):
        self.buffer_size = buffer_size
        self.send_base = 0  # Oldest unacknowledged byte
        self.next_seq_num = 0  # Next byte to send
        self.receiver_window = buffer_size  # Receiver's available buffer
    
    def can_send(self, data_size):
        """Check if we can send data."""
        # Effective window = min(our window, receiver's window)
        effective_window = self.receiver_window - (self.next_seq_num - self.send_base)
        return data_size <= effective_window
    
    def send_data(self, data_size):
        """Send data if possible."""
        if self.can_send(data_size):
            self.next_seq_num += data_size
            print(f"Sent {data_size} bytes, next_seq = {self.next_seq_num}")
            return True
        else:
            print(f"Cannot send {data_size} bytes (window full)")
            return False
    
    def receive_ack(self, ack_num, receiver_window):
        """Handle ACK from receiver."""
        self.send_base = ack_num
        self.receiver_window = receiver_window
        print(f"ACK received: {ack_num}, receiver window: {receiver_window}")

# Example
fc = TCPFlowControl(buffer_size=10000)
print("\n=== TCP Flow Control ===")
fc.send_data(3000)
fc.send_data(3000)
fc.send_data(3000)  # Should fail (window full)
fc.receive_ack(6000, 8000)  # Receiver acknowledges, opens window
fc.send_data(3000)  # Now should succeed

CHAPTER 4: UDP (USER DATAGRAM PROTOCOL)
UDP Basics
# UDP: Connectionless, unreliable, fast protocol.
# No handshake, no congestion control, no guaranteed delivery.
# Used for: DNS, video streaming, online games, VoIP.

import socket

def udp_server(host='localhost', port=8080):
    """Simple UDP server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"UDP server listening on {host}:{port}")
    
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received {data.decode()} from {addr}")
        sock.sendto(f"Echo: {data.decode()}".encode(), addr)

def udp_client(host='localhost', port=8080, message="Hello UDP"):
    """Simple UDP client."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (host, port))
    data, addr = sock.recvfrom(1024)
    print(f"Response: {data.decode()}")
    sock.close()

# Usage:
# import threading
# threading.Thread(target=udp_server, daemon=True).start()
# time.sleep(1)
# udp_client()

UDP Header
# UDP header is only 8 bytes:
# - Source Port (16 bits)
# - Destination Port (16 bits)
# - Length (16 bits)
# - Checksum (16 bits)

import struct

class UDPHeader:
    """UDP header structure (8 bytes)."""
    
    def __init__(self, src_port, dst_port, length, checksum=0):
        self.src_port = src_port
        self.dst_port = dst_port
        self.length = length
        self.checksum = checksum
    
    def to_bytes(self):
        """Pack UDP header into bytes."""
        return struct.pack(
            '!HHHH',
            self.src_port,
            self.dst_port,
            self.length,
            self.checksum
        )
    
    def __repr__(self):
        return f"UDP(src={self.src_port}, dst={self.dst_port}, len={self.length})"

# Example
udp_hdr = UDPHeader(src_port=12345, dst_port=80, length=100)
print("UDP Header:", udp_hdr)
print("Bytes:", udp_hdr.to_bytes().hex())

Reliable UDP (RUDP)
# RUDP: Adds reliability to UDP (acknowledgments, retransmissions).
# Used in some gaming protocols.

class ReliableUDP:
    """Simple reliable UDP implementation."""
    
    def __init__(self):
        self.seq_num = 0
        self.ack_num = 0
        self.sent_packets = {}
        self.timeout = 1.0  # seconds
    
    def send(self, data):
        """Send packet with sequence number."""
        packet = {
            'seq': self.seq_num,
            'data': data,
            'time': time.time()
        }
        self.sent_packets[self.seq_num] = packet
        self.seq_num += 1
        print(f"Sent packet seq={packet['seq']}")
        return packet
    
    def receive_ack(self, ack_num):
        """Handle ACK."""
        if ack_num in self.sent_packets:
            del self.sent_packets[ack_num]
            print(f"ACK received for seq={ack_num}")
    
    def check_timeout(self):
        """Check for timed-out packets."""
        current_time = time.time()
        for seq, packet in list(self.sent_packets.items()):
            if current_time - packet['time'] > self.timeout:
                print(f"Timeout! Retransmitting seq={seq}")
                # Retransmit
                packet['time'] = current_time

import time

# Example
rudp = ReliableUDP()
print("\n=== Reliable UDP ===")
rudp.send("Packet 1")
rudp.send("Packet 2")
rudp.receive_ack(0)  # ACK for first packet
time.sleep(1.5)
rudp.check_timeout()  # Should retransmit packet 2

CHAPTER 5: HTTP PROTOCOLS
HTTP/1.1
# HTTP/1.1: Text-based, request-response protocol.
# Methods: GET, POST, PUT, DELETE, HEAD, OPTIONS, PATCH
# Status codes: 200 OK, 404 Not Found, 500 Internal Server Error

import socket

def parse_http_request(request):
    """Parse HTTP request."""
    lines = request.split('\r\n')
    request_line = lines[0].split()
    
    method = request_line[0]
    path = request_line[1]
    version = request_line[2]
    
    headers = {}
    for line in lines[1:]:
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()
    
    return {
        'method': method,
        'path': path,
        'version': version,
        'headers': headers
    }

def create_http_response(status_code=200, body="Hello", content_type="text/plain"):
    """Create HTTP response."""
    status_messages = {
        200: "OK",
        404: "Not Found",
        500: "Internal Server Error"
    }
    
    status_text = status_messages.get(status_code, "Unknown")
    
    response = f"HTTP/1.1 {status_code} {status_text}\r\n"
    response += f"Content-Type: {content_type}\r\n"
    response += f"Content-Length: {len(body)}\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"
    response += body
    
    return response

# Example
request = "GET /index.html HTTP/1.1\r\nHost: example.com\r\nUser-Agent: curl\r\n\r\n"
parsed = parse_http_request(request)
print("\n=== HTTP/1.1 Request ===")
print(f"Method: {parsed['method']}")
print(f"Path: {parsed['path']}")
print(f"Headers: {parsed['headers']}")

response = create_http_response(200, "<h1>Hello World</h1>", "text/html")
print("\n=== HTTP/1.1 Response ===")
print(response[:100])

HTTP/2
# HTTP/2: Binary protocol, multiplexing, header compression.
# Features:
# - Binary framing (not text)
# - Multiplexing (multiple requests over single connection)
# - Header compression (HPACK)
# - Server push
# - Stream prioritization

class HTTP2Frame:
    """HTTP/2 frame structure."""
    
    def __init__(self, frame_type, stream_id, flags=0, payload=b''):
        self.length = len(payload)
        self.frame_type = frame_type
        self.flags = flags
        self.stream_id = stream_id
        self.payload = payload
    
    def to_bytes(self):
        """Pack frame into bytes (9-byte header + payload)."""
        header = struct.pack(
            '!I', self.length
        )[1:]  # 3 bytes for length
        header += struct.pack('!B', self.frame_type)
        header += struct.pack('!B', self.flags)
        header += struct.pack('>I', self.stream_id & 0x7FFFFFFF)  # 31 bits
        
        return header + self.payload
    
    def __repr__(self):
        types = {0: 'DATA', 1: 'HEADERS', 2: 'PRIORITY', 3: 'RST_STREAM',
                 4: 'SETTINGS', 5: 'PUSH_PROMISE', 6: 'PING', 7: 'GOAWAY',
                 8: 'WINDOW_UPDATE', 9: 'CONTINUATION'}
        type_name = types.get(self.frame_type, f'UNKNOWN({self.frame_type})')
        return f"HTTP2Frame({type_name}, stream={self.stream_id}, len={self.length})"

# Example
print("\n=== HTTP/2 Frames ===")
data_frame = HTTP2Frame(frame_type=0, stream_id=1, payload=b"Hello")
headers_frame = HTTP2Frame(frame_type=1, stream_id=1, payload=b"[compressed headers]")
settings_frame = HTTP2Frame(frame_type=4, stream_id=0, payload=b"[settings]")

print(data_frame)
print(headers_frame)
print(settings_frame)

HTTP/3 and QUIC
# HTTP/3: Uses QUIC (UDP-based) instead of TCP.
# Benefits:
# - 0-RTT connection establishment
# - No head-of-line blocking
# - Built-in encryption (TLS 1.3)
# - Connection migration

class QUICPacket:
    """QUIC packet structure (simplified)."""
    
    def __init__(self, packet_type, connection_id, packet_number, payload):
        self.packet_type = packet_type  # Initial, Handshake, 0-RTT, 1-RTT
        self.connection_id = connection_id
        self.packet_number = packet_number
        self.payload = payload
    
    def __repr__(self):
        return f"QUICPacket(type={self.packet_type}, conn_id={self.connection_id}, pkt_num={self.packet_number})"

class QUICConnection:
    """QUIC connection simulation."""
    
    def __init__(self, connection_id):
        self.connection_id = connection_id
        self.packet_number = 0
        self.streams = {}
    
    def send_packet(self, stream_id, data):
        """Send data over QUIC."""
        packet = QUICPacket(
            packet_type='1-RTT',
            connection_id=self.connection_id,
            packet_number=self.packet_number,
            payload=data
        )
        self.packet_number += 1
        print(f"Sent: {packet}")
        return packet
    
    def create_stream(self, stream_id):
        """Create a new stream."""
        self.streams[stream_id] = []
        print(f"Created stream {stream_id}")

# Example
print("\n=== HTTP/3 & QUIC ===")
quic = QUICConnection(connection_id='abc123')
quic.create_stream(1)
quic.create_stream(3)
quic.send_packet(1, b"Request 1")
quic.send_packet(3, b"Request 2")  # Can send on different streams without blocking

CHAPTER 6: DNS (DOMAIN NAME SYSTEM)
DNS Resolution
# DNS translates domain names to IP addresses.
# Query types: A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail), NS (nameserver)

import socket

def dns_lookup(domain, record_type='A'):
    """Perform DNS lookup."""
    try:
        if record_type == 'A':
            # Get IPv4 address
            result = socket.getaddrinfo(domain, None, socket.AF_INET)
            ips = list(set([addr[4][0] for addr in result]))
            return ips
        elif record_type == 'AAAA':
            # Get IPv6 address
            result = socket.getaddrinfo(domain, None, socket.AF_INET6)
            ips = list(set([addr[4][0] for addr in result]))
            return ips
        else:
            return ["Record type not supported in this example"]
    except socket.gaierror:
        return ["Domain not found"]

# Example
print("\n=== DNS Lookup ===")
domain = "example.com"
ipv4 = dns_lookup(domain, 'A')
print(f"{domain} A records: {ipv4}")

DNS Message Format
# DNS message structure:
# - Header (12 bytes): ID, flags, question count, answer count, etc.
# - Question: Domain name, query type, query class
# - Answer: Resource records
# - Authority: Name server records
# - Additional: Additional records

import struct

class DNSHeader:
    """DNS header (12 bytes)."""
    
    def __init__(self, id, flags, qdcount, ancount, nscount, arcount):
        self.id = id
        self.flags = flags
        self.qdcount = qdcount  # Question count
        self.ancount = ancount  # Answer count
        self.nscount = nscount  # Authority count
        self.arcount = arcount  # Additional count
    
    def to_bytes(self):
        """Pack DNS header."""
        return struct.pack(
            '!HHHHHH',
            self.id,
            self.flags,
            self.qdcount,
            self.ancount,
            self.nscount,
            self.arcount
        )
    
    def __repr__(self):
        return f"DNSHeader(id={self.id}, flags=0x{self.flags:04x}, questions={self.qdcount}, answers={self.ancount})"

def encode_dns_name(domain):
    """Encode domain name for DNS query."""
    labels = domain.split('.')
    encoded = b''
    for label in labels:
        encoded += bytes([len(label)]) + label.encode()
    encoded += b'\x00'  # Null terminator
    return encoded

# Example
print("\n=== DNS Message ===")
header = DNSHeader(id=0x1234, flags=0x0100, qdcount=1, ancount=0, nscount=0, arcount=0)
print(header)
print("Header bytes:", header.to_bytes().hex())

domain = "www.example.com"
encoded_name = encode_dns_name(domain)
print(f"Encoded '{domain}':", encoded_name.hex())

DNS over HTTPS (DoH)
# DoH: DNS queries over HTTPS for privacy.
# Uses POST requests to DNS resolver.

import requests

def dns_over_https(domain, record_type='A'):
    """Query DNS over HTTPS (using Cloudflare)."""
    url = "https://cloudflare-dns.com/dns-query"
    headers = {
        'Accept': 'application/dns-json'
    }
    params = {
        'name': domain,
        'type': record_type
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        data = response.json()
        
        answers = []
        if 'Answer' in data:
            for answer in data['Answer']:
                answers.append({
                    'name': answer['name'],
                    'type': answer['type'],
                    'data': answer['data'],
                    'ttl': answer['TTL']
                })
        
        return answers
    except Exception as e:
        return [{'error': str(e)}]

# Example (requires internet)
# print("\n=== DNS over HTTPS ===")
# results = dns_over_https('example.com', 'A')
# for r in results:
#     print(r)

CHAPTER 7: TLS/SSL
TLS Handshake
# TLS 1.3 handshake (simplified):
# 1. Client → Server: ClientHello (supported versions, ciphers, key share)
# 2. Server → Client: ServerHello (selected cipher, key share)
# 3. Server → Client: EncryptedExtensions, Certificate, CertificateVerify, Finished
# 4. Client → Server: Finished
# 5. Application data exchange

class TLSMessage:
    """TLS message types."""
    
    CLIENT_HELLO = 1
    SERVER_HELLO = 2
    CERTIFICATE = 11
    SERVER_KEY_EXCHANGE = 12
    SERVER_HELLO_DONE = 14
    CLIENT_KEY_EXCHANGE = 16
    FINISHED = 20

class TLSHandshake:
    """Simulate TLS 1.3 handshake."""
    
    def __init__(self):
        self.client_random = b'client_random_32_bytes'
        self.server_random = b'server_random_32_bytes'
        self.session_id = b'session_id'
    
    def client_hello(self):
        """Client sends ClientHello."""
        print("1. Client → Server: ClientHello")
        print(f"   - Supported versions: TLS 1.3")
        print(f"   - Cipher suites: TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256")
        print(f"   - Client random: {self.client_random[:10]}...")
        print(f"   - Key share: x25519 public key")
    
    def server_hello(self):
        """Server responds with ServerHello."""
        print("\n2. Server → Client: ServerHello")
        print(f"   - Selected cipher: TLS_AES_256_GCM_SHA384")
        print(f"   - Server random: {self.server_random[:10]}...")
        print(f"   - Key share: x25519 public key")
    
    def server_certificate(self):
        """Server sends certificate."""
        print("\n3. Server → Client: Certificate")
        print(f"   - Subject: CN=example.com")
        print(f"   - Issuer: CN=Let's Encrypt Authority X3")
        print(f"   - Valid: 2024-01-01 to 2024-12-31")
    
    def finished(self):
        """Handshake complete."""
        print("\n4. Handshake complete!")
        print("   - Session key established")
        print("   - Ready for application data")

# Example
print("\n=== TLS 1.3 Handshake ===")
tls = TLSHandshake()
tls.client_hello()
tls.server_hello()
tls.server_certificate()
tls.finished()

HTTPS with Python
# HTTPS client using Python's ssl module

import ssl
import urllib.request

def https_request(url):
    """Make HTTPS request."""
    # Create SSL context
    context = ssl.create_default_context()
    
    # Make request
    try:
        with urllib.request.urlopen(url, context=context, timeout=10) as response:
            data = response.read()
            return {
                'status': response.status,
                'headers': dict(response.headers),
                'body': data.decode('utf-8', errors='ignore')[:500]
            }
    except Exception as e:
        return {'error': str(e)}

# Example (requires internet)
# print("\n=== HTTPS Request ===")
# result = https_request('https://example.com')
# print(f"Status: {result.get('status')}")
# print(f"Body preview: {result.get('body', '')[:100]}")

CHAPTER 8: WEBSOCKET
WebSocket Protocol
# WebSocket: Full-duplex communication over single TCP connection.
# Starts with HTTP upgrade, then switches to WebSocket protocol.
# Used for: real-time apps, chat, gaming, live updates.

import socket
import hashlib
import base64

def websocket_handshake_key(key):
    """Generate WebSocket accept key."""
    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    accept = hashlib.sha1((key + GUID).encode()).digest()
    return base64.b64encode(accept).decode()

class WebSocketFrame:
    """WebSocket frame structure."""
    
    def __init__(self, opcode, payload, masked=False, mask_key=None):
        self.fin = 1  # Final fragment
        self.opcode = opcode  # 0x1=text, 0x2=binary, 0x8=close, 0x9=ping, 0xA=pong
        self.payload = payload
        self.masked = masked
        self.mask_key = mask_key
    
    def to_bytes(self):
        """Pack WebSocket frame."""
        # First byte: FIN + opcode
        first_byte = (self.fin << 7) | self.opcode
        
        # Second byte: MASK + payload length
        length = len(self.payload)
        if length < 126:
            second_byte = length
            length_bytes = b''
        elif length < 65536:
            second_byte = 126
            length_bytes = struct.pack('>H', length)
        else:
            second_byte = 127
            length_bytes = struct.pack('>Q', length)
        
        if self.masked:
            second_byte |= 0x80
        
        frame = bytes([first_byte, second_byte]) + length_bytes
        
        if self.masked and self.mask_key:
            frame += self.mask_key
            # Mask payload
            masked_payload = bytes([
                self.payload[i] ^ self.mask_key[i % 4]
                for i in range(len(self.payload))
            ])
            frame += masked_payload
        else:
            frame += self.payload
        
        return frame
    
    def __repr__(self):
        opcodes = {0x1: 'TEXT', 0x2: 'BINARY', 0x8: 'CLOSE', 0x9: 'PING', 0xA: 'PONG'}
        return f"WebSocketFrame(opcode={opcodes.get(self.opcode, self.opcode)}, len={len(self.payload)})"

# Example
print("\n=== WebSocket ===")
frame = WebSocketFrame(opcode=0x1, payload=b"Hello, WebSocket!")
print(frame)
print("Frame bytes:", frame.to_bytes()[:20].hex(), "...")

# WebSocket handshake example
client_key = "dGhlIHNhbXBsZSBub25jZQ=="
accept_key = websocket_handshake_key(client_key)
print(f"\nClient key: {client_key}")
print(f"Server accept key: {accept_key}")

WebSocket Server
import asyncio
import websockets

async def websocket_server(websocket, path):
    """Simple WebSocket server."""
    print(f"Client connected from {websocket.remote_address}")
    
    try:
        async for message in websocket:
            print(f"Received: {message}")
            await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

# Usage:
# async def start_ws_server():
#     async with websockets.serve(websocket_server, "localhost", 8765):
#         await asyncio.Future()  # run forever
# 
# asyncio.run(start_ws_server())

CHAPTER 9: SOCKET PROGRAMMING ADVANCED
Non-blocking I/O
# Non-blocking sockets allow handling multiple connections without threads.

import socket
import select

def non_blocking_server(host='localhost', port=8080):
    """Non-blocking TCP server using select."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    server.setblocking(False)
    
    # Track connections
    inputs = [server]
    outputs = []
    message_queues = {}
    
    print(f"Non-blocking server on {host}:{port}")
    
    while inputs:
        # Wait for ready sockets
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        
        # Handle readable sockets
        for s in readable:
            if s is server:
                # New connection
                connection, client_address = s.accept()
                connection.setblocking(False)
                inputs.append(connection)
                message_queues[connection] = []
                print(f"Connection from {client_address}")
            else:
                # Data from client
                data = s.recv(1024)
                if data:
                    print(f"Received: {data.decode()}")
                    message_queues[s].append(f"Echo: {data.decode()}")
                    if s not in outputs:
                        outputs.append(s)
                else:
                    # Client disconnected
                    inputs.remove(s)
                    if s in outputs:
                        outputs.remove(s)
                    del message_queues[s]
                    s.close()
        
        # Handle writable sockets
        for s in writable:
            if message_queues[s]:
                msg = message_queues[s].pop(0)
                s.send(msg.encode())
            else:
                outputs.remove(s)
        
        # Handle exceptions
        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]

Asyncio Server
# Modern async I/O using asyncio

import asyncio

async def async_echo_server(host='localhost', port=8080):
    """Async TCP server using asyncio."""
    
    async def handle_client(reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Client connected: {addr}")
        
        while True:
            data = await reader.read(1024)
            if not data:
                break
            
            message = data.decode()
            print(f"Received: {message}")
            
            response = f"Echo: {message}"
            writer.write(response.encode())
            await writer.drain()
        
        print(f"Client disconnected: {addr}")
        writer.close()
    
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    print(f"Async server on {addr}")
    
    async with server:
        await server.serve_forever()

# Usage:
# asyncio.run(async_echo_server())

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Network Performance Metrics
# Bandwidth: Maximum data transfer rate (bits/second)
# Latency: Time for packet to travel (milliseconds)
# Throughput: Actual data transfer rate
# Packet loss: Percentage of packets lost
# Jitter: Variation in latency

# Example: Measure latency
import time

def measure_latency(host, port=80, count=5):
    """Measure network latency."""
    latencies = []
    
    for _ in range(count):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        start = time.time()
        try:
            sock.connect((host, port))
            end = time.time()
            latency = (end - start) * 1000  # ms
            latencies.append(latency)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sock.close()
    
    if latencies:
        avg = sum(latencies) / len(latencies)
        min_lat = min(latencies)
        max_lat = max(latencies)
        print(f"\nLatency to {host}:")
        print(f"  Average: {avg:.2f} ms")
        print(f"  Min: {min_lat:.2f} ms")
        print(f"  Max: {max_lat:.2f} ms")
    
    return latencies

# Example
# measure_latency('google.com')

Network Security
# Firewall: Filters traffic based on rules
# NAT (Network Address Translation): Maps private IPs to public IP
# VPN (Virtual Private Network): Encrypted tunnel
# IDS/IPS (Intrusion Detection/Prevention): Detects attacks

# Example: Simple packet filter (conceptual)
class SimpleFirewall:
    """Simple firewall rule engine."""
    
    def __init__(self):
        self.rules = []
    
    def add_rule(self, action, protocol, src_ip, dst_ip, src_port, dst_port):
        """Add firewall rule."""
        rule = {
            'action': action,  # 'ALLOW' or 'DENY'
            'protocol': protocol,
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'src_port': src_port,
            'dst_port': dst_port
        }
        self.rules.append(rule)
    
    def check_packet(self, protocol, src_ip, dst_ip, src_port, dst_port):
        """Check if packet should be allowed."""
        for rule in self.rules:
            if (rule['protocol'] == protocol or rule['protocol'] == 'ANY') and \
               (rule['src_ip'] == src_ip or rule['src_ip'] == 'ANY') and \
               (rule['dst_ip'] == dst_ip or rule['dst_ip'] == 'ANY') and \
               (rule['src_port'] == src_port or rule['src_port'] == 'ANY') and \
               (rule['dst_port'] == dst_port or rule['dst_port'] == 'ANY'):
                return rule['action']
        
        return 'DENY'  # Default deny

# Example
fw = SimpleFirewall()
fw.add_rule('ALLOW', 'TCP', 'ANY', '192.168.1.100', 'ANY', 80)
fw.add_rule('ALLOW', 'TCP', 'ANY', '192.168.1.100', 'ANY', 443)
fw.add_rule('DENY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY')

print("\n=== Firewall ===")
print("Allow HTTP:", fw.check_packet('TCP', '10.0.0.1', '192.168.1.100', 12345, 80))
print("Allow HTTPS:", fw.check_packet('TCP', '10.0.0.1', '192.168.1.100', 12345, 443))
print("Allow SSH:", fw.check_packet('TCP', '10.0.0.1', '192.168.1.100', 12345, 22))

Recommended Reading
# - "Computer Networking: A Top-Down Approach" by Kurose & Ross
# - "TCP/IP Illustrated" by Stevens
# - "High Performance Browser Networking" by Ilya Grigorik (free online)
# - "Beej's Guide to Network Programming" (free online)
# - RFC documents: https://www.rfc-editor.org/

# Tools to Learn
# - Wireshark: Packet analyzer
# - tcpdump: Command-line packet capture
# - netcat: Networking Swiss army knife
# - curl: HTTP client
# - nmap: Network scanner
# - iperf3: Network performance testing

# End of Networking Protocols Reference