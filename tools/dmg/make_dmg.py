#!/usr/bin/env python3
"""Builds a pretty "drag to Applications" disk image for one app.

Shared layout for every app (serif headline, hand-drawn arrow, dashed
Applications spot); each app gets its own colour and background art.
Uses dmgbuild, which writes the window layout straight into the image, so
the background shows every time the disk image is opened, on any Mac.

Usage: make_dmg.py --app X.app --name Ludus --out Ludus.dmg   (style and colour come from PRESETS)
"""
import argparse, math, os, random, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont

W, H = 660, 420
# Where Finder opens the window. Finder counts from the BOTTOM-left of the screen, and the spot is fixed
# inside the image, so it can't follow each Mac's screen. (405, 268) is the exact middle of a 13"/15"
# MacBook Air (1470x956) and within about 20 points of the middle on a 14" MacBook Pro.
# (200, 140) was the old value: bottom-left.
WINDOW_POS = (405, 268)
# Each app's look, so a release only needs --app and --name.
PRESETS = {"Ludus": ("ludus", "#c16545"), "Awayke": ("awayke", "#e66c0e"), "Memo": ("memo", "#3552aa"),
           "Nox": ("nox", "#5a44c3"), "Roomy": ("roomy", "#2f8f86"), "Stats": ("stats", "#5e6878"),
           "murmur": ("murmur", "#4a4a50")}
APP_POS, APPS_POS = (190, 250), (470, 250)
INK = (44, 40, 36)
SUP = "/System/Library/Fonts/Supplemental/"
FONTS = {  # (regular face, bold face) as (file, index or variation name)
    "rounded": (("/System/Library/Fonts/SFNSRounded.ttf", "Regular"), ("/System/Library/Fonts/SFNSRounded.ttf", "Semibold")),
    "avenir": (("/System/Library/Fonts/Avenir Next.ttc", 7), ("/System/Library/Fonts/Avenir Next.ttc", 2)),
    "futura": ((SUP + "Futura.ttc", 0), (SUP + "Futura.ttc", 2)),
    "baskerville": ((SUP + "Baskerville.ttc", 2), (SUP + "Baskerville.ttc", 4)),
    "gill": ((SUP + "GillSans.ttc", 7), (SUP + "GillSans.ttc", 4)),
}
FONT = "rounded"


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    return tuple(round(a[i] * (1 - t) + b[i] * t) for i in range(3))


def art(d, s, style, accent, rnd):
    """Each app's own background art, faint so the text stays easy to read."""
    soft = accent + (34,)
    line = accent + (60,)
    if style == "ludus":  # confetti of little game pieces
        for _ in range(36):
            x, y, r = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(3, 7)
            if rnd.random() < .5:
                d.ellipse([s * (x - r), s * (y - r), s * (x + r), s * (y + r)], fill=soft)
            else:
                d.rectangle([s * (x - r), s * (y - r), s * (x + r), s * (y + r)], fill=soft)
    elif style == "memo":  # ruled notebook lines and a margin
        for y in range(40, H, 26):
            d.line([0, s * y, s * W, s * y], fill=line, width=max(1, s))
        d.line([s * 48, 0, s * 48, s * H], fill=accent + (80,), width=2 * s)
    elif style == "nox":  # moon and stars
        d.ellipse([s * 540, s * 34, s * 610, s * 104], fill=accent + (40,))
        d.ellipse([s * 558, s * 26, s * 628, s * 96], fill=(0, 0, 0, 0))
        for _ in range(28):
            x, y, r = rnd.uniform(0, W), rnd.uniform(0, H * .6), rnd.uniform(1, 2.4)
            d.ellipse([s * (x - r), s * (y - r), s * (x + r), s * (y + r)], fill=accent + (70,))
    elif style == "awayke":  # sun rays from the corner
        for k in range(9):  # short rays that stay in the corner
            a = math.radians(4 + k * 10.5)
            r0, r1 = 66, 128
            d.line([s * (W - r0 * math.cos(a)), s * r0 * math.sin(a), s * (W - r1 * math.cos(a)), s * r1 * math.sin(a)],
                   fill=accent + (55,), width=4 * s)
        d.ellipse([s * (W - 52), s * -52, s * (W + 52), s * 52], fill=accent + (70,))
    elif style == "stats":  # one simple line chart with its data points
        pts = [(x, 372 - 26 * math.sin(x / 85) - x * .07) for x in range(-10, W + 20, 60)]
        d.polygon([(s * x, s * y) for x, y in pts] + [(s * (W + 20), s * H), (s * -10, s * H)], fill=accent + (16,))
        d.line([(s * x, s * y) for x, y in pts], fill=accent + (80,), width=3 * s, joint="curve")
        for x, y in pts:
            d.ellipse([s * (x - 4), s * (y - 4), s * (x + 4), s * (y + 4)], fill=accent + (110,))
    elif style == "roomy":  # menu bar with tidy icon dots
        d.rectangle([0, 0, s * W, s * 22], fill=accent + (40,))
        for k in range(16):
            x = W - 30 - k * 24
            d.ellipse([s * (x - 5), s * 6, s * (x + 5), s * 16], fill=accent + (90,))
    elif style == "murmur":  # sound waves across the bottom
        for k in range(3):
            amp, off = 14 + k * 8, 336 + k * 16
            pts = [(x, off + amp * math.sin(x / (38 + k * 7) + k)) for x in range(0, W + 6, 6)]
            d.line([(s * x, s * y) for x, y in pts], fill=accent + (40 + k * 6,), width=2 * s)


