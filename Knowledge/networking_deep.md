# Networking Deep Dive Complete Reference


---

# CHAPTER 1: THE OSI AND TCP/IP MODELS


## Remarks

Networking is the foundation of every internet application. Understanding how data travels from browser to server and back — through DNS resolution, TCP handshakes, TLS negotiation, HTTP framing, and routing — makes you a dramatically better debugger and system designer. Most "mysterious" production bugs are networking bugs.

Key concepts: **OSI 7 layers** (physical → application), **TCP/IP 4 layers** (link → application), **TCP** (reliable, ordered, connection-oriented), **UDP** (fast, unreliable, connectionless), **DNS** (name → IP resolution), **TLS** (encryption in transit), **HTTP/1.1 vs HTTP/2 vs HTTP/3** (protocol evolution), **WebSockets** (full-duplex), **NAT** (IP address translation), **Routing** (how packets find their way).

Tools: **curl** (HTTP client), **dig/nslookup** (DNS), **tcpdump** (packet capture), **Wireshark** (packet analysis GUI), **netstat/ss** (connection listing), **traceroute** (path discovery), **mtr** (continuous traceroute), **nmap** (port scanning), **openssl s_client** (TLS debugging).


## OSI Model vs TCP/IP

```
OSI MODEL (7 layers):          TCP/IP MODEL (4 layers):

7. Application  (HTTP, DNS)     ┐
6. Presentation (TLS, JSON)     ├── Application
5. Session      (sessions)      ┘
4. Transport    (TCP, UDP)      ─── Transport
3. Network      (IP, ICMP)      ─── Internet
2. Data Link    (Ethernet, WiFi)┐
1. Physical     (cables, radio) ┘── Network Access

DATA ENCAPSULATION (sending):
  Application: "Hello"
  Transport:   TCP header + "Hello"             → Segment
  Network:     IP header + TCP header + "Hello"  → Packet
  Data Link:   Eth header + IP + TCP + "Hello" + Eth trailer → Frame
  Physical:    Bits on wire / radio waves

Each layer adds its header. Receiver strips them in reverse.

WHAT DEVELOPERS CARE ABOUT:
  Layer 7 (Application): HTTP, gRPC, WebSocket, DNS
  Layer 4 (Transport):   TCP vs UDP, ports, connections
  Layer 3 (Network):     IP addresses, routing, subnets
  Layers 1-2:            Usually handled by OS/hardware
```


---

# CHAPTER 2: TCP (TRANSMISSION CONTROL PROTOCOL)


## TCP Fundamentals

```
TCP PROVIDES:
  ✅ Reliable delivery (retransmits lost packets)
  ✅ Ordered delivery (reassembles out-of-order packets)
  ✅ Flow control (sender doesn't overwhelm receiver)
  ✅ Congestion control (doesn't overwhelm network)
  ✅ Connection-oriented (handshake before data)
  ❌ NOT fast for real-time (overhead from reliability)

USED BY: HTTP, HTTPS, SSH, FTP, SMTP, databases, most apps

TCP HEADER (20 bytes minimum):
  Source Port (16 bit)
  Destination Port (16 bit)
  Sequence Number (32 bit)        ← byte position in stream
  Acknowledgment Number (32 bit)  ← next byte expected from other side
  Flags: SYN, ACK, FIN, RST, PSH, URG
  Window Size (16 bit)            ← flow control
  Checksum (16 bit)               ← integrity
```


## Three-Way Handshake

```
CLIENT                          SERVER

  SYN (seq=100)        →
                        ←      SYN-ACK (seq=300, ack=101)
  ACK (seq=101, ack=301) →

Connection established! (1.5 round trips)

WHY THREE STEPS:
  1. Client → Server: "I want to connect" (SYN)
  2. Server → Client: "OK, I heard you" (SYN-ACK)
  3. Client → Server: "I heard your OK" (ACK)
  Both sides confirm they can send AND receive.

COST: 1 RTT (round-trip time) before ANY data.
  Same datacenter:   ~0.5ms
  Same continent:    ~30-50ms
  Cross-ocean:       ~100-200ms
  This is why connection reuse (keep-alive) matters!
```


