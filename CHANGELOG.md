# Hotel Green Plaza — build changelog

The Riorelax luxury-hotel theme has been rebuilt into the Hotel Green Plaza
website for Bhilwara, Rajasthan. Every word of copy comes from
`Hotel_Green_Plaza_Website_Content_Design_Specification.md`; nothing is invented.

---

## 1. What you received

```
/                       index.html
/about-us/              about-us/index.html
/accommodation/         accommodation/index.html
/restaurant/            restaurant/index.html
/banquets/              banquets/index.html
/services/              services/index.html
/gallery/               gallery/index.html
/contact/               contact/index.html
404.html                styled, noindex
enquiry.php             form handler (validation, honeypot, mail)
sitemap.xml, robots.txt
assets/css/style.css    44 KB — the whole design system, one file
assets/js/main.js       14 KB — all behaviour, no jQuery
assets/img/…            logo, icons and 33 placeholder photographs
_build/                 the generator + audit scripts (see §7)
_theme-original/        the untouched Riorelax theme (see §7)
```

Total CSS + JS is **58 KB uncompressed**, down from the theme's ~700 KB of CSS
and ~370 KB of JS.

---

## 2. Theme sections kept

Kept in substance, rebuilt in the new visual language:

| Theme block | Became |
|---|---|
| `container` / `row` / `col-*` grid, 576/768/992/1200 breakpoints | Re-implemented as a colour-free grid layer inside `style.css` — same class names and breakpoints, so the layout engineering and responsive behaviour carry over |
| Sticky header + logo-left / menu-right structure | `.gp-header`, transparent over the hero, solid on scroll |
| Full-bleed hero with overlay | `.gp-hero`, 88vh, single static image |
| Card grid (rooms / services) | `.gp-card`, one card component sitewide |
| Two-column image + text blocks | `.gp-split` |
| Four-column footer | `.gp-footer` |
| Gallery grid + lightbox | `.gp-masonry` + a purpose-written vanilla lightbox |
| Contact form | `.gp-form` with real validation |

## 3. Theme sections removed

**Pages deleted:** `index-2/3/4`, `about`, `room`, `single-rooms`, `services`,
`single-service`, `projects`, `team`, `team-single`, `blog`, `blog-details`,
`faq`, `pricing`, `shop`, `shop-details`, `thank-you`, `mail.php`, `news-mail.php`.

**Sections deleted:** hero slider carousel, date-picker "booking" bar (a fake
availability widget), pricing tables, team members, the theme's own fabricated
testimonials, brand-logo strip, blog feed, shop/product grids, counters, skill
bars, video-popup band, newsletter bar, social links, "Mon–Fri 9:00–19:00" top
bar and its demo phone number. (A real "What Our Guests Say" section was added
back later — see §4a — once actual guest reviews were supplied.)

**CSS deleted:** `bootstrap.min.css`, `animate.min.css`, `dripicons.css`,
`fontawesome-all.min.css`, `magnific-popup.css`, `meanmenu.css`, `slick.css`,
`default.css`, `style.css`, `responsive.css` — the entire colour, type and
component layer.

**JS deleted:** jQuery, Popper, Bootstrap JS, Modernizr, `slick`, `wow`,
`waypoints`, `counterup`, `typed`, `particles` (×2), `parallax` (×2), `paroller`,
`parallax-scroll`, `isotope`, `imagesloaded`, `magnific-popup`, `meanmenu`,
`scrollUp`, `one-page-nav`, `element-in-view`, `ajax-form`. Also the icon fonts
(FontAwesome, Dripicons) and all 100+ demo images.

Nothing from the theme's demo content, links or plugin credits survives — the
audit script greps for it on every build and currently reports zero hits.

## 4. Sections built new

Built from scratch in the theme's visual language: **trust band**, **amenities
icon grid**, **room-facility chips**, **gallery category filter**, **accessible
lightbox**, **enquiry form with enquiry-type dropdown**, **sticky mobile
`Call | Enquire | Book` bar**, **inner-page banner + breadcrumbs**, **click-to-load
map**, **404 page**, a **guest reviews section** (§4a), and a **35-symbol inline
SVG icon set** (1.5 px stroke, one style, replacing two mismatched icon fonts).

## 4a. Guest reviews — real, not fabricated

The spec (§49, §36) forbids inventing testimonials, and none existed at first —
so the original build shipped without a reviews section at all. The hotel later
supplied `hotel_greenplaza_1396_reviews.csv`, its own exported Google/Tripadvisor
reviews, plus the current Google Business Profile aggregate: **4.1 / 5 from
2,981 reviews**.

