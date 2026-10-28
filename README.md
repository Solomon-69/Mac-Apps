# Mac Apps

Four small, free apps by Solomon. Quiet, fast and made to stay out of your way. Open [index.html](index.html) for the full pages, or read on.

## Ludus

<img src="ludus/img/icon-light.png" width="72" alt="Ludus icon">

Little games for little breaks, right from your menu bar or tray. 43 quick mini games that work offline: arcade, puzzles, duels against the computer and two-player games.

<img src="ludus/img/panel-light.png" width="300" alt="Ludus panel"> <img src="ludus/intro/ludus-mac-1-light.png" width="240" alt="Ludus welcome screen">

<img src="ludus/showcase/ludus-covers.png" width="560" alt="Cover art of all 43 Ludus games">

Version 1.12.30, 43 games.

Download: [Mac (.zip)](https://github.com/Solomon-69/Ludus/releases/latest/download/Ludus-mac.zip) | [Windows](https://github.com/Solomon-69/Ludus/releases/latest/download/Ludus-windows.zip)

## Memo

<img src="memo/img/icon-light.png" width="72" alt="Memo icon">

Everything you copy, one shortcut away. Memo keeps a searchable history of text, links, pictures, files and colours, and pastes them back.

<img src="memo/showcase/memo-1-light.png" width="420" alt="Memo panel"> <img src="memo/showcase/memo-3-light.png" width="420" alt="Searching Memo"> <img src="memo/intro/memo-welcome-1.png" width="260" alt="Memo welcome window">

Version 1.1.1.

Download: [Mac](https://github.com/Solomon-69/Memo/releases/latest/download/Memo-mac.zip) | [Windows](https://github.com/Solomon-69/Memo/releases/latest/download/Memo-windows.zip)

## Nox

<img src="nox/img/icon.png" width="72" alt="Nox icon">

One switch for light and dark. Flip your Mac between light and dark, set a schedule, and make web pages follow.

<img src="nox/img/panel-light.png" width="300" alt="Nox panel"> <img src="nox/showcase/nox-2-light.png" width="420" alt="A page before and after Nox"> <img src="nox/intro/nox-welcome-1.png" width="260" alt="Nox welcome window">

Version 1.4.1.

Download: [Mac (.dmg)](https://github.com/Solomon-69/Nox/releases/latest/download/Nox.dmg) | [Mac (.zip)](https://github.com/Solomon-69/Nox/releases/latest/download/Nox-mac.zip) | [Windows](https://github.com/Solomon-69/Nox/releases/latest/download/Nox-windows.zip)

## Awayke

<img src="awayke/img/icon.png" width="72" alt="Awayke icon">

Keep your MacBook awake with the lid closed. Set a timer or a low-battery cutoff and forget about it.

<img src="awayke/img/panel-light.png" width="300" alt="Awayke panel"> <img src="awayke/showcase/aw-3-light.png" width="420" alt="Awayke timer"> <img src="awayke/intro/awayke-welcome-1.png" width="260" alt="Awayke welcome window">

Version 1.5.0.

Download: [Mac (.dmg)](https://github.com/Solomon-69/Awayke/releases/latest/download/Awayke.dmg) | [Mac (.zip)](https://github.com/Solomon-69/Awayke/releases/latest/download/Awayke-1.5.0.zip)

## Installing

**Mac:** open the .dmg (Ludus and Memo come as a .zip: unzip it) and drag the app to Applications. The first time, right-click the app and choose **Open**, then **Open** again. If you see no Open button, go to System Settings, Privacy & Security, and click **Open Anyway**.

**Windows:** unzip the download and run the app. If Windows SmartScreen warns you, click **More info**, then **Run anyway**.

Each app has its own Releases page (for example [Ludus](https://github.com/Solomon-69/Ludus/releases)); the download links above always give the latest build.

## Unsigned apps: how to open them, and how to check your download

These apps are not signed yet. Signing needs Apple's paid developer account (and a Windows code-signing certificate), which the project does not have yet. The apps are safe to use as far as the author knows, but your computer cannot prove who made them, so it warns you the first time.

- **Mac:** right-click the app, choose **Open**, then **Open** again. If there is no Open button, go to System Settings > Privacy & Security and click **Open Anyway**.
- **Windows:** if SmartScreen says "Windows protected your PC", click **More info**, then **Run anyway**.

To check that a download has not been changed, compare its SHA-256 fingerprint with the one in [CHECKSUMS.md](CHECKSUMS.md) (Mac: `shasum -a 256 <file>` in Terminal; Windows: `certutil -hashfile <file> SHA256`).

## Credits and trademarks

Awayke is based on Sleepless by Adam Boudjemaa (MIT). Ludus uses Leaflet, Pannellum, Panoramax photos and Esri map tiles; see THIRD_PARTY.md in the [Ludus repository](https://github.com/Solomon-69/Ludus) (page: https://solomon-69.github.io/Ludus/). Not affiliated with or endorsed by Apple, Microsoft or the makers of any game or app these resemble; all trademarks belong to their owners.

This page repository only shows the apps. Ludus is all rights reserved; Memo, Nox and Awayke are MIT licensed in their own repositories.
