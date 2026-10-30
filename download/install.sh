#!/usr/bin/env bash
# One-line Mac installer for Awayke, Ludus, Memo and Nox. Downloading with curl (not a browser)
# means macOS does not add its "cannot be verified" block, so the app just opens.
#   curl -fsSL https://solomon-69.github.io/Mac-Apps/download/install.sh | bash -s ludus
# Apps: awayke  ludus  memo  nox.   Remove: rm -rf ~/Applications/<Name>.app
set -euo pipefail
[ "$(uname -s)" = "Darwin" ] || { echo "This installer is for Mac."; exit 1; }
KEY="$(echo "${1:-}" | tr '[:upper:]' '[:lower:]')"
case "$KEY" in
  awayke) NAME=Awayke ;; ludus) NAME=Ludus ;; memo) NAME=Memo ;; nox) NAME=Nox ;;
  *) echo "Usage: install.sh awayke|ludus|memo|nox"; exit 1 ;;
esac
REPO="Solomon-69/$NAME"
DEST="${APP_DEST:-$HOME/Applications}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
BASE="https://github.com/$REPO/releases/latest/download"
echo "Downloading $NAME..."
curl -fsSL "$BASE/$NAME-mac.zip" -o "$TMP/app.zip"
# Check the fingerprint when the release lists one.
for S in SHA256SUMS SHA256SUMS.txt; do
  if curl -fsSL "$BASE/$S" -o "$TMP/sums" 2>/dev/null; then
    WANT="$(grep " \*\{0,1\}$NAME-mac.zip\$" "$TMP/sums" | awk '{print $1}' | head -1 || true)"
    if [ -n "$WANT" ]; then
      GOT="$(shasum -a 256 "$TMP/app.zip" | awk '{print $1}')"
      [ "$WANT" = "$GOT" ] || { echo "Download check failed (checksum mismatch). Nothing was installed."; exit 1; }
    fi
    break
  fi
done
mkdir -p "$DEST" "$TMP/x"
ditto -x -k "$TMP/app.zip" "$TMP/x"
APP="$(find "$TMP/x" -maxdepth 2 -name "$NAME.app" -print -quit)"
[ -n "$APP" ] || { echo "The download had no $NAME.app inside."; exit 1; }
pkill -x "$NAME" 2>/dev/null || true
rm -rf "$DEST/$NAME.app"
ditto "$APP" "$DEST/$NAME.app"
xattr -dr com.apple.quarantine "$DEST/$NAME.app" 2>/dev/null || true
echo "Installed $DEST/$NAME.app"
[ -n "${APP_NO_OPEN:-}" ] || open "$DEST/$NAME.app"
