# Vapor Engineering LLC — the boring checklist

> Status as of 2026-07-16. The unglamorous work that makes the fun work
> shippable. Owner: Eli (Jack reviews the ones marked both).

## Done ✅

- [x] Oregon LLC filed (2026-07-16, registry #260312492, $100)
- [x] vapor.engineering registered (Route 53, $71/yr)
- [x] Operating-agreement DRAFT written (music-as-code PR #11 — nothing
      final until reviewed, printed, signed in person — both members)
- [x] Fronted-expense ledger started ($171 so far, in the draft agreement)

## Waiting ⏳

- [x] ~~LLC filing acknowledgment~~ — **Articles APPROVED + e-filed
      2026-07-16, same day.** The LLC is fully official; EIN unblocked.
- [x] ~~Domain registration~~ — registered 2026-07-16; site live with
      HTTPS enforced at https://vapor.engineering same day.
- [x] ~~Jack reads PR #11~~ — merged, then SIGNED (see item 8).

## Next, in dependency order

1. [x] **EIN** — assigned 2026-07-16, same day as the Articles. Letter PDF
       in Eli's records (number deliberately not in this public repo). — Eli
2. [x] **Business bank account** — Mercury APPROVED 2026-07-16 (same
       day!). Steam pays here; migrate reimbursements + renewals here. — Eli
3. [x] **Bookkeeping, minimum viable** — DONE 2026-07-17:
       music-as-code `business/bookkeeping.xlsx` (fronted-expense ledger
       seeded with the $271 + Mercury transaction log + Read Me).
       Discipline: add a row per transaction, commit after updates.
       Upgrade to real software when there's revenue. — Eli
4. [x] **Email on the domain** — DONE 2026-07-17: ImprovMX free tier,
       MX + SPF as Terraform in `infra/dns.tf`. support@, hello@, and a
       catch-all forward to both members; test delivery confirmed.
       Replying AS support@ (send-as via ImprovMX SMTP) not set up —
       revisit if support volume ever warrants it (Zoho/Workspace is the
       upgrade path). — Eli
5. [x] **DNS + site live** — done 2026-07-16: records managed as Terraform
       in `infra/` (imported, plan clean), site serving at
       vapor.engineering; HTTPS enforcement flips when GitHub's cert
       finishes provisioning. Longer-term: the domain + zone live on Eli's
       PERSONAL AWS account — migrate to a company AWS account when the
       LLC has a bank account to pay for it. — Eli
6. [~] **Steamworks onboarding** — SUBMITTED 2026-07-16 (same day as
       everything else): partner account created as the LLC ($100 fee,
       recoupable/first-app credit), tax interview done as single-member
       LLC, identity verification pending 2-7 business days. Retake the
       tax interview as a partnership when Jack formally joins. — Eli
7. [ ] **DBA decisions** — if a game ships under "Vapor Studios" or
       "TeamVapor" branding, file the assumed business name (~$50, Oregon
       online). Decide when store pages get built, not before. — both
8. [x] **Signing day** — DONE 2026-07-17: both members signed two paper
       originals (one each); blanks filled in ink and initialed — Big
       Decision spending threshold **$1,000**, drift window **24 months**.
       Scan filed at music-as-code
       `business/signed/operating-agreement-SIGNED-2026-07-17.pdf`. — both

## Recurring (calendar these now)

| What | When | Amount |
|---|---|---|
| Oregon annual report | anniversary of 2026-07-16, yearly | $100 |
| vapor.engineering renewal | yearly (auto-renew ON in Route 53) | $71 |
| Registered-agent address check | if Eli moves, update SoS within 30 days | free |

## Explicitly NOT yet (revisit triggers)

- **Trademark registration** — revisit when a title has a locked name and
  a store page (USPTO ~$250-350/class; premature before that).
- **Business insurance** — revisit at first revenue or first contractor.
- **FinCEN BOI report** — domestic LLCs were exempted from beneficial-
  ownership reporting by the 2025 interim rule; VERIFY current rule at
  fincen.gov when the EIN arrives (rules moved several times).
- **Accountant** — revisit at first revenue year-end, or when Jack joins
  (partnership return year one is worth professional eyes).
- **S-corp election** — a tax optimization that only makes sense at real
  profit levels; ignore until an accountant raises it.
