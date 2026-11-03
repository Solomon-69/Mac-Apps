#!/usr/bin/env python3
"""Rewrites every .pv panel image on each app page to a rounded bell-arrow popover (make_glass.popover)."""
import re, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from make_glass import popover, root
APPS = ["weather", "stats", "memo", "nox", "awayke", "ludus", "menubarguard"]
done = {}
for k in APPS:
    p = root/k/"index.html"; h = p.read_text()
    def fix(m):
        blk = m.group(0)
        def sub(mm):
            pre, path, post = mm.group(1), mm.group(2), mm.group(3)
            if path.startswith("img/win/") or not path.endswith(".png") or "icon" in path: return mm.group(0)
            name = pathlib.Path(path).name
            if name.startswith("pop-"): return mm.group(0)
            dst = f"{k}/img/pop-{name}"
            if dst not in done:
                popover(f"{k}/{path}", dst, "dark" in name); done[dst] = 1
            return f'{pre}img/pop-{name}{post}'
        return re.sub(r'(src=(?:"|\')|srcset=(?:"|\'))(img/[^"\']+)("|\')', sub, blk)
    h2 = re.sub(r'<div class="pv".*?</div>', fix, h, flags=re.S)
    if h2 != h: p.write_text(h2); print("updated", k)
print(len(done), "images")
