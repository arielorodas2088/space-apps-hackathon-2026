# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

"DRACO: Misión 500", a browser game for the NASA Space Apps Challenge 2026 **Space Mission Design Game** challenge. The player designs a mission to a solar-system body (Moon, Venus, Mars, Bennu, Europa, Titan, Neptune), flies a corridor and gets a report explaining what went right or wrong. All UI text, docs and code comments are in **Spanish (rioplatense: "abrí", "revisá")**. Keep new player-facing text in that register.

It is a static site plus one Vercel Python serverless function (`api/live-data.py`). There is no build step, package manager or test suite. To run it, open `index.html` in a browser; it falls back to the committed snapshot of the data. It is deployed on **Vercel** (zero-config: static root + `api/*.py`).

## Commands

```
python tools/fetch_data.py          # regenerate the snapshot assets/live-data.{js,json} from the live APIs (~4 s)
pip install reportlab && python tools/build_pdf.py   # regenerate docs/documento_proyecto.pdf from the .md
```

There is no Vercel CLI setup in the repo; to test the function locally, load `api/live-data.py` with importlib and serve its `handler` class with `http.server`.

## Architecture

The whole game lives in `index.html`: inline `<style>`, then one inline `<script>` with minified-style, terse JS (short identifiers, template-string HTML, no framework).

- **Data tables (top of script):** `D` = destinations (cost, energy, solar factor, science target `t`, insertion tolerance `tol`, signal delay `dl`), `OR` = orbits, `DU` = durations, `RK` = rockets, `BUS` = spacecraft buses, `IT` = items as positional arrays (id, category, name, cost, mass, power use, power gen, …, max qty), `ROUTES`, `TRAVEL` (distance ranges and real-time flight seconds per destination), `HAZARDS`, `EV` (random mission events, each with a condition that mitigates it).
- **State:** a single global `S` (`ph` phase: `'plan' | 'fly' | 'report'`, chosen options, item quantities `q`, team size `n`, active role `act`, ready list `rd`, flight state `fl`, report `rep`).
- **Render loop:** mutators (`set`, `go`, `qt`, `changeRoute`, `reactObstacle`, …) change `S` and call `draw()`, which replaces `#app.innerHTML` with `plan()`, `fly()` or `rep()`. Event handlers are inline `onclick="..."` strings, so any function they call must be global.
- **Derived numbers:** `calc()` computes budget, mass, power, data and science from `S`. `checks()` produces the pre-flight validation list. `dash()` renders the resource bars.
- **Multiplayer roles:** `TABS` maps each planning tab to a role index in `ROL` (Planificador, Ingeniero, Científico, Logística). `can()` gates edits to the active role, and every player must mark ready (`S.rd`) before launch.
- **Flight:** `launch()` starts `window.flightClock` (setInterval) that advances `S.fl`. Keyboard arrows and the touch D-pad set `S.fl.keys` via `holdKey`. `man()` is a manual maneuver, and `ins()` resolves orbit insertion and the events, then builds the report.
- **Live data (three tiers):** at load, `applyLive(window.LIVE_DATA,'snapshot')` uses `assets/live-data.js`, then (over http only) `fetch('api/live-data')` with an 8 s timeout calls `applyLive(json,'live')` and redraws if still in planning. With neither, hardcoded values are used. `LIVE.src` drives the "Datos: …" label. `applyLive` mutates `D`, `TRAVEL` and `HAZARDS` in place and must stay idempotent (it can run twice). It sets: real distance (`d.distNow`, which `travelFor` prefers over the random roll), delay text, Bennu's `en` from Mission Design v∞ (`enFromVinf`), a dynamic `neo` destination from NeoWs, and `LIVE.sw` (DONKI), which `ins()` uses to force and scale the 'Tormenta solar' event (`EV[0]`).
- **Data backend:** `api/_live.py` (stdlib only) has `build()`, shared by `api/live-data.py` (Vercel, `Cache-Control: s-maxage=21600`) and `tools/fetch_data.py`. Each source fails independently into `errors`. Endpoint gotchas, verified 15/11/2026: Horizons is `ssd.jpl.nasa.gov/api/horizons.api` (the `ssd-api` host 404s) and returns 503 under concurrency (a semaphore of 2 plus retries); DONKI lives at `ccmc.gsfc.nasa.gov/DONKI-API/get/` (the `api.nasa.gov/DONKI` route 404s); for `mdesign.api`, `step` must be one of 1, 2, 5, 10, 15, 20 or 30; NeoWs uses env `NASA_API_KEY`, falling back to `DEMO_KEY` (10 req/h). JPL endpoints send no CORS headers, so the browser must never call them directly.

## Data honesty conventions

Costs, masses and powers are **estimaciones de juego**, not real values. `assets/curated/sources.csv` tracks each in-game number with its real value, source and status (`estimacion_juego`, `por verificar`, `verificado`). `docs/documento_proyecto.md` labels each capability Hecho/Parcial/Pendiente and uses `[COMPLETAR]` for team-only info. Keep that framing: don't present game numbers as real. When you change a game value, update the CSV and the doc too.
