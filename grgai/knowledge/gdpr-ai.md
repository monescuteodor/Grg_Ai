# Using AI on personal data under GDPR

General reference, not legal advice. For a specific case, confirm with a qualified lawyer/DPO.

## Core principles (Art. 5) — apply them every time
- **Lawfulness, fairness, transparency** — have a legal basis and tell people.
- **Purpose limitation** — use data only for the stated purpose.
- **Data minimisation** — send the model only what the task needs, nothing more.
- **Accuracy**, **storage limitation** (keep only as long as needed), **integrity & confidentiality** (secure it), **accountability** (be able to prove compliance).

## Lawful basis (Art. 6) — pick ONE before processing
consent · contract · legal obligation · vital interests · public task · legitimate interests.
**Special-category data** (health, biometrics, etc. — Art. 9) needs an extra condition, usually **explicit consent** or a legal/medical basis. Medical and most sensitive HR data fall here → extra care.

## Roles: controller vs processor
- The firm deciding *why/how* = **controller**. The AI tool/vendor acting on its behalf = **processor**.
- Controller↔processor needs a **Data Processing Agreement (DPA, Art. 28)**.
- Any **sub-processors** (e.g. model providers) must be disclosed and bound by the same terms ("flow-down").

## International transfers (Art. 44+)
If personal data reaches a provider outside the EU/EEA (e.g. a US model API), you need a transfer mechanism: **adequacy decision** or **Standard Contractual Clauses (SCCs)** + a transfer risk assessment.
**Mitigation that avoids the problem:** redact/pseudonymise personal data *before* it is sent (so no identifiable data crosses the border), or run the model **on your own EU/on-prem infrastructure**.

## Data-subject rights (Art. 15–22) — respond within 1 month
access · rectification · **erasure ("right to be forgotten")** · restriction · **portability** · objection · rights around automated decisions.
Example (DSAR): a person emails "send me all data you hold on me and delete it." → verify identity → export their records → delete and confirm, within 30 days.

## DPIA (Art. 35)
Do a Data Protection Impact Assessment before **high-risk** processing (large-scale special-category data, systematic monitoring, new tech on sensitive data). Document risks and mitigations.

## Breaches (Art. 33–34)
Notify the supervisory authority within **72 hours** of becoming aware; notify affected people if high risk. Keep an internal breach log regardless.

## Practical playbook: "I want to use AI on documents with personal data"
1. **Minimise** — send only the relevant excerpt, not the whole file.
2. **Pseudonymise/redact first** — replace names, emails, national IDs (CNP), IBANs, card numbers with placeholders *before* the text leaves your device; map them back locally. (This is exactly how Grg AI private agents work.)
3. **Pick a lawful basis** and record it.
4. **Sign a DPA** with the vendor; check their sub-processors and where data is processed.
5. **Set retention** — don't keep prompts/outputs longer than needed; prefer zero-persistence for sensitive sessions.
6. **Log the decision**, not the personal data.

### Example: safe vs unsafe
- Unsafe: paste a full contract with 20 real names + CNPs into a public chatbot in the US. (transfer + no DPA + no minimisation)
- Safer: redact names/CNPs to [NAME_1]/[CNP_1] on-device, send only the clause you need, under a DPA, with EU processing or on-prem.

## What a client's compliance officer will ask you (be ready)
- Where is my data processed, and by whom (sub-processors)?
- Is there a DPA? What's the retention? Can you delete on request?
- How is data secured in transit and at rest?
- Do you train models on my data? (Correct answer for a privacy-first product: **no**.)
- What leaves our environment, and what stays local/redacted?

**Rule of thumb for a privacy-first AI product:** minimise → redact on-device → DPA + disclosed sub-processors → EU/on-prem option → never train on client data.
