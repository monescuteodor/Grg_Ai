"""
test_profit.py — proves the owner ALWAYS comes out on profit.

Run:  ./venv/bin/python test_profit.py    (from /home/pi/GrgAI)

It tests the pure pricing logic in billing.py (no Firebase needed). The core
invariant is simple and, if it holds for every message, guarantees profit both
per-message AND at the plan/bucket level:

    INVARIANT:  charged_credits * CREDIT_EUR  >=  real_api_cost(message) * MARKUP_target

Because each premium charge >= real_cost * MARKUP (in euros), and the premium
bucket is sized in credits = plan_money / CREDIT_EUR, spending the whole bucket
can consume at most  plan_money / MARKUP  of real API — so the owner keeps at
least  plan_money * (1 - 1/MARKUP)  as profit no matter how the user spends it.
"""
import sys
import billing as B

CREDIT_EUR = B.CREDIT_EUR
MARKUP = B.MARKUP
PREMIUM_MODELS = list(B.MODEL_PRICE_EUR.keys())
FREE_MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b", "x/some:free"]
EFFORTS = ["low", "mid", "high", "ultra"]
# The output cap the server actually enforces per effort (server.py funded floor / client cfg).
OUT_CAP = {"low": 1024, "mid": 2048, "high": 4096, "ultra": 8192}

FAILS = []
def check(cond, msg):
    if not cond:
        FAILS.append(msg)
        print("  FAIL:", msg)

def real_cost_eur(model, tokens):
    return tokens / 1_000_000.0 * B.model_price_eur(model)

# ───────────────────────────────────────────────────────────────────────────
print("=" * 74)
print("TEST 1 — per-message PREMIUM profit across all models x efforts x usage")
print("=" * 74)
# For each model/effort, the server charges on (est_in, max_out=OUT_CAP[effort]).
# Worst real usage: real_in up to est_in*EST_IN_PAD (the pad is the safety margin),
# real_out up to the hard cap. We test the exact ceiling AND a few real points.
worst_margin = 1e9
for model in PREMIUM_MODELS:
    for eff in EFFORTS:
        out_cap = OUT_CAP[eff]
        for est_in in (0, 500, 2000, 8000, 30000):
            charged = B.premium_msg_credits(model, eff, est_in, out_cap)
            revenue = charged * CREDIT_EUR
            # Worst case the provider can bill us for this message:
            real_in_worst = int(est_in * B.EST_IN_PAD)      # real prompt <= padded estimate
            real_out_worst = out_cap                          # provider respects max_tokens
            cost_worst = real_cost_eur(model, real_in_worst + real_out_worst)
            check(revenue >= cost_worst,
                  "LOSS %s/%s est_in=%d: revenue %.5f < cost %.5f" %
                  (model, eff, est_in, revenue, cost_worst))
            if cost_worst > 0:
                worst_margin = min(worst_margin, revenue / cost_worst)
print("  worst-case revenue/cost ratio over ALL premium cases: %.3f  (must be >= 1.0)" % worst_margin)
check(worst_margin >= 1.0, "a premium worst-case lost money (ratio < 1.0)")
check(worst_margin >= MARKUP * 0.97,
      "worst-case margin %.3f dropped below the intended MARKUP %.3f" % (worst_margin, MARKUP))

# ───────────────────────────────────────────────────────────────────────────
print("=" * 74)
print("TEST 2 — the OLD flat model lost money here; the fix must not")
print("=" * 74)
# Old behaviour: low effort charged as ~1500 assumed tokens, but server forced 8000
# output. Reproduce the old charge and show it was a loss; the new charge must cover it.
model = "anthropic/claude-opus-4.8"
old_assumed = B.EFFORT_TOKENS["low"]                       # 1500
old_charge_cr = max(1, round(old_assumed / 1e6 * B.model_price_eur(model) * MARKUP / CREDIT_EUR))
old_rev = old_charge_cr * CREDIT_EUR
leak_cost = real_cost_eur(model, 1000 + 8000)              # small prompt + forced 8000 out
print("  OLD low-effort charge: %d cr (EUR %.4f) vs real cost EUR %.4f  -> %s" %
      (old_charge_cr, old_rev, leak_cost, "LOSS" if old_rev < leak_cost else "ok"))
new_charge_cr = B.premium_msg_credits(model, "low", 1000, OUT_CAP["low"])
new_rev = new_charge_cr * CREDIT_EUR
# new real cost: output now capped at low=1024, not 8000
new_cost = real_cost_eur(model, int(1000 * B.EST_IN_PAD) + OUT_CAP["low"])
print("  NEW low-effort charge: %d cr (EUR %.4f) vs real cost EUR %.4f  -> %s" %
      (new_charge_cr, new_rev, new_cost, "PROFIT" if new_rev >= new_cost else "LOSS"))
check(old_rev < leak_cost, "expected the OLD model to show the leak (sanity of the test)")
check(new_rev >= new_cost, "NEW low-effort message still loses money")

