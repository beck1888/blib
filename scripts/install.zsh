#!/bin/zsh

# Script URL: https://raw.githubusercontent.com/beck1888/junkdrawer/refs/heads/main/scripts/install.zsh

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Prepare target folder
TARGET_DIR="junkdrawer"
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"

# Download and extract repo (no git history)
TEMP_DIR=$(mktemp -d)
echo "${GREEN}1)  Downloading code from GitHub...${NC}"
curl -L https://github.com/beck1888/junkdrawer/archive/refs/heads/main.tar.gz | tar -xz -C "$TEMP_DIR"

# Move contents into junkdrawer/
mv "$TEMP_DIR"/junkdrawer-main/* "$TARGET_DIR"/ 2>/dev/null
mv "$TEMP_DIR"/junkdrawer-main/.[!.]* "$TARGET_DIR"/ 2>/dev/null

rm -rf "$TEMP_DIR"
echo "${GREEN}✔︎ Files copied into ./${TARGET_DIR}${NC}"

# Remove non .py/.zsh files
echo "${YELLOW}2) Cleaning up non-Python/Zsh files...${NC}"
find "$TARGET_DIR" -type f ! \( -name "*.py" -o -name "*.zsh" \) -exec rm -v {} \;

# Delete empty directories
echo "${YELLOW}3)  Removing empty directories...${NC}"
find "$TARGET_DIR" -type d -empty -delete

echo "${GREEN}✔︎ Done! Your junkdrawer is ready in './$TARGET_DIR'${NC}"
