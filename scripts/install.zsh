#!/bin/zsh

# Script URL: https://raw.githubusercontent.com/geckoDev/blib/refs/heads/main/scripts/install.zsh

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Prepare target folder
TARGET_DIR="blib"
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"

# Download and extract repo (no git history)
TEMP_DIR=$(mktemp -d)
echo "${BLUE}INSTALLING:${NC} Beck's Library..."
curl -sL https://github.com/beck1888/blib/archive/refs/heads/main.tar.gz | tar -xz -C "$TEMP_DIR"

# Move contents into blib/
mv "$TEMP_DIR"/blib-main/* "$TARGET_DIR"/ 2>/dev/null
mv "$TEMP_DIR"/blib-main/.[!.]* "$TARGET_DIR"/ 2>/dev/null

rm -rf "$TEMP_DIR"

# Remove non .py/.zsh/.mp3 files
find "$TARGET_DIR" -type f ! \( -name "*.py" -o -name "*.zsh" -o -name "*.mp3" \) -exec rm {} \;

# Delete empty directories
find "$TARGET_DIR" -type d -empty -delete

echo "${GREEN}INSTALLED:${NC}  Beck's Library"
