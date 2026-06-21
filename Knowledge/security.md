# Security Complete Reference for Developers


---

# CHAPTER 1: SECURITY FUNDAMENTALS


## Remarks

Application security is the practice of protecting systems, data, and users from malicious actors. Most security incidents come from **basic mistakes** (weak passwords, SQL injection, missed patches) — not sophisticated attacks. A developer who knows the OWASP Top 10 and applies basic hygiene prevents 95% of real-world breaches.

Key concepts: **CIA Triad** (Confidentiality, Integrity, Availability), **Defense in Depth** (layered security), **Principle of Least Privilege** (minimum permissions needed), **Zero Trust** (never trust, always verify), **Threat Modeling** (think like an attacker), **Cryptography** (math-based security), **Authentication vs Authorization** (who vs what they can do).

Used in: every production system. Security is not a feature — it's a property of well-built software.

Tools: **OWASP** (security org and resources), **Burp Suite** (web testing), **nmap** (network scanning), **Wireshark** (packet analysis), **Metasploit** (exploit framework), **bcrypt/argon2** (password hashing), **let's encrypt** (free TLS certs), **HashiCorp Vault** (secrets), **Snyk/Dependabot** (dependency scanning).


## CIA Triad

```
CONFIDENTIALITY
  Only authorized parties can read data.
  Threats: eavesdropping, theft, leaks.
  Defenses: encryption, access control, authentication.

INTEGRITY
  Data unchanged except by authorized parties.
  Threats: tampering, corruption, MITM.
  Defenses: hashing, signatures, audit logs, checksums.

AVAILABILITY
  System accessible when needed.
  Threats: DDoS, hardware failure, ransomware.
  Defenses: redundancy, rate limiting, backups, monitoring.

Every security decision balances these. Strong confidentiality often hurts availability (e.g., MFA blocks legitimate access if 2nd factor lost).
```


## Threat Modeling — STRIDE

```
A simple framework to think about threats:

S - SPOOFING       Pretending to be someone else
                   Defense: authentication, signatures

T - TAMPERING      Modifying data in transit or at rest
                   Defense: integrity checks (HMAC), TLS

R - REPUDIATION    Denying actions taken
                   Defense: audit logs, signed actions

I - INFO DISCLOSURE  Leaking sensitive info
                     Defense: encryption, access control

D - DENIAL OF SERVICE  Making system unusable
                       Defense: rate limit, capacity, CDN

E - ELEVATION OF PRIVILEGE  Gaining unauthorized access
                            Defense: authorization, least privilege

For each component in your system, ask: which STRIDE threats apply?
For each, what's your defense?
```


## Defense in Depth

```
LAYERED DEFENSE:
  No single defense is perfect. Stack multiple layers.

Example for a web app:
  Layer 1 (Network):    Firewall, DDoS protection (Cloudflare)
  Layer 2 (Transport):  TLS encryption everywhere (HTTPS)
  Layer 3 (App input):  Validation, rate limiting, WAF
  Layer 4 (App logic):  Authentication, authorization
  Layer 5 (Data):       Encryption at rest, access controls
  Layer 6 (Logs):       Monitoring, alerting on anomalies
  Layer 7 (People):     Training, principle of least privilege

If attacker bypasses one, others still protect.

PRINCIPLE OF LEAST PRIVILEGE:
  Every user/process/service gets minimum permissions needed.
  
  Bad:  App runs as root (full system access)
  Good: App runs as 'appuser' with read on /etc/app/config and write on /var/log/app

  Bad:  Database user has DROP TABLE privilege
  Good: App user can only SELECT/INSERT/UPDATE on specific tables
```


---

# CHAPTER 2: AUTHENTICATION


## Passwords — Storage Done Right

```
NEVER:
  ❌ Store plain text passwords
  ❌ Encrypt passwords (encryption is reversible)
  ❌ Use MD5 or SHA-1 for passwords (broken)
  ❌ Use plain SHA-256 (too fast — vulnerable to brute force)

ALWAYS:
  ✅ Hash with a slow, adaptive algorithm
  ✅ Use a unique random salt per password
  ✅ Verify in constant time (prevent timing attacks)

RECOMMENDED ALGORITHMS (slow on purpose):
  1. Argon2id    — winner of password hashing competition (2015)
  2. bcrypt      — battle-tested, widely supported
  3. scrypt      — memory-hard
  4. PBKDF2      — only if FIPS compliance required

Time targets: hashing should take 100-500ms (slow brute force, fast for legit login)
```


### bcrypt Example

