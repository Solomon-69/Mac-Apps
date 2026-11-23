#!/bin/zsh
# Keeps every app code folder in ~/Code the same on both Macs, through GitHub.
# Pull: any clean repo behind GitHub is fast-forwarded (never overwrites local edits).
# Report: repos with unpushed commits or uncommitted edits are listed, so chats push them.
# Usage: code_sync.sh [--quiet]
LOG="$HOME/Library/Logs/code_sync.log"
for d in $HOME/Code/*(/); do
  [[ -d "$d/.git" ]] || continue
  cd "$d" || continue
  up=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null) || continue
  git fetch -q 2>/dev/null || { echo "$(date +%F\ %T) $d: fetch failed" >>"$LOG"; continue; }
  read behind ahead <<<"$(git rev-list --left-right --count $up...HEAD)"
  dirty=$(git status --porcelain --untracked-files=no | wc -l | tr -d ' ')
  if (( behind > 0 && dirty == 0 && ahead == 0 )); then
    git merge -q --ff-only "$up" && echo "$(date +%F\ %T) $d: pulled $behind" >>"$LOG"
  elif (( behind > 0 )); then
    echo "$(date +%F\ %T) $d: behind $behind but has local work, not pulled" >>"$LOG"
  fi
  [[ "$1" == "--quiet" ]] || { (( ahead > 0 || dirty > 0 )) && echo "${d:t} [$(git branch --show-current)] unpushed=$ahead edited=$dirty behind=$behind"; }
done
exit 0
