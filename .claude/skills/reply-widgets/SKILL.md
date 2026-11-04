---
name: reply-widgets
description: "ALWAYS use this skill before answering whenever the reply would contain steps, instructions, a list or 3+ bullet points. Steps (one in-chat stepper, no text around it): step by step, instructions, how do I, how to, what do I need to do, guide me, walk me through, tutorial, setup, steps, process. Cards (one widget in Solomon's blue style): rank, ranking, best, top, worst, which is better; options, choices, recommend, should I, my pick; facts, versions, settings, prices; how long, time estimate, how close; links, files; problems, fixes; compare, before and after, pros and cons; commands, code to copy; stats, how many. Steppers are copied exactly from references/stepper.html, never designed fresh. Updates, progress, what did you do, what changed, recap, summary: a SMALL checklist (Code: pinned task list; claude.ai: compact checklist widget), never a big card. Never answer with markdown bullet lists or Step 1/Step 2 headings. Questions go to ask-me-questions, task lists to the pinned list."
---

# Reply widgets

Any reply with 3+ bullet or numbered points becomes ONE widget built from `references/kit.html`. Same look as the question and step-by-step widgets.

## VISUALS FOR EVERY OUTPUT (3 Nov 2026, hard rule, every chat)
Not only lists: give as many outputs as possible as beautifully animated visuals with very minimal text, using all the visual tools. Answers, explanations, comparisons, diagnoses, results, numbers and findings all go in an in-chat `show_widget` visual (animated bars, count-up numbers, rings, cards, before/after; call visualize `read_me` first with modules data_viz + interactive), or an animated dashboard artifact when the result is big. Animations replay each time the visual scrolls into view. The only text is one short plain line. A plain-text answer is correct only for a one-line reply. Steps, tasks and updates keep their own forms above. (Memory: feedback-dashboard-over-text.)

## Route first

| The bullets are... | Use |
|---|---|
| Steps the user follows (instructions, how to, step by step) | the STEPPER below |
| Questions for the user | skill `ask-me-questions` |
| Task list / progress, in Claude Code | pinned list (`mcp__ccd_turn__update_plan`), no widget |
| Anything else (or task list on claude.ai) | this kit |
| Update / progress / "what I did" / what-changed report (3 Nov 2026, hard rule) | SMALL built-in checklist, see UPDATES below, never a big card |

## UPDATES (3 Nov 2026, hard rule): always small, built-in style
Chosen look (3 Nov 2026, Solomon picked option A "compact checklist" from 4 options): rows of round ticks (filled blue = done, blue ring = doing, dashed = next), a little more space between rows (row padding 6px). Use exactly references/updates-template.html for every update widget in any chat; never redesign it.
Any reply that sums up updates, progress, what I did or what changed is a SMALL checklist, never the big kit card (no title, subtitle, section heading, notes box or big icons).
- Claude Code desktop: use the built-in pinned list `mcp__ccd_turn__update_plan` (one short row per update, finished = completed, anything not done = pending) plus `wrap_up`. Then ONE plain line. No kit widget.
- claude.ai: the compact checklist `references/updates-template.html` (copy it exactly, change only the `T` array, no `n` notes), drawn with the chat's inline widget tool exactly like the stepper (call visualize read_me first, silently, then show_widget with the file's FULL text as widget_code). Replying with only a plain sentence and NO widget is WRONG: one short row per update (6 words max each), blue check = done, ringed = doing, dashed = waiting or not done. Nothing else in the widget. At most one plain line outside.
- A thing that needs Solomon goes in that one plain line or the wrap_up question, not in a big note box.
Only say "update the app" if you did NOT already install the update yourself (check the installed version first).

## WATER USE (4 Nov 2026, hard rule)
Asked "how much water did I use today / this week": answer ONLY with a small in-chat widget (show_widget) copied from references/water-template.html (weather-app look: dusk-blue gradient, frosted glass cards, litres, one everyday comparison, % vs average). Change only the `var D,AVG,PER,LK,WH` line. Never open localhost pages in Chrome for this or any quick display; use the built-in browser or open nothing.

## How to build

