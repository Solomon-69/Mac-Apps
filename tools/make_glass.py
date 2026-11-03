#!/usr/bin/env python3
"""Turns the real app panel screenshots into see-through glass for the deck cards:
flat areas lose their baked-in background and go translucent (the card colour shows through),
text/icons/edges stay solid. Also adds the menu bar arrow to panels that lack one."""
import sys, pathlib
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
root = pathlib.Path(__file__).resolve().parent.parent

def lum(a): return a[..., 0]*.299 + a[..., 1]*.587 + a[..., 2]*.114

def add_notch(im):
    w, h = im.size; nh = int(w*.045); nw = int(w*.075)
    out = Image.new("RGBA", (w, h+nh), (0, 0, 0, 0)); out.paste(im, (0, nh))
    a = np.array(im); al = a[..., 3]
    ys, xs = np.where(al > 200); top = ys.min(); band = a[top+int(h*.01):top+int(h*.03), :, :3][al[top+int(h*.01):top+int(h*.03)] > 200]
    col = tuple(int(v) for v in band.mean(axis=0)) if len(band) else (60, 60, 60)
    cx = w//2; d = ImageDraw.Draw(out)
    d.polygon([(cx-nw, nh+2), (cx, 0), (cx+nw, nh+2)], fill=col+(255,))
    out = out.filter(ImageFilter.GaussianBlur(.6)) if False else out
    return out

def glass(src, dst, dark, notch):
    im = Image.open(root/src).convert("RGBA")
    if notch: im = add_notch(im)
    a = np.array(im).astype(np.float32); A = a[..., 3]/255
    rgb = Image.fromarray(a[..., :3].astype(np.uint8))
    blur = np.array(rgb.filter(ImageFilter.GaussianBlur(max(6, im.width//70)))).astype(np.float32)
    D = np.abs(lum(a) - lum(blur)); w = np.clip(D*6/255, 0, 1)
    wi = Image.fromarray((w*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(.8))
    w = np.array(wi).astype(np.float32)/255
    m = A > .9; g = lum(a)[m].mean() if m.any() else 128
    neutral = np.array([g, g, g*1.02]) * (1 if dark else 1)
    neutral = np.clip(neutral, 0, 255)
    base = .40 if dark else .50
    rgbn = neutral*(1-w[..., None]) + a[..., :3]*w[..., None]
    alpha = A*(base + (1-base)*w)
    out = np.dstack([rgbn, alpha*255]).clip(0, 255).astype(np.uint8)
    Image.fromarray(out, "RGBA").save(root/dst, optimize=True)

JOBS = {
 "ludus":  [("ludus/img/home-light.png","light",True),("ludus/img/home-dark.png","dark",True)],
 "memo":   [("memo/img/hero-panel-light.png","light",False),("memo/img/hero-panel-dark.png","dark",False)],
 "nox":    [("nox/img/panel-light.png","light",False),("nox/img/panel-dark.png","dark",False)],
 "awayke": [("awayke/img/panel-light.png","light",True),("awayke/img/panel-dark.png","dark",True)],
 "stats":[("stats/img/panel-light.png","light",True),("stats/img/panel-dark.png","dark",True)],
 "weather":[("weather/img/panel-light.png","light",True),("weather/img/panel-dark.png","dark",True)],
}
if __name__ == "__main__":
    (root/"assets/cards").mkdir(parents=True, exist_ok=True)
    for k, lst in JOBS.items():
        for src, mode, notch in lst:
            glass(src, f"assets/cards/{k}-{mode}.png", mode == "dark", notch)
            print("made", k, mode)
