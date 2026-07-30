# vapor.engineering

Company site for **Vapor Engineering LLC** (Oregon, est. 2026) — the
TeamVapor studio entity. Currently a coming-soon page; grows when there's
something to show.

- `index.html` — the page (static, zero dependencies, GitHub Pages serves it)
- `docs/steam-page-checklist.md` — everything a Steam store page needs,
  speced ahead of time so the wishlist window opens early
- The company checklist and LLC records live in the private
  [vapor-ops](https://github.com/TeamVapor/vapor-ops) repo (moved
  2026-07-29)

## Deploy

GitHub Pages from `main`. Custom domain: `vapor.engineering` (Route 53) —
DNS records are Terraform in `infra/`; the setup history is in vapor-ops
`business-todo.md`.

Zone rules, same as everywhere in TeamVapor: this repo is shared company
space — PRs welcome from members, marketing copy needs both members' eyes
before it ships.
