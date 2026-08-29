"""Assemble the Hotel Green Plaza static site from shared partials.

The deliverable is the plain HTML this script writes. It exists so that the
header, mobile panel, footer, action bar, icon sprite and lightbox are provably
identical on every page rather than eight hand-maintained copies.

Run:  python _build/build.py
"""
import hashlib
import io
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def asset_ver(rel):
    """Short content hash appended to CSS/JS URLs so a changed file busts the
    browser cache automatically (returning visitors never get stale assets),
    while an unchanged file keeps its cached copy."""
    try:
        with open(os.path.join(ROOT, rel), "rb") as fh:
            return hashlib.md5(fh.read()).hexdigest()[:8]
    except OSError:
        return "1"


CSS_VER = asset_ver("assets/css/style.css")
JS_VER = asset_ver("assets/js/main.js")

# Domain taken from the business card supplied by the hotel.
SITE = "https://www.hotelgreenplaza.com"

# ---------------------------------------------------------------------------
# Verified contact details — Hotel Green Plaza business card.
# Branch 1 (Bhilwara) is the hotel this website is about. Branches 2 and 3 are
# listed on the Contact page only; no room, dining or banquet claims are made
# for them because none were supplied.
# ---------------------------------------------------------------------------

BHILWARA = {
    "locality": "Bhilwara",
    "region": "Rajasthan",
    "postal": "311025",
    "street": "Bhilwara Chittor Road, N.H. 48, Hawai Patti ke Pass, Vill. Takhatpura, Tehsil Hamirgarh",
    "short": "Hamirgarh, Bhilwara",
    "html": ("Bhilwara Chittor Road, N.H.&nbsp;48, Hawai Patti ke Pass,<br>"
             "Vill. Takhatpura, Tehsil Hamirgarh,<br>"
             "Bhilwara 311025, Rajasthan, India"),
    "phones": [("+918107367300", "+91 81073 67300"),
               ("+919724847600", "+91 97248 47600"),
               ("+917891434274", "+91 78914 34274")],
    "email": "hotelgreenplazaindia@gmail.com",
}

BRANCHES = [
    {
        "name": "Neemuch",
        "html": ("Neemuch By Pass Highway, SH&nbsp;-&nbsp;31,<br>"
                 "Village Barukheda, Tehsil &amp; Dist. Neemuch,<br>"
                 "Neemuch 458441, Madhya Pradesh"),
        "phones": [("+918107367200", "+91 81073 67200"),
                   ("+917016667428", "+91 70166 67428"),
                   ("+917984487576", "+91 79844 87576")],
        "email": "hotelgreenindia@gmail.com",
    },
    {
        # The hotel's own menu names this the "Jaora Branch"; the town is Jaora,
        # in Dist. Ratlam. Named by its town here, with the district kept in the
        # address below.
        "name": "Jaora",
        "html": ("S.H.&nbsp;-&nbsp;31, Village Parwaliya,<br>"
                 "Tehsil Jaora 457226,<br>"
                 "Dist. Ratlam, Madhya Pradesh"),
        "phones": [("+918107367400", "+91 81073 67400"),
                   ("+919998682236", "+91 99986 82236"),
                   ("+916377610214", "+91 63776 10214")],
        "email": "hotelgreenplazaindia3@gmail.com",
    },
]

PRIMARY_TEL, PRIMARY_TEL_LABEL = BHILWARA["phones"][0]

# WhatsApp click-to-chat — the hotel's primary mobile, with a prefilled message
# so the guest lands in a ready-to-send enquiry. [VERIFY: confirm this number is
# WhatsApp-enabled; swap if the hotel uses a different chat line]
WHATSAPP_NUMBER = "918107367300"
WHATSAPP_LINK = ("https://wa.me/" + WHATSAPP_NUMBER +
                 "?text=Hi%20Hotel%20Green%20Plaza%2C%20I%27d%20like%20to%20make%20an%20enquiry.")

# Built from the verified street address rather than a confirmed place ID, so it
# resolves by address search. [VERIFY: Google Business Profile place link] —
# swap both of these for the hotel's own listing URL / embed once confirmed.
MAPS_QUERY = "Hotel+Green+Plaza,+Bhilwara+Chittor+Road,+NH+48,+Hamirgarh,+Bhilwara+311025,+Rajasthan"
MAPS_LINK = "https://www.google.com/maps/search/?api=1&amp;query=" + MAPS_QUERY
MAPS_EMBED = "https://maps.google.com/maps?q=" + MAPS_QUERY + "&amp;output=embed"


def phone_links(phones, sep=" &middot; "):
    return sep.join('<a href="tel:%s">%s</a>' % (t, label) for t, label in phones)


# ---------------------------------------------------------------------------
# Guest reviews — curated from hotel_greenplaza_1396_reviews.csv (the hotel's
# own exported Google/Tripadvisor reviews). 166 unique reviews after removing
# duplicate export rows; the aggregate score/count below are the hotel's
# current Google Business Profile figures, supplied directly by the hotel.
# Quotes are trimmed to a display length and lightly punctuated for
# readability; wording and sentiment are unedited and unfabricated.
# ---------------------------------------------------------------------------

AGGREGATE_RATING = "4.1"
AGGREGATE_COUNT = 2981
REVIEWS_SOURCE_LINK = "https://www.google.com/search?q=Hotel+Green+Plaza+Bhilwara+reviews"
# [VERIFY: Google Business Profile review link] — swap the line above for the
# hotel's own "See all reviews" short link once confirmed.

REVIEWS = [
    (5, "Abdul Hamid Shaikh", "Google",
     "Very good restaurant, pure veg, very clean, and the food quality is also good."),
    (5, "Shoeb Ansari", "Google",
     "Best ever hotel on this route. 100% safe for family stay, very good in behaviour. The food is always good."),
    (5, "SumithD_13", "Tripadvisor",
     "Lots of parking, and a very good place on the highway. Neat and clean restaurant and washrooms — it's pure vegetarian, and food was served fast and tasty."),
    (5, "Amogh Shenoy", "Google",
     "The room is quite good, and they also have a restaurant open till 3am. The food is good too — thanks to Musa Bhai for managing the hotel rooms."),
    (5, "Atul Soral", "Google",
     "Excellent tasty food at a reasonable price. Great service too."),
    (5, "Daksh Wankhade", "Google",
     "A self-sufficient place to stay for days. The staff and management here are great — they try to help you as much as possible."),
    (5, "Yuvraj Malik", "Google",
     "Nice garden and play area for kids, and the food quality is great. Big AC hall for parties too."),
    (4, "SRT2013", "Tripadvisor",
     "We stay here regularly — rooms are clean, location is good near the highway, and the food is very good."),
    (5, "ADITYA DHADIWAL", "Google",
     "Good to have a safe and comfortable stay when you're out on the road, and this place has 24/7 service."),
]


def initials(name):
    parts = [p for p in name.split() if p]
    letters = "".join(p[0] for p in parts[:2])
    return letters.upper()


def stars_markup(rating, size_cls=""):
    star = f'<svg class="gp-star{(" " + size_cls) if size_cls else ""}" aria-hidden="true"><use href="#gp-star"/></svg>'
    return star * int(round(rating))


def rating_badge_markup(rating, count):
    stars = ('<svg class="gp-star" aria-hidden="true"><use href="#gp-star"/></svg>' * 5)
    return f"""    <div class="gp-rating gp-reveal">
      <span class="gp-rating__score">{rating}</span>
      <div class="gp-rating__meta">
        <div class="gp-stars" style="--gp-rating:{rating};" role="img" aria-label="Rated {rating} out of 5">
          <div class="gp-stars__track">{stars}</div>
          <div class="gp-stars__fill">{stars}</div>
        </div>
        <p class="gp-small">Based on {count:,} Google reviews</p>
      </div>
    </div>"""


def testimonials_section():
    slides = "\n".join(f"""          <li class="gp-carousel__slide">
            <article class="gp-testimonial">
              <div class="gp-testimonial__stars">{stars_markup(rating)}</div>
              <p class="gp-testimonial__quote">&ldquo;{quote}&rdquo;</p>
              <div class="gp-testimonial__author">
                <span class="gp-testimonial__avatar" aria-hidden="true">{initials(name)}</span>
                <div>
                  <strong>{name}</strong>
                  <span class="gp-small">{platform} Review</span>
                </div>
              </div>
            </article>
          </li>""" for rating, name, platform, quote in REVIEWS)

    return f"""  <!-- ============================= TESTIMONIALS ============================= -->
  <section class="gp-section gp-bg-cream" id="reviews">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">Guest Reviews</span>
        <h2>What Our Guests Say</h2>
        <p>Real feedback from guests who have stayed, dined and celebrated with us in Bhilwara.</p>
      </div>

      <div class="gp-text-center">
{rating_badge_markup(AGGREGATE_RATING, AGGREGATE_COUNT)}
      </div>

      <div class="gp-carousel gp-reveal" role="region" aria-label="Guest review carousel" data-carousel>
        <div class="gp-carousel__viewport" tabindex="0">
          <ul class="gp-carousel__track">
{slides}
          </ul>
        </div>
        <div class="gp-carousel__nav">
          <button class="gp-carousel__btn gp-carousel__btn--prev" type="button" aria-label="Previous reviews">
            {icon('chevron-left', 'gp-icon--primary')}
          </button>
          <div class="gp-carousel__progress" aria-hidden="true">
            <span class="gp-carousel__progress-bar"></span>
          </div>
          <button class="gp-carousel__btn gp-carousel__btn--next" type="button" aria-label="Next reviews">
            {icon('chevron-right', 'gp-icon--primary')}
          </button>
        </div>
      </div>

      <div class="gp-text-center gp-mt-40">
        <a class="gp-btn gp-btn--secondary" href="{REVIEWS_SOURCE_LINK}" target="_blank" rel="noopener">Read More Reviews on Google</a>
      </div>
    </div>
  </section>
"""

NAV = [
    ("Home", "/"),
    ("About Us", "/about-us/"),
    ("Accommodation", "/accommodation/"),
    ("Restaurant", "/restaurant/"),
    ("Services", "/services/"),
    ("Banquets", "/banquets/"),
    ("Gallery", "/gallery/"),
    ("Contact Us", "/contact/"),
]

# --------------------------------------------------------------------------
# Icon sprite — one stroke set, 1.5px, used sitewide
# --------------------------------------------------------------------------

