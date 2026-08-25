"""Replace the abstract branded placeholder graphics with real random
photographs at the exact same paths, dimensions and aspect ratios.

These are still placeholders — the goal is to make the site preview like a
finished hotel site instead of a set of text cards, not to publish these as
final photography. Every image keeps the same filename, so swapping in real
property photos later still requires no markup changes.

Source: loremflickr.com — serves real, freely licensed Flickr photos matched
to keywords, at an exact requested size. Each request is cache-busted with a
random id so repeated categories (e.g. four different room shots) don't all
return the same photo.

Run:  python _build/fetch_placeholder_photos.py
"""
import io
import os
import random
import time
import urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# (relative path from repo root, width, height, keyword list for the photo search)
IMAGES = [
    # --- hero / banner plates -------------------------------------------------
    # hotel-green-plaza-bhilwara-exterior.webp is intentionally NOT in this list:
    # it's a real photo of the hotel now (see _build/build.py), not a placeholder.
    ("assets/img/hero/hotel-green-plaza-about-banner.webp", 1920, 760, "hotel,lobby,interior"),
    ("assets/img/hero/hotel-green-plaza-accommodation-banner.webp", 1920, 760, "hotel,bedroom"),
    ("assets/img/hero/hotel-green-plaza-restaurant-banner.webp", 1920, 760, "restaurant,interior"),
    ("assets/img/hero/hotel-green-plaza-banquets-banner.webp", 1920, 760, "banquet,hall,event"),
    ("assets/img/hero/hotel-green-plaza-services-banner.webp", 1920, 760, "hotel,reception,frontdesk"),
    ("assets/img/hero/hotel-green-plaza-gallery-banner.webp", 1920, 760, "hotel,architecture"),
    ("assets/img/hero/hotel-green-plaza-contact-banner.webp", 1920, 760, "hotel,reception"),
    ("assets/img/hero/hotel-green-plaza-cta-band.webp", 1920, 700, "hotel,resort,building"),

    # --- general (homepage teasers, about/services split blocks) --------------
    ("assets/img/general/hotel-green-plaza-lobby.webp", 1000, 1250, "hotel,lobby"),
    ("assets/img/general/hotel-green-plaza-hospitality.webp", 1000, 1250, "hotel,interior,corridor"),
    ("assets/img/general/hotel-green-plaza-comfortable-rooms.webp", 900, 600, "hotel,bedroom"),
    ("assets/img/general/hotel-green-plaza-restaurant.webp", 900, 600, "restaurant,interior"),
    ("assets/img/general/hotel-green-plaza-banquet-hall.webp", 900, 600, "banquet,hall"),
    ("assets/img/general/hotel-green-plaza-guest-services.webp", 900, 600, "hotel,reception,frontdesk"),
    ("assets/img/general/hotel-green-plaza-vegetarian-thali.webp", 1100, 733, "indian,food,vegetarian"),
    ("assets/img/general/hotel-green-plaza-banquet-event-setup.webp", 1100, 733, "wedding,banquet,event"),
    ("assets/img/general/hotel-green-plaza-restaurant-interior.webp", 1100, 733, "restaurant,interior,wood"),
    ("assets/img/general/hotel-green-plaza-restaurant-dining.webp", 900, 600, "restaurant,dining"),
    ("assets/img/general/hotel-green-plaza-conference-setup.webp", 900, 600, "conference,meetingroom"),
    ("assets/img/general/hotel-green-plaza-front-desk.webp", 1100, 733, "hotel,reception,frontdesk"),
    ("assets/img/general/hotel-green-plaza-room-facilities.webp", 1100, 733, "hotel,bedroom,interior"),
    # hotel-green-plaza-bhilwara-share.jpg is also cropped from the real exterior
    # photo — not in this list for the same reason as the hero image above.

    # --- room categories --------------------------------------------------------
    ("assets/img/rooms/hotel-green-plaza-ac-non-ac-room.webp", 880, 660, "hotel,bedroom"),
    ("assets/img/rooms/hotel-green-plaza-double-bed-room.webp", 880, 660, "hotel,bedroom,doublebed"),
    ("assets/img/rooms/hotel-green-plaza-double-triple-bed-room.webp", 880, 660, "hotel,room,beds"),
    ("assets/img/rooms/hotel-green-plaza-super-deluxe-triple-room.webp", 880, 660, "hotel,suite"),

    # --- gallery ------------------------------------------------------------
    ("assets/img/gallery/hotel-green-plaza-exterior-view.webp", 900, 675, "hotel,exterior,building"),
    ("assets/img/gallery/hotel-green-plaza-main-entrance.webp", 900, 1200, "hotel,entrance,lobby"),
    ("assets/img/gallery/hotel-green-plaza-lobby-seating.webp", 900, 675, "hotel,lobby,seating"),
    ("assets/img/gallery/hotel-green-plaza-guest-room-interior.webp", 900, 1200, "hotel,bedroom"),
    ("assets/img/gallery/hotel-green-plaza-room-bathroom.webp", 900, 675, "bathroom,hotel"),
    ("assets/img/gallery/hotel-green-plaza-restaurant-seating.webp", 900, 675, "restaurant,interior"),
    ("assets/img/gallery/hotel-green-plaza-vegetarian-dishes.webp", 900, 1200, "indian,food,vegetarian"),
    ("assets/img/gallery/hotel-green-plaza-banquet-hall-setup.webp", 900, 675, "banquet,hall,event"),
    ("assets/img/gallery/hotel-green-plaza-conference-hall.webp", 900, 675, "conference,meetingroom"),
    ("assets/img/gallery/hotel-green-plaza-event-celebration.webp", 900, 1200, "wedding,celebration,event"),
    ("assets/img/gallery/hotel-green-plaza-reception-desk.webp", 900, 675, "hotel,reception,frontdesk"),
    ("assets/img/gallery/hotel-green-plaza-corridor-interior.webp", 900, 675, "hotel,corridor,hallway"),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; HotelGreenPlazaBuild/1.0)"}