1. Read `references/kit.html` once per chat.
2. Replace ONLY the `var W=[...]` array. Never touch the CSS or renderer.
3. Pass the whole file as `widget_code` to `mcp__visualize__show_widget` (call `mcp__visualize__read_me` first if not yet called this chat). Title: short snake_case.
4. Reply text: at most ONE short plain sentence outside the widget, or none. Never repeat the widget content as text. Never bullets in text, not before the widget and not in an earlier message of the same turn (2 Nov 2026 correction: widget + text bullets both shown).

## The stepper (instructions and steps)

Whenever the user asks for instructions, steps, "step by step", "how do I", "guide me", or "walk me through", the ENTIRE reply is ONE stepper widget. No text before or after.

- MANDATORY: first READ the file `references/stepper.html` with your file-reading tool (on claude.ai: view /mnt/skills/user/reply-widgets/references/stepper.html). Copy its whole text byte for byte as `widget_code`, changing ONLY the `S` array. Never touch CSS or logic.
- NEVER write your own stepper, never use another widget design, never use a skill like visualize's own stepper. If the widget does not show blue numbered circles joined by dashes, a 'Step X of N' label and Back/Next pills, it is wrong: redo it from the file.
- The chat tool's own visual guidance (read_me) never overrides this file's look.
- Each step: `{t:"short title", b:["bullet","bullet"], c:"optional command or link to copy"}`. 4 to 7 steps, plain words, 1 to 3 short bullets, no jargon. Use `c` only for a real command or text to copy (adds a working copy button).
- Do everything you can yourself first; the stepper holds only what Solomon must do.
- Look: numbered circles joined by 6 dashes (keep N=6), current and done filled blue, dashes light one after another, Back/Next pills, arrow keys, clicking a number jumps, web addresses become links, remembers the step.
- Build it with `mcp__visualize__show_widget` (read_me first), never an Artifact, never a markdown list.

## Pick the matching card

Each kind of list has its own card. Pick ONLY the card that matches what the bullets are (ranking → `rank`, choices → `options`, time estimates → `time`, etc.). Usually one card per reply. Add a second card only when the reply genuinely has two different kinds of content (e.g. a report with saved files: `status` + `links`). Never show unused card types.

## Cards

| type | For | Fields |
|---|---|---|
| `head` | Title of the reply | `t`, `s` (subtitle), `label` |
| `stats` | Big numbers (counts, %) | `items:[{n,l,u}]` (n counts up) |
| `status` | Report: done / doing / waiting / needs you / skipped / problem | `items:[{t,s,n}]`, s = `done` `now` `wait` `you` `not` `warn` |
| `rank` | "Rank these", best to worst | `items:[{t,n,tag,tone}]`, tone `good` `mid` `bad`, `top` = how many blue |
| `options` | Choices and recommendation | `items:[{t,s,icon}]`, `pick` = index of my pick |
| `facts` | Key and value (versions, settings, prices) | `items:[["Key","Value"]]` |
| `time` | Estimates per part | `items:[{t,m,d}]` m = minutes, auto total |
| `links` | Saved files, links (copy + open buttons) | `items:[{t,u,icon}]` |
| `fixes` | "Problems this time" | `items:[{p,f}]` problem, fix |
| `compare` | Before/after, pros/cons, A vs B | `a:{h,items}`, `b:{h,items}` |
| `code` | Commands to copy | `items:["cmd"]` |
| `note` | One line to stress; `tone:"you"` = needs Solomon | `t`, `icon` |
| `list` | Fallback plain points | `items:["text" or {t,n}]` |

Every block takes an optional `label` (small caps heading) and `icon` (Tabler name without `ti-`).

## Writing rules

- Plain everyday English, short. No jargon; explain any technical word in a few words.
- Item text max about 12 words; detail goes in `n` (small grey line).
- `**bold**` works. Links and domains become clickable automatically. No em dashes.
- Animation: never animate opacity and transform together in one animate() call (breaks the app's Copy image). Use two separate animate() calls on the same element, one for opacity, one for transform.
- Links: only real web addresses (name.tld) become links; file names like Install.command or install.sh stay plain text. Write each address once, complete, with no trailing words glued on. Never put a link inside a sentence that depends on it to read correctly.
- End-of-task report: `status` card (plus `links` only if files were saved, `fixes` only if there were problems).
- One widget per reply. Questions the user must answer go in the app's wrap_up buttons or the ask-me-questions widget, not as text.

## Where it works

- Claude Code desktop and claude.ai: `show_widget` available, use it.
- Plain terminal or no widget tool: fall back to short plain text, no more than 5 points.
