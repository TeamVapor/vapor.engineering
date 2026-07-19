# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Company site + infrastructure for **Vapor Engineering LLC** (the TeamVapor studio entity). This is a public repo and shared company space: never commit the live relay URL, the EIN, or anything from Eli's private records. Marketing copy needs both members' review before it ships.

Three independent pieces:

- **`index.html`** — the entire site: a static, zero-dependency page (project teasers, demo embed, feedback box). GitHub Pages serves it from `main`, so merging to `main` *is* the deploy — and Pages sometimes misses the merge hook, so if the live site lags, queue a build: `gh api -X POST repos/TeamVapor/vapor.engineering/pages/builds`. `CNAME` binds the custom domain (`vapor.engineering`) — don't delete or rename it. No build, lint, or test tooling exists anywhere in this repo.
- **`infra/`** — Terraform root #1: Route 53 DNS records (GitHub Pages apex/www + ImprovMX email) **plus the site-feedback stack** (below). The hosted zone is a **data source, not a resource** — Route 53 Domains owns it; Terraform only manages records inside it, so a destroy can never take down the zone or domain. Keep it that way.
- **`infra/jamrelay/`** — Terraform root #2 (separate state): the jam-parcel relay.

Two constants in `index.html` couple it to the outside world:
- `DEMO_URL` — the playable teaser, served from the public artifact-only repo **TeamVapor/vapor-teaser-web** (Pages). Source + pipeline docs live in the private vapor-teaser repo and vapor-drag-racing's README/CLAUDE.md. The website never changes when the demo updates — only if that URL does.
- `FEEDBACK_URL` — the feedback box endpoint (public by nature, fine to commit — unlike the jam relay URL).

`docs/` is business/planning material (LLC checklist, Steam page spec, release tracker), not code documentation. `docs/business-todo.md` is the source of truth for company-status facts and pending migrations.

## Terraform

The two roots are independent — `init`/`plan`/`apply` in each directory separately. State is local and gitignored. Both use AWS profile `terraform`, region `us-west-2`, currently against **Eli's personal AWS account** (migration to a company account is planned; the jamrelay README documents the cutover, which is a variable change + re-apply, not a state migration).

```bash
cd infra          # or infra/jamrelay
terraform init
terraform plan
terraform apply   # jamrelay: prints relay_url
```

## The site feedback stack (infra/feedback.tf + feedback.py)

The site's feedback box posts to the "scribe" Lambda (`vapor-site-feedback`, Function URL, CORS locked to the site origin — it will not work from localhost). Each submission is written to `s3://vapor-engineering-feedback/feedback/YYYY/MM/DD/` (**no lifecycle expiry — feedback keeps forever**) and published to the SNS topic `vapor-site-feedback`, which emails hello@vapor.engineering (ImprovMX fans out to both members). The SNS publish is deliberately best-effort: S3 is the source of truth, email is a convenience.

Caps are layered like jamrelay's — 8KB body, 4000-char message, 64-char name (Lambda) and reserved concurrency 1 (cost fuse). Editing `feedback.py` + `terraform apply` redeploys via source hash.

## The jam-parcel relay (jamrelay)

The 1.0 transport for `.jamparcel` exchange: one Lambda ("the postmaster") issuing presigned S3 URLs via an unauthenticated Function URL. No accounts, no database; the app only ever knows the Function URL.

- **`postmaster.py`** is the Lambda source. Editing it and re-running `terraform apply` redeploys (source hash). Three ops: `send` (quota check → presigned POST), `mailbox` (list prefix), `fetch` (presigned GET + DELETE).
- **The S3 bucket is deliberately NOT in Terraform** (`teamvapor-jam-drops`, created by hand). A relay bucket must have Block Public Access all ON and a 30-day lifecycle expiry — those two settings enforce the security and TTL guarantees, so verify them before pointing the Lambda at a new bucket.
- **Cost/abuse caps are layered by design** — 200MB max parcel (S3 presign condition), 1GB per mailbox (postmaster), reserved concurrency 2 (Lambda), 30-day expiry (lifecycle). Don't remove one layer because another seems to cover it.
- The unauthenticated URL is an **accepted alpha posture**, documented in `infra/jamrelay/README.md` — don't add auth unprompted, and don't commit the live URL (it lives in `terraform output relay_url` and app config only).
- Both `aws_lambda_permission` resources (`InvokeFunctionUrl` *and* `InvokeFunction`) are required for a public Function URL — removing either breaks it with a 403.
- **`parcelrelay.py` is a reference copy**, not the canonical client — that lives in the denoodler tree and syncs here via PR. Changes to the wire protocol must keep `postmaster.py`, `parcelrelay.py`, and the denoodler copy in agreement (e.g., the address alphabet regexes in both files).