def fetch(width, height, keywords, tries=4):
    for attempt in range(tries):
        rand = random.randint(1, 10_000_000)
        url = f"https://loremflickr.com/{width}/{height}/{keywords}?random={rand}"
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
            if len(data) > 3000:  # loremflickr's "not found" placeholder is tiny
                return data
        except Exception as exc:  # noqa: BLE001 - just retry
            print(f"  attempt {attempt + 1} failed: {exc}")
        time.sleep(1)
    return None


def main():
    from PIL import Image

    ok, failed = 0, []
    for rel_path, w, h, keywords in IMAGES:
        out = os.path.join(ROOT, rel_path)
        print(f"{rel_path}  ({w}x{h})  [{keywords}]")
        data = fetch(w, h, keywords)
        if not data:
            print("  FAILED — keeping existing placeholder")
            failed.append(rel_path)
            continue

        img = Image.open(io.BytesIO(data)).convert("RGB")
        # loremflickr already returns the exact size, but crop/resize defensively
        img = crop_to_ratio(img, w, h)

        if out.lower().endswith((".jpg", ".jpeg")):
            img.save(out, "JPEG", quality=86, optimize=True)
        else:
            img.save(out, "WEBP", quality=82, method=6)
        ok += 1

    print(f"\n{ok}/{len(IMAGES)} images replaced.")
    if failed:
        print("Kept the branded placeholder for:")
        for f in failed:
            print(" -", f)


def crop_to_ratio(img, target_w, target_h):
    from PIL import Image

    target_ratio = target_w / target_h
    w, h = img.size
    ratio = w / h
    if abs(ratio - target_ratio) > 0.01:
        if ratio > target_ratio:
            new_w = int(h * target_ratio)
            x = (w - new_w) // 2
            img = img.crop((x, 0, x + new_w, h))
        else:
            new_h = int(w / target_ratio)
            y = (h - new_h) // 2
            img = img.crop((0, y, w, y + new_h))
    if img.size != (target_w, target_h):
        img = img.resize((target_w, target_h), Image.LANCZOS)
    return img


if __name__ == "__main__":
    main()
