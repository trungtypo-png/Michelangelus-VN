#!/bin/bash
# ==============================================================================
# Michelangelus VN - 1-Click Font Installer for macOS
# ==============================================================================
set -e

# Change directory to the folder where this script is located
cd "$(dirname "$0")"

TARGET_DIR="$HOME/Library/Fonts"
mkdir -p "$TARGET_DIR"

echo "=========================================================="
echo "    CÀI ĐẶT FONT MICHELANGELUS VN (1-CLICK macOS)"
echo "=========================================================="
echo ""
echo "Đang cài đặt 4 kiểu font vào: $TARGET_DIR"
echo ""

FONTS=(
  "Michelangelus-VN-Regular.ttf"
  "Michelangelus-VN-Bold.ttf"
  "Michelangelus-VN-Italic.ttf"
  "Michelangelus-VN-BoldItalic.ttf"
)

COUNT=0
for FONT in "${FONTS[@]}"; do
  SRC=""
  if [ -f "$FONT" ]; then
    SRC="$FONT"
  elif [ -f "../$FONT" ]; then
    SRC="../$FONT"
  fi

  if [ -n "$SRC" ]; then
    cp -f "$SRC" "$TARGET_DIR/"
    echo "  [OK] Đã cài đặt: $FONT"
    COUNT=$((COUNT + 1))
  else
    echo "  [!] Không tìm thấy file: $FONT"
  fi
done

echo ""
if [ $COUNT -eq 4 ]; then
  echo "🎉 [THÀNH CÔNG] Đã cài đặt trọn bộ 4 font Michelangelus VN vào macOS!"
  echo "Bạn có thể sử dụng ngay trong Pages, Keynote, Microsoft Word, Photoshop, v.v."
elif [ $COUNT -gt 0 ]; then
  echo "⚠️ Đã cài đặt $COUNT/4 font vào $TARGET_DIR."
else
  echo "❌ [NHẮC NHỞ] Không tìm thấy các file font Michelangelus-VN-*.ttf nào trong thư mục này."
  echo "👉 Bạn có thể tải trọn bộ font đã dựng sẵn tại Google Drive:"
  echo "   https://drive.google.com/drive/folders/1hE8nc5wfGN0kCS44mlHzgg6-QP9CjUdz?usp=sharing"
  echo ""
  read -p "Bạn có muốn mở link Google Drive trên trình duyệt để tải không? (y/n): " OPEN_DRIVE
  if [[ "$OPEN_DRIVE" =~ ^[Yy] ]]; then
    open "https://drive.google.com/drive/folders/1hE8nc5wfGN0kCS44mlHzgg6-QP9CjUdz?usp=sharing"
  fi
fi

echo ""
read -p "Nhấn [Enter] để kết thúc..."
