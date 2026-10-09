# Monthly Financial Review — July 2026

> Automated review run: 3 August 2026, (Frank not present)
> Status: **BLOCKED — 4th CONSECUTIVE MONTH. Grade: F (process broken).**

---

## TL;DR

Fourth review in a row with zero bank statements uploaded. April, May, June, and now July are all missing. `transactions/` is still completely empty. There is nothing to parse, categorise, or grade — the review cannot happen because the input never arrives.

July was also supposed to be the month Aqua hit **£0** (the Q2/Q3 boundary target from the original plan). That cannot be confirmed. Life insurance — flagged as the single highest-priority item three reviews running — is, as far as this system can tell, still not active.

This is no longer a spending problem. It's a process that has failed 4/4 times since it was built. The prior report predicted this exact outcome and recommended redesigning the review around automatic bank import instead of manual upload. That recommendation stands, now with one more month of evidence behind it.

**Grade: F.** Same as May, June, and July's review of June. Not for the numbers (unknown) — for a 4-month streak of a "no exceptions" rule (Rule 11) being broken every single time it's been tested.

---

## What was supposed to happen this month

| Item | Plan | Actual |
|------|------|--------|
| Aqua balance (Jul target) | **£0 — CLEARED** | UNVERIFIED (last known ~£1,209, 25 Apr) |
| Aqua DD at £700 | Should have run May, Jun, Jul | UNVERIFIED |
| Klarna | £0 | UNVERIFIED |
| Capital One | £0 | UNVERIFIED |
| Life insurance | Active | **NOT DONE — ~97+ days overdue** |
| Nnenna allowance | £600 fixed, no top-ups | UNVERIFIED |
| Variable spending | Under £440 | UNVERIFIED |
| Emergency fund (HSBC) | ~£4,260 (plan estimate) | UNVERIFIED (last known £3,950, 25 Apr — 100 days stale) |
| Monthly review | Completed with statements | **BLOCKED — 4th consecutive time** |

---

## The accountability questions (unanswered — Frank not present)

1. Did you use Klarna or any BNPL this month? — **UNANSWERED**
2. Did you give Nnenna money outside the £600 standing order? — **UNANSWERED**
3. Did you lend money to anyone (Clinton, Nigeria, others)? — **UNANSWERED**
4. Any impulse purchases? — **UNANSWERED**
5. Did the Aqua DD go through at £700? — **UNANSWERED**
6. Current HSBC balance? — **UNANSWERED**
7. Current Aqua balance? — **UNANSWERED**
8. Any unexpected expenses? — **UNANSWERED**
9. Did you actually go to JD Gyms this month? — **UNANSWERED**
10. Any income besides salary? — **UNANSWERED**

---

## Report card

| Metric | Result |
|--------|--------|
| Total income vs out vs budget | **Cannot compute — no statements** |
| Variance by category | **Cannot compute** |
| Debt progress | **Unverified** — Aqua at 44.9% APR has now had 100 days of unconfirmed status |
| Emergency fund progress | **Unverified** — last known figure is 100 days old |
| Net worth change MoM | **Cannot compute** |
| Life insurance | ❌ **Still not active. ~97+ days overdue.** |
| **Overall grade** | **F — 4th consecutive blocked review** |

---

## Brutally honest read

Four for four. Every review since this system was built in April has hit the same wall: no statements. The July report said, almost word for word, that August was the decision point — if it blocked too, "the honest conclusion will be that the monthly-review system itself needs redesigning." That's now the honest conclusion.

Two things are true at once. First, this doesn't necessarily mean the plan has failed financially — it's entirely possible Aqua is at £0, HSBC is growing, and everything is fine. But nobody, including this system, can say that with evidence. A plan that can't be checked isn't being followed, it's being hoped for. Second, life insurance remains the one item that isn't a spreadsheet problem. Roughly 97 days without cover on a single income supporting a wife and a baby is the one line item on this whole list that carries real downside if ignored.

The manual-upload design has now failed identically four months running despite the same reminder appearing in the daily brief roughly 30+ times. Repeating "upload your statements" a fifth time is unlikely to produce a different result in September. The fix that actually has a chance of working is removing the manual step — either an Open Banking connector/read-only bank feed so the review pulls data itself, or shrinking the monthly review to a 5-minute WhatsApp-style Q&A (the 10 questions above) that doesn't depend on statement upload at all, with statements analysed only quarterly.

---

## Specific actions before the next review (deadline: 1 Sep 2026)

1. **Get life insurance now.** ~97 days overdue. comparethemarket.com, £250k, 25-year term, ~£15–25/month, ~20 minutes. This has been the top action item for three consecutive reports.
2. **Pick one: fix the upload, or fix the process.** Either commit to uploading Apr–Jul statements for Lloyds, HSBC, Revolut (and Aqua) before 1 September, or tell me to switch the review to the lightweight Q&A format so it stops failing on data collection.
3. **Confirm Aqua balance** — this is the load-bearing number for Rule 1 (no investing with 20%+ APR debt) and for whether the August LISA/Ebuka restart can proceed at all.
4. **Confirm HSBC balance** to replace the 100-day-old £3,950 estimate.
5. **August restart stays on hold.** Moneybox LISA (£334), Nnenna LISA (£334), Ebuka (£500) do not restart until Aqua is confirmed £0.

---

## Rule compliance check

| Rule | Status |
|------|--------|
| 6. Life insurance must stay active | ❌ **BROKEN — never activated, ~97+ days** |
| 8. No Klarna / BNPL / eBay | ⚠️ Unverifiable — no statements |
| 9. Nnenna £600 fixed, no top-ups | ⚠️ Unverifiable — no statements |
| 11. Monthly review on the 1st, no exceptions | ❌ **BROKEN — 4th consecutive month blocked** |

Rules 1–5, 7, 10 cannot be assessed without data.

---

## Next review

**1 September 2026.** If this is also blocked, that's five consecutive months and the manual-statement design should be retired in favour of an automatic feed or a no-statements-required Q&A format — the data at that point will speak for itself.

---

*Prior blocked reviews: [April](2026-05-review-april.md) · [May](2026-06-review-may.md) · [June + Q2](2026-07-review-june.md)*