```javascript
import bcrypt from 'bcrypt';

// Register: hash password
const password = 'user-input-password';
const SALT_ROUNDS = 12;   // 2^12 iterations, ~250ms on modern CPU
const hash = await bcrypt.hash(password, SALT_ROUNDS);
// Store ONLY hash in DB. Salt is embedded in hash.

await db.users.create({
    email: 'alice@example.com',
    password_hash: hash,   // Looks like: $2b$12$N9qo8uLOickgx2ZMRZoMye...
});

// Login: verify password
const user = await db.users.findByEmail(email);
if (!user) {
    // CRITICAL: still do a fake hash to prevent timing attack
    await bcrypt.compare(password, '$2b$12$invalidinvalidinvalidinvalidinv');
    return res.status(401).json({ error: 'Invalid credentials' });
}

const valid = await bcrypt.compare(password, user.password_hash);
if (!valid) {
    return res.status(401).json({ error: 'Invalid credentials' });
    // NEVER say "wrong password" vs "no such user" — helps attackers enumerate
}

// Login successful
```


### Argon2 (Modern Best Practice)

```python
# Python with argon2-cffi
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher(
    time_cost=3,         # iterations
    memory_cost=65536,   # 64 MB
    parallelism=4,
)

# Hash
hash_str = ph.hash("user-password")
# Returns: $argon2id$v=19$m=65536,t=3,p=4$...

# Verify
try:
    ph.verify(stored_hash, "user-password")
    # Valid!
except VerifyMismatchError:
    # Invalid
    pass

# Re-hash if parameters need upgrade (e.g., increase cost over years)
if ph.check_needs_rehash(stored_hash):
    new_hash = ph.hash("user-password")
    db.update_user_hash(user_id, new_hash)
```


## Password Policy

```
GOOD POLICY:
  ✅ Minimum length: 12 characters (longer is better than complex)
  ✅ Allow ALL characters (no banned special chars)
  ✅ Check against breach databases (haveibeenpwned API)
  ✅ Allow paste in password field
  ✅ Show "Show password" toggle
  ✅ Never email passwords (even temporary)

BAD POLICY (still common!):
  ❌ Maximum length (e.g., 16 chars) — suspicious, suggests storing plain text
  ❌ "Must contain uppercase, number, symbol" — actually weakens password choice
  ❌ Force change every 90 days — leads to "Password1", "Password2"
  ❌ Disallow special chars (causes "$5%" workarounds)

MODERN RECOMMENDATIONS (NIST SP 800-63B):
  - Length over complexity (passphrase > complex short)
  - Block known breached passwords
  - No periodic forced changes (only if compromise detected)
  - Allow paste (helps password managers)

EXAMPLE STRONG PASSWORDS:
  "correct horse battery staple"  (passphrase, 28 chars)
  "Tr3$tr-of-Pr0xim8-V0lc4n!"   (complex, 25 chars)
```


## Multi-Factor Authentication (MFA / 2FA)

```
WHAT YOU KNOW (password) — 1st factor
WHAT YOU HAVE (phone, hardware key) — 2nd factor
WHAT YOU ARE (biometric) — 3rd factor

TYPES (ranked by security):
  1. Hardware key (YubiKey, FIDO2) — STRONGEST, phishing-resistant
  2. TOTP (Google Authenticator, Authy) — strong, free
  3. Push notification (Authy, Duo) — convenient
  4. SMS — WEAK (SIM swap attacks), but better than nothing
  5. Email — WEAK (account takeover spreads)

IMPLEMENTING TOTP:
```

```python
# Python with pyotp
import pyotp
import qrcode

# Setup
def enable_2fa(user_id: int):
    secret = pyotp.random_base32()         # 32-char base32 secret
    # Save secret in DB (encrypted!)
    db.update_user(user_id, totp_secret=encrypt(secret))

    # Show QR code to user (to scan with Authenticator app)
    uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user.email,
        issuer_name="MyApp"
    )
    qr = qrcode.make(uri)
    return qr   # Display in UI

# Login: verify code
def verify_2fa(user_id: int, code: str) -> bool:
    user = db.get_user(user_id)
    if not user.totp_secret:
        return True   # 2FA not enabled

    totp = pyotp.TOTP(decrypt(user.totp_secret))
    return totp.verify(code, valid_window=1)
    # valid_window=1 → also accept previous 30s code (clock skew tolerance)


# Backup codes (in case phone lost)
import secrets
def generate_backup_codes(user_id: int) -> list[str]:
    codes = [secrets.token_hex(5) for _ in range(10)]   # 10 single-use codes
    hashed = [bcrypt.hash(c, 12) for c in codes]
    db.save_backup_codes(user_id, hashed)
    return codes   # Show to user ONCE, never again
```


## JWT (JSON Web Tokens)

```
WHAT IS JWT?
  Self-contained token: <header>.<payload>.<signature>
  
  Header  (base64):  {"alg": "HS256", "typ": "JWT"}
  Payload (base64):  {"sub": "user-123", "exp": 1700000000}
  Signature:         HMAC-SHA256(header + "." + payload, SECRET)

  Anyone can read payload (base64 is NOT encryption!)
  Only server can create/verify (knows secret).

WHEN TO USE:
  ✅ Short-lived access tokens (15-60 minutes)
  ✅ Stateless API authentication
  ✅ Service-to-service auth

WHEN NOT TO USE:
  ❌ Long-lived sessions (too risky if leaked)
  ❌ Sensitive data in payload (not encrypted!)
  ❌ Sole revocation mechanism (can't easily revoke before exp)

REFRESH TOKEN PATTERN:
  Access token:   short (15min), in memory or HttpOnly cookie
  Refresh token:  long (7-30 days), stored in DB, can be revoked
  When access expires → use refresh to get new access
```