- The CSV's 331 rows are 166 unique reviews once exact duplicate export rows
  are removed. One long review was excluded from consideration because it's
  about *other, unrelated* hotels named "Hotel Green" in different states —
  not this property — so quoting it would misattribute someone else's opinion.
- Nine reviews are quoted on the homepage (`REVIEWS` in `_build/build.py`),
  chosen for topic spread (food, rooms, family/kids, parking, staff, value,
  pure-veg, highway convenience) across both platforms and ratings 4–5.
  Wording is unedited; only punctuation/capitalisation was cleaned up for
  on-site readability.
- The aggregate score renders as a genuine partial-fill star (4.1 → 82% of the
  fifth star), and both figures are attributed: *"Based on 2,981 Google
  reviews."* The same figures back an `AggregateRating` node on the Hotel
  schema for search-result star snippets.
- **`Read More Reviews on Google`** currently points at a Google *search* URL
  (`google.com/search?q=Hotel+Green+Plaza+Bhilwara+reviews`) because no
  confirmed Google Business Profile link was supplied. [VERIFY: swap
  `REVIEWS_SOURCE_LINK` in `build.py` for the hotel's actual "see all reviews"
  short link once available] — it works today, just not as precisely as a
  direct listing link would.
- Star-rating icons are solid-fill, not the sitewide outline stroke style —
  a deliberate, documented exception (`style.css`, "Testimonials" section):
  rating stars are a distinct, universally recognised convention, not a
  decorative feature icon.

## 5. Design decisions worth knowing

- **Colour.** All colour lives in `:root`. The audit fails the build if a hex or
  `rgba()` appears anywhere else. Measured on the homepage: 70.7 % white/cream/tint,
  14.2 % flat deep green, 15.1 % photo bands, lime at **0.017 %** of painted area
  and never a fill. No two flat-green blocks touch — the photo CTA band separates
  the final band from the footer.