def arrow(img, s, accent):
    """The pencil arrow (arrow.png), filled with the app's own colour."""
    shape = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "arrow.png")).convert("RGBA")
    art = Image.new("RGBA", shape.size, accent + (255,))
    art.putalpha(shape.getchannel("A"))
    w = 156
    h = round(w * art.height / art.width)
    art = art.resize((w * s, h * s), Image.LANCZOS)
    img.alpha_composite(art, ((APP_POS[0] + 52) * s, (APP_POS[1] - 60 - h) * s))


def font(path, face, size):
    if isinstance(face, int):
        return ImageFont.truetype(path, size, index=face)
    f = ImageFont.truetype(path, size)
    f.set_variation_by_name(face)
    return f


def render(name, style, color, path, s):
    accent = hex_rgb(color)
    paper = mix(accent, (247, 244, 238), 0.9)
    img = Image.new("RGBA", (W * s, H * s), paper + (255,))
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    art(ImageDraw.Draw(layer), s, style, accent, random.Random(name))
    img = Image.alpha_composite(img, layer)
    top = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(top)
    arrow(top, s, accent)
    (lp, li), (bp, bi) = FONTS[os.environ.get("DMG_FONT", FONT)]
    f_light, f_bold = (font(p, i, 30 * s) for p, i in ((lp, li), (bp, bi)))
    grey, dark = (118, 112, 106, 255), INK + (255,)
    for row, parts in enumerate([[("To install, drag ", f_light, grey), (name, f_bold, dark)],
                                 [("to ", f_light, grey), ("Applications", f_bold, dark)]]):
        widths = [d.textlength(t, font=f) for t, f, _ in parts]
        x = (W * s - sum(widths)) / 2
        for (t, f, c), w in zip(parts, widths):
            d.text((x, (44 + row * 40) * s), t, font=f, fill=c)
            x += w
    Image.alpha_composite(img, top).convert("RGB").save(path, dpi=(72 * s, 72 * s))


def applications_alias(tmp):
    """An alias to /Applications that carries its own modern icon (a symlink
    would always show the system folder icon). /Applications is not touched."""
    here = os.path.dirname(os.path.abspath(__file__))
    tool = os.path.join(tmp, "mkalias")
    subprocess.run(["swiftc", "-O", os.path.join(here, "mkalias.swift"), "-o", tool], check=True, capture_output=True)
    out = os.path.join(tmp, "Applications")
    subprocess.run([tool, "/Applications", out, os.path.join(here, "applications-icon.png")], check=True, capture_output=True)
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--app", required=True); p.add_argument("--name", required=True)
    p.add_argument("--style"); p.add_argument("--color")
    p.add_argument("--out", required=True); p.add_argument("--volname")
    p.add_argument("--background-only", action="store_true")
    a = p.parse_args()
    if not (a.style and a.color):
        if a.name not in PRESETS: p.error("--style and --color are needed for an app without a preset")
        a.style, a.color = a.style or PRESETS[a.name][0], a.color or PRESETS[a.name][1]
    tmp = tempfile.mkdtemp()
    one, two, tiff = (os.path.join(tmp, n) for n in ("bg.png", "bg@2x.png", "bg.tiff"))
    render(a.name, a.style, a.color, one, 1)
    render(a.name, a.style, a.color, two, 2)
    subprocess.run(["tiffutil", "-cathidpicheck", one, two, "-out", tiff], check=True, capture_output=True)
    if a.background_only:
        print(two); return
    import dmgbuild
    app = os.path.abspath(a.app); base = os.path.basename(app)
    if not app.startswith("/Applications/"):  # show "Ludus", not "Ludus.app"
        subprocess.run(["SetFile", "-a", "E", app], check=False)
    alias = applications_alias(tmp)
    settings = {
        "files": [app, alias],
        "background": tiff, "icon_locations": {base: APP_POS, "Applications": APPS_POS},
        "window_rect": (WINDOW_POS, (W, H)), "icon_size": 104, "text_size": 15,
        "show_status_bar": False, "show_tab_view": False, "show_toolbar": False,
        "show_pathbar": False, "show_sidebar": False, "default_view": "icon-view",
        "hide_extensions": [base], "format": "UDZO", "filesystem": "HFS+",
    }
    dmgbuild.build_dmg(a.out, a.volname or a.name, settings=settings)
    print(a.out)


if __name__ == "__main__":
    main()