```javascript
// JWT in Node.js
import jwt from 'jsonwebtoken';

// Sign
function createTokens(user) {
    const accessToken = jwt.sign(
        { sub: user.id, role: user.role },
        process.env.JWT_SECRET,
        {
            expiresIn: '15m',
            issuer: 'myapp',
            audience: 'myapp-api',
        }
    );

    // Refresh token: random, stored in DB
    const refreshToken = crypto.randomBytes(32).toString('hex');
    db.refresh_tokens.create({
        token_hash: bcrypt.hashSync(refreshToken, 10),
        user_id: user.id,
        expires_at: new Date(Date.now() + 7 * 24 * 3600 * 1000),
    });

    return { accessToken, refreshToken };
}

// Verify middleware
function authMiddleware(req, res, next) {
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) return res.status(401).json({ error: 'No token' });

    try {
        const payload = jwt.verify(token, process.env.JWT_SECRET, {
            issuer: 'myapp',
            audience: 'myapp-api',
        });
        req.user = payload;
        next();
    } catch (err) {
        if (err.name === 'TokenExpiredError') {
            return res.status(401).json({ error: 'Token expired' });
        }
        return res.status(401).json({ error: 'Invalid token' });
    }
}

// Refresh
app.post('/auth/refresh', async (req, res) => {
    const { refreshToken } = req.body;

    // Find token in DB
    const tokens = await db.refresh_tokens.findActive();
    const valid = tokens.find(t => bcrypt.compareSync(refreshToken, t.token_hash));

    if (!valid) return res.status(401).json({ error: 'Invalid refresh token' });

    // Issue new access token
    const accessToken = jwt.sign({ sub: valid.user_id }, process.env.JWT_SECRET, { expiresIn: '15m' });
    res.json({ accessToken });
});

// Logout — revoke refresh token
app.post('/auth/logout', async (req, res) => {
    await db.refresh_tokens.deleteByUser(req.user.sub);
    res.json({ ok: true });
});
```


---

# CHAPTER 3: AUTHORIZATION


## Authentication vs Authorization

```
AUTHENTICATION:  "Who are you?"
                 → Login with credentials → identity established

AUTHORIZATION:   "What can you do?"
                 → Check if identity allowed for action
                 → Access control

Both required for security. Never confuse them.
```


## Authorization Patterns

```
RBAC (Role-Based Access Control):
  Users have roles. Roles have permissions.
  
  Example:
    Role "admin"     → can: delete_users, create_users, view_logs
    Role "moderator" → can: delete_posts, ban_users
    Role "user"      → can: create_post, edit_own_post
  
  Simple, common, good for most apps.

ABAC (Attribute-Based Access Control):
  Decisions based on attributes (user, resource, environment, action).
  
  Example: "User can edit document IF 
    user.department == document.department 
    AND time is during business hours
    AND user.clearance >= document.classification"
  
  More flexible than RBAC but complex. Use for enterprise.

OWNERSHIP-BASED:
  User can act on their own resources.
  
  if request.user.id == resource.owner_id: allow
  
  Simple but often combined with roles ("admins can edit anyone's post").

POLICY-BASED:
  Centralized rule engine (OPA, Cedar).
  Policies written in domain-specific language.
  Best for complex enterprise needs.
```


### RBAC Implementation

```python
# Define permissions
class Permission(str, Enum):
    USER_READ = "user:read"
    USER_WRITE = "user:write"
    USER_DELETE = "user:delete"
    POST_READ = "post:read"
    POST_WRITE = "post:write"
    POST_DELETE = "post:delete"
    ADMIN_ALL = "admin:*"

ROLE_PERMISSIONS = {
    "admin": [Permission.ADMIN_ALL],
    "moderator": [Permission.POST_DELETE, Permission.USER_READ],
    "user": [Permission.POST_READ, Permission.POST_WRITE],
    "guest": [Permission.POST_READ],
}

def has_permission(user, required: Permission) -> bool:
    perms = ROLE_PERMISSIONS.get(user.role, [])
    if Permission.ADMIN_ALL in perms:
        return True
    return required in perms

# Decorator for FastAPI / Flask
def require_permission(perm: Permission):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user=Depends(get_current_user), **kwargs):
            if not has_permission(current_user, perm):
                raise HTTPException(403, "Forbidden")
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# Usage
@app.delete("/posts/{post_id}")
@require_permission(Permission.POST_DELETE)
async def delete_post(post_id: int, current_user: User = Depends(get_current_user)):
    await db.posts.delete(post_id)
    return {"deleted": post_id}
```


