# Kunstquiz — Blueprint

A reference for how **kunstquiz.art** is built: architecture, data, styling, and the
conventions you'd want to keep (or deliberately change) if rebuilding from scratch.

> **One-line summary:** A zero-build, vanilla-JS single-page app that quizzes you on the
> artist behind Norwegian paintings. Data is scraped from Wikimedia/Wikidata into static
> JSON; the front end is one HTML file, one CSS file, one JS file, served as static files
> on GitHub Pages.

---

## 1. Tech stack & philosophy

| Layer | Choice | Notes |
|---|---|---|
| Front end | **Vanilla HTML/CSS/JS** | No framework, no bundler, no build step. Edit a file → commit → live. |
| Hosting | **GitHub Pages** | Custom domain via `CNAME` → `kunstquiz.art`. Static files served with gzip. |
| Data | **Static JSON** in `data/` | Generated offline by Python scripts; the site only ever *reads* JSON. |
| Images | **Wikimedia Commons** | Loaded on demand from `commons.wikimedia.org` (see §6). Not stored in repo. |
| Icons | **Lucide** | Loaded from `unpkg` CDN, `defer`. Pre-rendered SVGs are also inlined for nav. |
| Fonts | **Montserrat** (Google Fonts) | 400 + 700 weights, non-blocking load. |
| Analytics | **Google Analytics 4** (`gtag`) | Loaded `async`. Custom events in `trackEvent()`. |

**Design philosophy:** keep it deployable by editing three files. There is no `package.json`,
no node_modules, no transpilation. The Python in `scripts/` is a *separate* offline data
pipeline — it is not part of the runtime and is never shipped to the browser.

---

## 2. File structure

```
kunstquiz/
├── index.html              # The whole DOM: all pages + modals live here, toggled by display
├── assets/
│   ├── css/style.css        # ~5,500 lines, single stylesheet (no preprocessor, no variables)
│   └── js/script.js         # ~5,500 lines, single script (no modules, all globals + functions)
├── data/
│   ├── paintings.json       # The quiz corpus: one row per painting (see §5)
│   ├── artists.json         # One row per artist: bios, dates, movements, portrait (see §5)
│   ├── app_data.json        # LEGACY/UNUSED by the site — safe to ignore at runtime
│   └── raw/paintings_raw.json  # Pipeline intermediate
├── scripts/                 # Offline Python data pipeline (see §9) — not shipped
│   ├── workflow.py          # 6-step orchestrator (collect → clean → process → deploy)
│   ├── collect_art.py, clean.py, process.py, diagnostics.py, stats.py, utils.py
├── logo.svg                 # Favicon
├── CNAME                    # kunstquiz.art
└── CLAUDE.md, README.md, BLUEPRINT.md, diagnostics.md, docs/
```

The site loads **only** `data/paintings.json` and `data/artists.json` at runtime.
`app_data.json` (~5 MB) is a legacy artifact and is not fetched.

---

## 3. Runtime architecture

It is a **multi-"page" SPA implemented with hash routing inside one HTML document.** Every
"page" is a `<div class="page">` that is shown/hidden via `display`. No client-side router
library — routing is `window.location.hash` + a `hashchange` listener.

### Pages (all in `index.html`)
| Hash | Element id | Purpose |
|---|---|---|
| *(none)* | `#quiz-page` | The quiz itself (default) |
| `#painters` | `#painters-page` | Browsable list of all artists with inline galleries |
| `#gallery` | `#gallery-page` | Infinite-scroll collage of all paintings |
| `#how-to-play` | `#how-to-play-page` | Instructions |

`showPage(pageId)` toggles visibility; `handleHashChange()` maps the hash to a page and
triggers that page's render function. Modals (`congrats`, `round-results`, `diploma`,
`artists`, `gallery`, `how-to-play`, `painting-viewer`) are separate `display:none` divs
toggled imperatively.

### Boot sequence (`DOMContentLoaded` in `script.js`)
1. Init Lucide icons, theme, hash routing.
2. **Resolve the data promises** kicked off in `<head>` (see §6) → `paintings`, `artistBios`.
3. `initializeArtistWeights()` → `updateCategoryDropdown()` → `updateCollectionInfo()` → `updateLanguageUI()`.
4. `preloadInitialImages()` then `startNewRound()`.
5. Background: `startGalleryBackgroundPreload()`, memory-cleanup interval, scroll/resize handlers.

### State (module-level globals in `script.js`)
- `paintings` / `artistBios` — the loaded corpora.
- `selectedCategory`, `currentRound`, `streak`, `currentPainting`.
- `artistWeights` (Map) + `lastSelectedArtists` (Set) — anti-repetition weighting.
- Caches: `imageCache`, `memoryCache`, `domCache`, `validPaintingsCache`, `categoryCountsCache`, `galleryPreloadCache`.
- `currentLanguage` (`'en'` | `'no'`), persisted in `localStorage` under `language`.

---

## 4. Quiz logic

