"""Generate branded placeholder imagery for Hotel Green Plaza.

Every file produced here is a PLACEHOLDER sized to the exact aspect ratio the
layout expects. Replace each file with a real photograph of the same dimensions
and the site will need no markup changes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

PRIMARY = (47, 93, 50)
DARK = (36, 61, 39)
OLIVE = (122, 151, 59)
FRESH = (148, 174, 73)
TINT = (238, 243, 229)
LINE = (232, 228, 216)
CREAM = (247, 247, 241)
WHITE = (255, 255, 255)

FONT_CANDIDATES = [
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/calibri.ttf",
]
FONT_BOLD_CANDIDATES = [
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def load_font(size, bold=False):
    for path in (FONT_BOLD_CANDIDATES if bold else FONT_CANDIDATES):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def quad(p0, p1, p2, steps=40):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    return pts


def leaf_polygon(cx, cy, size, tilt=0.0):
    """A single leaf built from two mirrored quadratic curves."""
    tip = (cx, cy - size)
    base = (cx, cy + size * 0.55)
    bulge = size * 0.62
    right = quad(tip, (cx + bulge, cy - size * 0.25), base)
    left = quad(base, (cx - bulge, cy - size * 0.25), tip)
    pts = right + left
    if tilt:
        import math
        c, s = math.cos(tilt), math.sin(tilt)
        pts = [((x - cx) * c - (y - cy) * s + cx, (x - cx) * s + (y - cy) * c + cy) for x, y in pts]
    return pts


def draw_leaf_mark(base, cx, cy, size, colour, opacity):
    """Layered two-leaf mark echoing the logo, drawn as a soft watermark."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rgba = colour + (int(255 * opacity),)
    d.polygon(leaf_polygon(cx - size * 0.30, cy + size * 0.10, size * 0.86, -0.45), fill=rgba)
    d.polygon(leaf_polygon(cx + size * 0.24, cy - size * 0.04, size, 0.30), fill=rgba)
    base.alpha_composite(layer)


