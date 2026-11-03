#!/usr/bin/env python3
"""Rebuilds the app cards on index.html (and the download page) from apps.json.
Add a new app = add one entry to apps.json, then run:  python3 tools/build_index.py
Cards always sit in a neat, balanced grid; versions come from each app's newest GitHub release."""
import json, re, subprocess, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
apps = json.loads((root / "apps.json").read_text())
OWNER = "Solomon-69"
WORDS = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten", 11: "Eleven", 12: "Twelve"}

def version(a):
    try:
        t = subprocess.run(["gh", "release", "view", "-R", f"{OWNER}/{a['name']}", "--json", "tagName", "-q", ".tagName"], capture_output=True, text=True, timeout=30).stdout.strip()
        if t: return t.lstrip("v")
    except Exception: pass
    return a.get("version", "")

def tint(a):
    """The app's own colour: set "color" in apps.json, or it is sampled from the icon."""
    if a.get("color"): return a["color"]
    try:
        import colorsys
        from PIL import Image
        px = [q for q in Image.open(root / a["icon"]).convert("RGBA").resize((64, 64)).getdata() if q[3] > 200]
        sel = [q for q in px if (lambda h: h[1] > .5 and .45 < h[2] < .95)(colorsys.rgb_to_hsv(q[0]/255, q[1]/255, q[2]/255))] or px
        c = "#%02x%02x%02x" % tuple(sum(q[i] for q in sel) // len(sel) for i in range(3))
        a["color"] = c; return c
    except Exception:
        return "#a85432"

def cols(n):
    # even rows, no lonely card: pick a column count (3 to 5) that divides n, closest to 4 (6 -> 3, 8 -> 4, 9 -> 3, 10 -> 5, 12 -> 4); else the fullest last row
    if n <= 4: return n
    ok = [c for c in (3, 4, 5) if n % c == 0]
    if ok: return min(ok, key=lambda c: (abs(c - 4), c))
    return max((3, 4, 5), key=lambda c: (n % c, -abs(c - 4)))

def icon(a):
    img = f'<img src="{a["icon"]}" alt="{a["name"]} icon">'
    if a.get("icon_dark"):
        return f'<picture><source media="(prefers-color-scheme: dark)" srcset="{a["icon_dark"]}">{img}</picture>'
    return img

def rel(a, f): return f"https://github.com/{OWNER}/{a['name']}/releases/latest/download/{f}"

def dls(a, cls):
    m = f'<a class="{cls}" href="{rel(a, a["mac"])}">Mac <span>&darr;</span></a>'
    w = f'<a class="{cls}" href="{rel(a, a["win"])}">Windows <span>&darr;</span></a>' if a.get("win") else ""
    return m + w

def card(a):
    v = version(a); a["version"] = v
    return (f'    <div class="card" style="--tint:{tint(a)}"><a class="cardlink" href="{a["key"]}/index.html">\n'
            f'      <span class="ico">{icon(a)}</span>\n'
            f'      <h2>{a["name"]}</h2><p>{a["blurb"]} {a["platforms"]}. Version {v}.</p>\n'
            f'      <span class="go">See {a["name"]} <span>&rarr;</span></span>\n'
            f'    </a><div class="dls"><span class="dlh">Download, free</span>{dls(a, "dlmac")}</div></div>')

def deckcard(a):
    if not a.get("shot"):
        return deckcard_plain(a)
    dark = a.get("shot_dark")
    shot = (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{dark}"><img src="{a["shot"]}" alt="{a["name"]} open from the menu bar" loading="lazy"></picture>'
            if dark else f'<img src="{a["shot"]}" alt="{a["name"]} open from the menu bar" loading="lazy">')
    chips = "".join(f"<li>{c}</li>" for c in a.get("chips", []))
    winbtn = f'<a class="p w" href="{rel(a, a["win"])}">Download for Windows</a>' if a.get("win") else ""
    return (f'    <article class="dcard" data-name="{a["name"]}" data-key="{a["key"]}" data-side="{a.get("side","r")}" style="--tint:{tint(a)};--d:0;--ad:0">\n'
            f'      <div class="txt"><span class="ico">{icon(a)}</span><h3>{a["name"]}</h3><p class="feat">{a["feature"]}</p>\n'
            f'      <ul class="chips">{chips}</ul>\n'
            f'      <div class="acts"><a class="p" href="{rel(a, a["mac"])}">Download for Mac</a>{winbtn}<a class="s" href="{a["key"]}/index.html">See {a["name"]}</a></div></div>\n'
            f'      <div class="shot" aria-hidden="false">{shot}</div>\n'
            f'    </article>')

def deckcard_plain(a):
    winbtn = f'<a class="p w" href="{rel(a, a["win"])}">Download for Windows</a>' if a.get("win") else ""
    return (f'    <article class="dcard plain" data-name="{a["name"]}" style="--tint:{tint(a)};--d:0;--ad:0">\n'
            f'      <div class="txt"><span class="ico">{icon(a)}</span><h3>{a["name"]}</h3><p class="feat">{a["short"]}</p>\n'
            f'      <div class="acts"><a class="p" href="{rel(a, a["mac"])}">Download for Mac</a>{winbtn}<a class="s" href="{a["key"]}/index.html">See {a["name"]}</a></div></div>\n'
            f'    </article>')

def dcard(a):
    ic = a["icon"]
    win = f'\n        <a class="btn alt" href="{rel(a, a["win"])}">Windows <small>{a["win"]}</small><span>&darr;</span></a>' if a.get("win") else ""
    mac = a["mac"] if a["mac"].endswith(".zip") else a["mac"]
    return (f'    <section class="card" style="--tint:{tint(a)}">\n'
            f'      <div class="top"><img src="../{ic}" alt=""><div><h2>{a["name"]}</h2><p>{a["short"]}</p></div></div>\n'
            f'      <div class="btns">\n'
            f'        <a class="btn" href="{rel(a, a["mac"])}">Mac <small>{mac}</small><span>&darr;</span></a>{win}\n'
            f'      </div>\n'
            f'      <button class="cmd" data-cmd="curl -fsSL https://solomon-69.github.io/Mac-Apps/download/install.sh | bash -s {a["key"]}" title="Copy">Mac install line (recommended)<span>copy</span></button>\n'
            f'    </section>')

def put(path, start, end, body):
    p = root / path; s = p.read_text()
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    assert pat.search(s), f"markers missing in {path}"
    p.write_text(pat.sub(lambda m: start + "\n" + body + "\n    " + end, s, count=1))

n = len(apps)
put("index.html", "<!-- APPS:START -->", "<!-- APPS:END -->", "\n".join(card(a) for a in apps))
put("index.html", "<!-- DECK:START -->", "<!-- DECK:END -->", "\n".join(deckcard(a) for a in apps))
put("download/index.html", "<!-- APPS:START -->", "<!-- APPS:END -->", "\n".join(dcard(a) for a in apps))
p = root / "index.html"; s = p.read_text()
H1 = " ".join(f'<span class="w" style="--i:{i}">{w}</span>' for i, w in enumerate("Little apps for your Mac.".split()))
s = re.sub(r"<h1>.*?</h1>", lambda m: f"<h1>{H1}</h1>", s, count=1)
s = re.sub(r'<div class="grid"[^>]*>', f'<div class="grid" style="--cols:{cols(n)}">', s, count=1)
s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + "Small, free apps for Mac: " + ", ".join(a["name"] for a in apps[:-1]) + f" and {apps[-1]['name']}.", s, count=1)
p.write_text(s)
(root / "apps.json").write_text(json.dumps(apps, indent=1))
print("built", n, "apps,", cols(n), "columns")
