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
- [ ] Jack reads PR #11 (operating agreement) — his pace, no rush. (He
      cleared #8/#12 and shipped his own STEAM-RELEASE.md absorbing #10.)

## Next, in dependency order

1. [x] **EIN** — assigned 2026-07-16, same day as the Articles. Letter PDF
       in Eli's records (number deliberately not in this public repo). — Eli
2. [ ] **Business bank account** — bring Articles + EIN letter + operating
       agreement (even the draft works for most banks). Steam pays here;
       reimbursements and renewals migrate here. — Eli
3. [ ] **Bookkeeping, minimum viable** — a spreadsheet is fine at this
       scale: the fronted-expense ledger + every company transaction.
       Upgrade to real software when there's revenue. — Eli
4. [ ] **Email on the domain** — support@ and hello@ vapor.engineering
       (Steam page needs a support contact; store fronts shouldn't use
       personal gmail). Cheapest paths: email forwarding via
       ImprovMX/Cloudflare (free) or Zoho Mail (free tier) before paying
       for Google Workspace. — Eli
5. [x] **DNS + site live** — done 2026-07-16: records managed as Terraform
       in `infra/` (imported, plan clean), site serving at
       vapor.engineering; HTTPS enforcement flips when GitHub's cert
       finishes provisioning. Longer-term: the domain + zone live on Eli's
       PERSONAL AWS account — migrate to a company AWS account when the
       LLC has a bank account to pay for it. — Eli
6. [ ] **Steamworks onboarding** — partner.steamgames.com as the LLC
       (legal name, EIN, bank). Verification takes days-weeks; start as
       soon as 1+2 are done even though no game is ready — the clock is
       the point. $100/app fee comes later, per title. — both (Jack's
       game likely ships first)
7. [ ] **DBA decisions** — if a game ships under "Vapor Studios" or
       "TeamVapor" branding, file the assumed business name (~$50, Oregon
       online). Decide when store pages get built, not before. — both
8. [ ] **Signing day** — operating agreement: discuss, edit, print two,
       sign (see PR #11). Calendar it once Jack's read the draft. — both

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
