# Mac-Apps repo instructions (for every Claude session, local or cloud)

- Always use the `reply-widgets` skill (in `.claude/skills/reply-widgets`) before answering anything with 3+ points, steps, options or updates: one in-chat card/stepper widget, never text bullet lists. Questions to the user go through the ask-me-questions style (one short question at a time, plain words).
- Plain, short, everyday English. Solomon does not code.
- Before reporting a site change done, open the LIVE page (add ?v=N) and compare it with his words. Never report "pushed, did not check".
- Test pages only in the built-in Claude browser, never Chrome or Playwright.
- The site is index.html + apps.json (run `python3 tools/build_index.py` after editing apps.json). Scroll strip rules: ends on the last 4 apps, links right below, no progress lines, no scroll bar.