SPRITE = """<svg class="gp-sprite" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false"><defs>
<symbol id="gp-bed" viewBox="0 0 24 24"><path d="M3 18v-6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6"/><path d="M3 18h18"/><path d="M3 21v-3M21 21v-3"/><path d="M7 10V7h4v3"/></symbol>
<symbol id="gp-utensils" viewBox="0 0 24 24"><path d="M5 3v6a2 2 0 0 0 4 0V3"/><path d="M7 11v10"/><path d="M17.5 3c1.4 2 2 4.6 2 7.2 0 1.7-.8 2.8-2 2.8h-1V3z"/><path d="M16.5 13v8"/></symbol>
<symbol id="gp-users" viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></symbol>
<symbol id="gp-bell" viewBox="0 0 24 24"><path d="M8 20a4 4 0 0 0 8 0"/><path d="M6 20v-8a6 6 0 0 1 12 0v8"/><path d="M4 20h16"/><path d="M12 6V3"/></symbol>
<symbol id="gp-room-service" viewBox="0 0 24 24"><path d="M2 19h20"/><path d="M4 19a8 8 0 0 1 16 0"/><path d="M12 8V5.5"/><path d="M10 5.5h4"/></symbol>
<symbol id="gp-sparkles" viewBox="0 0 24 24"><path d="M11 3.5 12.6 8l4.4 1.6-4.4 1.6L11 15.6 9.4 11.2 5 9.6l4.4-1.6z"/><path d="M18 14.5l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8z"/></symbol>
<symbol id="gp-coffee" viewBox="0 0 24 24"><path d="M17 9h1a3.5 3.5 0 0 1 0 7h-1"/><path d="M3 9h14v8a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4z"/><path d="M6 2v3M10 2v3M14 2v3"/></symbol>
<symbol id="gp-fridge" viewBox="0 0 24 24"><rect x="5" y="2" width="14" height="20" rx="2"/><path d="M5 10h14"/><path d="M8.5 6v2M8.5 13v2.5"/></symbol>
<symbol id="gp-tv" viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="m7 2 5 4 5-4"/></symbol>
<symbol id="gp-laundry" viewBox="0 0 24 24"><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M4 7h16"/><path d="M7.5 4.5h.01M10.5 4.5h.01"/><circle cx="12" cy="14.5" r="4.5"/></symbol>
<symbol id="gp-car" viewBox="0 0 24 24"><path d="M4 15v-4l2-5h12l2 5v4"/><path d="M4 15h16"/><circle cx="7.5" cy="16.5" r="1.8"/><circle cx="16.5" cy="16.5" r="1.8"/><path d="M6 11h12"/></symbol>
<symbol id="gp-doctor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 8v8M8 12h8"/></symbol>
<symbol id="gp-conference" viewBox="0 0 24 24"><path d="M3 3h18v11a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/><path d="M12 15v3"/><path d="m9 21 3-3 3 3"/><path d="M8 11V8.5M12 11V6.5M16 11V9.5"/></symbol>
<symbol id="gp-pin" viewBox="0 0 24 24"><path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11z"/><circle cx="12" cy="9.7" r="2.5"/></symbol>
<symbol id="gp-phone" viewBox="0 0 24 24"><path d="M15.5 21A13.5 13.5 0 0 1 3 8.5 3 3 0 0 1 6 5.5h1.4a1 1 0 0 1 1 .8l.7 3a1 1 0 0 1-.3 1L7.5 11.6a11 11 0 0 0 4.9 4.9l1.3-1.3a1 1 0 0 1 1-.3l3 .7a1 1 0 0 1 .8 1V18a3 3 0 0 1-3 3z"/></symbol>
<symbol id="gp-mail" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 7 8.5 6 8.5-6"/></symbol>
<symbol id="gp-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5.3l3.2 1.9"/></symbol>
<symbol id="gp-check" viewBox="0 0 24 24"><path d="m4 12.5 5 5L20 6.5"/></symbol>
<symbol id="gp-arrow-right" viewBox="0 0 24 24"><path d="M4 12h15"/><path d="m13 6 6 6-6 6"/></symbol>
<symbol id="gp-iron" viewBox="0 0 24 24"><path d="M3 16a9 9 0 0 1 9-9h5a3 3 0 0 1 3 3v6H3z"/><path d="M3 19h18"/><path d="M14 7V4.5h-4"/></symbol>
<symbol id="gp-newspaper" viewBox="0 0 24 24"><path d="M4 5h13v14H4z"/><path d="M17 8h3v9a2 2 0 0 1-3 1.73"/><path d="M7 8.5h7M7 11.5h7M7 14.5h5"/></symbol>
<symbol id="gp-ticket" viewBox="0 0 24 24"><path d="M3 8a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v2a2 2 0 0 0 0 4v2a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-2a2 2 0 0 0 0-4z"/><path d="M13 6.5v2M13 11v2M13 15.5v2"/></symbol>
<symbol id="gp-briefcase" viewBox="0 0 24 24"><rect x="3" y="8" width="18" height="13" rx="2"/><path d="M9 8V6a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2"/><path d="M3 13h18"/></symbol>
<symbol id="gp-bath" viewBox="0 0 24 24"><path d="M3 12h18v3a5 5 0 0 1-5 5H8a5 5 0 0 1-5-5z"/><path d="M7 12V6a2 2 0 1 1 4 0v.5"/><path d="M6.5 20 5 22M17.5 20 19 22"/></symbol>
<symbol id="gp-ac" viewBox="0 0 24 24"><path d="M12 3v18"/><path d="m4.5 7.5 15 9"/><path d="m19.5 7.5-15 9"/><path d="M9.5 4.5 12 6l2.5-1.5M9.5 19.5 12 18l2.5 1.5"/></symbol>
<symbol id="gp-building" viewBox="0 0 24 24"><path d="M4 21V5a2 2 0 0 1 2-2h7a2 2 0 0 1 2 2v16"/><path d="M15 10h3a2 2 0 0 1 2 2v9"/><path d="M3 21h18"/><path d="M8 7h3M8 11h3M8 15h3"/></symbol>
<symbol id="gp-leaf" viewBox="0 0 24 24"><path d="M4 20c0-8.3 6-14.3 16-15 0 10.2-5.2 15-13 15z"/><path d="M4 20c3.2-4.3 6.3-6.7 9.5-7.8"/></symbol>
<symbol id="gp-calendar" viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="16" rx="2"/><path d="M8 3v4M16 3v4M4 10h16"/></symbol>
<symbol id="gp-navigation" viewBox="0 0 24 24"><path d="m3 11 18-8-8 18-2-8z"/></symbol>
<symbol id="gp-close" viewBox="0 0 24 24"><path d="m6 6 12 12M18 6 6 18"/></symbol>
<symbol id="gp-chevron-left" viewBox="0 0 24 24"><path d="m14 6-6 6 6 6"/></symbol>
<symbol id="gp-chevron-right" viewBox="0 0 24 24"><path d="m10 6 6 6-6 6"/></symbol>
<symbol id="gp-celebration" viewBox="0 0 24 24"><path d="m3 21 5.5-13L16 15.5z"/><path d="M15 3v2M20 5.5 18.5 7M21 11h-2"/><path d="M12.5 6.5 14 8"/></symbol>
<symbol id="gp-star" viewBox="0 0 24 24"><path d="M12 2.5l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.8-6.2 3.8 1.6-7-5.4-4.7 7.1-.6z"/></symbol>
<symbol id="gp-parking" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M9 17V7h4a3 3 0 0 1 0 6H9"/></symbol>
<symbol id="gp-shield" viewBox="0 0 24 24"><path d="M12 3l7 3v5c0 4.6-3 7.7-7 9-4-1.3-7-4.4-7-9V6z"/><path d="m9 12 2 2 4-4"/></symbol>
<symbol id="gp-tree" viewBox="0 0 24 24"><path d="M12 3 7 11h3l-4 6h12l-4-6h3z"/><path d="M12 17v4"/></symbol>
<symbol id="gp-scissors" viewBox="0 0 24 24"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.12 15.88"/><path d="M14.47 14.48 20 20"/><path d="M8.12 8.12 12 12"/></symbol>
<symbol id="gp-ice-cream" viewBox="0 0 24 24"><path d="M8 11a4 4 0 0 1 8 0"/><path d="M7.5 11h9l-4.5 10z"/><path d="M9.3 15h5.4"/></symbol>
<symbol id="gp-zap" viewBox="0 0 24 24"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></symbol>
<symbol id="gp-gift" viewBox="0 0 24 24"><path d="M4 12v9h16v-9"/><rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M12 8C10 8 7.5 7.2 7.5 5.2 7.5 4.1 8.3 3.5 9.1 3.5 11 3.5 12 6 12 8zM12 8c2 0 4.5-.8 4.5-2.8 0-1.1-.8-1.7-1.6-1.7C13 3.5 12 6 12 8z"/></symbol>
<symbol id="gp-water" viewBox="0 0 24 24"><path d="M12 3s6 6.4 6 10.5A6 6 0 0 1 6 13.5C6 9.4 12 3 12 3z"/></symbol>
<symbol id="gp-bulb" viewBox="0 0 24 24"><path d="M9.5 18h5"/><path d="M10 21h4"/><path d="M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.3 1 2.5h6c0-1.2.2-1.7 1-2.5A6 6 0 0 0 12 3z"/></symbol>
<symbol id="gp-whatsapp" viewBox="0 0 24 24"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.46 1.32 4.97L2 22l5.25-1.38c1.45.79 3.08 1.21 4.79 1.21 5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2zm0 18.15c-1.53 0-3.03-.41-4.34-1.19l-.31-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.14c0-4.54 3.7-8.23 8.24-8.23 4.54 0 8.23 3.69 8.23 8.23s-3.69 8.24-8.23 8.24zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.12-.16.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.43.12-.14.16-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.42-.56-.43-.14 0-.31-.01-.48-.01s-.43.06-.66.31c-.23.25-.87.85-.87 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.14-1.18-.06-.11-.22-.17-.47-.29z"/></symbol>
</defs></svg>"""


def icon(name, cls=""):
    extra = (" " + cls) if cls else ""
    return f'<svg class="gp-icon{extra}" aria-hidden="true"><use href="#gp-{name}"/></svg>'


# --------------------------------------------------------------------------
# Shared chrome
# --------------------------------------------------------------------------

CURRENT = ' aria-current="page"'


def header(active):
    links = "\n".join(
        '          <li><a class="gp-nav__link" href="%s"%s>%s</a></li>'
        % (url, CURRENT if url == active else "", label)
        for label, url in NAV
    )
    return f"""<header class="gp-header">

  <!-- Contact strip: holds the phone, email and location so the main bar
       carries only the logo, the menu and one call to action. -->
  <div class="gp-topbar">
    <div class="container">
      <div class="gp-topbar__inner">
        <div class="gp-topbar__group">
          <span class="gp-topbar__item gp-topbar__location">
            {icon('pin', 'gp-icon--sm')}
            {BHILWARA['short']}, {BHILWARA['region']} {BHILWARA['postal']}
          </span>
        </div>
        <div class="gp-topbar__group">
          <a class="gp-topbar__phone" href="tel:{PRIMARY_TEL}">
            {icon('phone', 'gp-icon--sm')}
            <span class="gp-sr-only">Call us: </span>{PRIMARY_TEL_LABEL}
          </a>
          <a href="mailto:{BHILWARA['email']}">
            {icon('mail', 'gp-icon--sm')}
            {BHILWARA['email']}
          </a>
        </div>
      </div>
    </div>
  </div>

  <div class="container">
    <div class="gp-header__inner">

      <a class="gp-logo" href="/" aria-label="Hotel Green Plaza — home">
        <img src="/assets/img/logo/hotel-green-plaza-logo.png" width="108" height="62" alt="Hotel Green Plaza and Restaurant logo">
      </a>

      <nav class="gp-nav" aria-label="Main">
        <ul class="gp-nav__list">
{links}
        </ul>
      </nav>

      <div class="gp-header__actions">
        <a class="gp-btn gp-btn--primary" href="/contact/#enquiry">Book / Enquire</a>
        <button class="gp-burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="gp-mobile-panel">
          <span></span>
        </button>
      </div>

    </div>
  </div>
</header>"""


def mobile_panel(active):
    links = "\n".join(
        '    <a href="%s"%s>%s</a>' % (url, CURRENT if url == active else "", label)
        for label, url in NAV
    )
    return f"""<div class="gp-mobile-panel" id="gp-mobile-panel" role="dialog" aria-modal="true" aria-label="Site menu" aria-hidden="true">
  <div class="gp-mobile-panel__top">
    <img src="/assets/img/logo/hotel-green-plaza-logo.png" width="96" height="55" alt="Hotel Green Plaza and Restaurant logo">
    <button class="gp-panel-close" type="button" aria-label="Close menu">
      {icon('close', 'gp-icon--primary')}
    </button>
  </div>
  <nav class="gp-mobile-panel__list" aria-label="Mobile">
{links}
  </nav>
  <div class="gp-mobile-panel__foot">
    <a class="gp-btn gp-btn--primary gp-btn--block" href="/contact/#enquiry">Book / Enquire Now</a>
    <a class="gp-btn gp-btn--secondary gp-btn--block" href="tel:{PRIMARY_TEL}">Call {PRIMARY_TEL_LABEL}</a>
    <a class="gp-btn gp-btn--secondary gp-btn--block" href="{WHATSAPP_LINK}" target="_blank" rel="noopener">WhatsApp Us</a>
    <p class="gp-small gp-mb-0">
      <a href="mailto:{BHILWARA['email']}">{BHILWARA['email']}</a><br>
      {BHILWARA['short']}, {BHILWARA['region']} {BHILWARA['postal']}
    </p>
  </div>
</div>"""


FOOTER = f"""<footer class="gp-footer">
  <div class="container">
    <div class="row gp-gap-30">

      <div class="col-12 col-md-6 col-lg-3">
        <!-- The logo is never recoloured; on dark it sits on a white contrast plate -->
        <span class="gp-footer__logo">
          <img src="/assets/img/logo/hotel-green-plaza-logo.png" width="128" height="74" alt="Hotel Green Plaza and Restaurant logo">
        </span>
        <p>Comfortable stays, pure vegetarian dining, banquet facilities and dependable hospitality in Bhilwara.</p>
      </div>

      <div class="col-12 col-md-6 col-lg-3">
        <h3>Quick Links</h3>
        <nav class="gp-footer__links" aria-label="Footer">
{chr(10).join(f'          <a href="{u}">{l}</a>' for l, u in NAV)}
        </nav>
      </div>

      <div class="col-12 col-md-6 col-lg-3">
        <h3>Guest Services</h3>
        <div class="gp-footer__links">
          <a href="/contact/#enquiry">Room Enquiries</a>
          <a href="/contact/#enquiry">Restaurant Enquiries</a>
          <a href="/contact/#enquiry">Banquet Enquiries</a>
          <a href="/contact/#enquiry">General Enquiries</a>
        </div>
      </div>

      <div class="col-12 col-md-6 col-lg-3">
        <h3>Contact</h3>
        <ul class="gp-footer__contact">
          <li>
            {icon('pin', 'gp-icon--sm')}
            <span>{BHILWARA['html']}</span>
          </li>
          <li>
            {icon('phone', 'gp-icon--sm')}
            <span>{phone_links(BHILWARA['phones'], '<br>')}</span>
          </li>
          <li>
            {icon('mail', 'gp-icon--sm')}
            <a href="mailto:{BHILWARA['email']}">{BHILWARA['email']}</a>
          </li>
          <li>
            {icon('navigation', 'gp-icon--sm')}
            <a href="/contact/">Map / Directions</a>
          </li>
        </ul>
      </div>

    </div>
  </div>

  <div class="gp-footer__bottom">
    <div class="container">
      <p>&copy; <span class="gp-year">2026</span> Hotel Green Plaza. All Rights Reserved.</p>
      <p>Bhilwara, Rajasthan, India</p>
    </div>
  </div>
</footer>"""


ACTIONBAR = f"""<nav class="gp-actionbar" aria-label="Quick actions">
  <a href="tel:{PRIMARY_TEL}">
    {icon('phone', 'gp-icon--sm gp-icon--primary')}
    Call
  </a>
  <a class="gp-actionbar__wa" href="{WHATSAPP_LINK}" target="_blank" rel="noopener">
    {icon('whatsapp', 'gp-icon--sm gp-icon--fill')}
    WhatsApp
  </a>
  <a href="/contact/#enquiry">
    {icon('calendar', 'gp-icon--sm')}
    Book
  </a>
</nav>"""

# Floating WhatsApp button — shown on desktop / tablet (mobile uses the action bar)
FAB = f"""<a class="gp-fab" href="{WHATSAPP_LINK}" target="_blank" rel="noopener" aria-label="Chat with Hotel Green Plaza on WhatsApp">
  {icon('whatsapp', 'gp-icon--fill')}
  <span class="gp-fab__label">WhatsApp Us</span>
</a>"""