## Connection Termination

```
CLIENT                          SERVER

  FIN (seq=500)        →
                        ←      ACK (ack=501)
                        ←      FIN (seq=700)
  ACK (seq=501, ack=701) →

Four-way teardown (graceful close).
Either side can initiate FIN.

TIME_WAIT state:
  After sending final ACK, client waits 2×MSL (60-120 seconds).
  Prevents delayed packets from old connection confusing new one.
  
  PROBLEM: high-traffic servers → thousands of TIME_WAIT sockets.
  FIX: SO_REUSEADDR socket option, connection pooling.
```


## Flow Control and Congestion Control

```
FLOW CONTROL (don't overwhelm RECEIVER):
  Receiver advertises "window size" = how much data it can buffer.
  Sender never sends more than window allows.
  If receiver busy → shrinks window → sender slows down.
  If receiver catches up → grows window → sender speeds up.

CONGESTION CONTROL (don't overwhelm NETWORK):
  Sender maintains "congestion window" (cwnd).
  
  Slow Start:
    cwnd starts at 1 segment (~1.5 KB)
    Doubles every RTT (exponential growth)
    1 → 2 → 4 → 8 → 16 → ...
    Until: packet loss OR threshold reached
  
  Congestion Avoidance:
    After threshold: cwnd grows by 1 per RTT (linear)
    16 → 17 → 18 → 19 → ...
  
  On packet loss:
    cwnd drops dramatically (halved or back to 1)
    Start again

  IMPACT ON DEVELOPERS:
    New TCP connection starts SLOW (small cwnd).
    Takes several RTTs to reach full speed.
    This is why HTTP keep-alive and connection pooling matter.
    HTTP/2 multiplexing: one connection, full speed for all requests.

ALGORITHMS:
  Reno:     classic, halves cwnd on loss
  CUBIC:    Linux default, better for high-bandwidth
  BBR:      Google's algorithm, measures bandwidth instead of reacting to loss
```


## TCP vs UDP

```
TCP:                              UDP:
  ✅ Reliable                      ❌ Unreliable (best-effort)
  ✅ Ordered                       ❌ No ordering
  ✅ Flow/congestion control       ❌ No flow control
  ✅ Connection-oriented           ✅ Connectionless
  ❌ Higher latency (handshake)    ✅ Lower latency (no handshake)
  ❌ Head-of-line blocking         ✅ No HOL blocking
  ❌ Heavier (20-60 byte header)   ✅ Lighter (8 byte header)

UDP USE CASES:
  DNS queries (small, one-shot)
  Video streaming / VoIP (late data = useless)
  Gaming (need latest state, not old reliable state)
  IoT sensors (high volume, loss acceptable)
  QUIC / HTTP/3 (reliability built ON TOP of UDP)

UDP HEADER (8 bytes only):
  Source Port (16 bit)
  Destination Port (16 bit)
  Length (16 bit)
  Checksum (16 bit)
```


---

# CHAPTER 3: DNS (DOMAIN NAME SYSTEM)


## How DNS Works

```
USER TYPES: www.example.com

RESOLUTION (recursive):

  Browser cache → OS cache → Router cache → ISP DNS resolver
      ↓ (if not cached)
  Root DNS server (.)
    "Who handles .com?"     → returns .com NS servers
      ↓
  TLD DNS server (.com)
    "Who handles example.com?" → returns example.com NS servers
      ↓
  Authoritative DNS server (example.com)
    "What is www.example.com?" → returns 93.184.216.34
      ↓
  Response cached at each level (TTL = Time To Live)
  Browser connects to 93.184.216.34

RECORD TYPES:
  A:      domain → IPv4 address       example.com → 93.184.216.34
  AAAA:   domain → IPv6 address       example.com → 2606:2800:220:1:248:...
  CNAME:  alias → canonical name      www.example.com → example.com
  MX:     mail server                 example.com → mail.example.com (priority 10)
  TXT:    arbitrary text              SPF, DKIM, domain verification
  NS:     nameserver                  example.com → ns1.example.com
  SOA:    zone authority              Primary NS, admin email, serial
  SRV:    service location            _http._tcp.example.com → port 80

TTL (Time To Live):
  How long DNS resolvers can cache the record.
  Low TTL (60s):   fast propagation, more queries
  High TTL (86400): fewer queries, slow changes
  Common: 300-3600 seconds (5 min to 1 hour)
```


