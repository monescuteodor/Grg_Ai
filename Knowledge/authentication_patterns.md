# Authentication Patterns Complete Reference


---

# CHAPTER 1: SESSION VS TOKEN AUTHENTICATION


## Remarks

Authentication verifies WHO the user is. Authorization determines WHAT they can do. Every web application needs both. The two main approaches are session-based (server stores state) and token-based (client stores state/JWT).


## Session-Based Authentication

```
HOW IT WORKS:
1. User sends username + password
2. Server verifies → creates session in memory/database
3. Server sends session ID in cookie
4. Browser sends cookie with every request
5. Server looks up session ID → finds user

Client                          Server
  POST /login {user, pass}  →
                             ←  Set-Cookie: session=abc123
  GET /profile              →   (cookie sent automatically)
  Cookie: session=abc123
                             ←  {user: "Alice", role: "admin"}

STORAGE: Server-side (Redis, database, memory)
SESSION DATA: user_id, role, permissions, expiry
```

```python
# Flask session example
from flask import Flask, session, request
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.post('/login')
def login():
    user = authenticate(request.json['email'], request.json['password'])
    if not user:
        return {'error': 'Invalid credentials'}, 401
    session['user_id'] = user.id
    session['role'] = user.role
    return {'message': 'Logged in'}

@app.get('/profile')
def profile():
    if 'user_id' not in session:
        return {'error': 'Not authenticated'}, 401
    user = get_user(session['user_id'])
    return {'name': user.name, 'role': session['role']}

@app.post('/logout')
def logout():
    session.clear()
    return {'message': 'Logged out'}
```


## JWT (JSON Web Token) Authentication

```
HOW IT WORKS:
1. User sends username + password
2. Server verifies → creates signed JWT token
3. Server sends token in response body
4. Client stores token (localStorage/memory)
5. Client sends token in Authorization header
6. Server VERIFIES token signature (no database lookup!)

JWT STRUCTURE:
  header.payload.signature

  Header:  {"alg": "HS256", "typ": "JWT"}
  Payload: {"user_id": 123, "role": "admin", "exp": 1700000000}
  Signature: HMAC-SHA256(header + "." + payload, SECRET_KEY)

IMPORTANT: JWT is SIGNED, not ENCRYPTED!
  Anyone can READ the payload (base64 decode).
  But nobody can FORGE it without the secret key.
```

```python
import jwt
import bcrypt
from datetime import datetime, timedelta

SECRET = "your-secret-key-keep-it-safe"

# Login → generate token
@app.post('/login')
def login():
    user = db.find_user(request.json['email'])
    if not user or not bcrypt.checkpw(
        request.json['password'].encode(), user.password_hash
    ):
        return {'error': 'Invalid credentials'}, 401

    token = jwt.encode({
        'user_id': user.id,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(hours=24),
    }, SECRET, algorithm='HS256')

    return {'token': token}

# Middleware → verify token
def require_auth(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return {'error': 'No token'}, 401
        try:
            payload = jwt.decode(token, SECRET, algorithms=['HS256'])
            request.user = payload
        except jwt.ExpiredSignatureError:
            return {'error': 'Token expired'}, 401
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token'}, 401
        return f(*args, **kwargs)
    return wrapper

@app.get('/profile')
@require_auth
def profile():
    return {'user_id': request.user['user_id'], 'role': request.user['role']}
```


## Session vs JWT Comparison

```
Feature              Session              JWT
─────────────────────────────────────────────────────
State                Server-side          Client-side (stateless)
Storage              Redis/DB/memory      Client (header)
Scalability          Need shared store    Easy (no shared state)
Logout               Delete session       Can't invalidate easily
Security             Cookie: HttpOnly     Must protect from XSS
Size                 Small cookie (~32B)  Large token (~500B+)
Mobile               Cookies problematic  Works great (header)
Revocation           Instant (delete)     Hard (need blacklist)

WHEN TO USE SESSION:
  - Traditional web apps (server-rendered)
  - Need instant logout/revocation
  - Simple setup

WHEN TO USE JWT:
  - APIs consumed by mobile apps
  - Microservices (each service verifies independently)
  - Stateless architecture (no shared session store)
```


---

# CHAPTER 2: OAUTH 2.0


## OAuth Flow

