# Jam-parcel relay (the postmaster)

The 1.0 transport for `.jamparcel` exchange (music-as-code #24/#39, Eli's
workstream): a dumb S3 relay with presigned URLs. No accounts, no database,
media's home is each player's disk, the bucket is a mailbox with a 30-day
TTL. The app talks to ONE Lambda ("the postmaster") through its Function
URL and never holds AWS credentials.

## Pieces

- `postmaster.py` — the Lambda. Three ops: `send` (quota check → presigned
  POST with an S3-enforced size cap), `mailbox` (list your prefix),
  `fetch` (presigned GET + DELETE so mailboxes drain when read).
- `main.tf` — IAM role (scoped to `mail/*` in the one bucket), the Lambda
  (128MB, 10s, reserved concurrency 2 as the cost fuse), the Function URL.
- The **bucket is managed by hand**, not Terraform (the spike created it).
  A relay bucket must have: Block Public Access = all four ON, a lifecycle
  rule expiring objects at 30 days, and nothing else. Currently
  `teamvapor-jam-drops` (us-west-2, Eli's personal account).

## Deploy / iterate

```bash
cd infra/jamrelay
terraform init
terraform apply          # prints relay_url
```

Changing `postmaster.py` and re-applying redeploys the Lambda (source hash).
The app-side client (`parcelrelay.py` — reference copy here; it graduates
into the denoodler tree via PR) reads the relay URL from config — that URL
is the entire coupling surface. **Don't commit the live URL to this public
repo**: it's unauthenticated by design, no need to advertise it. It lives
in `terraform output relay_url` and in app config / private channels.

## Cost profile

Idle: $0. Active: S3 pennies/GB (transient, 30-day max), Lambda free tier
covers friend-scale traffic forever. The failure-mode caps: 200MB max
parcel (S3-enforced), 1GB per mailbox (postmaster-enforced), concurrency 2
(Lambda-enforced), 30-day expiry (lifecycle-enforced).

## Abuse posture (accepted for alpha)

The Function URL is unauthenticated by design (no accounts). Anyone who
learns the URL + an address could fill that mailbox up to quota with junk;
the caps bound the damage to ~nothing (transient pennies). If it ever
matters: addresses become keypairs and parcels get signed (v-next in the
JAM-ROOMS design), or the URL moves behind a shared app token. Deliberately
NOT built today.

## Moving to the company AWS account (when Eli sets it up)

The design makes cutover a config change, not a migration:

1. **Create the company account** — fresh standalone AWS account: company
   email (aws@vapor.engineering via the catch-all), Mercury card on
   billing, MFA on root, then create an `admin` IAM user (or better, IAM
   Identity Center) and a `terraform` CLI profile for it. Root stays in
   the safe. (Why a whole account, not an IAM user in the personal one:
   accounts are AWS's only hard boundary — clean billing for the books,
   transferable if the company changes shape, and blast-radius isolation
   both directions.)
2. **Create the relay bucket there** (any name, e.g. `vapor-jam-relay`):
   Block Public Access ON, 30-day lifecycle rule on the whole bucket.
3. **Re-apply this Terraform** at the new home:
   `terraform apply -var profile=<company-profile> -var bucket_name=<new-bucket>`
   (fresh state in the new account — or just keep two workspaces during
   the overlap).
4. **Flip the app config** to the new `relay_url`. Old bucket drains
   itself within 30 days by lifecycle; delete it after.
5. While at it, migrate the Route 53 zone per `docs/business-todo.md`
   item 5 — same "when the company account exists" trigger.

Until then, dev rides Eli's personal account under the `Project=jamrelay`
tag, so the cost line is at least visible for the fronted-expense ledger
(realistically $0.00-and-some-dust per month).
