# Privacy & security engineering (for developers)

How to build apps that handle personal/sensitive data safely and GDPR-compliantly. Practical, code-level.

## Privacy by design (defaults)
- **Data minimisation**: collect and store only what the feature truly needs. Don't log everything "just in case".
- **Purpose limitation & retention**: define why each field exists and when it's deleted; implement auto-deletion (TTL / scheduled purge).
- **Least privilege**: every service/user gets the minimum access. Scope DB rules per-user (row-level), not "any authenticated user can read all".

## Handle PII correctly
- **Pseudonymise / redact before third parties**: replace names, emails, national IDs, IBANs, card numbers, secrets with placeholders before sending to an external API; keep the map locally and restore after. (This is exactly the Grg AI private-agent pattern.)
  Example (JS): `text.replace(/[\w.+-]+@[\w.-]+\.\w{2,}/g, m => placeholder('EMAIL', m))`
- **Never put PII in URLs / query strings / logs / analytics.** Log an id, not the data.
- **Encrypt**: TLS in transit (always); encrypt sensitive fields at rest; use a KMS/managed keys, not hardcoded keys.

## Secrets management
- Secrets in **environment variables / a vault**, never in source or the client bundle. Add `.env` to `.gitignore`.
- Rotate keys; scope them; use least-privilege service accounts.
- Client-side (web) can't hold real secrets — call your backend; the backend holds keys.

## Access control & storage rules (example pattern)
```
// Firestore-style: a user can only touch their own doc
match /users/{uid} {
  allow read, write: if request.auth != null && request.auth.uid == uid;
}
```
Enforce authorization on the **server**, not just the UI. Validate every input (treat all client input as hostile).

## OWASP top risks → fixes (quick)
- **Injection (SQL/NoSQL)** → parameterised queries / ORM; never string-concat user input.
- **Broken auth** → strong session/JWT handling, short expiry, secure cookies (HttpOnly, SameSite), MFA where it matters.
- **XSS** → escape/encode output, Content-Security-Policy, framework auto-escaping; never `innerHTML` with user data.
- **Broken access control** → server-side authz checks on every endpoint and record.
- **Sensitive data exposure** → encryption + minimisation + no secrets in logs.
- **SSRF / unsafe fetch** → allowlist outbound URLs; don't fetch arbitrary user-supplied URLs.

## GDPR features to actually build
- **Consent** capture + record (what, when, version).
- **Data-subject rights endpoints**: export my data (portability), delete my data (erasure) — build these early.
- **Audit log** of access to sensitive data (who read what, when) — without storing the sensitive data itself.
- **DPA & sub-processor list** if you use third-party services (where does data go?).

## Shipping checklist
no secrets in repo · TLS everywhere · PII minimised & not logged · per-user access rules enforced server-side · input validated · dependencies updated (no known CVEs) · export + delete implemented · retention/auto-purge set · backups encrypted.

## Output style
Give concrete, runnable code and config for the stack in use, call out the security/privacy trade-off, and flag anything that needs a security review or a DPO/legal check.
