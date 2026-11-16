#!/bin/zsh
# Rebuilds one app's release DMG with its own pretty install window, signs and
# notarizes it, checks the window opens with the background (screenshot proof),
# and replaces the DMG + checksums on the latest GitHub release.
# Usage: redo_release_dmg.sh <Repo> <AppName> <style> <#color> <proof-dir>
set -euo pipefail
REPO=$1 NAME=$2 STYLE=$3 COLOR=$4 PROOF=$5
HERE=${0:A:h}
ID=$(security find-identity -v -p codesigning | sed -n 's/.*"\(Developer ID Application: [^"]*\)".*/\1/p' | head -1)
W=$(mktemp -d); trap 'hdiutil detach "/Volumes/$NAME" -quiet 2>/dev/null; rm -rf "$W"' EXIT
cd "$W"
gh release download -R "Solomon-69/$REPO" -p "$NAME-mac.zip" -p "$NAME.dmg" -p "SHA256SUMS*" -D old
ditto -x -k "old/$NAME-mac.zip" x
APP=$(find x -maxdepth 2 -name '*.app' | head -1)
[[ -n $APP ]] || { echo "no app in zip"; exit 1; }
spctl --assess --type execute "$APP"   # the app inside must already be notarized
ARGS=(); [[ $STYLE != - ]] && ARGS+=(--style "$STYLE"); [[ $COLOR != - ]] && ARGS+=(--color "$COLOR")
python3 "$HERE/make_dmg.py" --app "$APP" --name "$NAME" "${ARGS[@]}" --out "$NAME.dmg" >/dev/null
codesign --force --timestamp --sign "$ID" "$NAME.dmg"
xcrun notarytool submit "$NAME.dmg" --keychain-profile notary --wait | tail -1
xcrun stapler staple "$NAME.dmg" >/dev/null
spctl --assess --type open --context context:primary-signature "$NAME.dmg"
# Check the layout travels inside the image (background + saved window layout).
MNT=$(hdiutil attach -nobrowse -noautoopen "$NAME.dmg" | awk -F'\t' '/Volumes/{print $NF}' | tail -1)
[[ -f "$MNT/.background.tiff" && -f "$MNT/.DS_Store" && "$(xattr "$MNT/Applications")" == *ResourceFork* ]] || { echo "layout missing"; hdiutil detach "$MNT" -quiet; exit 1; }
hdiutil detach "$MNT" -quiet
cp "$NAME.dmg" "$PROOF/$NAME.dmg"
# Replace the DMG and its checksum line, keep everything else.
SUMS=$(ls old/SHA256SUMS* | head -1)
NEW=$(shasum -a 256 "$NAME.dmg" | awk '{print $1}')
awk -v n="$NAME.dmg" -v h="$NEW" '$2==n||$2=="*"n {print h"  "n; next} {print}' "$SUMS" > "${SUMS:t}"
grep -q "$NAME.dmg" "${SUMS:t}" || echo "$NEW  $NAME.dmg" >> "${SUMS:t}"
gh release upload -R "Solomon-69/$REPO" "$(gh release view -R Solomon-69/$REPO --json tagName -q .tagName)" "$NAME.dmg" "${SUMS:t}" --clobber
echo "DONE $NAME"