## Common Authorization Mistakes

```python
# IDOR (Insecure Direct Object Reference)
# BAD: anyone with order ID can view it
@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    return await db.orders.get(order_id)
    # Attacker tries /orders/1, /orders/2, ... reads everyone's orders!

# FIX: check ownership
@app.get("/orders/{order_id}")
async def get_order(order_id: int, current_user: User = Depends(get_current_user)):
    order = await db.orders.get(order_id)
    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(403, "Forbidden")
    return order


# Privilege escalation via params
# BAD: trusts user-supplied role
@app.post("/users")
async def create_user(data: dict):
    return await db.users.create(name=data["name"], role=data.get("role", "user"))
    # Attacker sends {"role": "admin"} → instant admin!

# FIX: never trust client for permission-related fields
@app.post("/users")
async def create_user(data: CreateUserSchema, current: User = Depends(get_current_user)):
    if data.role == "admin" and current.role != "admin":
        raise HTTPException(403)
    return await db.users.create(name=data.name, role=data.role)


# Mass assignment
# BAD: passes all fields to DB
@app.put("/users/me")
async def update_me(data: dict, current: User = Depends(get_current_user)):
    return await db.users.update(current.id, **data)
    # Attacker sends {"role": "admin", "balance": 99999} → updates those!

# FIX: explicit allow list
class UpdateMeSchema(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    # Note: role, balance, etc. NOT here

@app.put("/users/me")
async def update_me(data: UpdateMeSchema, current: User = Depends(get_current_user)):
    return await db.users.update(current.id, **data.dict(exclude_unset=True))
```


---

# CHAPTER 4: OWASP TOP 10 (THE BIG THREATS)


## A01: Broken Access Control

```
Most common vulnerability. Examples:
  - Viewing others' data (IDOR)
  - Bypassing access checks
  - Mass assignment
  - CORS misconfiguration

DEFENSES:
  ✅ Deny by default; explicit allow
  ✅ Verify ownership on every access
  ✅ Reject requests that try to set sensitive fields
  ✅ Test auth on EVERY endpoint
  ✅ Use proven libraries, not custom auth
```


## A02: Cryptographic Failures

```
EXAMPLES:
  - Passwords stored unhashed or with MD5
  - Sensitive data sent over HTTP (no TLS)
  - Hardcoded keys in code/repos
  - Self-signed certs in production

DEFENSES:
  ✅ HTTPS everywhere (Let's Encrypt is free)
  ✅ Argon2/bcrypt for passwords
  ✅ AES-256-GCM for data at rest
  ✅ TLS 1.3 (or at minimum 1.2)
  ✅ Secrets in env vars or vault, NOT in code
  ✅ Strong random: crypto.randomBytes() not Math.random()
```


## A03: Injection (SQL, NoSQL, Command)

```python
# SQL Injection
# BAD
query = f"SELECT * FROM users WHERE name = '{user_input}'"
# Attacker: user_input = "'; DROP TABLE users;--"

# GOOD: parameterized queries
cursor.execute("SELECT * FROM users WHERE name = %s", (user_input,))


# Command Injection
# BAD
import os
os.system(f"ping {user_input}")
# Attacker: user_input = "google.com; rm -rf /"

# GOOD: use lists, not shell
import subprocess
subprocess.run(["ping", "-c", "4", user_input], check=True)


# NoSQL Injection (MongoDB)
# BAD
db.users.find({"name": req.body.name, "password": req.body.password})
# Attacker: {"name": "admin", "password": {"$ne": null}} → matches anything!

# GOOD: validate types
if not isinstance(req.body.name, str): raise ValueError
if not isinstance(req.body.password, str): raise ValueError


# LDAP Injection
# BAD
filter = f"(uid={user_input})"
# Attacker: user_input = "*)(uid=*"

# GOOD: escape LDAP special chars
from ldap3.utils.dn import escape_attribute_value
filter = f"(uid={escape_attribute_value(user_input)})"
```


## A04: Insecure Design

```
This is about ARCHITECTURAL flaws, not bugs.

EXAMPLES:
  - No rate limiting on login → brute force possible
  - Password reset via email with no expiry
  - Critical action (transfer money) without confirmation
  - Search endpoint that allows DOS via expensive queries
  - User-facing error messages reveal internal architecture

DEFENSES:
  ✅ Threat modeling EARLY in design
  ✅ Rate limiting on sensitive endpoints
  ✅ Confirmations for destructive/financial actions
  ✅ Generic error messages to users; detailed errors to logs
```


## A05: Security Misconfiguration

```
EXAMPLES:
  - Default passwords still in place
  - Debug mode enabled in production
  - Detailed errors shown to users
  - Cloud bucket accidentally public
  - Outdated software with known vulnerabilities

DEFENSES:
  ✅ Automated config scanning (Snyk, Aqua)
  ✅ Same config across dev/staging/prod (12-factor)
  ✅ Disable debug, verbose errors in prod
  ✅ Regular updates of dependencies and OS
  ✅ Bucket policies reviewed regularly
```