LIGHTBOX = f"""<div class="gp-lightbox" role="dialog" aria-modal="true" aria-label="Image viewer" aria-hidden="true">
  <button class="gp-lightbox__btn gp-lightbox__close" type="button" aria-label="Close image viewer">
    {icon('close')}
  </button>
  <button class="gp-lightbox__btn gp-lightbox__prev" type="button" aria-label="Previous image">
    {icon('chevron-left')}
  </button>
  <button class="gp-lightbox__btn gp-lightbox__next" type="button" aria-label="Next image">
    {icon('chevron-right')}
  </button>
  <figure class="gp-lightbox__figure">
    <img class="gp-lightbox__image" alt="">
    <figcaption class="gp-lightbox__caption"></figcaption>
  </figure>
</div>"""


SCHEMA_NOTE = """<!--
  Address, phone and email come from the hotel's own business card.
  Still outstanding:
  [VERIFY: geo coordinates] — add "geo": { "@type": "GeoCoordinates", "latitude": …, "longitude": … }.
  [VERIFY: restaurant timings] — add "openingHoursSpecification" to the Restaurant node.
  Do not publish either until the hotel confirms them.
-->"""

HOTEL_SCHEMA = """    {
      "@type": ["Hotel", "LocalBusiness"],
      "@id": "%(site)s/#hotel",
      "name": "Hotel Green Plaza",
      "url": "%(site)s/",
      "image": "%(site)s/assets/img/general/hotel-green-plaza-bhilwara-share.jpg",
      "description": "Hotel Green Plaza offers comfortable accommodation, pure vegetarian dining, banquet facilities and essential hotel services in Bhilwara, Rajasthan.",
      "telephone": "+918107367300",
      "email": "hotelgreenplazaindia@gmail.com",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Bhilwara Chittor Road, N.H. 48, Hawai Patti ke Pass, Vill. Takhatpura, Tehsil Hamirgarh",
        "addressLocality": "Bhilwara",
        "addressRegion": "Rajasthan",
        "postalCode": "311025",
        "addressCountry": "IN"
      },
      "amenityFeature": [
        { "@type": "LocationFeatureSpecification", "name": "24-hour room service", "value": true },
        { "@type": "LocationFeatureSpecification", "name": "24/7 front desk", "value": true },
        { "@type": "LocationFeatureSpecification", "name": "Housekeeping", "value": true },
        { "@type": "LocationFeatureSpecification", "name": "Pure vegetarian multi-cuisine restaurant", "value": true },
        { "@type": "LocationFeatureSpecification", "name": "Banquet facilities", "value": true },
        { "@type": "LocationFeatureSpecification", "name": "Doctor on call", "value": true },
        { "@type": "LocationFeatureSpecification", "name": "Same-day laundry service", "value": true },
        { "@type": "LocationFeatureSpecification", "name": "Car rental", "value": true },
        { "@type": "LocationFeatureSpecification", "name": "Electric-vehicle charging station", "value": true },
        { "@type": "LocationFeatureSpecification", "name": "Free on-site parking", "value": true },
        { "@type": "LocationFeatureSpecification", "name": "24-hour security and CCTV", "value": true },
        { "@type": "LocationFeatureSpecification", "name": "On-site saloon", "value": true },
        { "@type": "LocationFeatureSpecification", "name": "Ice cream parlor", "value": true },
        { "@type": "LocationFeatureSpecification", "name": "Children's park and garden", "value": true }
      ],
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "%(rating)s",
        "reviewCount": "%(count)s",
        "bestRating": "5",
        "worstRating": "1"
      }
    }""" % {"site": SITE, "rating": AGGREGATE_RATING, "count": AGGREGATE_COUNT}

RESTAURANT_SCHEMA = """    {
      "@type": "Restaurant",
      "@id": "%(site)s/restaurant/#restaurant",
      "name": "Hotel Green Plaza Restaurant",
      "url": "%(site)s/restaurant/",
      "image": "%(site)s/assets/img/general/hotel-green-plaza-restaurant.webp",
      "servesCuisine": ["North Indian", "Punjabi", "Chinese", "South Indian", "Pure Vegetarian"],
      "priceRange": "₹₹",
      "hasMenu": "%(site)s/restaurant/#menu",
      "telephone": "+918107367300",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Bhilwara Chittor Road, N.H. 48, Hawai Patti ke Pass, Vill. Takhatpura, Tehsil Hamirgarh",
        "addressLocality": "Bhilwara",
        "addressRegion": "Rajasthan",
        "postalCode": "311025",
        "addressCountry": "IN"
      }
    }""" % {"site": SITE}


def breadcrumb_schema(title, url):
    return """    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "%(site)s/" },
        { "@type": "ListItem", "position": 2, "name": "%(title)s", "item": "%(site)s%(url)s" }
      ]
    }""" % {"site": SITE, "title": title, "url": url}


def page(url, title, description, body, og_image, hero_preload=None,
         crumb=None, extra_schema=None):
    canonical = SITE + url
    nodes = [
        """    {
      "@type": "WebSite",
      "@id": "%(site)s/#website",
      "url": "%(site)s/",
      "name": "Hotel Green Plaza",
      "inLanguage": "en-IN"
    }""" % {"site": SITE},
        HOTEL_SCHEMA,
    ]
    if extra_schema:
        nodes.extend(extra_schema)
    if crumb:
        nodes.append(breadcrumb_schema(crumb, url))

    preload = ""
    if hero_preload:
        preload = '\n<link rel="preload" as="image" fetchpriority="high" href="%s">' % hero_preload

    schema_nodes = ",\n".join(nodes)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<!-- Domain from the hotel's business card. [VERIFY: www vs non-www + HTTPS] — canonical, Open Graph and sitemap URLs all use {SITE}/ -->

<meta property="og:type" content="website">
<meta property="og:site_name" content="Hotel Green Plaza">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}{og_image}">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE}{og_image}">

<meta name="theme-color" content="#2f5d32">
<link rel="icon" href="/assets/img/logo/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/img/logo/apple-touch-icon.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&amp;family=Playfair+Display:wght@600&amp;display=swap">{preload}
<link rel="stylesheet" href="/assets/css/style.css?v={CSS_VER}">
<noscript>
  <!-- Scroll reveal is progressive enhancement: without JS everything is simply visible -->
  <style>.gp-reveal{{opacity:1;transform:none}}.gp-map__poster{{cursor:default}}</style>
</noscript>

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
{schema_nodes}
  ]
}}
</script>
{SCHEMA_NOTE}
</head>

<body>

<a class="gp-skip-link" href="#main">Skip to main content</a>

{SPRITE}

{header(url)}

{mobile_panel(url)}

<main id="main">
{body}
</main>

{FOOTER}

{ACTIONBAR}

{FAB}

{LIGHTBOX}

<script src="/assets/js/main.js?v={JS_VER}" defer></script>
</body>
</html>
"""


def banner(title, intro, crumb, img, alt):
    return f"""  <!-- ============================= PAGE BANNER ============================= -->
  <section class="gp-banner">
    <div class="gp-banner__media">
      <!-- PLACEHOLDER 1920×760 — replace with a real photograph at the same size -->
      <img src="{img}" width="1920" height="760" fetchpriority="high" alt="{alt}">
    </div>
    <div class="container">
      <h1>{title}</h1>
      <p>{intro}</p>
      <nav aria-label="Breadcrumb">
        <ol class="gp-breadcrumb">
          <li><a href="/">Home</a></li>
          <li><span aria-current="page">{crumb}</span></li>
        </ol>
      </nav>
    </div>
  </section>
"""


def cta_band():
    return f"""  <!-- ============================= CTA BAND ============================= -->
  <section class="gp-cta gp-on-dark">
    <div class="gp-cta__media">
      <!-- PLACEHOLDER 1920×700 — replace with a wide property photograph -->
      <img src="/assets/img/hero/hotel-green-plaza-cta-band.webp" width="1920" height="700" loading="lazy" alt="Hotel Green Plaza in Bhilwara">
    </div>
    <div class="container">
      <div class="gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">Get in Touch</span>
        <h2>Planning Your Stay or Event in Bhilwara?</h2>
        <p>Whether you need a comfortable room, a vegetarian dining experience or a venue for your next gathering, Hotel Green Plaza is here to help.</p>
        <div class="gp-btn-group gp-btn-group--center gp-mt-32">
          <a class="gp-btn gp-btn--primary" href="/contact/#enquiry">Book Your Stay</a>
          <a class="gp-btn gp-btn--ghost" href="/banquets/">Plan Your Event</a>
        </div>
      </div>
    </div>
  </section>
