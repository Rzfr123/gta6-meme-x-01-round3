#!/usr/bin/env python3
"""Render the gta6-meme-x-01 round-3 meme: RETRO PIXEL-ART, PC-USER gag.

GTA 6 launched on consoles (PS5/Xbox, 19 Nov 2026) and console players
are already playing — while PC players are still waiting, with no PC
version at launch (Rockstar's PC ports historically arrive much later;
GTA V took ~1.5 years). That wait IS the weakness gag, merged with the
13-year / delays theme: the pixel PC gamer waited so long he AGED at
his keyboard, grey hair and cobwebbed beard, while the console
controller lies unused on the floor.

Exactly three text elements in the whole picture (one clean gag, no
stack — round 1's judge critique was cluttered stacked text):

  - "WASTED": huge grey pixel death-screen lettering across the open
    night sky (GTA death screen, drawn as text — no copyrighted art).
  - One satire line: "CONSOLES PLAYING. PC STILL WAITING."
  - One punchline in the bottom bar, next to the REAL make.fun ghost:
    "MY AI AGENT ALREADY WON / REAL MONEY ON make.fun" (one punchline,
    split over two short lines).

Pixel style: the base scene is an original 16-bit-style illustration
generated in-session (no text, no logos in the art). ALL text is drawn
with PIL, rendered small and upscaled with NEAREST so the letters are
chunky pixels too. The ghost is the REAL make.fun press-kit asset
(assets/mark-1024.png), downscaled to 48px and upscaled NEAREST to
160px so it matches the bit style while staying the real asset and
clearly recognisable — it is NEVER redrawn.

Layout (1024x1024): starry night-sky band on top (y 0..220) holding
WASTED + the satire line; the base scene cropped to 16:9 and scaled to
1024x620 (y 220..840); a dark bottom bar (y 840..1024) holding the
pixelated ghost + the punchline.
"""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W = 1024
SKY_H = 220          # night-sky band on top
BASE_H = 620         # base scene height
BAR_Y0 = SKY_H + BASE_H   # 840, bottom punchline bar starts here
BASE = ASSETS / ("media-generation-gta6-round3-pixel-pc-base-0-"
                 "d77bcd88-5c96-465c-a5c1-e1a133037403.png")
GHOST = ASSETS / "mark-1024.png"

SKY = (23, 16, 46)        # dark night navy, sampled from the base sky
BAR = (18, 10, 36)        # darker plum for the bottom bar
WASTED_GREY = (200, 200, 205)


def pixel_text(base_img, cx, y_top, text, px_size, fill, scale=3,
               letter_gap=0, stroke_px=0, stroke_fill="black"):
    """Draw `text` as chunky pixel letters.

    Renders the text small on a throwaway layer (font px_size // scale)
    then upscales it with NEAREST so every glyph is made of square
    pixels. Returns the drawn height in full-size pixels.
    """
    small_size = max(8, px_size // scale)
    font = ImageFont.truetype(BOLD, small_size)
    # Measure at small scale, letter by letter for the gap.
    widths = []
    for ch in text:
        widths.append(font.getlength(ch))
    gap_small = letter_gap // scale
    total_small = sum(widths) + gap_small * max(0, len(text) - 1)
    layer_w = int(total_small) + 4 * small_size
    layer_h = small_size * 2 + 4
    layer = Image.new("RGBA", (layer_w, layer_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x = 2 * small_size
    y = small_size // 2
    sw = max(1, stroke_px // scale) if stroke_px else 0
    for ch, wch in zip(text, widths):
        d.text((x, y), ch, font=font, fill=fill,
               stroke_width=sw, stroke_fill=stroke_fill)
        x += wch + gap_small
    up = layer.resize((layer_w * scale, layer_h * scale), Image.NEAREST)
    # Trim transparent borders, then paste centred at cx / y_top.
    bbox = up.getbbox()
    up = up.crop(bbox)
    paste_x = cx - up.width // 2
    base_img.paste(up, (paste_x, y_top), up)
    return up.height


def pixelate(img, small, out_size):
    """Nearest-neighbour downscale then upscale: real asset, bit style."""
    tiny = img.resize((small, small), Image.LANCZOS)
    return tiny.resize(out_size, Image.NEAREST)


def main():
    img = Image.new("RGB", (W, W), SKY)
    draw = ImageDraw.Draw(img)

    # --- Starry pixel sky (deterministic) -------------------------------
    rng = random.Random(6)
    for _ in range(90):
        x = rng.randrange(0, W - 4)
        y = rng.randrange(0, SKY_H - 4)
        s = rng.choice([2, 2, 3, 3, 4])
        c = rng.choice([(255, 255, 255), (200, 180, 255),
                        (255, 200, 230), (160, 160, 220)])
        draw.rectangle([x, y, x + s - 1, y + s - 1], fill=c)
    for _ in range(10):  # plus-shaped sparkles, like the base sky
        x = rng.randrange(20, W - 20)
        y = rng.randrange(10, SKY_H - 20)
        c = (230, 220, 255)
        draw.rectangle([x - 5, y - 1, x + 5, y + 1], fill=c)
        draw.rectangle([x - 1, y - 5, x + 1, y + 5], fill=c)

    # --- Base scene: crop to 16:9, scale to 1024x620 --------------------
    base = Image.open(BASE).convert("RGB")
    bw, bh = base.size  # 1920x1280
    crop_h = int(bw * 9 / 16)  # 1080
    top = 60  # keep the desk, trim a little floor
    base = base.crop((0, top, bw, top + crop_h))
    base = base.resize((W, BASE_H), Image.LANCZOS)
    img.paste(base, (0, SKY_H))

    # --- Bottom bar ------------------------------------------------------
    draw.rectangle([0, BAR_Y0, W - 1, W - 1], fill=BAR)
    draw.rectangle([0, BAR_Y0, W - 1, BAR_Y0 + 5], fill=(255, 64, 160))

    # --- WASTED: huge pixel death-screen letters across the sky ---------
    wasted_h = pixel_text(img, W // 2, 18, "WASTED", 118,
                          WASTED_GREY, scale=4, letter_gap=16,
                          stroke_px=8, stroke_fill="black")
    assert wasted_h <= 140, f"WASTED too tall: {wasted_h}"

    # --- One satire line, under WASTED, still in the sky band -----------
    sat_h = pixel_text(img, W // 2, 158, "CONSOLES PLAYING. PC STILL WAITING.",
                       40, "white", scale=3, stroke_px=6,
                       stroke_fill="black")
    assert 158 + sat_h <= SKY_H - 4, "satire line runs past the sky band"

    # --- Real make.fun ghost, pixelated, in the bottom bar --------------
    ghost = Image.open(GHOST).convert("RGBA")
    ghost_px = pixelate(ghost, 48, (160, 160))
    img.paste(ghost_px, (28, BAR_Y0 + 14), ghost_px)

    # --- Punchline: one line of copy, two short rows, right of ghost ----
    px = 212
    y1 = BAR_Y0 + 30
    h1 = pixel_text(img, px + (W - px - 24) // 2, y1,
                    "MY AI AGENT ALREADY WON", 42, "white",
                    scale=3, stroke_px=6, stroke_fill="black")
    y2 = y1 + h1 + 12
    h2 = pixel_text(img, px + (W - px - 24) // 2, y2,
                    "REAL MONEY ON make.fun", 42, (255, 220, 90),
                    scale=3, stroke_px=6, stroke_fill="black")
    assert y2 + h2 <= W - 12, "punchline runs past the bottom edge"

    img.save(HERE / "meme.png", "PNG")
    print("wrote meme.png", img.size)


if __name__ == "__main__":
    main()
