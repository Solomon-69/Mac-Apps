# Adding a new app to the site

1. Put the app's page in `<key>/index.html` (copy an existing app folder, e.g. `nox/`).
2. Add one entry to `apps.json` (key, name, blurb, platforms, mac/win file names, icon paths).
3. Run `python3 tools/build_index.py`. It rebuilds the cards on `index.html` and `download/index.html`,
   keeps them in a balanced grid (2x2 for four apps, 3 across for 3, 5 or 6, and so on) and fills in each
   app's newest version from GitHub.
4. Commit and push. Check https://solomon-69.github.io/Mac-Apps/ once it deploys.