## A06: Vulnerable and Outdated Components

```
PROBLEM:
  Dependencies have CVEs. Don't update → vulnerable.

EXAMPLES:
  - log4shell (log4j 2021): RCE in Java logging library
  - Heartbleed (OpenSSL 2014): memory leak via TLS
  - Equifax (Apache Struts 2017): unpatched component → 147M records leaked

DEFENSES:
  ✅ Dependabot / Renovate / Snyk for auto-PRs
  ✅ npm audit / pip-audit / cargo audit regularly
  ✅ SBOM (Software Bill of Materials) for visibility
  ✅ Update at least monthly for non-critical, immediately for critical
  ✅ Subscribe to CVE feeds for your stack
```


## A07: Identification & Authentication Failures

```
EXAMPLES:
  - No rate limit on login → brute force
  - Predictable session IDs
  - Storing passwords in plain text
  - Session never expires
  - No MFA option

DEFENSES:
  ✅ Strong password storage (Argon2/bcrypt)
  ✅ Rate limit login attempts (per IP and per account)
  ✅ Account lockout after N failures (with timeout, not permanent)
  ✅ MFA available, required for admin
  ✅ Sessions expire (inactivity + absolute)
  ✅ HTTPS-only cookies (Secure flag), HttpOnly, SameSite
```


## A08: Software & Data Integrity Failures

```
EXAMPLES:
  - Pulling Docker images from untrusted sources
  - Auto-update from any source (supply chain attacks)
  - Deserializing untrusted data
  - No signing/verification of binaries

DEFENSES:
  ✅ Pin versions, use checksums
  ✅ Sign artifacts (cosign for containers)
  ✅ Don't deserialize untrusted input (pickle, ObjectInputStream)
  ✅ Code signing for releases
```


## A09: Security Logging & Monitoring Failures

```
EXAMPLES:
  - No logs of failed logins
  - Logs stored only on compromised server
  - No alerts on anomalies
  - Sensitive data IN logs (passwords, tokens)

DEFENSES:
  ✅ Log: logins (success/fail), permission denials, admin actions, errors
  ✅ Ship logs to central system (don't store only locally)
  ✅ Retain logs ≥ 90 days
  ✅ Alert on: failed login spikes, unusual patterns, errors
  ✅ Sanitize logs — never log secrets, PII
```


## A10: Server-Side Request Forgery (SSRF)

```
PROBLEM:
  App makes HTTP requests to URL provided by user.
  Attacker provides internal URL → app accesses internal services.

EXAMPLE:
  /fetch?url=https://evil.com (innocent)
  /fetch?url=http://169.254.169.254/latest/meta-data/  (AWS metadata → cloud creds!)
  /fetch?url=http://localhost:6379                     (Redis - probably no auth)
  /fetch?url=file:///etc/passwd                         (local files)

DEFENSES:
  ✅ Whitelist allowed domains
  ✅ Resolve hostname → block private IPs (10.x, 172.16.x, 192.168.x, 127.x, 169.254.x)
  ✅ Disable URL schemes besides http/https
  ✅ Use a dedicated egress proxy with rules
```

```python
import socket
import ipaddress
from urllib.parse import urlparse

ALLOWED_SCHEMES = {'http', 'https'}
PRIVATE_NETWORKS = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('127.0.0.0/8'),
    ipaddress.ip_network('169.254.0.0/16'),  # link-local (cloud metadata!)
]

def safe_fetch(url: str):
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError("Scheme not allowed")
    
    # Resolve hostname
    ip = socket.gethostbyname(parsed.hostname)
    ip_obj = ipaddress.ip_address(ip)
    
    if any(ip_obj in net for net in PRIVATE_NETWORKS):
        raise ValueError("Internal IP not allowed")
    
    if ip_obj.is_link_local or ip_obj.is_loopback:
        raise ValueError("Special IP not allowed")
    
    # Now safe to fetch
    return requests.get(url, timeout=5)
```


---

# CHAPTER 5: WEB SECURITY


## Cross-Site Scripting (XSS)

```
THREE TYPES:
  Reflected XSS:   user input appears in response (search results, error pages)
  Stored XSS:      attacker's script saved in DB, served to other users (worst!)
  DOM-based XSS:   script comes from URL fragment or DOM, processed by JS

EXAMPLE:
  Search page shows: <h1>Results for {{ query }}</h1>
  Attacker URL: /search?q=<script>steal_cookies()</script>
  Innocent user clicks → script runs in their browser → cookies stolen!

DEFENSES:

  1. ESCAPE OUTPUT (context-aware):
     HTML body:     &<>"' → entities
     HTML attr:     wrap in "..." and escape "
     JavaScript:    JSON.stringify or carefully escape
     URL:           encodeURIComponent
  
  2. CONTENT SECURITY POLICY (CSP):
     HTTP header that restricts what can run.
     
     Content-Security-Policy: default-src 'self'; script-src 'self' cdn.example.com
     
     Even if XSS injected, browser won't execute external scripts.

  3. INPUT VALIDATION (defense in depth):
     Allow-list characters, lengths.
     But: validation alone is NOT enough. Always escape output too.

  4. HttpOnly COOKIES:
     Set-Cookie: session=abc; HttpOnly
     JavaScript can't read → XSS can't steal session.
```

