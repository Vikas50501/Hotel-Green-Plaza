# Hotel Green Plaza — Official Website

Static website for **Hotel Green Plaza & Restaurant**, Bhilwara, Rajasthan.

## Project Structure

```
Hotel Green Plaza/
│
├── _build/                         ← Build & audit tools (never deployed)
│   ├── build.py                    ← Static site generator — ALL content lives here
│   ├── audit.py                    ← Quality checker (links, SEO, a11y, colour tokens)
│   ├── fetch_placeholder_photos.py
│   └── make_placeholders.py
│
├── docs/                           ← Complete deployable site (GitHub Pages source)
│   ├── assets/
│   │   ├── css/style.css           ← Single consolidated stylesheet
│   │   ├── js/main.js              ← Vanilla JS (nav, gallery, menu filter, carousel)
│   │   └── img/
│   │       ├── hero/               ← Full-bleed hero & page banner images
│   │       ├── gallery/            ← Gallery page images
│   │       ├── general/            ← Section content images
│   │       ├── rooms/              ← Room card images
│   │       └── logo/               ← Logo, favicon, PWA icons
│   ├── index.html                  ← Generated — do not hand-edit
│   ├── about-us/index.html
│   ├── accommodation/index.html
│   ├── banquets/index.html
│   ├── contact/index.html
│   ├── gallery/index.html
│   ├── restaurant/index.html
│   ├── services/index.html
│   ├── 404.html
│   ├── enquiry.php                 ← Server-side contact form handler
│   ├── sitemap.xml                 ← Auto-generated
│   └── robots.txt                  ← Auto-generated
│
├── .gitignore
├── CHANGELOG.md
└── README.md
```

## How to Build

```bash
python _build/build.py    # Regenerates everything inside docs/
python _build/audit.py    # Must print "No problems found." before every commit
```

All site content (text, menu items, room details, amenities, contact info, branch
data) lives inside `_build/build.py`. Edit there and rebuild — never hand-edit the
generated HTML files in `docs/`.

## Deployment

Point your host (GitHub Pages, Netlify, Vercel, cPanel) to the **`docs/`** folder.

**GitHub Pages:** Settings → Pages → Source → `docs/` folder on `main` branch.

## Tech Stack

- Pure static HTML/CSS/JS — no framework, no build pipeline, no npm
- Single stylesheet using CSS custom property design tokens (no stray hex values)
- Inline SVG sprite for all icons
- Asset cache-busting via MD5 content hash (`style.css?v=xxxx`)
- Vanilla JS: sticky header, mobile nav panel, gallery filter + lightbox, menu
  category sidebar filter, testimonial carousel

## Before Going Live

Run `python _build/audit.py` — it lists every `[VERIFY: ...]` placeholder:

- [ ] Real hotel photography (39 placeholder images in `docs/assets/img/`)
- [ ] Confirmed room names, pricing and availability
- [ ] Restaurant and breakfast timings
- [ ] Geo coordinates for the map embed
- [ ] Neemuch / Jaora branch details
- [ ] Domain confirmed (www vs non-www + HTTPS enforced)
- [ ] `$RECIPIENT` email address in `docs/enquiry.php`
- [ ] Google Business Profile link (currently placeholder)

## Contact

Hotel Green Plaza & Restaurant  
Hamirgarh, Bhilwara–Chittor Road (NH-48), Bhilwara, Rajasthan 311025  
+91 81073 67300 · hotelgreenplazaindia@gmail.com
