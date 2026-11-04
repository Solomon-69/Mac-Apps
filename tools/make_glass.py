#!/usr/bin/env python3
"""Turns the real app panel screenshots into clean menu bar popovers for the deck cards:
crops each screenshot to the panel body (dropping any baked-in shadow or old arrow),
gives it smooth rounded corners and a thin edge, and adds one macOS style arrow
(curved sides, rounded tip) centred on top. Everything is drawn 4x and scaled down
so the edges stay smooth."""
import pathlib
import numpy as np
from PIL import Image, ImageDraw
root = pathlib.Path(__file__).resolve().parent.parent
INSET = 4
SS = 4  # supersampling for smooth edges


def body(im):
    """Crop to the panel body: rows at least 90% as wide as the widest row."""
    a = np.array(im)[..., 3]
    w = (a > 200).sum(1); mx = w.max()
    rows = np.where(w > .9 * mx)[0]
    t, b = rows[0], rows[-1]
    cols = np.where((a[t:b+1] > 200).mean(0) > .5)[0]
    return im.crop((cols[0], t, cols[-1] + 1, b + 1))


def bez(p0, p1, p2, p3, n=40):
    t = np.linspace(0, 1, n)[:, None]
    return ((1-t)**3)*p0 + 3*((1-t)**2)*t*p1 + 3*(1-t)*t*t*p2 + (t**3)*p3


def arrow_pts(cx, base, aw, ah):
    """macOS popover arrow: concave sides that flare into the body, soft round tip."""
    L, R, tip = np.array([cx-aw/2, base]), np.array([cx+aw/2, base]), np.array([cx, base-ah])
    left = bez(L, L + [aw*.20, 0], tip + [-aw*.16, ah*.30], tip + [-aw*.075, ah*.06])
    cap = bez(tip + [-aw*.075, ah*.06], tip + [-aw*.03, -ah*.04], tip + [aw*.03, -ah*.04], tip + [aw*.075, ah*.06], 16)
    right = bez(tip + [aw*.075, ah*.06], tip + [aw*.16, ah*.30], R - [aw*.20, 0], R)
    return [tuple(p) for p in np.vstack([left, cap, right])]


def popover(src, dst, dark):
    im = body(Image.open(root/src).convert("RGBA"))
    im = im.crop((INSET, INSET, im.width - INSET, im.height - INSET))  # drop the dark rim baked into the screenshot edge
    w, h = im.size
    r = round(w * .05); ah = round(w * .036); aw = round(ah * 3.6)
    big = im.resize((w*SS, h*SS), Image.LANCZOS).convert("RGB")
    top = np.array(big)[SS*4:SS*10, w*SS//2 - aw*SS//2: w*SS//2 + aw*SS//2]
    col = tuple(int(v) for v in np.median(top.reshape(-1, 3), 0))
    H = (h + ah) * SS; W = w * SS; o = ah * SS
    canvas = Image.new("RGB", (W, H), col); canvas.paste(big.crop((0, SS*3, W, SS*3+1)).resize((W, o + SS*3)), (0, 0)); canvas.paste(big, (0, o))
    mask = Image.new("L", (W, H), 0); d = ImageDraw.Draw(mask)
    d.rounded_rectangle((0, o, W-1, H-1), r*SS, fill=255)
    d.polygon(arrow_pts(W/2, o + SS*2, aw*SS, ah*SS + SS*2), fill=255)
    edge = Image.new("L", (W, H), 0); e = ImageDraw.Draw(edge)
    e.rounded_rectangle((0, o, W-1, H-1), r*SS, outline=255, width=SS)
    e.polygon(arrow_pts(W/2, o + SS*4, aw*SS - SS*2, ah*SS), fill=0)
    e.line(arrow_pts(W/2, o + SS*2, aw*SS, ah*SS + SS*2), fill=255, width=SS)
    edge = Image.fromarray((np.array(edge) * (np.array(mask) > 0)).astype(np.uint8))
    line = (255, 255, 255) if dark else (0, 0, 0)
    canvas = Image.composite(Image.new("RGB", (W, H), line), canvas, edge.point(lambda v: v * (.16 if dark else .10)))
    out = canvas.convert("RGBA"); out.putalpha(mask)
    out.resize((w, h + ah), Image.LANCZOS).save(root/dst, optimize=True)


JOBS = {
 "ludus":  [("ludus/img/home-light.png", "light"), ("ludus/img/home-dark.png", "dark")],
 "memo":   [("memo/img/hero-panel-light.png", "light"), ("memo/img/hero-panel-dark.png", "dark")],
 "nox":    [("nox/img/panel-light.png", "light"), ("nox/img/panel-dark.png", "dark")],
 "awayke": [("awayke/img/panel-light.png", "light"), ("awayke/img/panel-dark.png", "dark")],
 "stats":  [("stats/img/panel-light.png", "light"), ("stats/img/panel-dark.png", "dark")],
 "roomy": [("roomy/img/panel-light.png", "light"), ("roomy/img/panel-dark.png", "dark")],
 "weather": [("weather/img/panel-light.png", "light"), ("weather/img/panel-dark.png", "dark")],
}
if __name__ == "__main__":
    (root/"assets/cards").mkdir(parents=True, exist_ok=True)
    for k, lst in JOBS.items():
        for src, mode in lst:
            popover(src, f"assets/cards/{k}-{mode}.png", mode == "dark")
            print("made", k, mode)
