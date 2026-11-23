#!/bin/zsh
# Run once on each Mac: installs code_sync.sh and runs it every 10 minutes.
cp "${0:h}/code_sync.sh" ~/tools/code_sync.sh && chmod +x ~/tools/code_sync.sh
P=~/Library/LaunchAgents/com.solomon.codesync.plist
cat > $P <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>com.solomon.codesync</string>
<key>ProgramArguments</key><array><string>/bin/zsh</string><string>$HOME/tools/code_sync.sh</string><string>--quiet</string></array>
<key>StartInterval</key><integer>600</integer>
<key>RunAtLoad</key><true/>
</dict></plist>
PL
launchctl bootout gui/$(id -u)/com.solomon.codesync 2>/dev/null
launchctl bootstrap gui/$(id -u) $P && echo "code sync on"