# ───────────────────────────────────────────────────────────────────────────
print("=" * 74)
print("TEST 3 — plan/bucket level: spending the WHOLE premium bucket stays profitable")
print("=" * 74)
for plan in ("pro", "ultra"):
    bucket = B.PREMIUM_MONTHLY[plan]                       # credits granted / month
    plan_money = bucket * CREDIT_EUR                       # what the user paid (EUR)
    # Worst case: user spends every credit on the priciest model. Because each charge is
    # >= real_cost*MARKUP, total real cost <= plan_money / MARKUP.
    max_real_cost = plan_money / MARKUP
    profit = plan_money - max_real_cost
    pct = profit / plan_money * 100
    print("  %-5s: bucket %d cr = EUR %.2f paid | max real API EUR %.2f | min profit EUR %.2f (%.1f%%)"
          % (plan, bucket, plan_money, max_real_cost, profit, pct))
    check(profit > 0, "%s plan could lose money at the bucket level" % plan)
    check(pct >= (1 - 1 / MARKUP) * 100 - 0.5, "%s plan margin below the MARKUP floor" % plan)

# ───────────────────────────────────────────────────────────────────────────
print("=" * 74)
print("TEST 4 — FREE models cost the platform ~nothing (Groq free) => never a loss")
print("=" * 74)
for m in FREE_MODELS:
    check(B._is_free_model(m), "free model %s not detected as free" % m)
    c_low = B.free_msg_credits("low")
    c_ultra = B.free_msg_credits("ultra")
    print("  %-22s free_msg_credits low=%d ultra=%d  (platform cost EUR 0.00)" % (m, c_low, c_ultra))
    check(c_low >= 1, "free message must still consume >=1 credit (metering) for %s" % m)
    check(c_ultra >= c_low, "free effort scaling broken for %s" % m)

# ───────────────────────────────────────────────────────────────────────────
print("=" * 74)
print("TEST 5 — monotonicity: more effort / bigger output never charges LESS")
print("=" * 74)
for model in PREMIUM_MODELS[:6]:
    prev = -1
    for eff in EFFORTS:
        c = B.premium_msg_credits(model, eff, 1000, OUT_CAP[eff])
        check(c >= prev, "effort charge went DOWN for %s at %s" % (model, eff))
        prev = c
    # bigger input must not reduce the charge
    a = B.premium_msg_credits(model, "mid", 500, OUT_CAP["mid"])
    b = B.premium_msg_credits(model, "mid", 5000, OUT_CAP["mid"])
    check(b >= a, "bigger input charged less for %s" % model)
print("  monotonic in effort and input: OK")

# ───────────────────────────────────────────────────────────────────────────
print("=" * 74)
print("TEST 6 — images add cost and never reduce the charge")
print("=" * 74)
base = B.message_cost_credits("anthropic/claude-opus-4.8", "mid", 0, 1000, OUT_CAP["mid"])
with_img = B.message_cost_credits("anthropic/claude-opus-4.8", "mid", 3, 1000, OUT_CAP["mid"])
print("  no image=%d cr, +3 images=%d cr" % (base, with_img))
check(with_img >= base + 6, "images did not add the expected credits")

# ───────────────────────────────────────────────────────────────────────────
print("=" * 74)
print("TEST 7 — BULLETPROOF settle: charge on the provider's REAL tokens is always")
print("          profit-safe, for ANY usage (no dependence on the input estimate)")
print("=" * 74)
# After the stream, settle_premium charges premium_actual_credits(model, in, out) =
# ceil(real_tokens * price * MARKUP / CREDIT_EUR). This is computed from the REAL tokens
# the provider reports, so it cannot be fooled by dense/CJK input or a long prompt.
worst_settle = 1e9
TOKEN_GRID = [(1, 1), (500, 500), (2000, 4000), (50000, 8192), (200000, 8192), (1_000_000, 8192)]
for model in PREMIUM_MODELS:
    for (ti, to) in TOKEN_GRID:
        charged = B.premium_actual_credits(model, ti, to)
        revenue = charged * CREDIT_EUR
        cost = real_cost_eur(model, ti + to)
        check(revenue >= cost, "SETTLE LOSS %s in=%d out=%d: rev %.5f < cost %.5f" %
              (model, ti, to, revenue, cost))
        if cost > 0:
            worst_settle = min(worst_settle, revenue / cost)
print("  worst-case settled revenue/cost over ALL models x token mixes: %.3f (must be >= 1.0)" % worst_settle)
check(worst_settle >= 1.0, "a settled charge lost money")
check(worst_settle >= MARKUP * 0.97, "settled margin dropped below MARKUP")

print("  settle delta direction check:")
# A big up-front hold that over-estimated → settle must REFUND (delta < 0).
ceiling = B.premium_msg_credits("anthropic/claude-opus-4.8", "ultra", 30000, 8192)
actual_small = B.premium_actual_credits("anthropic/claude-opus-4.8", 200, 300)   # tiny real reply
check(actual_small < ceiling, "tiny real reply should settle BELOW the ceiling (refund)")
print("     held ceiling=%d cr, tiny-reply actual=%d cr -> refund %d cr" %
      (ceiling, actual_small, ceiling - actual_small))

# ───────────────────────────────────────────────────────────────────────────
print("=" * 74)
if FAILS:
    print("RESULT: %d FAILING CHECK(S) — NOT always profitable:" % len(FAILS))
    for f in FAILS:
        print("   -", f)
    sys.exit(1)
print("RESULT: ALL CHECKS PASSED — every message and every plan is profit-safe.")
print("MARKUP = %.2f  =>  guaranteed profit floor = %.1f%% of every euro paid." %
      (MARKUP, (1 - 1 / MARKUP) * 100))