"""


def location_section(bg="gp-bg-cream"):
    return f"""  <!-- ============================= LOCATION ============================= -->
  <section class="gp-section {bg}">
    <div class="container">
      <div class="row gp-split">
        <div class="col-12 col-lg-5">
          <div class="gp-reveal">
            <span class="gp-eyebrow">Location</span>
            <h2>Find Us in Bhilwara</h2>
            <p>Hotel Green Plaza is located in Bhilwara, Rajasthan. Get in touch for directions or any assistance planning your visit.</p>

            <ul class="gp-contact-list gp-mt-32">
              <li class="gp-contact-item">
                <span class="gp-contact-item__icon">{icon('pin')}</span>
                <div>
                  <h3>Address</h3>
                  <p>{BHILWARA['html']}</p>
                </div>
              </li>
              <li class="gp-contact-item">
                <span class="gp-contact-item__icon">{icon('phone')}</span>
                <div>
                  <h3>Phone</h3>
                  <p>{phone_links(BHILWARA['phones'], '<br>')}</p>
                </div>
              </li>
            </ul>

            <div class="gp-mt-32">
              <a class="gp-btn gp-btn--secondary" href="{MAPS_LINK}" target="_blank" rel="noopener">Get Directions</a>
            </div>
          </div>
        </div>

        <div class="col-12 col-lg-7">
          <div class="gp-map gp-reveal">
            <!-- The embed loads only when a guest asks for it, so it never blocks first paint. -->
            <button class="gp-map__poster" type="button"
                    data-src="{MAPS_EMBED}"
                    data-title="Map showing Hotel Green Plaza, Bhilwara">
              <span>
                <strong>Hotel Green Plaza, Bhilwara</strong>
                <p>{BHILWARA['short']}, {BHILWARA['region']} {BHILWARA['postal']}<br>Tap to load the map</p>
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
"""


def enquiry_form(default_type=""):
    def opt(value):
        sel = ' selected' if value == default_type else ''
        return f'              <option value="{value}"{sel}>{value}</option>'

    return f"""            <form class="gp-form" action="/enquiry.php" method="post" novalidate>
              <div class="gp-hp" aria-hidden="true">
                <label for="gp-enq-website">Leave this field empty</label>
                <input type="text" id="gp-enq-website" name="website" tabindex="-1" autocomplete="off">
              </div>

              <div class="gp-field">
                <label for="gp-enq-name">Full Name <span class="gp-req" aria-hidden="true">*</span></label>
                <input type="text" id="gp-enq-name" name="name" autocomplete="name" data-label="Full name" required>
                <span class="gp-error" aria-live="polite"></span>
              </div>

              <div class="gp-field">
                <label for="gp-enq-phone">Phone Number <span class="gp-req" aria-hidden="true">*</span></label>
                <input type="tel" id="gp-enq-phone" name="phone" autocomplete="tel" data-label="Phone number" required>
                <span class="gp-error" aria-live="polite"></span>
              </div>

              <div class="gp-field">
                <label for="gp-enq-email">Email Address <span class="gp-req" aria-hidden="true">*</span></label>
                <input type="email" id="gp-enq-email" name="email" autocomplete="email" data-label="Email address" required>
                <span class="gp-error" aria-live="polite"></span>
              </div>

              <div class="gp-field">
                <label for="gp-enq-type">Enquiry Type <span class="gp-req" aria-hidden="true">*</span></label>
                <select id="gp-enq-type" name="enquiry_type" data-label="Enquiry type" required>
                  <option value="">Please choose…</option>
{opt('Room Booking')}
{opt('Restaurant')}
{opt('Banquet / Event')}
{opt('General Enquiry')}
                </select>
                <span class="gp-error" aria-live="polite"></span>
              </div>

              <div class="gp-field">
                <label for="gp-enq-checkin">Check-in Date</label>
                <input type="date" id="gp-enq-checkin" name="checkin" data-label="Check-in date">
                <span class="gp-error" aria-live="polite"></span>
              </div>

              <div class="gp-field">
                <label for="gp-enq-checkout">Check-out Date</label>
                <input type="date" id="gp-enq-checkout" name="checkout" data-label="Check-out date">
                <span class="gp-error" aria-live="polite"></span>
              </div>

              <div class="gp-field gp-field--full">
                <label for="gp-enq-guests">Number of Guests</label>
                <input type="number" id="gp-enq-guests" name="guests" min="1" max="60" inputmode="numeric" data-label="Number of guests">
                <span class="gp-error" aria-live="polite"></span>
              </div>

              <div class="gp-field gp-field--full">
                <label for="gp-enq-message">Message <span class="gp-req" aria-hidden="true">*</span></label>
                <textarea id="gp-enq-message" name="message" data-label="Message" required></textarea>
                <span class="gp-error" aria-live="polite"></span>
              </div>

              <p class="gp-form__note">Fields marked <span class="gp-req">*</span> are required. We use your details only to respond to this enquiry.</p>

              <p class="gp-form__status" hidden></p>

              <div class="gp-field gp-field--full">
                <button class="gp-btn gp-btn--primary" type="submit">Send Enquiry</button>
              </div>
            </form>"""


# --------------------------------------------------------------------------
# Page bodies
# --------------------------------------------------------------------------

def home_body():
    highlights = [
        ("Comfortable Rooms",
         "Well-furnished rooms with essential facilities designed for business travellers, families and holidaymakers.",
         "View Rooms", "/accommodation/",
         "/assets/img/general/hotel-green-plaza-comfortable-rooms.webp",
         "Well-furnished guest room at Hotel Green Plaza"),
        ("Pure Vegetarian Dining",
         "Enjoy a selection of delicious vegetarian dishes in a warm and comfortable restaurant setting.",
         "Explore Restaurant", "/restaurant/",
         "/assets/img/general/hotel-green-plaza-restaurant.webp",
         "Pure vegetarian restaurant at Hotel Green Plaza"),
        ("Banquets &amp; Events",
         "Suitable spaces for functions, gatherings, conferences, meetings and other events.",
         "Explore Banquets", "/banquets/",
         "/assets/img/general/hotel-green-plaza-banquet-hall.webp",
         "Banquet hall at Hotel Green Plaza"),
        ("Guest Services",
         "A range of services designed to make your stay convenient and comfortable.",
         "View Services", "/services/",
         "/assets/img/general/hotel-green-plaza-guest-services.webp",
         "Front desk and guest services at Hotel Green Plaza"),
    ]

    cards = "\n".join(f"""        <div class="col-12 col-sm-6 col-lg-3">
          <article class="gp-card gp-card--facility gp-reveal">
            <div class="gp-card__media">
              <!-- PLACEHOLDER 900×600 (3:2) — replace with a real photograph -->
              <img src="{img}" width="900" height="600" loading="lazy" alt="{alt}">
            </div>
            <div class="gp-card__body">
              <h3>{h}</h3>
              <p>{p}</p>
              <a class="gp-textlink" href="{href}">{cta}
                {icon('arrow-right', 'gp-icon--sm gp-icon--primary')}
              </a>
            </div>
          </article>
        </div>""" for h, p, cta, href, img, alt in highlights)

    trust = [
        ("bed", "Comfortable accommodation"),
        ("leaf", "Pure vegetarian dining"),
        ("users", "Banquet facilities"),
        ("bell", "Essential guest services"),
        ("clock", "24-hour room service"),
        ("briefcase", "Business and leisure suitability"),
    ]
    trust_items = "\n".join(
        f'        <li class="gp-trust__item">{icon(n, "gp-icon--lg")}<span>{t}</span></li>'
        for n, t in trust)

    amenities = [
        ("bell", "24/7 front desk"), ("sparkles", "Housekeeping"),
        ("room-service", "Room service"), ("utensils", "Lobby-level restaurant"),
        ("doctor", "Doctor on call"), ("laundry", "Same-day laundry service"),
        ("car", "Car rental"), ("zap", "EV charging station"),
        ("parking", "Vehicle parking"), ("shield", "24-hour security &amp; CCTV"),
        ("scissors", "Saloon"), ("ice-cream", "Ice cream parlor"),
        ("tree", "Children's park &amp; garden"), ("coffee", "In-room tea / coffee maker"),
        ("fridge", "Refrigerator"), ("tv", "In-room cable television"),
    ]
    amenity_items = "\n".join(
        f'        <li class="gp-amenity gp-reveal">{icon(n)}{t}</li>' for n, t in amenities)

    gallery = [
        ("exterior-view", 900, 675, "Hotel Green Plaza exterior in Bhilwara", "Hotel exterior"),
        ("guest-room-interior", 900, 1200, "Well-furnished guest room at Hotel Green Plaza", "Guest room"),
        ("restaurant-seating", 900, 675, "Pure vegetarian restaurant at Hotel Green Plaza", "Restaurant seating"),
        ("banquet-hall-setup", 900, 675, "Banquet hall at Hotel Green Plaza", "Banquet hall"),
        ("main-entrance", 900, 1200, "Main entrance of Hotel Green Plaza", "Main entrance"),
        ("lobby-seating", 900, 675, "Lobby seating area at Hotel Green Plaza", "Lobby seating"),
    ]
    gallery_items = "\n".join(f"""        <div class="gp-masonry__item gp-reveal">
          <button class="gp-thumb" type="button" aria-label="View larger image: {alt}">
            <img src="/assets/img/gallery/hotel-green-plaza-{slug}.webp" width="{w}" height="{h}" loading="lazy" alt="{alt}">
            <span class="gp-thumb__label">{label}</span>
          </button>
        </div>""" for slug, w, h, alt, label in gallery)

    return f"""  <!-- ============================== HERO ============================== -->
  <section class="gp-hero">
    <div class="gp-hero__media">
      <!-- Real photograph of the Hotel Green Plaza Bhilwara exterior -->
      <img src="/assets/img/hero/hotel-green-plaza-bhilwara-exterior.webp" width="1920" height="1080" fetchpriority="high" alt="Hotel Green Plaza exterior in Bhilwara at night">
    </div>
    <div class="container">
      <div class="gp-hero__content">
        <span class="gp-eyebrow">Bhilwara &middot; NH-48 &middot; 100% Pure Veg</span>
        <h1>Comfortable Rooms, Pure-Veg Dining, Warm Hospitality</h1>
        <p>A family-friendly hotel, restaurant and banquet venue on the Bhilwara&ndash;Chittor highway &mdash; with 24-hour room service, parking, EV charging and a pure vegetarian kitchen.</p>
        <div class="gp-btn-group">
          <a class="gp-btn gp-btn--primary" href="/contact/#enquiry">Book Your Stay</a>
          <a class="gp-btn gp-btn--ghost" href="/about-us/">Explore Hotel</a>
        </div>
        <div class="gp-hero__trust">
          <span class="gp-hero__trust-item">
            <svg class="gp-star" aria-hidden="true"><use href="#gp-star"/></svg>
            {AGGREGATE_RATING} rating
          </span>
          <span class="gp-hero__trust-sep" aria-hidden="true"></span>
          <span class="gp-hero__trust-item">{AGGREGATE_COUNT:,} Google reviews</span>
          <span class="gp-hero__trust-badge">100% Pure Vegetarian</span>
        </div>
      </div>
    </div>
  </section>

  <!-- ============================= WELCOME ============================= -->
  <section class="gp-section gp-bg-white">
    <div class="container">
      <div class="row gp-split">
        <div class="col-12 col-lg-5">
          <div class="gp-split__media gp-reveal">
            <!-- PLACEHOLDER 1000×1250 (4:5) — replace with the hotel lobby photograph -->
            <img src="/assets/img/general/hotel-green-plaza-lobby.webp" width="1000" height="1250" loading="lazy" alt="Lobby at Hotel Green Plaza in Bhilwara">
            <span class="gp-split__mark" aria-hidden="true">{icon('leaf')}</span>
          </div>
        </div>
        <div class="col-12 col-lg-7">
          <div class="gp-reveal">
            <span class="gp-eyebrow">Welcome</span>
            <h2>Welcome to Hotel Green Plaza</h2>
            <p>Hotel Green Plaza offers a comfortable and convenient stay in Bhilwara, with well-appointed rooms, a pure vegetarian multi-cuisine restaurant, banquet facilities and a range of essential hotel services.</p>
            <p>Whether you are visiting for business, a family trip, a holiday or a special occasion, our focus is on providing a welcoming environment and a comfortable experience.</p>
            <hr class="gp-rule">
            <a class="gp-btn gp-btn--secondary" href="/about-us/">Discover Hotel Green Plaza</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ========================== KEY HIGHLIGHTS ========================== -->
  <section class="gp-section gp-bg-cream">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">What We Offer</span>
        <h2>Stay, Dine and Celebrate</h2>
        <p>Four parts of Hotel Green Plaza, each built around the same idea — a comfortable, dependable experience in Bhilwara.</p>
      </div>

      <div class="row gp-gap-30">
{cards}
      </div>
    </div>
  </section>

  <!-- ============================ TRUST BAND ============================ -->
  <section class="gp-trust gp-on-dark">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-mb-0 gp-reveal">
        <span class="gp-eyebrow">Why Guests Choose Us</span>
        <h2>A Comfortable Choice for Your Stay in Bhilwara</h2>
      </div>

      <ul class="gp-trust__grid">
{trust_items}
      </ul>
    </div>
  </section>

  <!-- ========================= RESTAURANT TEASER ========================= -->
  <section class="gp-section gp-bg-white">
    <div class="container">
      <div class="row gp-split">
        <div class="col-12 col-lg-6">
          <div class="gp-reveal">
            <span class="gp-eyebrow">Restaurant</span>
            <h2>Pure Vegetarian Multi-Cuisine Dining</h2>
            <p>Hotel Green Plaza features a lobby-level multi-cuisine restaurant with warm wooden interiors and a pure vegetarian menu.</p>
            <ul class="gp-feature-list">
              <li>{icon('check', 'gp-icon--sm')}<span>Pure vegetarian restaurant</span></li>
              <li>{icon('check', 'gp-icon--sm')}<span>Multi-cuisine menu</span></li>
              <li>{icon('check', 'gp-icon--sm')}<span>Warm and comfortable interiors</span></li>
              <li>{icon('check', 'gp-icon--sm')}<span>Lobby-level location</span></li>
            </ul>
            <a class="gp-btn gp-btn--secondary" href="/restaurant/">Explore Restaurant</a>
          </div>
        </div>
        <div class="col-12 col-lg-6">
          <div class="gp-split__media gp-reveal">
            <!-- PLACEHOLDER 1100×733 (3:2) — replace with a real food photograph -->
            <img src="/assets/img/general/hotel-green-plaza-vegetarian-thali.webp" width="1100" height="733" loading="lazy" alt="Vegetarian dishes served at the restaurant of Hotel Green Plaza">
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ========================== BANQUET TEASER ========================== -->
  <section class="gp-section gp-bg-cream">
    <div class="container">
      <div class="row gp-split">
        <div class="col-12 col-lg-6">
          <div class="gp-split__media gp-reveal">
            <!-- PLACEHOLDER 1100×733 (3:2) — replace with a real banquet / event photograph -->
            <img src="/assets/img/general/hotel-green-plaza-banquet-event-setup.webp" width="1100" height="733" loading="lazy" alt="Banquet hall set up for an event at Hotel Green Plaza">
          </div>
        </div>
        <div class="col-12 col-lg-6">
          <div class="gp-reveal">
            <span class="gp-eyebrow">Banquets &amp; Events</span>
            <h2>Spaces for Every Occasion</h2>
            <p>Hotel Green Plaza offers banquet facilities in Bhilwara suitable for functions, gatherings, conferences, business meetings and a wide range of events.</p>
            <hr class="gp-rule">
            <div class="gp-btn-group">
              <a class="gp-btn gp-btn--primary" href="/banquets/">Plan Your Event</a>
              <a class="gp-btn gp-btn--secondary" href="/contact/#enquiry">Enquire About Banquets</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- =========================== AMENITIES GRID =========================== -->
  <section class="gp-section gp-bg-tint">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">Services &amp; Amenities</span>
        <h2>Everything You Need for a Comfortable Stay</h2>
        <p>Hotel Green Plaza offers a range of services designed to make every stay more convenient and comfortable.</p>
      </div>

      <ul class="gp-amenity-grid">
{amenity_items}
      </ul>

      <div class="gp-text-center gp-mt-40">
        <a class="gp-btn gp-btn--secondary" href="/services/">View All Services</a>
      </div>
    </div>
  </section>

  <!-- ========================== GALLERY PREVIEW ========================== -->
  <section class="gp-section gp-bg-white">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">Gallery</span>
        <h2>A Look Around the Hotel</h2>
        <p>Rooms, restaurant, banquet spaces and the property itself.</p>
      </div>

      <div class="gp-masonry">
{gallery_items}
      </div>

      <div class="gp-text-center gp-mt-40">
        <a class="gp-btn gp-btn--secondary" href="/gallery/">View Gallery</a>
      </div>
    </div>
  </section>

{testimonials_section()}
{location_section('gp-bg-white')}
{cta_band()}"""


def about_body():
    services = [
        ("bed", "Accommodation", "Well-appointed rooms with AC and Non-AC options, attached bathrooms, digital television and 24-hour room service."),
        ("utensils", "Restaurant", "A lobby-level multi-cuisine restaurant with warm wooden interiors and a pure vegetarian menu."),
        ("users", "Banquets", "Banquet facilities suitable for functions, gatherings, conferences, business meetings and a wide range of events."),
        ("bell", "Guest Services", "A 24/7 front desk, housekeeping, room service, doctor on call, laundry, car rental with EV charging, an in-house saloon, an ice cream parlor and a children's garden."),
    ]
    service_cards = "\n".join(f"""        <div class="col-12 col-sm-6 col-lg-3">
          <article class="gp-service gp-reveal">
            <span class="gp-service__icon">{icon(n)}</span>
            <h3>{t}</h3>
            <p>{d}</p>
          </article>
        </div>""" for n, t, d in services)

    amenities = [
        ("coffee", "In-room tea / coffee maker"), ("fridge", "Refrigerator"),
        ("iron", "Iron and ironing board on request"), ("phone", "Direct dialing from the room"),
        ("tv", "In-room cable television"), ("newspaper", "Newspaper"),
    ]
    amenity_items = "\n".join(
        f'        <li class="gp-amenity gp-reveal">{icon(n)}{t}</li>' for n, t in amenities)

    return banner(
        "About Hotel Green Plaza",
        "A comfortable hotel in Bhilwara offering accommodation, pure vegetarian dining, banquet facilities and a range of guest services.",
        "About Us",
        "/assets/img/hero/hotel-green-plaza-about-banner.webp",
        "Hotel Green Plaza exterior in Bhilwara",
    ) + f"""
  <!-- =========================== INTRODUCTION =========================== -->
  <section class="gp-section gp-bg-white">
    <div class="container">
      <div class="row gp-split">
        <div class="col-12 col-lg-7">
          <div class="gp-reveal">
            <span class="gp-eyebrow">Introduction</span>
            <h2>A Welcoming Hotel in Bhilwara</h2>
            <p>Hotel Green Plaza is a comfortable hotel in Bhilwara offering accommodation, pure vegetarian dining, banquet facilities and a range of guest services.</p>
            <p>Our focus is on providing a welcoming environment, practical amenities and dependable hospitality for business travellers, families, holidaymakers and event guests.</p>
          </div>
        </div>
        <div class="col-12 col-lg-5">
          <div class="gp-split__media gp-reveal">
            <!-- PLACEHOLDER 1000×1250 (4:5) — replace with a real property photograph -->
            <img src="/assets/img/general/hotel-green-plaza-hospitality.webp" width="1000" height="1250" loading="lazy" alt="Hotel Green Plaza in Bhilwara">
            <span class="gp-split__mark" aria-hidden="true">{icon('leaf')}</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ========================== OUR HOSPITALITY ========================== -->
  <section class="gp-trust gp-on-dark">
    <div class="container">
      <div class="gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">Our Hospitality</span>
        <h2>Our priority is your comfort.</h2>
        <p>From comfortable rooms and room service to dining and event facilities, Hotel Green Plaza is designed to provide the essential conveniences guests need during their stay.</p>
      </div>
    </div>
  </section>

  <!-- ============================ WHAT WE OFFER ============================ -->
  <section class="gp-section gp-bg-white">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">What We Offer</span>
        <h2>Four Parts of One Hotel</h2>
        <p>Accommodation, dining, events and everyday guest services — all under the same roof in Bhilwara.</p>
      </div>

      <div class="row gp-gap-30">
{service_cards}
      </div>
    </div>
  </section>

  <!-- ============================= AMENITIES ============================= -->
  <section class="gp-section gp-bg-tint">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">Amenities</span>
        <h2>In-Room Comforts</h2>
        <p>Practical amenities provided to make everyday stays easier.</p>
      </div>

      <ul class="gp-amenity-grid">
{amenity_items}
      </ul>

      <p class="gp-small gp-text-center gp-mt-32 gp-mx-auto gp-narrow">All services and amenities are subject to current availability. [VERIFY: confirm the current list against day-to-day operations before launch]</p>
    </div>
  </section>

