#!/usr/bin/env python3
"""Add search-engine and AI-search tags to every Mac-Apps page.
Safe to run again: it replaces the block between <!-- seo:start --> and <!-- seo:end -->.
Run after build_index.py:  python3 tools/seo_inject.py
"""
import json, re, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://solomon-69.github.io/Mac-Apps/"
AUTHOR = {"@type": "Person", "name": "Solomon", "url": BASE}
apps = json.load(open(ROOT / "apps.json"))

def meta(s, name):
    m = re.search(r'<meta (?:name|property)="%s" content="([^"]*)"' % re.escape(name), s)
    return html.unescape(m.group(1)) if m else ""

def block(s, url, ld, og_fallback):
    title = re.search(r"<title>(.*?)</title>", s, re.S).group(1).strip()
    desc = meta(s, "description")
    out = []
    if 'rel="canonical"' not in s:
        out.append(f'<link rel="canonical" href="{url}">')
    if 'property="og:title"' not in s:
        img = og_fallback
        out += [f'<meta property="og:type" content="website">',
                f'<meta property="og:title" content="{html.escape(title)}">',
                f'<meta property="og:description" content="{html.escape(desc)}">',
                f'<meta property="og:image" content="{img}">']
    if 'property="og:url"' not in s:
        out.append(f'<meta property="og:url" content="{url}">')
    out.append('<meta name="twitter:card" content="summary_large_image">')
    out.append('<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>")
    return "<!-- seo:start -->\n" + "\n".join(out) + "\n<!-- seo:end -->\n"

def app_ld(a, desc):
    os_ = "macOS" + (", Windows" if "Windows" in a.get("platforms", "") else "")
    return {"@type": "SoftwareApplication", "name": a["name"], "description": desc or a["blurb"],
            "url": BASE + a["key"] + "/", "image": BASE + a["icon"],
            "applicationCategory": "GameApplication" if a["key"] == "ludus" else "UtilitiesApplication",
            "operatingSystem": os_, "softwareVersion": a.get("version", ""),
            "downloadUrl": BASE + "download/",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "isAccessibleForFree": True, "author": AUTHOR}

def write(path, url, ld, og):
    s = path.read_text()
    s = re.sub(r"<!-- seo:start -->.*?<!-- seo:end -->\n?", "", s, flags=re.S)
    s = s.replace("</head>", block(s, url, ld, og) + "</head>", 1)
    path.write_text(s)

hero = BASE + "assets/favicon-512.png"
for a in apps:
    p = ROOT / a["key"] / "index.html"
    if not p.exists() or a["key"] == "murmur":  # murmur page owned by its own session
        continue
    desc = meta(p.read_text(), "description")
    ld = dict(app_ld(a, desc), **{"@context": "https://schema.org"})
    write(p, BASE + a["key"] + "/", ld, BASE + a.get("shot", a["icon"]))

items = [dict(app_ld(a, ""), **{}) for a in apps]
hub = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebSite", "name": "Mac Apps by Solomon", "url": BASE, "author": AUTHOR},
    {"@type": "ItemList", "name": "Free Mac apps by Solomon",
     "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": it} for i, it in enumerate(items)]}]}
write(ROOT / "index.html", BASE, hub, hero)
write(ROOT / "download" / "index.html", BASE + "download/",
      {"@context": "https://schema.org", "@type": "WebPage", "name": "Download free Mac apps by Solomon",
       "url": BASE + "download/", "author": AUTHOR}, hero)

# sitemap + llms.txt for this site
urls = [BASE, BASE + "download/"] + [BASE + a["key"] + "/" for a in apps if (ROOT / a["key"] / "index.html").exists()]
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
lines = ["# Mac Apps by Solomon", "", "> Small, free apps for Mac (some also for Windows), made by Solomon. No account, no ads. Download page: " + BASE + "download/", "", "## Apps", ""]
lines += [f"- [{a['name']}]({BASE}{a['key']}/): {a['blurb']} Free. Platforms: {a.get('platforms','Mac')}. Version {a.get('version','')}." for a in apps]
(ROOT / "llms.txt").write_text("\n".join(lines) + "\n")
print("seo ok:", len(urls), "pages")