## DNS Tools

```bash
# dig — detailed DNS lookup
dig example.com                    # A record
dig example.com AAAA               # IPv6
dig example.com MX                 # Mail servers
dig example.com NS                 # Nameservers
dig +trace example.com             # Full resolution path
dig +short example.com             # Just the IP
dig @8.8.8.8 example.com           # Query specific DNS server

# nslookup — simpler lookup
nslookup example.com
nslookup -type=MX example.com

# host — simplest
host example.com
host -t CNAME www.example.com

# Check DNS propagation
dig +short example.com @8.8.8.8         # Google DNS
dig +short example.com @1.1.1.1         # Cloudflare DNS
dig +short example.com @208.67.222.222  # OpenDNS
```


---

# CHAPTER 4: HTTP PROTOCOL


## HTTP/1.1

```
REQUEST:
  GET /api/users HTTP/1.1
  Host: api.example.com
  Accept: application/json
  Authorization: Bearer eyJhbGci...
  User-Agent: Mozilla/5.0
  Connection: keep-alive

RESPONSE:
  HTTP/1.1 200 OK
  Content-Type: application/json
  Content-Length: 1234
  Cache-Control: max-age=300
  Set-Cookie: session=abc123; HttpOnly; Secure
  
  {"users": [...]}

KEY FEATURES:
  Keep-Alive:     Reuse TCP connection for multiple requests (default on)
  Pipelining:     Send multiple requests without waiting for responses
                  (poorly supported, rarely used)
  Chunked:        Stream response in chunks (Transfer-Encoding: chunked)
  
LIMITATIONS:
  Head-of-line blocking: one slow response blocks subsequent ones
  6 connections per domain: browser limit
  Text headers: verbose, repeated for every request
  No server push: client must request everything
```


## HTTP/2

```
IMPROVEMENTS OVER HTTP/1.1:

MULTIPLEXING:
  Multiple requests/responses on ONE TCP connection simultaneously.
  No head-of-line blocking at HTTP level.
  Request 1 slow? Request 2 and 3 still arrive.

HEADER COMPRESSION (HPACK):
  Headers compressed and deduplicated.
  First request: send full headers.
  Subsequent: send only differences (index references).
  Saves 85-90% of header bytes.

BINARY PROTOCOL:
  Frames instead of text. Faster to parse.
  Frame types: DATA, HEADERS, PRIORITY, RST_STREAM, SETTINGS, PUSH_PROMISE

STREAM PRIORITIZATION:
  Client can indicate which resources are more important.
  Browser: HTML > CSS > JS > images

SERVER PUSH:
  Server sends resources before client requests them.
  Client requests index.html → server pushes style.css and app.js.
  Being deprecated in practice (hard to get right, wastes bandwidth).

SINGLE CONNECTION:
  One TCP connection per origin (not 6 like HTTP/1.1).
  TCP slow start only happens once.
  But: TCP-level HOL blocking still exists (one lost packet blocks all streams).
```


## HTTP/3 (QUIC)

```
HTTP/3 = HTTP over QUIC (instead of TCP).
QUIC = UDP + reliability + encryption built-in.

WHY:
  TCP has head-of-line blocking at transport level.
  Lost packet in one stream blocks ALL streams (even unrelated).
  QUIC: each stream independent — loss in one doesn't affect others.

BENEFITS:
  ✅ No HOL blocking (independent streams)
  ✅ Faster connection setup (0-RTT possible!)
      TCP: 1 RTT handshake + 1 RTT TLS = 2 RTT before data
      QUIC: 1 RTT (handshake + TLS combined), 0-RTT for repeat visits
  ✅ Connection migration (switch WiFi → cellular without reconnecting)
  ✅ Better on lossy networks (mobile, WiFi)
  ✅ Always encrypted (TLS 1.3 built into QUIC)

ADOPTION:
  Google (YouTube, Search): HTTP/3 since 2020
  Cloudflare: HTTP/3 for all sites
  Meta, Apple: adopting
  ~30% of web traffic uses HTTP/3 (2025)

ENABLING:
  Cloudflare: automatic for proxied domains
  Nginx: requires quiche or ngtcp2 module
  Caddy: built-in support
```


