#!/bin/bash
# ITAssist Broadcast Encoder - 100 (IBE-100)
# macOS DMG Creator Script
# Professional packaging for macOS

set -e

# Application Information
APP_NAME="IBE-100"
APP_VERSION="1.0.0"
APP_DESCRIPTION="ITAssist Broadcast Encoder - 100 (IBE-100)"
DMG_NAME="${APP_NAME}-${APP_VERSION}"
DMG_SIZE="500m"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🍎 Creating macOS DMG for ${APP_DESCRIPTION}${NC}"

# Check if app bundle exists
if [ ! -d "dist/${APP_NAME}.app" ]; then
    echo -e "${YELLOW}⚠️  App bundle not found. Building first...${NC}"
    ./build.sh onedir
fi

# Create temporary DMG directory
TEMP_DMG_DIR="temp_dmg"
mkdir -p "${TEMP_DMG_DIR}"

# Copy app bundle to temp directory
cp -R "dist/${APP_NAME}.app" "${TEMP_DMG_DIR}/"

# Create Applications symlink
ln -s /Applications "${TEMP_DMG_DIR}/Applications"

# Copy additional files
cp "README.md" "${TEMP_DMG_DIR}/"
cp "LICENSE.txt" "${TEMP_DMG_DIR}/"

# Create DMG
echo -e "${BLUE}📦 Creating DMG...${NC}"
hdiutil create -volname "${APP_NAME}" -srcfolder "${TEMP_DMG_DIR}" -ov -format UDZO "dist/${DMG_NAME}.dmg"

# Clean up
rm -rf "${TEMP_DMG_DIR}"

echo -e "${GREEN}✅ DMG created: dist/${DMG_NAME}.dmg${NC}"
echo -e "${BLUE}📁 Size: $(du -h "dist/${DMG_NAME}.dmg" | cut -f1)${NC}"
