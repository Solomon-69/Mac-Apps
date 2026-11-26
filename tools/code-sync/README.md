# App code lives in ~/Code on each Mac (23 Nov 2026)

iCloud does not keep the two Macs the same (the shared folder is empty on the M3, and git breaks inside iCloud), so GitHub is the only sync.

| App | Folder on each Mac | GitHub |
|---|---|---|
| Memo | ~/Code/Memo | Solomon-69/Memo |
| Stats | ~/Code/Stats | Solomon-69/Stats |
| Roomy | ~/Code/Roomy | Solomon-69/Roomy |
| Awayke | ~/Code/Awayke | Solomon-69/Awayke |
| Nox | ~/Code/nox-crashfix | Solomon-69/Nox |
| Ludus | ~/Code/ludus-fb | Solomon-69/Ludus |
| Murmur | ~/Code/murmur | Solomon-69/murmur |
| Mac-Apps site | ~/Code/Mac-Apps | Solomon-69/Mac-Apps |

Rules:
1. Missing folder on a Mac: `git clone https://github.com/Solomon-69/<repo>.git ~/Code/<App>`.
2. Start of work: `~/tools/code_sync.sh` (pulls what the other Mac pushed).
3. End of work: commit and push to GitHub, or the other Mac never sees it.
4. Install the 10-minute auto-pull once per Mac: run `~/Code/Mac-Apps/tools/code-sync/install.sh`.
5. The old app folders here are kept for reference only. Do not edit code here.