```javascript
// React auto-escapes by default (good!)
function Search({ query }) {
    return <h1>Results for {query}</h1>;   // SAFE
}

// DANGER: dangerouslySetInnerHTML (the name warns you!)
function Bad({ html }) {
    return <div dangerouslySetInnerHTML={{ __html: html }} />;
    // XSS if html comes from user!
}

// If you MUST render HTML, sanitize first
import DOMPurify from 'dompurify';
function Safe({ html }) {
    const clean = DOMPurify.sanitize(html);
    return <div dangerouslySetInnerHTML={{ __html: clean }} />;
}

// In Express, set CSP header
import helmet from 'helmet';
app.use(helmet.contentSecurityPolicy({
    directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "https://cdn.example.com"],
        styleSrc: ["'self'", "'unsafe-inline'"],   // try to avoid 'unsafe-inline'
        imgSrc: ["'self'", "data:", "https:"],
    },
}));
```


## Cross-Site Request Forgery (CSRF)

```
PROBLEM:
  User is logged in to bank.com (cookie set).
  Visits evil.com.
  evil.com has a hidden form that POSTs to bank.com/transfer.
  Browser sends cookie automatically → transfer executed!

DEFENSES:

  1. SameSite COOKIES (modern, easy):
     Set-Cookie: session=...; SameSite=Lax    (or Strict)
     Browser sends cookie only on same-site requests.
     Default in Chrome since 2020.

  2. CSRF TOKENS (older but still used):
     Server includes random token in form.
     Client must send it back.
     Attacker on evil.com can't read the token (cross-origin).

  3. CHECK Origin/Referer HEADER:
     For state-changing requests, verify Origin matches your domain.

  4. REQUIRE EXPLICIT CONFIRMATION FOR CRITICAL ACTIONS:
     Re-enter password, MFA prompt, etc.

REMEMBER: CSRF only affects cookie-based auth. JWT in headers is immune
(attacker on evil.com can't access your headers).
```

```python
# Flask example
from flask import Flask, session
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

# Enable CSRF
csrf = CSRFProtect(app)

# Cookies
app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=True,    # HTTPS only
    SESSION_COOKIE_HTTPONLY=True,
)

# Forms automatically get CSRF token via Jinja:
# <form method="post">
#   {{ csrf_token() }}
#   ...
# </form>
```


## HTTPS / TLS

```
NEVER SHIP HTTP IN PRODUCTION.

Why TLS:
  - Confidentiality: encrypted in transit
  - Integrity: tampering detected
  - Authenticity: verify server identity (cert)

LET'S ENCRYPT (free):
  Automatic certs with certbot or Caddy.
  
  # Caddyfile (auto HTTPS)
  example.com {
      reverse_proxy localhost:3000
  }
  # That's it! Caddy gets cert from Let's Encrypt automatically.

HSTS HEADER:
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  → Browser refuses to connect over HTTP for a year.

REDIRECT HTTP → HTTPS:
  All HTTP traffic redirected to HTTPS at LB/proxy level.

TLS VERSION:
  Minimum: TLS 1.2
  Modern: TLS 1.3 (faster, more secure)
  DO NOT enable: SSLv2, SSLv3, TLS 1.0, TLS 1.1 (insecure)

CERTIFICATE TYPES:
  DV (Domain Validated): cheap/free, verify domain owner. Sufficient for most.
  OV (Org Validated): verifies organization (extra trust shown in browsers? Mostly removed).
  EV (Extended Validation): formerly showed green bar; now removed from most browsers.
```


## Secure Cookies

```javascript
// Express example
res.cookie('session', sessionId, {
    httpOnly: true,             // Not accessible to JavaScript
    secure: true,               // HTTPS only
    sameSite: 'lax',            // CSRF protection
    maxAge: 24 * 3600 * 1000,   // 24 hours
    domain: '.example.com',     // Sets for all subdomains (be careful!)
    path: '/',
});
```


## Rate Limiting

```javascript
// Express with express-rate-limit
import rateLimit from 'express-rate-limit';

// Per IP, global
const globalLimit = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100,
    standardHeaders: true,
    legacyHeaders: false,
});

// Per IP, strict for sensitive endpoints
const loginLimit = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 5,
    skipSuccessfulRequests: true,
    message: 'Too many failed attempts, try again in 15 minutes',
});

app.use(globalLimit);
app.post('/auth/login', loginLimit, async (req, res) => { /* ... */ });

// For distributed apps: use Redis store
import RedisStore from 'rate-limit-redis';
const limiter = rateLimit({
    store: new RedisStore({ sendCommand: (...args) => redisClient.call(...args) }),
    windowMs: 15 * 60 * 1000,
    max: 100,
});
```


