#!/usr/bin/env python3
# Idempotent patch: add the GrgPro section, an nHash pay button, and the nHash payment modal
# (+CSS/JS) to static/index.html. Aborts if already patched. Stripe markup is left untouched.
import sys, time, shutil

P = "static/index.html"
s = open(P, encoding="utf-8").read()
if "nhash-overlay" in s:
    print("ALREADY_PATCHED — nothing to do"); sys.exit(0)

shutil.copyfile(P, P + ".pre-nhash." + time.strftime("%Y%m%d-%H%M%S"))

NHASH_CSS = """
        /* ─── nHash payment ─── */
        .grgpro-banner { background: linear-gradient(135deg,rgba(139,92,246,.14),rgba(99,102,241,.05)); border: 1px solid var(--border); border-radius: 16px; padding: 16px 18px; margin-bottom: 20px; display: flex; align-items: center; gap: 15px; }
        .grgpro-banner .gp-logo { flex: none; }
        .grgpro-banner .gp-txt { flex: 1; min-width: 0; }
        .grgpro-banner .gp-title { font-size: 18px; font-weight: 700; color: var(--text); }
        .grgpro-banner .gp-sub { font-size: 12.5px; color: var(--text-mute); margin-top: 2px; }
        .grgpro-pays { display: flex; gap: 8px; flex-wrap: wrap; }
        .gp-pay-btn { padding: 9px 14px; border-radius: 10px; font-family: var(--font); font-size: 13px; font-weight: 600; cursor: pointer; border: none; display: inline-flex; align-items: center; gap: 7px; white-space: nowrap; transition: all .2s; }
        .gp-pay-card { background: linear-gradient(135deg,var(--accent),#8b5cf6); color: #fff; }
        .gp-pay-nhash { background: var(--bg-hover); color: var(--text); border: 1px solid var(--border); }
        .gp-pay-btn:hover { opacity: .9; transform: translateY(-1px); }
        @media (max-width: 600px) { .grgpro-banner { flex-direction: column; text-align: center; } }
        .nhash-btn { background: var(--bg-hover); color: var(--text); border: 1px solid var(--border); margin-top: 8px; display: flex; align-items: center; justify-content: center; gap: 8px; }
        .nhash-btn:hover { border-color: var(--accent); }
        .nhash-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.75); backdrop-filter: blur(10px); z-index: 9500; display: flex; align-items: center; justify-content: center; opacity: 0; pointer-events: none; transition: opacity .3s; }
        .nhash-overlay.visible { opacity: 1; pointer-events: auto; }
        .nhash-card { background: var(--bg-surface); border: 1px solid var(--border); border-radius: 20px; padding: 28px; max-width: 440px; width: 92%; position: relative; text-align: center; }
        .nhash-close { position: absolute; top: 14px; right: 16px; background: none; border: 1px solid var(--border); color: var(--text-mute); width: 30px; height: 30px; border-radius: 8px; cursor: pointer; }
        .nhash-title { font-size: 20px; font-weight: 700; color: var(--text); margin: 2px 0; display: flex; align-items: center; justify-content: center; gap: 9px; }
        .nhash-sub { font-size: 13px; color: var(--text-mute); margin-bottom: 16px; }
        .nhash-field { background: var(--bg); border: 1px solid var(--border); border-radius: 10px; padding: 10px 12px; margin-bottom: 10px; text-align: left; overflow: hidden; }
        .nhash-field .lab { font-size: 10px; text-transform: uppercase; letter-spacing: .08em; color: var(--text-mute); margin-bottom: 4px; }
        .nhash-field .val { font-family: ui-monospace,monospace; font-size: 13px; color: var(--text); word-break: break-all; }
        .nhash-field .amt { font-size: 19px; font-weight: 700; }
        .nhash-copy { float: right; background: var(--bg-hover); border: 1px solid var(--border); color: var(--text-mute); font-size: 11px; padding: 2px 8px; border-radius: 6px; cursor: pointer; }
        .nhash-copy:hover { color: var(--text); }
        .nhash-warn { font-size: 12px; color: #f59e0b; margin: 2px 0 14px; }
        .nhash-status { display: flex; align-items: center; justify-content: center; gap: 9px; font-size: 14px; font-weight: 600; color: var(--text); padding: 12px; border-radius: 10px; background: var(--bg-hover); }
        .nhash-spinner { width: 15px; height: 15px; border: 2px solid var(--border); border-top-color: var(--accent); border-radius: 50%; animation: nhspin .8s linear infinite; }
        @keyframes nhspin { to { transform: rotate(360deg); } }
        .nhash-status.paid { color: #22c55e; }
        .nhash-status.expired { color: #ef4444; }
"""