{location_section('gp-bg-white')}
{cta_band()}"""


def accommodation_body():
    rooms = [
        ("AC &amp; Non-AC Rooms", "ac-non-ac-room", "Well-furnished guest room at Hotel Green Plaza",
         [("ac", "AC and Non-AC options"), ("bed", "Single and double bed facilities"),
          ("sparkles", "Well-furnished rooms"), ("bath", "Attached bathrooms"),
          ("tv", "Airtel Digital Dish TV with multiple channels"), ("clock", "24-hour room service")]),
        ("Double Bed Accommodation", "double-bed-room", "Double bed guest room at Hotel Green Plaza",
         [("ac", "AC and Non-AC options"), ("bed", "Double bed facilities"),
          ("sparkles", "Well-furnished rooms"), ("bath", "Attached bathrooms"),
          ("tv", "Digital TV"), ("clock", "24-hour room service")]),
        ("Double / Triple Bed Accommodation", "double-triple-bed-room", "Double and triple bed guest room at Hotel Green Plaza",
         [("ac", "AC and Non-AC options"), ("bed", "Double and triple bed facilities"),
          ("sparkles", "Well-furnished rooms"), ("bath", "Attached bathrooms"),
          ("tv", "Digital TV"), ("clock", "24-hour room service")]),
        ("Super Deluxe Triple Bed", "super-deluxe-triple-room", "Super deluxe triple bed room at Hotel Green Plaza",
         [("bed", "Triple bed accommodation"), ("ac", "AC / Non-AC availability subject to current inventory"),
          ("bath", "Attached bathroom"), ("tv", "Digital TV"), ("room-service", "Room service")]),
    ]

    cards = []
    for title, slug, alt, chips in rooms:
        chip_html = "\n".join(
            '                <span class="gp-chip">%s%s</span>' % (icon(n, "gp-icon--sm"), t)
            for n, t in chips)
        cards.append(f"""        <div class="col-12 col-lg-6">
          <article class="gp-card gp-card--room gp-reveal">
            <div class="gp-card__media">
              <!-- PLACEHOLDER 880×660 (4:3) — replace with a real photograph of this room type -->
              <img src="/assets/img/rooms/hotel-green-plaza-{slug}.webp" width="880" height="660" loading="lazy" alt="{alt}">
            </div>
            <div class="gp-card__body">
              <h3>{title}</h3>
              <div class="gp-chips">
{chip_html}
              </div>
              <div class="gp-card__actions">
                <a class="gp-btn gp-btn--primary" href="/contact/#enquiry">Check Availability</a>
                <a class="gp-btn gp-btn--secondary" href="/contact/#enquiry">Enquire Now</a>
              </div>
            </div>
          </article>
        </div>""")

    gallery = [
        ("guest-room-interior", 900, 1200, "Well-furnished guest room at Hotel Green Plaza", "Guest room"),
        ("room-bathroom", 900, 675, "Attached bathroom in a guest room at Hotel Green Plaza", "Attached bathroom"),
        ("corridor-interior", 900, 675, "Guest room corridor at Hotel Green Plaza", "Corridor"),
    ]
    gallery_items = "\n".join(f"""        <div class="gp-masonry__item gp-reveal">
          <button class="gp-thumb" type="button" aria-label="View larger image: {alt}">
            <img src="/assets/img/gallery/hotel-green-plaza-{slug}.webp" width="{w}" height="{h}" loading="lazy" alt="{alt}">
            <span class="gp-thumb__label">{label}</span>
          </button>
        </div>""" for slug, w, h, alt, label in gallery)

    facilities = [
        ("ac", "Air conditioning", "AC and Non-AC rooms are available across room categories."),
        ("bath", "Attached bathrooms", "Every room category includes an attached bathroom."),
        ("tv", "Digital television", "In-room digital television with multiple channels."),
        ("room-service", "24-hour room service", "Room service is available around the clock."),
        ("coffee", "Tea / coffee maker", "An in-room tea and coffee maker for everyday convenience."),
        ("phone", "Direct dialing", "Direct dialing is available from the room."),
    ]
    facility_cards = "\n".join(f"""        <div class="col-12 col-sm-6 col-lg-4">
          <article class="gp-service gp-reveal">
            <span class="gp-service__icon">{icon(n)}</span>
            <h3>{t}</h3>
            <p>{d}</p>
          </article>
        </div>""" for n, t, d in facilities)

    return banner(
        "Accommodation",
        "Choose from comfortable and well-furnished rooms designed to meet the needs of business travellers, families and holidaymakers.",
        "Accommodation",
        "/assets/img/hero/hotel-green-plaza-accommodation-banner.webp",
        "Well-furnished guest room at Hotel Green Plaza",
    ) + f"""
  <!-- =========================== ROOM CATEGORIES =========================== -->
  <section class="gp-section gp-bg-white">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">Our Rooms</span>
        <h2>Room Categories</h2>
        <p>Choose from comfortable and well-furnished rooms designed to meet the needs of business travellers, families and holidaymakers.</p>
      </div>

      <div class="row gp-gap-30">
{chr(10).join(cards)}
      </div>

      <p class="gp-small gp-text-center gp-mt-40 gp-mx-auto gp-narrow">Room names, rates, occupancy and availability are confirmed at the time of enquiry. [VERIFY: current room names, pricing, occupancy and inventory before publishing]</p>
    </div>
  </section>

  <!-- =========================== ROOM FACILITIES =========================== -->
  <section class="gp-section gp-bg-cream">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">Room Facilities</span>
        <h2>What Every Room Includes</h2>
        <p>Practical facilities provided across our room categories.</p>
      </div>

      <div class="row gp-gap-30">
{facility_cards}
      </div>
    </div>
  </section>

  <!-- ============================ ROOM GALLERY ============================ -->
  <section class="gp-section gp-bg-white">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">Room Gallery</span>
        <h2>A Closer Look</h2>
      </div>

      <div class="gp-masonry">
{gallery_items}
      </div>

      <div class="gp-text-center gp-mt-40">
        <a class="gp-btn gp-btn--secondary" href="/gallery/">View Full Gallery</a>
      </div>
    </div>
  </section>

