#!/bin/bash
# ==============================================================================
# Michelangelus VN - 1-Click Font Uninstaller for macOS
# ==============================================================================
set -e

TARGET_DIR="$HOME/Library/Fonts"

echo "=========================================================="
echo "    GỠ BỎ FONT MICHELANGELUS VN (1-CLICK macOS)"
echo "=========================================================="
echo ""

FONTS=(
  "Michelangelus-VN-Regular.ttf"
  "Michelangelus-VN-Bold.ttf"
  "Michelangelus-VN-Italic.ttf"
  "Michelangelus-VN-BoldItalic.ttf"
)

for FONT in "${FONTS[@]}"; do
  FILE="$TARGET_DIR/$FONT"
  if [ -f "$FILE" ]; then
    rm -f "$FILE"
    echo "  [-] Đã gỡ bỏ: $FONT"
  else
    echo "  [-] Không tồn tại: $FONT"
  fi
done

echo ""
echo "🎉 [HOÀN TẤT] Đã gỡ bỏ toàn bộ font Michelangelus VN khỏi macOS."
echo ""
read -p "Nhấn [Enter] để kết thúc..."
