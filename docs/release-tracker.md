# Release tracker — nothing → wishlistable → shipped

> The one rollup. Every item here is owned in detail by another doc — this
> file just counts them. Sources: `business-todo.md`,
> `steam-page-checklist.md` (this repo); `studio/docs/STEAM-RELEASE.md`,
> `STEAM-PAGE.md`, `ROADMAP.md`, `TESTING.md`, `PLAN.md` (music-as-code).
>
> Scoring: `[x]` = 1, `[~]` = 0.5, `[ ]` = 0. Bucket % = points / items,
> rounded to 5. The three numbers feed the bars on the front page
> (`index.html`) — update them together, no fancier pipeline until this
> gets annoying by hand.

## Bucket I — Company (65%)

The legal/financial spine. Detail: `business-todo.md`.

- [x] Oregon LLC filed + Articles approved (#260312492)
- [x] vapor.engineering registered, site live, HTTPS
- [x] EIN assigned
- [x] Business bank account (Mercury)
- [x] Operating agreement drafted (music-as-code PR #11)
- [ ] Operating agreement reviewed + signed (both members, in person)
- [~] Steamworks partner verification (submitted 2026-07-16, 2–7 business days)
- [ ] Bookkeeping, minimum viable (ledger → every company transaction)
- [x] Email on the domain (support@ / hello@ / catch-all via ImprovMX,
      delivery tested 2026-07-17)
- [ ] DBA decision (only when a store page gets built)

## Bucket II — Page-live / wishlistable (5%)

Everything between now and a Coming Soon page collecting wishlists.
Detail: `steam-page-checklist.md` + STEAM-PAGE.md. Target: live 6+ months
before ship.

- [ ] 1.0 fence decided (guitar-only vs guitar + jam v1 — ROADMAP.md;
      deadline is THIS list, per Eli's #13 review)
- [ ] Final title decided + collision-searched
- [~] Copy drafted (short description / About This Game candidates exist
      in STEAM-PAGE.md, unreviewed)
- [ ] Capsule art family (the one asset worth commissioning)
- [ ] Screenshots (min 5, real gameplay)
- [ ] Trailer (30s, splash → gameplay)
- [ ] Tags, genre, system requirements
- [ ] Licensing gate cleared (Strudel ship-vs-fetch line + sample-pack
      provenance — STEAM-RELEASE.md)
- [ ] App fee paid for the title (+30-day clock starts)
- [ ] Content survey + Valve page review passed

## Bucket III — Release (5%)

The ship gates between page-live and the launch button.
Detail: STEAM-RELEASE.md (M5) + TESTING.md (alpha).

- [ ] 1.0 content complete per the fence
- [~] Native audio engine — offline bake (PR #32 in progress)
- [ ] Polish queue landed (mixer, calibration UX, seamless drill looping,
      take mix, timing trust — PLAN.md cycle-4)
- [ ] Steamworks binding spike, incl. overlay vs GL/WebEngine surfaces
- [ ] Achievements mapped + icons drawn
- [ ] Career export/import (the no-Auto-Cloud stance)
- [ ] Offline honesty: page + app state exactly what works without internet
- [ ] Alpha program complete (7 loops × device matrix, 2 cold installs,
      ~20 crash-free tester hours)
- [ ] 30-day fee→release window elapsed