{location_section('gp-bg-cream')}
{cta_band()}"""


# ---------------------------------------------------------------------------
# Restaurant menu — transcribed from the hotel's own printed menu card
# (pure vegetarian; Punjabi, Chinese & South Indian). Prices are in rupees.
# Items with a "(Dry / Gravy)" style choice carry a single listed price.
# ---------------------------------------------------------------------------

MENU = [
    {"name": "Soups", "icon": "utensils", "note": "A 1×2 (half-and-half) portion is ₹10 extra.", "items": [
        ("Cream of Tomato", "110"), ("Sweet Corn Vegetable", "110"),
        ("Vegetable Manchow", "110"), ("Vegetable Hot &amp; Sour", "110"),
        ("Mushroom Soup", "110"), ("Veg. Noodles Soup", "110"),
    ]},
    {"name": "South Indian", "icon": "leaf", "items": [
        ("Sp. Green Plaza Masala Dosa", "145"), ("Plain Dosa", "100"),
        ("Plain Cheese Dosa", "125"), ("Masala Dosa", "110"),
        ("Masala Butter Dosa", "120"), ("Paneer Masala Dosa", "150"),
        ("Cheese Masala Dosa", "155"), ("Rava Sada Dosa", "120"),
        ("Rava Masala Dosa", "125"), ("Mysore Masala Dosa", "135"),
        ("Onion Tomato Uthappam", "120"), ("Mix Veg. Uthappam", "120"),
        ("Idli Sambhar", "70"), ("Wada Sambhar", "85"), ("Idli Wada (mix)", "85"),
        ("Fry Idli", "85"), ("Dahi Wada", "85"), ("Spring Dosa", "145"),
        ("Puri Bhaji", "90"), ("Aloo Paratha Fry (with curd)", "85"),
        ("Paneer Pakoda", "140"), ("Onion (mix) Pakoda", "75"),
    ]},
    {"name": "Chinese Starters", "icon": "utensils", "note": "Schezwan / green chutney charged extra.", "items": [
        ("Paneer Tikka Schezwan Dry", "270"), ("Paneer Tikka Dry", "240"),
        ("Paneer Lollipop", "250"), ("Paneer Chilli (Dry / Gravy)", "220"),
        ("Paneer Manchurian (Dry / Gravy)", "225"), ("Paneer Schezwan (Dry)", "250"),
        ("Paneer 65", "235"), ("Paneer Crispy", "300"),
        ("Chhole Schezwan Dry", "175"), ("Veg. Manchurian (Dry / Gravy)", "200"),
        ("Mushroom Manchurian (Dry / Gravy)", "245"), ("Veg. 65", "210"),
        ("Veg. Crispy", "250"), ("Veg. Spring Roll", "205"),
        ("Mushroom Tikka Dry", "250"), ("Baby Corn Chilli (Dry / Gravy)", "250"),
        ("American Choupsey", "215"), ("Aloo Chilly Dry", "210"),
        ("Veg. Hakka Noodles", "190"), ("Schezwan Noodles", "200"),
        ("Manchurian with Noodles", "200"), ("Veg. Chowmein", "190"),
        ("Chinese Bhel", "175"), ("Veg. Fried Rice", "175"),
        ("Schezwan Fried Rice", "195"), ("Manchurian with Fried Rice", "200"),
        ("Triple Schezwan Fried Rice", "260"), ("Mushroom Fried Rice", "240"),
    ]},
    {"name": "Punjabi Dishes", "icon": "utensils", "items": [
        ("Sp. Green Plaza Vegetables", "260"), ("Veg. Garden", "250"),
        ("Veg. Mumtaz", "260"), ("Veg. Toofani", "245"), ("Veg. Jafrani", "230"),
        ("Veg. Hyderabadi", "220"), ("Veg. Kadai", "190"), ("Veg. Handi", "190"),
        ("Veg. Kolhapuri", "180"), ("Veg. Jaipuri", "180"),
        ("Veg. Makkhanwala", "180"), ("Veg. Tawa", "210"),
        ("Veg. Navratan Korma (Sweet)", "210"), ("Kaju Curry (Spicy)", "185"),
        ("Kaju Mushroom Masala", "240"), ("Mushroom Masala", "220"),
        ("Dum Aloo Punjabi (Spicy)", "220"), ("Aloo Mutter", "140"),
        ("Aloo Palak", "140"), ("Malai Pyaz", "190"), ("Veg. Kheema", "170"),
        ("Aloo Gobi", "140"), ("Jeera Aloo", "140"), ("Aloo Sukhi Bhaji", "140"),
        ("Chana Masala", "135"), ("Moong Masala", "135"), ("Bhindi Masala", "135"),
        ("Bhindi Fry", "150"), ("Moong Fry", "150"), ("Sev Tomato", "135"),
        ("Sev Masala", "135"), ("Plain Palak", "135"), ("Sev Masala (Milk)", "140"),
        ("Curd Fry", "135"), ("Dal Fry", "120"), ("Dal Tadka", "140"),
        ("Dal Makhni", "160"), ("Dal Fry Butter", "140"), ("Shahi Dal", "170"),
        ("Methi Mutter Masala", "160"),
    ]},
    {"name": "Paneer", "icon": "utensils", "items": [
        ("Paneer Butter Masala", "190"), ("Paneer Tikka Masala", "190"),
        ("Paneer Bhurji", "210"), ("Paneer Mutter", "180"), ("Paneer Chana", "180"),
        ("Paneer Shahi", "200"), ("Paneer Handi", "200"), ("Paneer Palak", "170"),
        ("Paneer Kadai", "205"), ("Paneer Tawa", "240"), ("Paneer Kaju", "220"),
        ("Paneer Lasuniya", "220"),
    ]},
    {"name": "Paneer Special", "icon": "sparkles", "items": [
        ("Sp. Paneer Green Plaza", "290"), ("Paneer Banjara", "290"),
        ("Paneer Shabnam", "270"), ("Paneer Toofani", "280"),
        ("Paneer Kasturi", "280"), ("Paneer Banarasya", "280"),
        ("Paneer Pasanda", "280"), ("Paneer Lazeez", "250"),
        ("Paneer Rajwadi", "280"), ("Paneer Patiyala", "280"),
        ("Paneer Begum Bahar", "260"), ("Paneer Jafrani", "260"),
        ("Paneer Tawa Kaju", "270"), ("Paneer Garlic Tawa", "270"),
        ("Paneer Hyderabadi", "230"), ("Paneer La Jawab", "260"),
        ("Paneer Chatpata", "260"), ("Kaju Banarasya", "280"),
        ("Cheese Butter Masala", "240"), ("Cheese Angoori", "290"),
        ("Cheese Lasuniya", "260"), ("Cheese Begum Bahar", "280"),
    ]},
    {"name": "Kofta", "icon": "utensils", "items": [
        ("Sp. Green Plaza Kofta", "270"), ("Paneer Kofta", "230"),
        ("Veg. Kofta", "210"), ("Kaju Kofta", "240"), ("Nargis Kofta", "230"),
        ("Malai Kofta (Sweet / Spicy)", "200"), ("Cheese Kofta", "240"),
    ]},
    {"name": "Jain Dishes", "icon": "leaf", "items": [
        ("Paneer Butter Masala", "260"), ("Paneer Palak", "260"),
        ("Plain Palak", "200"), ("Chana Masala", "190"), ("Kaju Curry", "270"),
        ("Sev Tomato", "190"), ("Sev Milk", "200"),
    ]},
    {"name": "Tandoor Se", "icon": "utensils", "items": [
        ("Tandoori Roti", "17"), ("Tandoori Butter Roti", "20"),
        ("Plain Naan", "40"), ("Butter Naan", "45"), ("Cheese Naan", "80"),
        ("Garlic Naan", "70"), ("Laccha Paratha", "50"), ("Kulcha Paratha", "50"),
        ("Paneer Paratha", "100"), ("Stuffed Naan", "100"),
        ("Aloo Paratha Tandoori (with curd)", "95"), ("Missi Roti", "50"),
        ("Missi Roti Butter", "55"), ("Cheese Garlic Naan", "100"),
    ]},
    {"name": "Tawa ka Kamal", "icon": "utensils", "items": [
        ("Plain Chapati", "15"), ("Butter Chapati", "18"),
        ("Chapati Paratha Butter", "50"),
    ]},
    {"name": "Basmati Khazana", "icon": "utensils", "note": "Birishta (fried onion) charged extra.", "items": [
        ("Sp. Green Plaza Biryani", "210"), ("Veg. Handi Biryani", "195"),
        ("Veg. Hyderabadi Biryani", "195"), ("Veg. Biryani", "175"),
        ("Sp. Tawa Biryani", "205"), ("Veg. Pulav", "150"),
        ("Paneer Pulav", "180"), ("Kaju Pulav", "195"),
        ("Kashmiri Pulav (Sweet)", "185"), ("Green Peas Pulav", "160"),
        ("Masala Rice", "110"), ("Jeera Rice", "95"), ("Steam Rice", "95"),
        ("Plain Rice", "85"), ("Dal Khichdi Butter", "140"),
    ]},
    {"name": "Thali", "icon": "utensils", "items": [
        ("Punjabi Thali", "200", "Dal fry, chana masala, mix veg, plain rice, roasted papad and 3 chapatis."),
        ("Sp. Punjabi Thali", "230", "Paneer masala, mix veg, dal fry, jeera rice, roasted papad, veg. raita, 3 butter chapatis and buttermilk."),
    ]},
    {"name": "Pizza", "icon": "utensils", "items": [
        ("Veg. Italian Pizza", "160"), ("Paneer Pizza", "160"),
        ("Cheese Pizza", "160"),
    ]},
    {"name": "Sandwiches", "icon": "utensils", "items": [
        ("Grilled Vegetable", "70"), ("Grilled Cheese", "90"),
        ("Vegetable Sandwich", "65"), ("Plain Cheese", "70"),
        ("Aloo Mutter Grilled", "85"), ("Bread Butter", "40"),
        ("Bread Butter Jam", "45"), ("Toast Butter", "45"),
        ("Toast Butter Jam", "50"), ("French Fries", "100"),
        ("Grilled Vegetable Cheese Slice", "110"),
    ]},
    {"name": "Raita, Salad &amp; Papad", "icon": "leaf", "items": [
        ("Green Salad", "80"), ("Tomato Salad", "70"), ("Kachumbar Salad", "80"),
        ("Veg. Raita", "80"), ("Boondi Raita", "80"), ("Pineapple Raita", "100"),
        ("Fruit Raita", "100"), ("Curd", "70"), ("Roasted Papad", "20"),
        ("Fry Papad", "20"), ("Roasted Masala Papad", "35"), ("Fry Masala Papad", "35"),
    ]},
    {"name": "Tea &amp; Coffee", "icon": "coffee", "note": "Prices shown as AC Hall / Hall.", "items": [
        ("Golden Tea", "35 / 30"), ("Kathyavadi", "30 / 25"), ("Tea", "25 / 20"),
        ("Green Tea", "35 / 30"), ("Nes Coffee", "35 / 30"), ("Hot Milk", "35 / 30"),
        ("Cold Coffee", "85 / 80"), ("Cold Coffee with Ice Cream", "110 / 100"),
    ]},
    {"name": "Milk Shakes", "icon": "coffee", "note": "Served with ice cream.", "items": [
        ("Mango Milk Shake", "100"), ("Pineapple Milk Shake", "100"),
        ("Strawberry Milk Shake", "100"), ("Kesar Pista Milk Shake", "110"),
        ("Chocolate Milk Shake", "100"), ("Butter Scotch Shake", "100"),
    ]},
    {"name": "Refreshers", "icon": "coffee", "items": [
        ("Fresh Lime Soda / Water", "55"), ("Butter Milk", "25"),
        ("Sp. Kheer", "80"), ("Plain Lassi", "55"), ("Sp. Green Rose Lassi", "85"),
        ("Sp. Green Mango Lassi", "100"), ("Sp. Green Pineapple Lassi", "100"),
        ("Sp. Green Chocolate Lassi", "100"),
    ]},
    {"name": "Ice Cream", "icon": "ice-cream", "items": [
        ("Vanilla", "50"), ("Strawberry", "50"), ("Two in One", "60"),
        ("Havmor Kulfi", "70"), ("Chocolate Chips", "60"), ("Butter Scotch", "60"),
        ("Kaju Draksh", "60"), ("Kesar Pista", "70"), ("Chocolate Mud Cake", "70"),
        ("American Nuts", "60"), ("Raj Bhog", "70"), ("Black Current", "60"),
        ("Paan", "60"), ("Almond Carnival", "60"), ("Mango", "60"),
        ("Pineapple", "60"),
    ]},
]

# Restaurant house rules, printed on the menu card.
MENU_NOTES = [
    "Please allow around 20 minutes after placing your order.",
    "Tandoori dishes are served during lunch and dinner hours only.",
    "Party and bulk orders are welcome.",
    "Parcel charges apply on takeaway orders.",
    "Once placed, orders cannot be cancelled.",
]


# Higher-level courses so the 19 sections collapse to a short, tappable filter
# bar rather than 19 chips. Each menu group maps to one course below.
MENU_FILTERS = [
    ("all", "All"),
    ("starters", "Soups &amp; Starters"),
    ("south-indian", "South Indian"),
    ("mains", "Main Course"),
    ("breads-rice", "Breads &amp; Rice"),
    ("snacks", "Snacks &amp; Sides"),
    ("beverages", "Beverages"),
    ("desserts", "Desserts"),
]

MENU_CAT = {
    "Soups": "starters", "Chinese Starters": "starters",
    "South Indian": "south-indian",
    "Punjabi Dishes": "mains", "Paneer": "mains", "Paneer Special": "mains",
    "Kofta": "mains", "Jain Dishes": "mains", "Thali": "mains",
    "Tandoor Se": "breads-rice", "Tawa ka Kamal": "breads-rice",
    "Basmati Khazana": "breads-rice",
    "Pizza": "snacks", "Sandwiches": "snacks", "Raita, Salad &amp; Papad": "snacks",
    "Tea &amp; Coffee": "beverages", "Milk Shakes": "beverages", "Refreshers": "beverages",
    "Ice Cream": "desserts",
}


def menu_group(group):
    cat = MENU_CAT.get(group["name"], "")
    note = ""
    if group.get("note"):
        note = f'\n          <p class="gp-menu__note">{group["note"]}</p>'
    rows = []
    for item in group["items"]:
        name, price = item[0], item[1]
        desc = item[2] if len(item) > 2 else ""
        name_html = name
        if desc:
            name_html = f'{name}<span class="gp-menu__desc">{desc}</span>'
        rows.append(f"""            <li class="gp-menu__row">
              <span class="gp-menu__name">{name_html}</span>
              <span class="gp-menu__dots" aria-hidden="true"></span>
              <span class="gp-menu__price">₹{price}</span>
            </li>""")
    rows_html = "\n".join(rows)
    return f"""        <div class="gp-menu__group gp-reveal" data-category="{cat}">
          <div class="gp-menu__group-head">
            {icon(group['icon'], 'gp-icon--sm')}
            <h3>{group['name']}</h3>
          </div>{note}
          <ul class="gp-menu__list">
{rows_html}
          </ul>
        </div>"""


def menu_section():
    groups = "\n".join(menu_group(g) for g in MENU)
    filters = "\n".join(
        '        <button class="gp-filter__btn" type="button" data-filter="%s" aria-pressed="%s">%s</button>'
        % (slug, "true" if slug == "all" else "false", label)
        for slug, label in MENU_FILTERS)
    notes = "\n".join(
        f"""            <li>{icon('check', 'gp-icon--sm')}<span>{n}</span></li>"""
        for n in MENU_NOTES)
    return f"""  <!-- ============================== MENU ============================== -->
  <section class="gp-section gp-bg-cream" id="menu">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">Our Menu</span>
        <h2>Pure Vegetarian Menu</h2>
        <p>Punjabi, Chinese and South Indian dishes, freshly prepared. Tap a course to jump straight to it. Prices are in rupees and may change; please confirm current availability when you visit.</p>
      </div>

      <div class="gp-menu-nav" role="group" aria-label="Filter menu by course" data-menu-nav>
{filters}
      </div>

      <div class="gp-menu">
{groups}
      </div>

      <div class="gp-menu__foot gp-reveal">
        <h3>Good to Know</h3>
        <ul class="gp-feature-list gp-feature-list--2col">
{notes}
        </ul>
      </div>
    </div>
  </section>
"""


def restaurant_body():
    highlights = [
        ("leaf", "Pure vegetarian restaurant"),
        ("utensils", "Multi-cuisine menu"),
        ("sparkles", "Warm and comfortable interiors"),
        ("building", "Lobby-level location"),
        ("users", "Suitable for hotel guests and dining visitors"),
    ]
    highlight_items = "\n".join(
        f'        <li class="gp-amenity gp-reveal">{icon(n)}{t}</li>' for n, t in highlights)

    gallery = [
        ("restaurant-seating", 900, 675, "Pure vegetarian restaurant at Hotel Green Plaza", "Restaurant seating"),
        ("vegetarian-dishes", 900, 1200, "Vegetarian dishes served at Hotel Green Plaza", "Vegetarian dishes"),
        ("lobby-seating", 900, 675, "Lobby seating area at Hotel Green Plaza", "Lobby"),
    ]
    gallery_items = "\n".join(f"""        <div class="gp-masonry__item gp-reveal">
          <button class="gp-thumb" type="button" aria-label="View larger image: {alt}">
            <img src="/assets/img/gallery/hotel-green-plaza-{slug}.webp" width="{w}" height="{h}" loading="lazy" alt="{alt}">
            <span class="gp-thumb__label">{label}</span>
          </button>
        </div>""" for slug, w, h, alt, label in gallery)

    return banner(
        "Restaurant",
        "A lobby-level multi-cuisine restaurant with warm wooden interiors and a pure vegetarian menu.",
        "Restaurant",
        "/assets/img/hero/hotel-green-plaza-restaurant-banner.webp",
        "Pure vegetarian restaurant at Hotel Green Plaza",
    ) + f"""
  <!-- ========================== INTRODUCTION ========================== -->
  <section class="gp-section gp-bg-white">
    <div class="container">
      <div class="row gp-split">
        <div class="col-12 col-lg-6">
          <div class="gp-reveal">
            <span class="gp-eyebrow">Dining</span>
            <h2>Pure Vegetarian Multi-Cuisine Dining</h2>
            <p>Hotel Green Plaza features a lobby-level multi-cuisine restaurant with warm wooden interiors and a pure vegetarian menu spanning Punjabi, Chinese and South Indian dishes.</p>
            <p>Guests can enjoy a selection of delicious dishes in a comfortable and welcoming dining environment.</p>
            <hr class="gp-rule">
            <div class="gp-btn-group">
              <a class="gp-btn gp-btn--primary" href="#menu">View the Menu</a>
              <a class="gp-btn gp-btn--secondary" href="/contact/#enquiry">Dining Enquiries</a>
            </div>
          </div>
        </div>
        <div class="col-12 col-lg-6">
          <div class="gp-split__media gp-reveal">
            <!-- PLACEHOLDER 1100×733 (3:2) — replace with a real restaurant interior photograph -->
            <img src="/assets/img/general/hotel-green-plaza-restaurant-interior.webp" width="1100" height="733" loading="lazy" alt="Warm wooden interiors of the restaurant at Hotel Green Plaza">
            <span class="gp-split__mark" aria-hidden="true">{icon('leaf')}</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ====================== PURE VEGETARIAN HIGHLIGHT ====================== -->
  <section class="gp-section gp-bg-tint">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">Restaurant Highlights</span>
        <h2>What Defines Our Restaurant</h2>
      </div>

      <ul class="gp-amenity-grid">
{highlight_items}
      </ul>
    </div>
  </section>

  <!-- ========================= DINING ENVIRONMENT ========================= -->
  <section class="gp-section gp-bg-white">
    <div class="container">
      <div class="row gp-split">
        <div class="col-12 col-lg-6">
          <div class="gp-split__media gp-reveal">
            <!-- PLACEHOLDER 900×600 (3:2) — replace with a real dining area photograph -->
            <img src="/assets/img/general/hotel-green-plaza-restaurant-dining.webp" width="900" height="600" loading="lazy" alt="Dining area of the restaurant at Hotel Green Plaza">
          </div>
        </div>
        <div class="col-12 col-lg-6">
          <div class="gp-reveal">
            <span class="gp-eyebrow">The Setting</span>
            <h2>A Comfortable Place to Eat</h2>
            <p>The restaurant sits at lobby level, which makes it convenient for hotel guests and easy to reach for dining visitors.</p>
            <ul class="gp-feature-list">
              <li>{icon('check', 'gp-icon--sm')}<span>Warm wooden interiors</span></li>
              <li>{icon('check', 'gp-icon--sm')}<span>Comfortable and welcoming dining environment</span></li>
              <li>{icon('check', 'gp-icon--sm')}<span>Open to hotel guests and dining visitors</span></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>

