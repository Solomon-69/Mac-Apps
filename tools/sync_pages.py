#!/usr/bin/env python3
"""Publishes each app's website page as the GitHub Pages site of that app's own repo (docs/index.html + docs/pg + docs/assets).
Usage: python3 tools/sync_pages.py [key ...]   (default: all)"""
import re, shutil, subprocess, sys, pathlib, tempfile
root = pathlib.Path(__file__).resolve().parent.parent
APPS = {"ludus": "Ludus", "memo": "Memo", "nox": "Nox", "awayke": "Awayke", "weather": "Weather", "stats": "Stats", "menubarguard": "MenuBarGuard"}
SITE = "https://solomon-69.github.io/Mac-Apps/"
work = pathlib.Path(tempfile.mkdtemp(prefix="pages-"))
def sh(*a, cwd=None): return subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True).stdout
for key in (sys.argv[1:] or APPS):
    repo = APPS[key]; base = f"https://solomon-69.github.io/{repo}/"
    d = work/repo; sh("git", "clone", "-q", "--depth", "1", f"https://github.com/Solomon-69/{repo}.git", str(d))
    docs = d/"docs"; docs.mkdir(exist_ok=True)
    s = (root/key/"index.html").read_text()
    s = re.sub(r'content="(?:\.\./)?(img|covers)/', lambda m: f'content="{base}pg/{m.group(1)}/', s)
    s = s.replace('"../assets/', '"assets/').replace('href="../index.html"', f'href="{SITE}"').replace('href="../download/index.html"', f'href="{SITE}download/index.html"')
    s = re.sub(r'(["\'(])(img|covers|intro|showcase)/', r'\1pg/\2/', s)
    (docs/"index.html").write_text(s)
    (docs/"assets").mkdir(exist_ok=True)
    for f in ("site.css", "site.js"): shutil.copy(root/"assets"/f, docs/"assets"/f)
    pg = docs/"pg"
    if pg.exists(): shutil.rmtree(pg)
    pg.mkdir()
    for sub in ("img", "covers"):
        if (root/key/sub).exists(): shutil.copytree(root/key/sub, pg/sub)
    left = re.findall(r'["\'(](?:\.\./|/)[^"\')]+', s)
    sh("git", "add", "-A", cwd=d)
    if sh("git", "status", "--porcelain", cwd=d).strip():
        sh("git", "commit", "-qm", "docs: Pages site matches the Mac-Apps website page", cwd=d)
        sh("git", "push", "-q", cwd=d)
        print(key, "pushed", "| leftover relative refs:", left[:3])
    else: print(key, "unchanged")
