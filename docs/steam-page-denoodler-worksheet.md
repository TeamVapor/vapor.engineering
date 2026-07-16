# DeNoodler — Steam page production worksheet

> Companion to `steam-page-checklist.md`: that doc is WHAT Steam requires;
> this one is the work, in order, with draft material to react to.
> DeNoodler is Jack's game — everything here is proposal-grade until he
> edits it. Final copy ships with both members' sign-off.

## The tasklist, in production order

### Phase 1 — words (can start NOW, no footage needed)

- [ ] Positioning sentence: who is it for, what does it replace? (Draft:
      "practice that plays like a campaign" — the anti-Yousician: your
      real instrument, real telemetry, a coach with attitude, no
      subscription.)
- [ ] Short description (~300 chars) — candidates below, pick/blend
- [ ] Feature bullets (the "About" skeleton) — draft below
- [ ] Tag research: pull the tag sets of Rocksmith+, Yousician, Melodics,
      Trombone Champ, Rhythm Doctor; pick our 20, weight the first 5
- [ ] Name check: "DeNoodler" store search + trademark scan (already
      believed clean vs riffscribe; do the formal pass)
- [ ] Content survey answers (trivial: no violence; note user-generated
      content via packs)

### Phase 2 — footage (starts when there's something concrete to show)

- [ ] GIF shot list (see below) — capture at 616px-wide-friendly ratios,
      under ~8 MB each, loop cleanly, one idea per GIF
- [ ] 5+ screenshots at 1920x1080: real gameplay, no marketing text
- [ ] 30-second trailer (concept in checklist: splash → highway → coach
      nudge → stats card). Cut a 15s variant for socials while at it.
- [ ] Capsule art — the one thing worth commissioning. Brief an artist
      with: the splash's neon dive-bar look, title legible at 231x87.

### Phase 3 — technical facts

- [ ] System requirements (draft below — verify on the low-end machine
      during the alpha program's device matrix pass)
- [ ] Offline behavior statement (page must be honest: what works without
      internet — ties to the Strudel ship-vs-fetch licensing decision,
      music-as-code issue #10)
- [ ] Input-device requirement wording (an instrument IS a requirement —
      unusual for Steam, must be impossible to miss on the page)

### Phase 4 — Steam integration (code, Jack's zone, sized for M5)

- [ ] **Achievements** — the app already HAS an achievements engine and
      db table; the task is mapping them to Steamworks stats/achievements
      and drawing icons (256x256, locked+unlocked variants). Starter set
      below.
- [ ] **Cloud saves** — career.db is a single SQLite file in
      %LOCALAPPDATA%\DeNoodler. Steam Auto-Cloud can sync it BUT sqlite +
      sync = corruption risk if synced while open; needs a
      close-clean-then-sync pattern or WAL-checkpoint on exit. Decide:
      auto-cloud with care, or explicit export/import, or skip at 1.0.
- [ ] **Overlay check** — Steam overlay injects into GL/D3D; Qt +
      QOpenGLWindow highway + WebEngine is an unusual stack. Test early;
      overlay breakage is a common review complaint. (Fallback: ship with
      overlay expectations documented.)
- [ ] **Workshop (later, matches M4 stage 3)** — data packs are already
      folder-shaped; Workshop is the natural distribution for them. Not
      1.0.
- [ ] Python Steamworks binding choice (SteamworksPy or a thin ctypes
      shim over steam_api64.dll; PyInstaller onedir already accommodates
      bundled DLLs)
- [ ] Launch options / DRM decision (DRM-free binary is fine and
      Steam-normal for this genre)

## Draft material (react, don't accept)

### Short description candidates

1. "Your guitar practice, as a campaign. Plug in, pick a quest, and play —
   DeNoodler hears every note, grades your pocket, and coaches you like it
   means it. Real telemetry, a riff vault that never forgets, and a boss
   fight at the end of every arc."
2. "A practice game that listens. Plug your real guitar (or drums) in:
   quests with actual music theory inside, a coach that reads your timing
   and intonation, and a vault that records everything so nothing you play
   is lost."
3. "Stop practicing scales. Start clearing quests. DeNoodler turns real-
   instrument practice into an RPG campaign — live pitch tracking, honest
   grading, neon stages, and a coach with attitude."

### Feature bullets (About This Game skeleton)

- **A campaign, not a chore list** — five arcs from "know your modes" to
  "compose a game theme," each with boss fights you actually record
- **It hears you** — live pitch + timing telemetry on your real
  instrument: in-scale %, chord-target hits, cents-level intonation,
  pocket stats
- **A coach with attitude** — from "baby me" to "let me have it";
  optional AI deep-coach with your own key, never required
- **Nothing you play is lost** — the silence-gated riff vault records
  every doodle, auto-filed
- **Rocksmith-style drill highway** — scrolling fingerings, vsync-locked
- **Your look** — themes from plain studio to neon nights; stats
  dashboards and shareable session cards
- **Moddable from day one** — quests, drills, tracks, and themes are
  plain-file data packs
- (each bullet gets a GIF — see shot list)

### GIF shot list (one idea per GIF, ~6s loops)

1. Drill highway scrolling at speed — hits blooming on the line
2. Capture page: gate opens on a riff, clip files itself into the vault
3. Coach nudge appearing mid-play (pick a funny-but-true one)
4. Stats dashboard assembling / share card export
5. Theme swap: plain studio → neon nights live
6. Quest tree → dossier → backing track launch flow
7. (drums, if PR-era footage exists: TD-27 clip capture with pad names)

### System requirements draft (verify in alpha device matrix)

|  | Minimum | Recommended |
|---|---|---|
| OS | Windows 10 64-bit | Windows 11 64-bit |
| CPU | dual-core from the last decade (audio DSP is numpy, cheap) | quad-core |
| RAM | 4 GB (WebEngine is the hog) | 8 GB |
| GPU | anything; GL splash/highway auto-fall back to raster | any dGPU/iGPU with GL 2.1+ |
| Disk | ~2 GB (Chromium runtime + ONNX model) | SSD |
| **Audio** | **REQUIRED: any audio input** — USB interface, mic, or e-kit | 4-ch ASIO interface (Pod Go-class) for DI + tone |
| Internet | first-run downloads; backing-track engine per licensing decision | broadband |

### Achievements starter set (engine already exists in-app)

- One per arc boss (5 guitar + 5 drums when the drum arcs land)
- "First Blood" — first riff filed in the vault
- "The Read" — first mode dossier read unlocked
- "Planted" — pass a timing quest within the pocket window
- "Marksman" — call-and-hit targeting boss
- "Curator" — install a data pack / "Author" — make one (Workshop era)
- Streak achievements (7/30-day practice)
- A couple of joke ones in the coach's voice ("Told You So" — follow a
  coach nudge and immediately improve)

## Sequencing note

Phase 1 needs zero footage and zero Jack-hours beyond a review pass — good
"boring week" work. Phase 2 waits on the game being show-ready (Jack's
call). Phase 3's device matrix is already in the alpha plan. Phase 4 is
real engineering — belongs in PLAN.md M5 when Jack schedules it.
