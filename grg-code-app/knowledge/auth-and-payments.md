# Auth & Payments

## Auth options
- **Managed**: Clerk, Auth0, Supabase Auth, Firebase Auth — fastest, handle email/OAuth/MFA.
- **Roll your own**: sessions (cookie + server store) or JWT (access + refresh).

## JWT pattern
- Short-lived access token (15m) + long-lived refresh token (httpOnly, Secure cookie).
- Hash passwords with **bcrypt/argon2** (never plain, never MD5/SHA alone).
- Verify tokens on every protected route; scope by roles/permissions.
- OAuth2/OIDC for "Login with Google/GitHub".

## Security must-dos
- httpOnly + Secure + SameSite cookies. CSRF protection for cookie auth.
- Rate-limit login; lock/backoff on brute force. Email verification + password reset via one-time tokens.
- Never log secrets/tokens.

## Payments with Stripe
```js
// server: create a Checkout Session
const session = await stripe.checkout.sessions.create({
  mode: 'subscription', line_items:[{ price: PRICE_ID, quantity:1 }],
  success_url: url+'?ok=1', cancel_url: url });
// redirect user to session.url
```
- Use **Stripe Checkout** or Payment Element; never handle raw card numbers.
- Fulfill on **webhooks** (`checkout.session.completed`, `invoice.paid`), verify the signature, make handlers idempotent.
- Test mode keys + test cards first. Store customer/subscription ids, not card data.
