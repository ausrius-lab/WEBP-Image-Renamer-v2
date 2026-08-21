#!/bin/bash
# Launcher for the RenameImages.app bundle.
# Opens a Terminal window and runs the actual worker binary, pointed at
# the folder the .app itself is sitting in (so it can find 1920px, 992px,
# 768px, 576px, 375px etc. next to it).

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN="$DIR/../Resources/rename_images_bin"
BASE="$(cd "$DIR/../../.." && pwd)"

osascript <<APPLESCRIPT
tell application "Terminal"
    activate
    do script "\"$BIN\" \"$BASE\""
end tell
APPLESCRIPT