{menu_section()}
  <!-- ======================= RESTAURANT INFORMATION ======================= -->
  <section class="gp-section gp-bg-white">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">Restaurant Information</span>
        <h2>Planning a Visit</h2>
        <p>What to expect when you dine with us.</p>
      </div>

      <div class="row gp-gap-30">
        <div class="col-12 col-sm-6 col-lg-4">
          <article class="gp-service gp-reveal">
            <span class="gp-service__icon">{icon('clock')}</span>
            <h3>Timings</h3>
            <p>Tandoori dishes are served during lunch and dinner hours. [VERIFY: exact opening, breakfast, lunch and dinner timings — do not publish specific hours until confirmed]</p>
          </article>
        </div>
        <div class="col-12 col-sm-6 col-lg-4">
          <article class="gp-service gp-reveal">
            <span class="gp-service__icon">{icon('leaf')}</span>
            <h3>Menu</h3>
            <p>A fully pure vegetarian menu of Punjabi, Chinese and South Indian dishes. <a class="gp-textlink" href="#menu">See the full menu with prices</a>.</p>
          </article>
        </div>
        <div class="col-12 col-sm-6 col-lg-4">
          <article class="gp-service gp-reveal">
            <span class="gp-service__icon">{icon('phone')}</span>
            <h3>Reservations</h3>
            <p>Send us an enquiry and our team will get back to you about dining and table reservations.</p>
          </article>
        </div>
      </div>
    </div>
  </section>

  <!-- ============================== GALLERY ============================== -->
  <section class="gp-section gp-bg-cream">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">Gallery</span>
        <h2>Inside the Restaurant</h2>
      </div>

      <div class="gp-masonry">
{gallery_items}
      </div>
    </div>
  </section>

{cta_band()}"""


def banquets_body():
    events = [
        ("users", "Family functions"), ("celebration", "Social gatherings"),
        ("briefcase", "Business meetings"), ("conference", "Conferences"),
        ("building", "Corporate events"), ("celebration", "Celebrations"),
        ("users", "Private functions"), ("calendar", "Other special occasions"),
    ]
    event_items = "\n".join(
        f'        <li class="gp-event gp-reveal">{icon(n)}{t}</li>' for n, t in events)

    gallery = [
        ("banquet-hall-setup", 900, 675, "Banquet hall at Hotel Green Plaza", "Banquet hall"),
        ("event-celebration", 900, 1200, "Event celebration at Hotel Green Plaza", "Celebration"),
        ("conference-hall", 900, 675, "Conference hall at Hotel Green Plaza", "Conference hall"),
    ]
    gallery_items = "\n".join(f"""        <div class="gp-masonry__item gp-reveal">
          <button class="gp-thumb" type="button" aria-label="View larger image: {alt}">
            <img src="/assets/img/gallery/hotel-green-plaza-{slug}.webp" width="{w}" height="{h}" loading="lazy" alt="{alt}">
            <span class="gp-thumb__label">{label}</span>
          </button>
        </div>""" for slug, w, h, alt, label in gallery)

    facilities = [
        ("utensils", "Catering", "Food and catering arrangements are handled by our pure vegetarian kitchen. [VERIFY: current catering options and menus]"),
        ("users", "Capacity", "[VERIFY: hall capacity and layout options — do not publish numbers until confirmed]"),
        ("bell", "On-site support", "Front desk and housekeeping support throughout your event."),
    ]
    facility_cards = "\n".join(f"""        <div class="col-12 col-sm-6 col-lg-4">
          <article class="gp-service gp-reveal">
            <span class="gp-service__icon">{icon(n)}</span>
            <h3>{t}</h3>
            <p>{d}</p>
          </article>
        </div>""" for n, t, d in facilities)

    return banner(
        "Banquets &amp; Events",
        "Banquet facilities in Bhilwara suitable for functions, gatherings, conferences, business meetings and a wide range of events.",
        "Banquets",
        "/assets/img/hero/hotel-green-plaza-banquets-banner.webp",
        "Banquet hall at Hotel Green Plaza",
    ) + f"""
  <!-- =========================== INTRODUCTION =========================== -->
  <section class="gp-section gp-bg-white">
    <div class="container">
      <div class="row gp-split">
        <div class="col-12 col-lg-6">
          <div class="gp-reveal">
            <span class="gp-eyebrow">Banquets</span>
            <h2>Spaces for Every Occasion</h2>
            <p>Hotel Green Plaza offers banquet facilities in Bhilwara suitable for functions, gatherings, conferences, business meetings and a wide range of events.</p>
            <hr class="gp-rule">
            <div class="gp-btn-group">
              <a class="gp-btn gp-btn--primary" href="#enquiry">Plan Your Event</a>
              <a class="gp-btn gp-btn--secondary" href="#enquiry">Enquire About Banquets</a>
            </div>
          </div>
        </div>
        <div class="col-12 col-lg-6">
          <div class="gp-split__media gp-reveal">
            <!-- PLACEHOLDER 1100×733 (3:2) — replace with a real banquet hall photograph -->
            <img src="/assets/img/general/hotel-green-plaza-banquet-event-setup.webp" width="1100" height="733" loading="lazy" alt="Banquet hall set up for an event at Hotel Green Plaza">
            <span class="gp-split__mark" aria-hidden="true">{icon('leaf')}</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ========================= VENUE PHOTOGRAPHS ========================= -->
  <section class="gp-section gp-bg-cream">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">The Venue</span>
        <h2>Our Banquet Spaces</h2>
      </div>

      <div class="gp-masonry">
{gallery_items}
      </div>
    </div>
  </section>

  <!-- ============================ EVENT TYPES ============================ -->
  <section class="gp-section gp-bg-white">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">Event Types</span>
        <h2>Suitable Occasions</h2>
        <p>Our banquet facilities are suitable for a wide range of gatherings.</p>
      </div>

      <ul class="gp-event-grid">
{event_items}
      </ul>
    </div>
  </section>

  <!-- ============================= FACILITIES ============================= -->
  <section class="gp-section gp-bg-tint">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">Facilities</span>
        <h2>Event Support</h2>
        <p>Details of catering, capacity and packages are shared at the time of enquiry.</p>
      </div>

      <div class="row gp-gap-30">
{facility_cards}
      </div>
    </div>
  </section>

  <!-- =========================== ENQUIRY FORM =========================== -->
  <section class="gp-section gp-bg-white" id="enquiry">
    <div class="container">
      <div class="row gp-split align-items-start">
        <div class="col-12 col-lg-5">
          <div class="gp-reveal">
            <span class="gp-eyebrow">Enquiries</span>
            <h2>Plan Your Event</h2>
            <p>Tell us about your event and our team will get back to you with availability and details.</p>

            <ul class="gp-contact-list gp-mt-32">
              <li class="gp-contact-item">
                <span class="gp-contact-item__icon">{icon('phone')}</span>
                <div>
                  <h3>Banquet Enquiries</h3>
                  <p>{phone_links(BHILWARA['phones'], '<br>')}</p>
                </div>
              </li>
              <li class="gp-contact-item">
                <span class="gp-contact-item__icon">{icon('mail')}</span>
                <div>
                  <h3>Email</h3>
                  <p><a href="mailto:{BHILWARA['email']}">{BHILWARA['email']}</a></p>
                </div>
              </li>
              <li class="gp-contact-item">
                <span class="gp-contact-item__icon">{icon('pin')}</span>
                <div>
                  <h3>Address</h3>
                  <p>{BHILWARA['html']}</p>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <div class="col-12 col-lg-7">
          <div class="gp-form-panel gp-reveal">
            <h3>Send Us an Enquiry</h3>
{enquiry_form('Banquet / Event')}
          </div>
        </div>
      </div>
    </div>
  </section>

{location_section('gp-bg-cream')}
{cta_band()}"""


def services_body():
    special = [
        ("bed", "Smartly designed rooms", "Rooms designed to suit different guest requirements."),
        ("bell", "24/7 front desk", "Assistance at the front desk at any hour of the day or night."),
        ("sparkles", "Housekeeping", "Regular housekeeping to keep rooms clean and comfortable."),
        ("room-service", "Room service", "24-hour room service for meals and requests."),
        ("utensils", "Full-service restaurant", "A lobby-level pure vegetarian restaurant serving Punjabi, Chinese and South Indian food."),
        ("doctor", "Doctor on call", "Medical assistance arranged on call when needed."),
        ("laundry", "Same-day laundry service", "Same-day laundry and pressing for guests."),
        ("car", "Car rental &amp; EV charging", "Car-on-rent arrangements plus an on-site electric-vehicle charging station."),
        ("scissors", "Saloon", "An in-house saloon on the premises for guests' grooming needs."),
        ("tree", "Children's park &amp; garden", "A garden and children's play area to relax and unwind."),
    ]
    special_cards = "\n".join(f"""        <div class="col-12 col-sm-6 col-lg-4">
          <article class="gp-service gp-reveal">
            <span class="gp-service__icon">{icon(n)}</span>
            <h3>{t}</h3>
            <p>{d}</p>
          </article>
        </div>""" for n, t, d in special)

    amenities = [
        ("coffee", "In-room tea / coffee maker"), ("fridge", "Refrigerator"),
        ("iron", "Iron and ironing board on request"), ("phone", "Direct dialing from the room"),
        ("tv", "In-room cable television"), ("newspaper", "Newspaper"),
    ]
    amenity_items = "\n".join(
        f'        <li class="gp-amenity gp-reveal">{icon(n)}{t}</li>' for n, t in amenities)

    facility_icons = [
        ("bed", "AC &amp; Non-AC rooms"), ("bath", "Attached bathrooms"),
        ("utensils", "Pure veg restaurant"), ("users", "AC family hall"),
        ("room-service", "24-hour room service"), ("sparkles", "Housekeeping"),
        ("parking", "Vehicle parking"), ("shield", "24-hour security &amp; CCTV"),
        ("car", "Car on rent"), ("zap", "EV charging station"),
        ("doctor", "Doctor on call"), ("laundry", "Laundry service"),
        ("scissors", "Saloon"), ("ice-cream", "Ice cream parlor"),
        ("tree", "Children's park &amp; garden"), ("gift", "Shopping area / gifts"),
        ("water", "24-hour hot &amp; cold water"), ("bulb", "24-hour electricity"),
    ]
    facility_items = "\n".join(
        f'        <li class="gp-amenity gp-reveal">{icon(n)}{t}</li>' for n, t in facility_icons)

    return banner(
        "Hotel Services",
        "A range of services designed to make every stay more convenient and comfortable.",
        "Services",
        "/assets/img/hero/hotel-green-plaza-services-banner.webp",
        "Front desk and guest services at Hotel Green Plaza",
    ) + f"""
  <!-- =========================== INTRODUCTION =========================== -->
  <section class="gp-section gp-bg-white">
    <div class="container">
      <div class="row gp-split">
        <div class="col-12 col-lg-6">
          <div class="gp-reveal">
            <span class="gp-eyebrow">Services</span>
            <h2>Made for an Easier Stay</h2>
            <p>Hotel Green Plaza offers a range of services designed to make every stay more convenient and comfortable.</p>
            <hr class="gp-rule">
            <a class="gp-btn gp-btn--primary" href="/contact/#enquiry">Enquire Now</a>
          </div>
        </div>
        <div class="col-12 col-lg-6">
          <div class="gp-split__media gp-reveal">
            <!-- PLACEHOLDER 1100×733 (3:2) — replace with a real front desk photograph -->
            <img src="/assets/img/general/hotel-green-plaza-front-desk.webp" width="1100" height="733" loading="lazy" alt="Front desk at Hotel Green Plaza in Bhilwara">
            <span class="gp-split__mark" aria-hidden="true">{icon('leaf')}</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ========================== SPECIAL SERVICES ========================== -->
  <section class="gp-section gp-bg-cream">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">Special Services</span>
        <h2>What We Provide</h2>
        <p>The services our team looks after day to day.</p>
      </div>

      <div class="row gp-gap-30">
{special_cards}
      </div>
    </div>
  </section>

  <!-- ============================= AMENITIES ============================= -->
  <section class="gp-section gp-bg-tint">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">Amenities</span>
        <h2>In-Room Amenities</h2>
        <p>Everyday comforts provided in the room.</p>
      </div>

      <ul class="gp-amenity-grid">
{amenity_items}
      </ul>
    </div>
  </section>

  <!-- =========================== FACILITY GRID =========================== -->
  <section class="gp-section gp-bg-white">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">At a Glance</span>
        <h2>Facilities</h2>
      </div>

      <ul class="gp-amenity-grid">
{facility_items}
      </ul>

      <p class="gp-small gp-text-center gp-mt-32 gp-mx-auto gp-narrow">Facilities listed above are from the hotel's own information. [VERIFY: confirm the full list is current and complete before launch]</p>
    </div>
  </section>