```
OAuth 2.0 = let users login with Google/GitHub/etc.
You NEVER see their password. The provider handles auth.

AUTHORIZATION CODE FLOW (most secure, for web apps):

User → Your App → Redirect to Google →
  Google login page → User logs in →
  Google redirects back with CODE →
  Your server exchanges CODE for TOKEN (server-to-server) →
  Your server uses TOKEN to get user info from Google API

Step by step:
1. User clicks "Login with Google"
2. Redirect to:
   https://accounts.google.com/o/oauth2/auth?
     client_id=YOUR_ID&
     redirect_uri=https://yourapp.com/callback&
     scope=openid%20email%20profile&
     response_type=code&
     state=random_csrf_token

3. User logs in on Google, grants permission
4. Google redirects: https://yourapp.com/callback?code=AUTH_CODE&state=...
5. Your SERVER (not browser!) exchanges code for token:
   POST https://oauth2.googleapis.com/token
     client_id=YOUR_ID
     client_secret=YOUR_SECRET
     code=AUTH_CODE
     redirect_uri=...
     grant_type=authorization_code

6. Google returns: { access_token, id_token, refresh_token }
7. Use access_token to call Google API:
   GET https://www.googleapis.com/oauth2/v2/userinfo
   Authorization: Bearer ACCESS_TOKEN
   → { email, name, picture }
```

```python
# FastAPI + Google OAuth
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name='google',
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_SECRET',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_url='https://oauth2.googleapis.com/token',
    client_kwargs={'scope': 'openid email profile'},
)

@app.get('/login/google')
async def login_google(request: Request):
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get('/callback')
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    # Create or update user in YOUR database
    user = find_or_create_user(email=user_info['email'], name=user_info['name'])
    # Issue YOUR session/JWT
    return create_session(user)
```


---

# CHAPTER 3: PASSWORD BEST PRACTICES

```
HASHING:
  NEVER store plain text passwords.
  NEVER use MD5 or SHA-256 (too fast to brute force).
  USE bcrypt (cost factor 12+) or Argon2id.

  bcrypt hash: $2b$12$LJ3m4ys3Lg2kEZS9GIH5tu...
  Built-in salt. 250ms per hash. Attacker: ~4 guesses/sec.

PASSWORD POLICY (NIST SP 800-63B):
  ✅ Minimum 12 characters (length > complexity)
  ✅ Check against breached passwords (haveibeenpwned API)
  ✅ Allow paste into password fields
  ✅ Show password strength meter
  ❌ Don't require special characters (leads to Password1!)
  ❌ Don't force periodic rotation
  ❌ Don't use security questions

MULTI-FACTOR AUTHENTICATION (MFA):
  Something you KNOW (password)
  + Something you HAVE (phone, hardware key)
  + Something you ARE (fingerprint, face)

  TOTP (Time-based One-Time Password):
    App generates 6-digit code every 30 seconds.
    Google Authenticator, Authy, 1Password.

  WebAuthn/FIDO2:
    Hardware key (YubiKey) or biometric.
    Phishing-resistant. Gold standard.
```


---

# CHAPTER 4: COMMON PITFALLS

```
PITFALL 1: Storing JWT in localStorage
  Vulnerable to XSS (any injected script can steal it).
  Fix: HttpOnly cookie for web apps, or memory-only + refresh token.

PITFALL 2: No CSRF protection with cookies
  Attacker site can trigger requests with user's cookies.
  Fix: SameSite=Lax cookie + CSRF token for forms.

PITFALL 3: Long-lived JWTs without refresh
  24h JWT stolen → attacker has 24h access, can't revoke.
  Fix: short access token (15min) + refresh token (7 days).

PITFALL 4: Not validating redirect URIs in OAuth
  Open redirect → attacker steals auth code.
  Fix: whitelist exact redirect URIs, validate state parameter.

PITFALL 5: Timing attacks on password comparison
  if password == stored_hash → early exit reveals length.
  Fix: use constant-time comparison (bcrypt does this internally).

PITFALL 6: No rate limiting on login
  Attacker brute-forces passwords at 1000 attempts/sec.
  Fix: rate limit to 5 attempts per minute per IP/account.

PITFALL 7: Leaking user existence
  "Email not found" vs "Wrong password" → attacker knows which emails exist.
  Fix: always return "Invalid credentials" for both cases.

PITFALL 8: Not using HTTPS
  Credentials sent in plain text → anyone on network can read them.
  Fix: HTTPS everywhere. HSTS header. No exceptions.
```