---

# CHAPTER 5: TLS (TRANSPORT LAYER SECURITY)


## TLS Handshake

```
TLS 1.3 HANDSHAKE (1 RTT):

CLIENT                              SERVER

  ClientHello                →
    (supported ciphers,
     key share,
     SNI: hostname)
                              ←      ServerHello
                                       (chosen cipher,
                                        key share,
                                        certificate,
                                        certificate verify,
                                        finished)
  Finished                   →

  === Application Data ===          (encrypted from here)

TLS 1.2 was 2 RTT. TLS 1.3 reduced to 1 RTT.
0-RTT resumption: for repeat connections, send data with first message!
  (Risk: replay attacks. Only safe for idempotent requests.)

KEY EXCHANGE:
  ECDHE (Elliptic Curve Diffie-Hellman Ephemeral):
    Both sides generate temporary key pairs.
    Exchange public keys.
    Compute shared secret independently.
    Even if server's private key later leaked → past sessions safe
    (Perfect Forward Secrecy).

CIPHER SUITE EXAMPLE:
  TLS_AES_256_GCM_SHA384
  TLS = protocol
  AES_256_GCM = symmetric encryption (bulk data)
  SHA384 = hash for integrity

CERTIFICATE CHAIN:
  Server cert → signed by Intermediate CA → signed by Root CA
  Browser has list of trusted Root CAs (~150).
  Verifies entire chain.

  Let's Encrypt: free, automated, 90-day certs.
  ACME protocol: automated cert issuance and renewal.
```


## TLS Debugging

```bash
# Check certificate
openssl s_client -connect example.com:443 -servername example.com

# Show certificate details
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -text -noout

# Check certificate expiry
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -enddate -noout

# Test TLS version support
openssl s_client -connect example.com:443 -tls1_3

# curl with TLS details
curl -v https://example.com 2>&1 | grep -E 'SSL|TLS|subject|expire'

# Check supported ciphers
nmap --script ssl-enum-ciphers -p 443 example.com
```


---

# CHAPTER 6: NETWORK DEBUGGING TOOLS


## Essential Commands

```bash
# IP AND INTERFACE
ip addr show                         # Show IP addresses
ip route show                        # Routing table
ifconfig                             # Legacy (ip addr is modern)

# DNS RESOLUTION
dig example.com +short               # Quick DNS lookup
dig +trace example.com               # Full resolution chain
nslookup example.com                 # Simple lookup

# CONNECTIVITY
ping -c 5 example.com                # Basic reachability (ICMP)
traceroute example.com               # Path to destination (hops)
mtr example.com                      # Continuous traceroute (best!)

# PORTS AND CONNECTIONS
ss -tlnp                             # Listening TCP ports
ss -tanp                             # All TCP connections
ss -s                                # Connection statistics
netstat -tlnp                        # Legacy (ss is modern)
lsof -i :8000                        # What's using port 8000?

# HTTP DEBUGGING
curl -v https://example.com          # Verbose HTTP request
curl -I https://example.com          # Headers only (HEAD)
curl -w "\nDNS: %{time_namelookup}\nConnect: %{time_connect}\nTLS: %{time_appconnect}\nTTFB: %{time_starttransfer}\nTotal: %{time_total}\n" -o /dev/null -s https://example.com
# Shows timing breakdown: DNS, TCP connect, TLS, TTFB, total

# PACKET CAPTURE
sudo tcpdump -i eth0 port 443        # Capture HTTPS traffic
sudo tcpdump -i any host 10.0.0.5    # Traffic to/from specific host
sudo tcpdump -i eth0 -w capture.pcap # Save to file (open in Wireshark)

# PORT SCANNING
nmap -sT localhost                   # TCP port scan
nmap -sV -p 80,443 example.com      # Service version detection

# BANDWIDTH TESTING
iperf3 -s                            # Start server
iperf3 -c server-ip                  # Test bandwidth to server

# SSL/TLS
openssl s_client -connect host:443   # TLS debugging
curl --resolve host:443:IP https://host/  # Override DNS (testing)
```