NHASH_BANNER = """        <!-- GrgPro banner (card + nHash) -->
        <div class="grgpro-banner">
            <div class="gp-logo"><svg viewBox="0 0 44 44" width="40" height="40" aria-hidden="true"><defs><linearGradient id="nhgA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#6366f1"/></linearGradient></defs><rect x="2" y="2" width="40" height="40" rx="12" fill="url(#nhgA)"/><text x="19" y="30" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="22" fill="#fff">n</text><g stroke="#fff" stroke-width="1.7" opacity=".55"><line x1="27" y1="13" x2="24.5" y2="31"/><line x1="31" y1="13" x2="28.5" y2="31"/></g></svg></div>
            <div class="gp-txt">
                <div class="gp-title">GrgPro</div>
                <div class="gp-sub">One membership, two ways to pay &mdash; card or nHash.</div>
            </div>
            <div class="grgpro-pays">
                <button class="gp-pay-btn gp-pay-card" onclick="startUpgrade();closePlansModal()">Pay with card</button>
                <button class="gp-pay-btn gp-pay-nhash" onclick="payWithNhash()">Pay with nHash</button>
            </div>
        </div>
"""

NHASH_PRO_BTN = """                <button class="plan-col-btn nhash-btn" onclick="payWithNhash()"><svg viewBox="0 0 40 40" width="16" height="16" aria-hidden="true"><defs><linearGradient id="nhgB" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#6366f1"/></linearGradient></defs><rect x="2" y="2" width="36" height="36" rx="10" fill="url(#nhgB)"/><text x="18" y="28" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="20" fill="#fff">n</text></svg>Pay with nHash</button>"""

NHASH_MODAL = """<!-- nHASH PAYMENT MODAL -->
<div class="nhash-overlay" id="nhash-overlay" onclick="if(event.target===this)closeNhashModal()">
    <div class="nhash-card">
        <button class="nhash-close" onclick="closeNhashModal()">&#10005;</button>
        <div class="nhash-title"><svg viewBox="0 0 40 40" width="24" height="24" aria-hidden="true"><defs><linearGradient id="nhgC" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#6366f1"/></linearGradient></defs><rect x="2" y="2" width="36" height="36" rx="10" fill="url(#nhgC)"/><text x="18" y="28" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="20" fill="#fff">n</text></svg>Pay with nHash</div>
        <div class="nhash-sub" id="nhash-plan-sub">Grg Pro</div>
        <div class="nhash-field"><button class="nhash-copy" onclick="nhashCopy('nhash-amount-val')">copy</button><div class="lab">Send exactly</div><div class="val amt" id="nhash-amount-val">&mdash;</div></div>
        <div class="nhash-warn">Send this <b>exact</b> amount &mdash; the final digits identify your order.</div>
        <div class="nhash-field"><button class="nhash-copy" onclick="nhashCopy('nhash-addr-val')">copy</button><div class="lab">To nHash address</div><div class="val" id="nhash-addr-val">&mdash;</div></div>
        <div class="nhash-status" id="nhash-status"><span class="nhash-spinner"></span><span id="nhash-status-text">Waiting for payment&hellip;</span></div>
        <div class="nhash-sub" style="margin-top:12px">Confirms on the next block. Keep this window open.</div>
    </div>
</div>

"""