- **A round = 10 questions** (`currentRound`). The streak bar shows 10 circles.
- `getValidPaintings()` filters the corpus by `selectedCategory` (cached per category).
- `getWeightedRandomPainting()` picks the next painting, down-weighting recently-seen
  artists (`artistWeights` + `lastSelectedArtists`) so the same painter doesn't dominate.
- `generateOptions(correct, ...)` builds 4 answer buttons (1 correct + 3 distractor artists).
- On answer: `button.correct` / `button.wrong` styling + animation, feedback message,
  streak update, then advance. End of round → `showRoundResults()`; a perfect 10/10 →
  `showDiploma()` (downloadable via lazily-loaded `html2canvas`).
- Click the painting → `showPaintingViewer()` full-screen at original resolution.

### Categories (`CATEGORY_DEFS`)
`all`, `popular`, `landscape`, `realism`, `expressionism`, `impressionism`,
`romantic_nationalism`, `female_artists`. Each maps to a predicate in `categoryFilters`
that inspects a painting's `categories` / `inferred_categories` plus artist
`movement` / `genre` / `gender`. Counts shown in the dropdown come from `getCategoryCounts()`.

---

## 5. Data model

### `paintings.json` — array of paintings (the quiz corpus)
```jsonc
{
  "title": "…",                 // raw Wikimedia title (run cleanWorkTitle() before display)
  "url": "https://…",           // Wikimedia image URL (upload.* or Special:FilePath form)
  "artist": "Edvard Munch",     // join key into artists.json (by name)
  "categories": ["Expressionism", "Portraits"],   // per-painting tags
  "inferred_categories": ["expressionism"],
  // The following are DUPLICATED from the artist on every row (bloat — see note):
  "artist_bio", "artist_birth", "artist_death", "artist_gender",
  "movement", "genre", "birth_year", "death_year",
  "artist_movement": [...], "artist_genre": [...]
}
```

### `artists.json` — array of artists (lookup by `name`)
```jsonc
{
  "name": "Edvard Munch",
  "birth_year": "1863", "death_year": "1944",
  "birthplace", "deathplace", "aliases": [],
  "english_bio", "norwegian_bio", "summary",
  "movement": ["Symbolism","Expressionism"], "genre": ["Painting","Graphic art"],
  "awards": [], "gender": "male", "is_female": false, "country": "…",
  "self_portrait_url": "https://…",          // shown in artist popups
  "notable_works": [{ "title", "year" }, …]
}
```

> **Known data-debt (carry forward if rebuilding):** every painting row repeats the full
> artist bio and metadata, which roughly **doubles** `paintings.json` (~2.5 MB vs ~1.1 MB
> slim). All of that artist-level data already exists in `artists.json`, keyed by `artist`
> name. A clean rebuild should store only `{title, url, artist, categories,
> inferred_categories}` per painting and derive artist fields from a `Map(name → artist)`.
> Note `scripts/process.py` re-introduces the duplicated fields on every regen, so the
> slimming must be done in the pipeline, not just the JSON. (One painter, *Martin Aagaard*,
> exists in paintings but not `artists.json` — handle the missing-artist case.)

---

## 6. Image & data loading (performance-critical)

This app is **image-bound**, not code-bound. The two levers that matter most:

### a) Early, parallel data fetch
`index.html` `<head>` kicks off both JSON fetches *before* `script.js` even downloads:
```html
<script>
  window.__kunstquizData = {
    paintings: fetch('./data/paintings.json').then(r => r.json()),
    artists:   fetch('./data/artists.json').then(r => r.json())
  };
</script>
```
`script.js` then `await`s those promises (with a self-fetch fallback if the inline script
didn't run). This overlaps the 2.5 MB download with the 197 KB script download instead of
serializing them.

### b) Wikimedia thumbnails, not full-res scans
Wikimedia originals are museum scans (often several MB each). `optimizeImageUrl(url, width)`
rewrites any Wikimedia URL to the stable **`Special:FilePath`** endpoint with a width:
```
https://commons.wikimedia.org/wiki/Special:FilePath/<filename>?width=800
```
Wikimedia snaps to an allowed thumbnail size server-side and 302-redirects to the resized
image (~50–200 KB). This works for both `upload.wikimedia.org/.../a/ab/File.jpg` and existing
`Special:FilePath` URLs. Width per use: **800** quiz display, **400** gallery, **150** tiny
artist thumbs. The **full-screen viewer uses the original URL** (unmodified) so zoomed
detail stays crisp.

> Do **not** use `/thumb/<a>/<ab>/File.jpg/<w>px-File.jpg` directly — Wikimedia now returns
> HTTP 400 for non-allowlisted widths. `Special:FilePath?width=` is the robust path.

### c) Preloading & caching
- `preloadAllRoundImages()` eager-loads the round's images into `imageCache` (keyed by the
  **original** URL) and `img.decode()`s them for flicker-free display.
- Every preload path falls back to the original URL on error, so the cache always holds a
  working src even if a thumbnail fails.