---

# CHAPTER 6: CRYPTOGRAPHY ESSENTIALS


## Symmetric Encryption (AES)

```python
# AES-256-GCM (authenticated encryption, recommended)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

# Generate key (32 bytes = 256 bits)
key = AESGCM.generate_key(bit_length=256)

# Encrypt
def encrypt(plaintext: bytes, key: bytes) -> bytes:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)        # 96-bit nonce — NEVER reuse with same key!
    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)
    return nonce + ciphertext     # Prepend nonce

# Decrypt
def decrypt(blob: bytes, key: bytes) -> bytes:
    aesgcm = AESGCM(key)
    nonce, ciphertext = blob[:12], blob[12:]
    return aesgcm.decrypt(nonce, ciphertext, associated_data=None)

# Use
plaintext = b"sensitive data"
encrypted = encrypt(plaintext, key)
decrypted = decrypt(encrypted, key)
```

**KEY MANAGEMENT IS HARDER THAN ENCRYPTION:**
- Where to store the key? (NOT in code or env vars for serious apps)
- How to rotate? (replace key periodically)
- Use KMS: AWS KMS, GCP KMS, HashiCorp Vault


## Asymmetric Encryption (RSA, EC)

```
PUBLIC + PRIVATE KEY PAIR:
  Encrypt with public → only private can decrypt (privacy)
  Sign with private → anyone can verify with public (authenticity)

USE CASES:
  - TLS handshake (key exchange)
  - SSH login (auth via keypair)
  - Signing software releases
  - Encrypting symmetric keys (hybrid encryption)

RSA: classic, large keys (2048+ bits)
ECC (Elliptic Curve): smaller keys, faster, modern. Use Ed25519 for signing.

RULE: NEVER encrypt large data with asymmetric directly.
      Use symmetric (AES) for data, asymmetric for the AES key.
      This is "hybrid encryption" — how TLS works.
```


## Hashing vs Encryption

```
HASHING (one-way):
  - SHA-256, SHA-3 for integrity checks
  - bcrypt, Argon2 for passwords (slow on purpose)
  - Cannot be reversed
  - Output is fixed-size

ENCRYPTION (two-way):
  - AES, RSA, ChaCha20
  - Requires a key
  - Can be reversed (with key)

WHEN TO USE:
  - Passwords: HASH (never encrypt)
  - User data at rest: ENCRYPT
  - File checksums: HASH (SHA-256)
  - API keys for verification: HASH (don't store plain text)
```


## HMAC (Hash-based Message Authentication Code)

```
HMAC: hash + secret key → message authentication.

USE WHEN: need to verify message NOT tampered with AND from authorized sender.

WEBHOOKS often signed with HMAC:
  Stripe, GitHub, etc. send Webhook with HMAC signature.
  You verify on your side.
```

```python
import hmac
import hashlib

# Verify webhook signature
def verify_webhook(payload: bytes, signature_header: str, secret: bytes) -> bool:
    expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    received = signature_header.replace('sha256=', '')
    return hmac.compare_digest(expected, received)   # constant-time compare!

@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get('Stripe-Signature')
    
    if not verify_webhook(payload, signature, STRIPE_WEBHOOK_SECRET):
        raise HTTPException(401, "Invalid signature")
    
    event = json.loads(payload)
    # Process event...
```


## Random Numbers

```
CRYPTOGRAPHICALLY SECURE RANDOM:
  Python:      secrets.token_bytes(32)
  Node.js:     crypto.randomBytes(32)
  Browser JS:  crypto.getRandomValues(new Uint8Array(32))
  Go:          crypto/rand
  Rust:        rand::rngs::OsRng

INSECURE — DO NOT USE FOR SECURITY:
  Python:      random.random()
  Node.js:     Math.random()
  JS:          Math.random()

USE SECURE FOR:
  - Tokens (session, CSRF, reset)
  - Salts
  - Nonces
  - API keys
  - UUIDs (use UUID v4 or v7)

EXAMPLE: generate a random token
```

```python
import secrets

# 32 hex chars (16 bytes of entropy)
token = secrets.token_hex(16)

# Base64-style URL-safe token
token = secrets.token_urlsafe(32)

# Choose from list
elem = secrets.choice(['rock', 'paper', 'scissors'])

# Random int in range
n = secrets.randbelow(1000)
```


---

# CHAPTER 7: SECURE DEVELOPMENT PRACTICES


## Secrets Management