- **One accessible olive was added.** `--gp-olive` (`#7A973B`) is only **3.3:1**
  on white and **2.9:1** on `--gp-tint`, so it fails AA for the 13 px eyebrow text
  the spec assigns it to. Spec §28 anticipates this ("green text on light green
  backgrounds should be tested"). `--gp-olive` still colours icons and rules;
  eyebrow *text* uses `--gp-olive-text` (`#5D732D`) — the same hue at 0.76×,
  giving 5.3:1 on white, 4.9:1 on cream, 4.7:1 on tint. Every other pair passes
  AA; the full matrix is in §8.
- **Logo untouched.** Never recoloured or retyped. Over the hero it sits on a
  white plate; in the dark footer it sits on a white plate. Clear space is set to
  the height of the "H" in HOTEL.
- **No booking engine, so no fake calendar.** Every `Book Your Stay`,
  `Book / Enquire Now` and `Check Availability` CTA opens the enquiry form at
  `/contact/#enquiry`.
- **Testimonials are real, sourced from the hotel's own reviews export — see §4a.**
- **No video gallery** — spec §15 says not to ship empty gallery states.
- **No social icons** — no verified profiles were supplied.
- **Critical CSS is not inlined.** The spec asks for it, but the whole stylesheet
  is one 44 KB file (~10 KB gzipped) on a single HTTP/2 request, and the LCP
  element is the hero image, which is preloaded with `fetchpriority="high"`.
  Inlining would have duplicated a critical block across nine hand-maintained
  pages for no measurable gain and a real FOUC risk. Say the word if you want it.
- **Paths are root-relative** (`/assets/…`, `/about-us/`). This assumes the site
  is served from the domain root, which the spec's URL structure requires. It
  will not work from a subfolder or by double-clicking the HTML files — use
  `python -m http.server` locally.

## 6. Motion

Fade-and-rise only: 18 px, 500 ms, `cubic-bezier(.2,.6,.2,1)`, 80 ms stagger,
fires once. Plus card-image zoom to 1.05 on hover and the header state change.
All of it is disabled under `prefers-reduced-motion: reduce`. A `<noscript>`
block and an on-`load` safety net guarantee content is never left invisible.

## 7. Two folders to delete before you deploy

- **`_theme-original/`** — the complete original Riorelax theme, moved rather
  than deleted so you keep your source copy. **It is not part of the website.**
- **`_build/`** — `build.py` regenerates all nine pages from shared partials so
  the header, footer, mobile menu, icon sprite and lightbox are provably identical
  everywhere; `audit.py` is the check described below; `make_placeholders.py`
  regenerates the placeholder imagery. Edit page content in `build.py` and re-run
  it, **not** in the generated HTML, or your next build will overwrite you.

`robots.txt` disallows both as a backstop, but delete them.

## 8. Verification actually run

`_build/audit.py` — **0 problems**, covering all 9 pages: one `<h1>` each, no
heading-level jumps, no duplicate IDs, alt text and `width`/`height` on every
image, `loading="lazy"` below the fold, every internal link and asset resolving,
every form control labelled, unique title + meta description, canonical + full
Open Graph set, no stray colour outside `:root`, no leftover template strings.

In-browser, at **1440 / 1280 / 1024 / 768 / 390** across all 9 pages:

- **Horizontal overflow: 0 px everywhere.**
- Nav ↔ hamburger swap at 992 px; action bar appears only below 768 px; masonry
  goes 3 → 2 → 1 columns.
- Mobile panel: opens, traps focus, closes on Esc and on link click, restores
  focus, locks body scroll, `aria-expanded` / `aria-hidden` correct.
- Gallery: all 9 filters return items (no empty states); lightbox opens, respects
  the active filter, arrow-keys and Esc work, focus is trapped and restored.
- Form: 5 required fields flagged, focus jumps to the first error, check-out
  before check-in is caught, honeypot is off-screen, status stays hidden until
  submit.
- Room cards: equal heights, media exactly 4:3 (facility cards 3:2).
- Exactly two font families render (Lato, Playfair Display; three weights).

Contrast (all AA or better): ink on white 15.8, on cream 14.7, on tint 14.0 ·
muted 6.3 / 5.8 / 5.5 · headings 7.7 / 7.2 / 6.8 · white on primary 7.7 ·
white on dark 11.9 · body on dark 7.9 · footer meta on dark 5.2 · fresh eyebrow
on dark 4.8 · error text 7.3 / 6.4 · eyebrow olive-text 5.3 / 4.9 / 4.7.

**Not verified:** I could not take screenshots — the browser pane never
composited in this environment, so the page reported `visibilityState: hidden`.
Everything above was measured from the live DOM and computed styles rather than
by eye. **Please open the site and look at it before signing off.**

---

## 9. `[VERIFY:]` placeholders you must fill in

23 distinct markers are in the markup. In priority order:

| # | Placeholder | Where |
|---|---|---|
| 1 | **Phone number** | header `Call Us`, sticky bar `Call`, footer, contact, location blocks. Change `href="/contact/"` to `tel:+91…` in `build.py` (`header()`, `ACTIONBAR`) |
| 2 | **Email address** | footer, contact page |
| 3 | **Complete postal address + PIN** | footer, contact, every location block, and `streetAddress` / `postalCode` in the JSON-LD |
| 4 | **Google Maps embed URL** | `location_section()` — put it in the poster's `data-src` |
| 5 | **Google Maps place link** | every `Get Directions` button |
| 6 | **Geo coordinates** | add a `geo` node to the Hotel schema |
| 7 | **Production domain** | `SITE` in `build.py` — currently `https://www.hotelgreenplaza.in`, which drives every canonical, OG and sitemap URL |
| 8 | **Enquiry recipient email** | `$RECIPIENT` in `enquiry.php` — the form returns an error until this is set |
| 9 | **Restaurant timings** and breakfast/lunch/dinner availability | restaurant page + `openingHoursSpecification` |
| 10 | **Menu categories / signature dishes** | restaurant page |
| 11 | **Room names, rates, occupancy, inventory** | accommodation page |
| 12 | **Banquet capacity, catering options, packages** | banquets page |
| 13 | **Separate hotel / banquet / restaurant enquiry contacts** | contact page |
| 14 | **Confirm the services and amenities list** against current operations | services + about pages |

### Also outstanding

- **All 33 photographs are placeholders.** Each is a real WebP at the exact
  aspect ratio the layout expects, with the production filename already in place —
  drop a real photo in at the same size and nothing else changes. Every `<img>`
  has an HTML comment above it stating the required dimensions.
- **The logo is only 179 × 103 px.** It renders crisply at the 108 × 62 px used
  in the header, but there is no headroom. Please supply a vector (SVG/AI/EPS) or
  a 2× PNG. A white-on-dark variant would also let the footer drop its contrast
  plate.
- **Old URLs.** If `/accomodation/` (the legacy misspelling) or any other old URL
  has search value, add 301 redirects — spec §52.
- **Analytics and Search Console** are not installed.

---

## 10. Rebuilding

```bash
python _build/build.py     # regenerate all 9 pages + sitemap + robots
python _build/audit.py     # must print "No problems found."
```