def make(path, w, h, label, variant="light"):
    img = Image.new("RGBA", (w, h), WHITE + (255,))
    d = ImageDraw.Draw(img)

    if variant == "dark":
        d.rectangle([0, 0, w, h], fill=DARK + (255,))
        # soft diagonal tonal bands so the plate is not visually flat
        band = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        bd = ImageDraw.Draw(band)
        for i, alpha in enumerate((26, 16, 10)):
            off = w * (0.18 + i * 0.26)
            bd.polygon(
                [(off, h), (off + w * 0.34, h), (off + w * 0.62, 0), (off + w * 0.28, 0)],
                fill=PRIMARY + (alpha,),
            )
        img.alpha_composite(band)
        draw_leaf_mark(img, w * 0.5, h * 0.44, min(w, h) * 0.30, FRESH, 0.16)
        text_col = (255, 255, 255, 215)
        meta_col = (255, 255, 255, 130)
    else:
        d.rectangle([0, 0, w, h], fill=TINT + (255,))
        band = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        bd = ImageDraw.Draw(band)
        bd.polygon([(0, h), (w * 0.46, h), (w * 0.14, 0), (0, 0)], fill=CREAM + (170,))
        img.alpha_composite(band)
        draw_leaf_mark(img, w * 0.5, h * 0.42, min(w, h) * 0.26, OLIVE, 0.20)
        d.rectangle([0, 0, w - 1, h - 1], outline=LINE + (255,), width=max(1, w // 400))
        text_col = PRIMARY + (255,)
        meta_col = (90, 99, 87, 255)

    unit = min(w, h)
    f_label = load_font(max(13, int(unit * 0.052)), bold=True)
    f_meta = load_font(max(11, int(unit * 0.034)))

    label = label.upper()
    lw = d.textlength(label, font=f_label)
    ly = h * 0.66
    d.text((w / 2 - lw / 2, ly), label, font=f_label, fill=text_col)

    meta = f"PLACEHOLDER  ·  {w}×{h}"
    mw = d.textlength(meta, font=f_meta)
    d.text((w / 2 - mw / 2, ly + unit * 0.085), meta, font=f_meta, fill=meta_col)

    # lime hairline rule under the label — the brand's micro-accent
    rule_w = unit * 0.10
    ry = ly - unit * 0.045
    d.rectangle([w / 2 - rule_w / 2, ry, w / 2 + rule_w / 2, ry + max(2, unit * 0.006)],
                fill=(140, 198, 62, 255))

    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    rgb = img.convert("RGB")
    if out.lower().endswith((".jpg", ".jpeg")):
        rgb.save(out, "JPEG", quality=86, optimize=True)
    elif out.lower().endswith(".png"):
        img.save(out, "PNG", optimize=True)
    else:
        rgb.save(out, "WEBP", quality=82, method=6)
    print(f"{path}  {w}x{h}")


# ---------------------------------------------------------------- heroes
make("assets/img/hero/hotel-green-plaza-bhilwara-exterior.webp", 1920, 1080, "Hotel exterior", "dark")
for slug, label in [
    ("about", "About the hotel"),
    ("accommodation", "Guest rooms"),
    ("restaurant", "Restaurant"),
    ("banquets", "Banquet hall"),
    ("services", "Guest services"),
    ("gallery", "Hotel gallery"),
    ("contact", "Reception"),
]:
    make(f"assets/img/hero/hotel-green-plaza-{slug}-banner.webp", 1920, 760, label, "dark")
make("assets/img/hero/hotel-green-plaza-cta-band.webp", 1920, 700, "Hotel grounds", "dark")

# ---------------------------------------------------------------- general 3:2 / 4:3
make("assets/img/general/hotel-green-plaza-lobby.webp", 1000, 1250, "Hotel lobby")
make("assets/img/general/hotel-green-plaza-hospitality.webp", 1000, 1250, "Hospitality at Green Plaza")
make("assets/img/general/hotel-green-plaza-comfortable-rooms.webp", 900, 600, "Comfortable rooms")
make("assets/img/general/hotel-green-plaza-restaurant.webp", 900, 600, "Pure vegetarian dining")
make("assets/img/general/hotel-green-plaza-banquet-hall.webp", 900, 600, "Banquets & events")
make("assets/img/general/hotel-green-plaza-guest-services.webp", 900, 600, "Guest services")
make("assets/img/general/hotel-green-plaza-vegetarian-thali.webp", 1100, 733, "Vegetarian cuisine")
make("assets/img/general/hotel-green-plaza-banquet-event-setup.webp", 1100, 733, "Event setup")
make("assets/img/general/hotel-green-plaza-restaurant-interior.webp", 1100, 733, "Restaurant interior")
make("assets/img/general/hotel-green-plaza-restaurant-dining.webp", 900, 600, "Dining area")
make("assets/img/general/hotel-green-plaza-conference-setup.webp", 900, 600, "Conference setup")
make("assets/img/general/hotel-green-plaza-front-desk.webp", 1100, 733, "24/7 front desk")
make("assets/img/general/hotel-green-plaza-room-facilities.webp", 1100, 733, "Room facilities")

# ---------------------------------------------------------------- rooms 4:3
for slug, label in [
    ("ac-non-ac-room", "AC & Non-AC rooms"),
    ("double-bed-room", "Double bed room"),
    ("double-triple-bed-room", "Double / triple bed"),
    ("super-deluxe-triple-room", "Super deluxe triple"),
]:
    make(f"assets/img/rooms/hotel-green-plaza-{slug}.webp", 880, 660, label)

# ---------------------------------------------------------------- gallery
GALLERY = [
    ("exterior-view", "Hotel exterior", 900, 675),
    ("main-entrance", "Main entrance", 900, 1200),
    ("lobby-seating", "Lobby seating", 900, 675),
    ("guest-room-interior", "Guest room", 900, 1200),
    ("room-bathroom", "Attached bathroom", 900, 675),
    ("restaurant-seating", "Restaurant seating", 900, 675),
    ("vegetarian-dishes", "Vegetarian dishes", 900, 1200),
    ("banquet-hall-setup", "Banquet hall", 900, 675),
    ("conference-hall", "Conference hall", 900, 675),
    ("event-celebration", "Event celebration", 900, 1200),
    ("reception-desk", "Reception desk", 900, 675),
    ("corridor-interior", "Hotel corridor", 900, 675),
]
for slug, label, w, h in GALLERY:
    make(f"assets/img/gallery/hotel-green-plaza-{slug}.webp", w, h, label)

# ---------------------------------------------------------------- social card
make("assets/img/general/hotel-green-plaza-bhilwara-share.jpg", 1200, 630, "Hotel Green Plaza · Bhilwara", "dark")


# ---------------------------------------------------------------- logo + icons
src = os.path.join(ROOT, "assets/img/logo/hotel-green-plaza-logo-source.jpg")
logo = Image.open(src).convert("RGB")
print("source logo:", logo.size)
logo.save(os.path.join(ROOT, "assets/img/logo/hotel-green-plaza-logo.png"), "PNG", optimize=True)
logo.save(os.path.join(ROOT, "assets/img/logo/hotel-green-plaza-logo.webp"), "WEBP", quality=92, method=6)

# favicon / touch icon: the leaf mark on brand green (a mark, not the logo itself)
for size, name in [(32, "favicon-32.png"), (180, "apple-touch-icon.png"), (512, "icon-512.png")]:
    ic = Image.new("RGBA", (size, size), PRIMARY + (255,))
    draw_leaf_mark(ic, size * 0.5, size * 0.5, size * 0.30, (255, 255, 255), 0.92)
    ic.save(os.path.join(ROOT, "assets/img/logo", name), "PNG", optimize=True)
print("icons written")
