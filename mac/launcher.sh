#!/bin/bash
# Launcher for the RenameImages.app bundle.
# Opens a Terminal window and runs the actual worker binary, which will
# show its own folder-picker dialog to choose the project folder.

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN="$DIR/../Resources/rename_images_bin"

osascript <<APPLESCRIPT
tell application "Terminal"
    activate
    do script "\"$BIN\""
end tell
APPLESCRIPT