NHASH_JS = """<script>
/* ─── nHash payment (Grg Pro) ─── */
var _nhashPoll = null, _nhashOrder = null;
async function payWithNhash(){
  if (typeof _currentUser === 'undefined' || !_currentUser){ try{closePlansModal();}catch(e){} try{openAuthModal(false);}catch(e){} return; }
  var interval = (typeof _billingInterval !== 'undefined' && _billingInterval) ? _billingInterval : 'monthly';
  try{
    var res = await fetch('/api/nhash/create-order', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({uid:_currentUser.uid, interval:interval})});
    var data = await res.json();
    if (data.error || !data.order_id){ alert('nHash payments are not available right now.'); return; }
    _nhashOrder = data.order_id;
    document.getElementById('nhash-amount-val').textContent = Number(data.amount_nhash).toFixed(8) + ' nHash';
    document.getElementById('nhash-addr-val').textContent = data.address;
    document.getElementById('nhash-plan-sub').textContent = 'Grg Pro \\u2014 ' + (interval==='yearly'?'yearly':'monthly');
    setNhashStatus('waiting','Waiting for payment\\u2026');
    try{ closePlansModal(); }catch(e){}
    document.getElementById('nhash-overlay').classList.add('visible');
    if(_nhashPoll) clearInterval(_nhashPoll);
    _nhashPoll = setInterval(pollNhash, 8000);
    pollNhash();
  }catch(e){ alert('Could not start nHash payment. Please try again.'); }
}
function setNhashStatus(kind, text){
  var el=document.getElementById('nhash-status'), t=document.getElementById('nhash-status-text');
  el.className='nhash-status'+(kind==='paid'?' paid':(kind==='expired'?' expired':''));
  var sp=el.querySelector('.nhash-spinner'); if(sp) sp.style.display=(kind==='waiting')?'inline-block':'none';
  t.textContent=text;
}
async function pollNhash(){
  if(!_nhashOrder) return;
  try{
    var res = await fetch('/api/nhash/check-order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({order_id:_nhashOrder})});
    var d = await res.json();
    if(d.status==='paid'){ clearInterval(_nhashPoll); _nhashPoll=null; setNhashStatus('paid','\\u2713 Payment received \\u2014 Grg Pro unlocked!'); try{loadSubscriptionStatus();}catch(e){} setTimeout(closeNhashModal, 2800); }
    else if(d.status==='expired'){ clearInterval(_nhashPoll); _nhashPoll=null; setNhashStatus('expired','Order expired \\u2014 please start again.'); }
  }catch(e){}
}
function closeNhashModal(){ var o=document.getElementById('nhash-overlay'); if(o) o.classList.remove('visible'); if(_nhashPoll){clearInterval(_nhashPoll);_nhashPoll=null;} _nhashOrder=null; }
function nhashCopy(id){ var t=document.getElementById(id).textContent.replace(' nHash','').trim(); if(navigator.clipboard) navigator.clipboard.writeText(t).then(function(){},function(){}); }
</script>
"""

def ins_before(text, anchor, block, name):
    i = text.find(anchor)
    if i < 0:
        raise SystemExit("ANCHOR_NOT_FOUND: " + name)
    return text[:i] + block + text[i:]

# 1) CSS inside <style>, before the plans-overlay rule
s = ins_before(s, "        .plans-overlay {", NHASH_CSS, "css")
# 2) GrgPro banner above the plans grid
s = ins_before(s, '        <div class="plans-grid">', NHASH_BANNER, "banner")
# 3) nHash button right after the Stripe upgrade button
i = s.find('id="plans-upgrade-btn"')
if i < 0:
    raise SystemExit("ANCHOR_NOT_FOUND: pro-button")
j = s.find("</button>", i)
if j < 0:
    raise SystemExit("no </button> after pro-button")
j += len("</button>")
s = s[:j] + "\n" + NHASH_PRO_BTN + s[j:]
# 4) payment modal before the upgrade popup
s = ins_before(s, "<!-- UPGRADE POPUP -->", NHASH_MODAL, "modal")
# 5) JS after the LAST real </script> (the file has </body> inside JS strings, so anchor on the
#    final script close, which is unambiguous — script strings escape </script> as <\/script>).
k = s.rfind("</script>")
if k < 0:
    raise SystemExit("ANCHOR_NOT_FOUND: last </script>")
k += len("</script>")
s = s[:k] + "\n" + NHASH_JS + s[k:]

open(P, "w", encoding="utf-8").write(s)
print("PATCHED_OK new_len", len(s))