```
NEVER:
  ❌ Commit secrets to Git (rotate immediately if you did)
  ❌ Email/Slack secrets in plain text
  ❌ Hardcode in source code
  ❌ Log secrets

PROPER STORAGE:
  Local dev:   .env file (in .gitignore!)
  Production:  Secret manager (Vault, AWS Secrets Manager, GCP Secret Manager)
               Or K8s Secrets (with encryption at rest enabled)

ROTATION:
  - Regularly rotate (90 days for high-value)
  - Immediately after employee departure
  - Immediately after any leak

DETECTION:
  - Pre-commit hooks (gitleaks, detect-secrets)
  - CI scanning (TruffleHog, GitGuardian)
  - GitHub's secret scanning (free for public repos)

EXAMPLE .gitignore:
  .env
  .env.*
  !.env.example       # commit a template with placeholders
  *.pem
  *.key
  secrets/
```


## Dependency Security

```bash
# Check for vulnerabilities
npm audit                       # Node
npm audit fix                   # Auto-fix where possible
pip-audit                       # Python
cargo audit                     # Rust
gradle dependencyCheckAnalyze   # Java

# Better: use Snyk, Dependabot, Renovate for auto-PRs

# SBOM (Software Bill of Materials) — list what's in your image
syft myapp:1.0.0 -o json > sbom.json
grype myapp:1.0.0           # Scan for vulnerabilities

# In CI, fail build on high-severity findings:
npm audit --audit-level=high
```


## Container Security

```dockerfile
# DOCKERFILE BEST PRACTICES

# 1. Use minimal, official, pinned images
FROM node:20.5.1-alpine        # Not 'latest', not full Ubuntu

# 2. Multi-stage to remove build tools from final image
FROM node:20-alpine AS builder
# ... build steps ...
FROM node:20-alpine
COPY --from=builder /build/dist ./dist

# 3. Don't run as root
RUN addgroup -S app && adduser -S app -G app
USER app

# 4. Don't store secrets in image
# BAD:  ENV DB_PASSWORD=secret
# GOOD: pass at runtime via env or secret mount

# 5. Read-only filesystem (run with --read-only)
# Only write to specific volumes

# 6. Set healthcheck
HEALTHCHECK --interval=30s CMD curl -f http://localhost:3000/health

# 7. Drop capabilities at runtime
# docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp
```


## Logging and Monitoring for Security

```python
# What to log
def log_security_event(event_type: str, **kwargs):
    logger.warning("security_event", extra={
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "ip": request.client.host,
        "user_agent": request.headers.get("user-agent"),
        **kwargs,
    })

# Examples
log_security_event("login_success", user_id=user.id)
log_security_event("login_failure", email=email)
log_security_event("permission_denied", user_id=user.id, resource=resource_id)
log_security_event("password_changed", user_id=user.id)
log_security_event("api_key_generated", user_id=user.id)

# DO NOT LOG:
#   - Passwords
#   - API keys / tokens (log only first few chars + hash)
#   - Credit card numbers
#   - Personal identification (SSN, etc.)
#   - Session tokens

# Sanitize
def sanitize_log(data: dict) -> dict:
    SENSITIVE = {'password', 'token', 'authorization', 'cookie', 'api_key'}
    return {k: '***' if k.lower() in SENSITIVE else v for k, v in data.items()}
```


## Common Pitfalls

```
PITFALL 1: Trust user input
  → Validate EVERYTHING from client. Never trust types, lengths, values.

PITFALL 2: Custom crypto
  → Don't write your own. Use vetted libraries.

PITFALL 3: Defense by obscurity alone
  → Hiding the URL of admin page isn't security. Add real auth.

PITFALL 4: Disabled HTTPS in dev "to make testing easier"
  → Bugs only surface in HTTPS environment. Use HTTPS dev (mkcert).

PITFALL 5: Excessive permissions
  → DB user with full privileges. Process running as root.
  → Always least privilege.

PITFALL 6: Treating security as separate phase
  → "We'll add security later" = redesign required later. Build in from start.

PITFALL 7: No incident response plan
  → Breach happens. Without plan: chaos, missed evidence, slow response.
  → Have a written playbook. Practice drills.

PITFALL 8: Ignoring updates
  → Old library with CVE. "It still works" — until exploited.
  → Update regularly. Automate where possible.

PITFALL 9: Storing tokens insecurely on client
  → localStorage accessible by XSS. Sensitive tokens → HttpOnly cookies.

PITFALL 10: Not testing security
  → Run regular security tests: SAST (code analysis), DAST (dynamic), pen tests.
  → Bug bounty programs catch what your team misses.

PITFALL 11: Verbose error messages to users
  → "Database connection to 10.0.5.13:5432 failed" → reveals infrastructure.
  → User sees: "Something went wrong". Logs see: full details.

PITFALL 12: Same password for everything (people, including admins!)
  → Use password manager. Unique random per service.

PITFALL 13: Open S3 buckets / cloud storage
  → Default to private. Audit regularly. Public link with knowledge of UUID = not security.

PITFALL 14: No backup, OR backup but never tested
  → Ransomware: pay or restore? If backup untested, you'll find out it doesn't work then.
  → Regular drills: restore on a test system, verify integrity.

PITFALL 15: Forgetting about exit (employee leaves, access revoked when?)
  → Process to immediately disable accounts/keys upon departure.
```