- `predictivePreload()` loads question *i+2* and the next self-portrait while you answer *i*.
- Gallery images preload in the background and lazy-load on scroll (IntersectionObserver).

### d) Other front-end perf
- Montserrat loads non-blocking (`media="print"` swap trick) with a `<noscript>` fallback.
- `preconnect` hints to fonts, gtag, unpkg, cdnjs.
- `html2canvas` (diploma export) and Lucide are loaded lazily / `defer`.
- Throttled scroll, debounced resize, a periodic memory-cleanup pass, and pause-on-hidden.

---

## 7. Styling system

Single stylesheet, **no preprocessor and no CSS custom properties** — values are inlined
literals. If rebuilding, the first improvement is to lift the palette into `:root` variables.

### Fonts
- **Montserrat** (`400`, `700`), fallback `Arial, sans-serif`.
- `text-rendering: optimizeLegibility`, antialiased smoothing.

### Color palette (the de-facto tokens, by frequency)
| Role | Light | Dark |
|---|---|---|
| **Brand green** (primary, accents, focus rings) | `#4caf50` | `#4caf50` |
| Green (darker border / filled) | `#388e3c` | — |
| Green tints | `rgba(76,175,80,…)` (hover bg `#e6f7ee`, correct `#c8f7c5`) | |
| Wrong / error | `#f44336`, `#d32f2f`, `rgba(244,67,54,…)` | |
| Text | `#222` / secondary `#444` | `#e0e0e0` |
| Page background | gradient `#fafbfc → #f5f7fa` | gradient `#000 → #111` |
| Card / surface | `#fff` | `#2d2d2d` |
| Borders | `#d0d0d0`, `#e0e0e0` | `#444` |

Dark theme is `html.dark-theme …` overrides (toggle persisted in `localStorage`, applied by
`applyTheme()`). There's a subtle fixed radial-dot texture on `body::before`.

### Layout
- **Quiz page** = a two-column flex (`.main-flex`): `.img-col` (≈55%, painting + streak bar)
  and `.btn-col` (≈40%, the four answer buttons). Centered, `max-width: 1400px`, sized to
  fit the viewport (`calc(100vh - 110px)`, no page scroll on the quiz).
- The top bar is `position: absolute` with a `backdrop-filter: blur` translucent background.
- Other pages scroll normally; the quiz page intentionally does not.

### Breakpoints (mobile-first-ish, max-width queries)
`1200`, `1199/768`, `1024`, `1000`, `900`, `768`, `700`, `500`, `480`, plus
`(hover:none) and (pointer:coarse)` for touch and a landscape-phone query. On narrow
screens the two columns stack (image over buttons).

### Motion & a11y
- Transitions use `cubic-bezier(0.4, 0, 0.2, 1)`. Keyframes: `fadeInOptions`, `correctPulse`,
  `wrongShake`, `spin`, `loading-shimmer`.
- `@media (prefers-reduced-motion: reduce)` near-zeroes all animation/transition durations.
- `:focus-visible` green outline on buttons/links; min touch target `max(3rem, 44px)`;
  ARIA roles on the quiz region, options group, progressbar, and modals.

---

## 8. Internationalization

Two languages, **English (`en`)** and **Norwegian (`no`)**, toggled in the nav (persisted in
`localStorage`). All UI strings live in the `translations` object; `t('key')` resolves
dotted keys. Artist bios are bilingual in `artists.json` (`english_bio` / `norwegian_bio`).
Adding a language = add a block to `translations` + a bio field convention.

---

## 9. Offline data pipeline (`scripts/`, Python)

Not part of the site — run locally to regenerate `data/`. Orchestrated by `workflow.py`:

```
collect_art.py   # 1. scrape Wikimedia/Wikidata for paintings + metadata
clean.py         # 2. quality/dup removal; honor data/config/urls_to_{add,remove}.txt
process.py       # 5. build paintings.json + artists.json (assigns categories, joins artist meta)
diagnostics.py   # health checks (see diagnostics.md)
stats.py         # corpus stats
```
Typical: `python scripts/workflow.py --full` (or `--quick`). `process.py` is where the
per-painting artist-field duplication is (re)introduced — see the §5 note.

---

## 10. If you rebuild from scratch — recommended keeps & changes

**Keep:** the zero-build static-file model; hash-routed single-document pages; the
`Special:FilePath?width=` thumbnailing; early parallel data fetch; image preload + decode;
bilingual `translations` object; dark theme via a root class; the green/Montserrat identity.

**Change / improve:**
- Lift the palette into `:root` CSS custom properties (single source of truth).
- Slim `paintings.json` to painting-only fields; derive artist data from a `Map` over
  `artists.json` — and fix `process.py` so regen stays slim.
- Consider splitting the ~5.5k-line `script.js` into ES modules (still no bundler needed
  with `<script type="module">`).
- Audit the liberal `will-change` usage (30+ rules) — keep it only on elements actively
  animating, not permanently static ones.
