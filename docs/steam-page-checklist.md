# Steam store page checklist — spec'd before we need it

> Everything a "Coming Soon" Steam page requires, gathered so asset work can
> start whenever a game (DeNoodler first, most likely) approaches
> vertical-slice quality. Pixel specs below are from Steamworks docs as of
> mid-2026 — **re-verify against partner.steamgames.com/doc/store/assets
> when actually building**, Valve revises sizes occasionally.
>
> Why early: the page itself is the wishlist engine. Target is page-live
> **6+ months before launch**; Valve's page review takes ~2-5 business days,
> and the $100 app fee must be paid ~30 days before release capability.

## Gate: what must exist before the page can go live

- [ ] Steamworks partner account verified AS the LLC (blocks on EIN + bank)
- [ ] $100 app fee paid for the specific title
- [ ] Final title decided + collision-searched (store, trademark, domain)
- [ ] All required assets below
- [ ] Content survey / maturity questionnaire answered
- [ ] Page review passed (~2-5 business days)

## Required graphical assets (the capsule family)

| Asset | Size (px) | Where it shows | Notes |
|---|---|---|---|
| Header capsule | 460x215 | top of store page, recommendations | THE workhorse |
| Small capsule | 231x87 | search results, lists | must read at tiny size — logo legibility test |
| Main capsule | 616x353 | front-page features | |
| Vertical capsule | 374x448 | some front-page layouts | |
| Library capsule | 600x900 | player's library grid | poster-shaped |
| Library header | 460x215 | library detail view | |
| Library hero | 3840x1240 | library banner | no text in the art (logo overlays) |
| Library logo | 1280x720 PNG, transparent | overlays the hero | |
| Screenshots | 1920x1080, **minimum 5** | store page | actual gameplay; no marketing text in-frame |
| Page background | 1438x810 (optional) | behind the page | |

**Capsule art is the single highest-leverage marketing asset** (the
wishlist-click driver — worth hiring an artist even if everything else is
in-house). Rule from Valve: capsules must use game artwork + logo, readable
at small sizes, no review quotes or award logos.

## Trailer

- [ ] At least one video strongly recommended for wishlist conversion
      (pages without trailers convert measurably worse)
- Spec: 1920x1080, 30 or 60 fps, H.264 .mp4/.mov, high bitrate (Valve
  re-encodes; feed it the best source)
- **DeNoodler's 30-second version can be cheap and true:** the splash
  scene into real gameplay — drill highway scrolling, the coach nudging,
  a stats dashboard, a share card. The rock-show aesthetic IS the pitch.
- **Logistics Trail's version** (per its own docs): engine audio + weather
  + one event card — atmosphere carries it.

## Copy

- [ ] **Short description** — ~300 chars, shows at top of page. One breath:
      what it is, why it's different.
- [ ] **About This Game** — long description. Steam culture rewards honest
      + concrete over hype; bullets and section GIFs standard.
- [ ] **Tags** (up to 20, first ~5 weigh most) — for DeNoodler think: Music,
      Education, Rhythm, Simulation, Indie. Tags drive discovery queues;
      research comparable titles' tags before setting.
- [ ] Genre, developer ("Vapor Engineering" or DBA), publisher (same)
- [ ] System requirements (min/recommended)
- [ ] Content survey (violence/mature themes — trivial for both titles)
- [ ] Support contact (email on vapor.engineering domain — see biz todo)

## Launch-window extras (not needed for Coming Soon, queue anyway)

- [ ] Press kit page on vapor.engineering (screenshots, logo, fact sheet)
- [ ] Steam curator connect list / key distribution plan
- [ ] Launch discount decision (typical 10-15% opening)
- [ ] Regional pricing review (Valve suggests, we adjust)
- [ ] Demo? (Next Fest participation wants one — HUGE wishlist lever for
      niche titles; DeNoodler with a 3-quest demo slice is a natural fit)

## Title-specific notes

**DeNoodler:** screenshots want the flashy surfaces — splash, neon themes,
drill highway, stats dashboard, share cards. The share-card PNG export
(1600x900) is nearly capsule-shaped already; the art style is proven.
Licensing gate from music-as-code issue #10 (bundled samples, Strudel
ship-vs-fetch) must clear before page assets lock.

**Logistics Trail:** its repo already commits to page-at-vertical-slice
with capsule art investment (docs/business/checklist.md) — this checklist
supersedes/absorbs that one when the time comes.