## Common Network Issues

```
ISSUE: Connection refused
  Port not open or service not running.
  Check: ss -tlnp | grep PORT
  Check: systemctl status SERVICE

ISSUE: Connection timed out
  Firewall blocking, wrong IP, service too slow.
  Check: telnet HOST PORT (or nc -zv HOST PORT)
  Check: iptables -L -n (firewall rules)
  Check: security group (cloud)

ISSUE: DNS resolution failed
  DNS misconfigured, domain expired, propagation pending.
  Check: dig DOMAIN @8.8.8.8
  Check: cat /etc/resolv.conf

ISSUE: SSL certificate error
  Expired cert, wrong hostname, self-signed, incomplete chain.
  Check: openssl s_client -connect HOST:443 | openssl x509 -text

ISSUE: Slow response
  Network latency, server overloaded, DNS slow.
  Check: curl timing breakdown (-w option above)
  Check: mtr HOST (find slow hop)
  Check: server metrics (CPU, memory, disk I/O)

ISSUE: Intermittent failures
  Network flapping, DNS TTL issues, load balancer health checks.
  Check: mtr over time (packet loss at specific hop)
  Check: DNS TTL and multiple A records
  Check: load balancer logs
```


---

# CHAPTER 7: COMMON PITFALLS


## Networking Pitfalls

```
PITFALL 1: Not reusing connections
  New TCP + TLS per request = 2-3 RTT overhead each time.
  Fix: HTTP keep-alive, connection pooling, HTTP/2.

PITFALL 2: DNS as single point of failure
  DNS goes down → entire app unreachable.
  Fix: multiple DNS providers, low TTL for failover.

PITFALL 3: No timeouts
  Request hangs forever → thread/connection leak.
  Fix: always set connect timeout (5s) and read timeout (30s).

PITFALL 4: Ignoring DNS TTL
  Caching DNS forever → stale IP → wrong server.
  Fix: respect TTL, JVM needs networkaddress.cache.ttl setting.

PITFALL 5: Hardcoding IPs
  IP changes → app breaks.
  Fix: use hostnames, service discovery, DNS.

PITFALL 6: Not compressing
  Sending 1MB JSON when gzip would make it 100KB.
  Fix: Accept-Encoding: gzip, Brotli. Enable on server.

PITFALL 7: Ignoring MTU
  Packets too large → fragmentation → performance drop.
  Fix: Path MTU Discovery (default), don't set DF bit carelessly.

PITFALL 8: TCP for real-time
  Video call over TCP → retransmits cause latency spikes.
  Fix: UDP for real-time (or QUIC which handles loss better).

PITFALL 9: No TLS
  HTTP in production → credentials visible to any network observer.
  Fix: HTTPS everywhere. Let's Encrypt is free. No excuses.

PITFALL 10: Not understanding NAT
  "My server listens on 0.0.0.0 but can't be reached from internet."
  Fix: port forwarding, public IP, or tunnel (Cloudflare Tunnel — like Grg AI!).

PITFALL 11: HEAD-of-line blocking unawareness
  HTTP/1.1: one slow response blocks all.
  HTTP/2: TCP-level loss blocks all streams.
  Fix: HTTP/3 (QUIC) for true stream independence.

PITFALL 12: CORS confusion
  "API works in Postman but not browser."
  Fix: CORS is browser-only. Configure Access-Control-Allow-Origin on server.

PITFALL 13: Ephemeral port exhaustion
  Thousands of short connections → run out of source ports (TIME_WAIT).
  Fix: connection pooling, SO_REUSEADDR, tune TIME_WAIT.

PITFALL 14: Not monitoring latency percentiles
  Average latency 50ms. But p99 = 5 seconds (1% of users suffer).
  Fix: track p50, p95, p99, p99.9. Alert on p99.

PITFALL 15: Trusting client-reported IPs
  X-Forwarded-For header can be spoofed.
  Fix: trust only from known proxies (Cloudflare, your LB).
```