{location_section('gp-bg-cream')}
{cta_band()}"""


def gallery_body():
    filters = ["All", "Hotel", "Rooms", "Restaurant", "Banquets", "Facilities", "Exterior", "Interior", "Events"]
    filter_html = "\n".join(
        f'        <button class="gp-filter__btn" type="button" data-filter="{f.lower()}" aria-pressed="{"true" if f == "All" else "false"}">{f}</button>'
        for f in filters)

    items = [
        ("exterior-view", 900, 675, "Hotel Green Plaza exterior in Bhilwara", "Hotel exterior", "hotel exterior"),
        ("main-entrance", 900, 1200, "Main entrance of Hotel Green Plaza", "Main entrance", "hotel exterior"),
        ("lobby-seating", 900, 675, "Lobby seating area at Hotel Green Plaza", "Lobby seating", "hotel interior facilities"),
        ("guest-room-interior", 900, 1200, "Well-furnished guest room at Hotel Green Plaza", "Guest room", "rooms interior"),
        ("room-bathroom", 900, 675, "Attached bathroom in a guest room at Hotel Green Plaza", "Attached bathroom", "rooms facilities"),
        ("restaurant-seating", 900, 675, "Pure vegetarian restaurant at Hotel Green Plaza", "Restaurant seating", "restaurant interior"),
        ("vegetarian-dishes", 900, 1200, "Vegetarian dishes served at Hotel Green Plaza", "Vegetarian dishes", "restaurant"),
        ("banquet-hall-setup", 900, 675, "Banquet hall at Hotel Green Plaza", "Banquet hall", "banquets interior"),
        ("conference-hall", 900, 675, "Conference hall at Hotel Green Plaza", "Conference hall", "banquets facilities"),
        ("event-celebration", 900, 1200, "Event celebration at Hotel Green Plaza", "Celebration", "events banquets"),
        ("reception-desk", 900, 675, "Reception desk at Hotel Green Plaza", "Reception", "hotel facilities interior"),
        ("corridor-interior", 900, 675, "Guest room corridor at Hotel Green Plaza", "Corridor", "hotel interior"),
    ]
    item_html = "\n".join(f"""        <div class="gp-masonry__item gp-reveal" data-category="all {cats}">
          <button class="gp-thumb" type="button" aria-label="View larger image: {alt}">
            <img src="/assets/img/gallery/hotel-green-plaza-{slug}.webp" width="{w}" height="{h}" loading="lazy" alt="{alt}">
            <span class="gp-thumb__label">{label}</span>
          </button>
        </div>""" for slug, w, h, alt, label, cats in items)

    return banner(
        "Gallery",
        "Rooms, restaurant, banquet spaces and the property itself.",
        "Gallery",
        "/assets/img/hero/hotel-green-plaza-gallery-banner.webp",
        "Hotel Green Plaza in Bhilwara",
    ) + f"""
  <!-- ============================== GALLERY ============================== -->
  <section class="gp-section gp-bg-white">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">Photographs</span>
        <h2>A Look Around Hotel Green Plaza</h2>
        <p>Filter by area, then select any photograph to view it larger.</p>
      </div>

      <div class="gp-filter" role="group" aria-label="Filter gallery by category">
{filter_html}
      </div>

      <div class="gp-masonry">
{item_html}
      </div>

      <p class="gp-small gp-text-center gp-mt-40 gp-mx-auto gp-narrow">All photographs on this page are placeholders. [VERIFY: supply real hotel photography for every gallery category]</p>
    </div>
  </section>

{cta_band()}"""


def contact_body():
    blocks = [
        ("pin", "Address", BHILWARA["html"]),
        ("phone", "Phone", phone_links(BHILWARA["phones"], "<br>")),
        ("mail", "Email", '<a href="mailto:%s">%s</a>' % (BHILWARA["email"], BHILWARA["email"])),
        ("bed", "Hotel, Restaurant &amp; Banquet Enquiries",
         'All enquiries are handled on the numbers above, or send the form '
         'alongside and choose your enquiry type.<br>'
         '<span class="gp-small">[VERIFY: separate direct lines for hotel, restaurant '
         'and banquet enquiries, if the hotel uses them]</span>'),
    ]
    block_html = "\n".join(f"""              <li class="gp-contact-item">
                <span class="gp-contact-item__icon">{icon(n)}</span>
                <div>
                  <h3>{t}</h3>
                  <p>{d}</p>
                </div>
              </li>""" for n, t, d in blocks)

    branch_cards = "\n".join("""        <div class="col-12 col-md-6 col-lg-5">
          <article class="gp-service gp-reveal">
            <span class="gp-service__icon">%s</span>
            <h3>Hotel Green Plaza, %s</h3>
            <p>%s</p>
            <ul class="gp-feature-list gp-mt-24">
              <li>%s<span>%s</span></li>
              <li>%s<span><a href="mailto:%s">%s</a></span></li>
            </ul>
          </article>
        </div>""" % (
        icon("building"), b["name"], b["html"],
        icon("phone", "gp-icon--sm"), phone_links(b["phones"], "<br>"),
        icon("mail", "gp-icon--sm"), b["email"], b["email"],
    ) for b in BRANCHES)

    return banner(
        "Contact Hotel Green Plaza",
        "Have a question about accommodation, dining, banquets or hotel services? Get in touch with Hotel Green Plaza.",
        "Contact Us",
        "/assets/img/hero/hotel-green-plaza-contact-banner.webp",
        "Reception at Hotel Green Plaza in Bhilwara",
    ) + f"""
  <!-- ========================= CONTACT INFORMATION ========================= -->
  <section class="gp-section gp-bg-white" id="enquiry">
    <div class="container">
      <div class="row gp-split align-items-start">
        <div class="col-12 col-lg-5">
          <div class="gp-reveal">
            <span class="gp-eyebrow">Contact</span>
            <h2>Get in Touch</h2>
            <p>Have a question about accommodation, dining, banquets or hotel services? Get in touch with Hotel Green Plaza.</p>

            <ul class="gp-contact-list gp-mt-32">
{block_html}
            </ul>
          </div>
        </div>

        <div class="col-12 col-lg-7">
          <div class="gp-form-panel gp-reveal">
            <h3>Send Us an Enquiry</h3>
{enquiry_form()}
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ========================== OTHER LOCATIONS ========================== -->
  <section class="gp-section gp-bg-tint">
    <div class="container">
      <div class="gp-heading gp-text-center gp-narrow gp-mx-auto gp-reveal">
        <span class="gp-eyebrow">Our Other Locations</span>
        <h2>Hotel Green Plaza in Madhya Pradesh</h2>
        <p>This website covers our Bhilwara hotel. Our two other properties can be reached directly on the details below.</p>
      </div>

      <div class="row gp-gap-30 justify-content-center">
{branch_cards}
      </div>

      <p class="gp-small gp-text-center gp-mt-32 gp-mx-auto gp-narrow">[VERIFY: rooms, dining and banquet facilities at the Neemuch and Jaora properties — nothing is described here because no details were supplied]</p>
    </div>
  </section>

{location_section('gp-bg-cream')}
{cta_band()}"""


# --------------------------------------------------------------------------
# Write
# --------------------------------------------------------------------------

PAGES = [
    ("/", "index.html",
     "Hotel Green Plaza Bhilwara | Hotel, Restaurant &amp; Banquets",
     "Hotel Green Plaza in Bhilwara offers comfortable accommodation, pure vegetarian dining, banquet facilities and convenient hotel services for business, family and event stays.",
     home_body, None, "/assets/img/hero/hotel-green-plaza-bhilwara-exterior.webp", [RESTAURANT_SCHEMA]),

    ("/about-us/", "about-us/index.html",
     "About Hotel Green Plaza | Hotel in Bhilwara",
     "Hotel Green Plaza is a comfortable hotel in Bhilwara offering accommodation, pure vegetarian dining, banquet facilities and a range of guest services.",
     about_body, "About Us", "/assets/img/hero/hotel-green-plaza-about-banner.webp", None),

    ("/accommodation/", "accommodation/index.html",
     "Hotel Rooms in Bhilwara | Hotel Green Plaza",
     "Comfortable, well-furnished AC and Non-AC rooms at Hotel Green Plaza Bhilwara, with attached bathrooms, digital television and 24-hour room service.",
     accommodation_body, "Accommodation", "/assets/img/hero/hotel-green-plaza-accommodation-banner.webp", None),

    ("/restaurant/", "restaurant/index.html",
     "Pure Vegetarian Restaurant in Bhilwara | Hotel Green Plaza",
     "A lobby-level pure vegetarian multi-cuisine restaurant at Hotel Green Plaza Bhilwara, with warm wooden interiors and a comfortable dining environment.",
     restaurant_body, "Restaurant", "/assets/img/hero/hotel-green-plaza-restaurant-banner.webp", [RESTAURANT_SCHEMA]),

    ("/banquets/", "banquets/index.html",
     "Banquet Hall in Bhilwara | Hotel Green Plaza",
     "Banquet facilities at Hotel Green Plaza Bhilwara, suitable for family functions, social gatherings, conferences, business meetings and celebrations.",
     banquets_body, "Banquets", "/assets/img/hero/hotel-green-plaza-banquets-banner.webp", None),

    ("/services/", "services/index.html",
     "Hotel Services &amp; Amenities in Bhilwara | Hotel Green Plaza",
     "Hotel Green Plaza Bhilwara offers a 24/7 front desk, room service, doctor on call, laundry, car rental with EV charging, parking, a saloon, an ice cream parlor and more.",
     services_body, "Services", "/assets/img/hero/hotel-green-plaza-services-banner.webp", None),

    ("/gallery/", "gallery/index.html",
     "Gallery | Hotel Green Plaza Bhilwara",
     "Photographs of Hotel Green Plaza in Bhilwara — rooms, the pure vegetarian restaurant, banquet spaces, facilities and the property itself.",
     gallery_body, "Gallery", "/assets/img/hero/hotel-green-plaza-gallery-banner.webp", None),

    ("/contact/", "contact/index.html",
     "Contact Hotel Green Plaza | Bhilwara",
     "Contact Hotel Green Plaza in Bhilwara for accommodation, pure vegetarian dining, banquet and event enquiries, or send us a message using our enquiry form.",
     contact_body, "Contact Us", "/assets/img/hero/hotel-green-plaza-contact-banner.webp", None),
]


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with io.open(full, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)
    print("wrote", path)


SHARE_IMAGE = "/assets/img/general/hotel-green-plaza-bhilwara-share.jpg"

for url, path, title, desc, body_fn, crumb, og, extra in PAGES:
    # og/twitter always use the 1200x630 share card; `og` here is the page's
    # above-the-fold image and is only used as a preload hint.
    write(path, page(url, title, desc, body_fn(), SHARE_IMAGE, hero_preload=og,
                     crumb=crumb, extra_schema=extra))

# ---------------------------------------------------------------- 404
NOT_FOUND_BODY = f"""  <section class="gp-section gp-bg-white" style="padding-top:calc(var(--gp-header-h) + var(--gp-section))">
    <div class="container">
      <div class="gp-text-center gp-narrow gp-mx-auto">
        <span class="gp-eyebrow">Error 404</span>
        <h1>This page could not be found</h1>
        <p class="gp-lead gp-mx-auto">The page you were looking for may have moved or no longer exists. You can head back to the homepage or get in touch and we will help you find what you need.</p>
        <div class="gp-btn-group gp-btn-group--center gp-mt-32">
          <a class="gp-btn gp-btn--primary" href="/">Back to Homepage</a>
          <a class="gp-btn gp-btn--secondary" href="/contact/">Contact Us</a>
        </div>
        <hr class="gp-rule gp-rule-center">
        <nav aria-label="Popular pages">
          <h2 class="gp-h3">Popular pages</h2>
          <ul class="gp-btn-group gp-btn-group--center">
            <li><a class="gp-textlink" href="/accommodation/">Accommodation {icon('arrow-right', 'gp-icon--sm gp-icon--primary')}</a></li>
            <li><a class="gp-textlink" href="/restaurant/">Restaurant {icon('arrow-right', 'gp-icon--sm gp-icon--primary')}</a></li>
            <li><a class="gp-textlink" href="/banquets/">Banquets {icon('arrow-right', 'gp-icon--sm gp-icon--primary')}</a></li>
            <li><a class="gp-textlink" href="/gallery/">Gallery {icon('arrow-right', 'gp-icon--sm gp-icon--primary')}</a></li>
          </ul>
        </nav>
      </div>
    </div>
  </section>
"""

not_found = page("/404.html", "Page Not Found | Hotel Green Plaza Bhilwara",
                 "The page you were looking for could not be found. Return to the Hotel Green Plaza homepage or contact us for help.",
                 NOT_FOUND_BODY, "/assets/img/general/hotel-green-plaza-bhilwara-share.jpg")
not_found = not_found.replace('<link rel="canonical" href="%s/404.html">' % SITE,
                              '<meta name="robots" content="noindex, follow">')
write("404.html", not_found)

# ---------------------------------------------------------------- sitemap
urls = "\n".join(
    """  <url>
    <loc>%s%s</loc>
    <changefreq>monthly</changefreq>
    <priority>%s</priority>
  </url>""" % (SITE, u, "1.0" if u == "/" else "0.8")
    for u, *_ in PAGES)

write("sitemap.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
""")

write("robots.txt", f"""User-agent: *
Allow: /

# Working folders — delete both before deploying; these rules are a backstop only.
Disallow: /_build/
Disallow: /_theme-original/

Sitemap: {SITE}/sitemap.xml
""")

print("done")
