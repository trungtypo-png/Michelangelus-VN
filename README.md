# Michelangelus VN

**Bản Việt hóa chuẩn Typography & Bộ công cụ Cài đặt 1-Click cho font Michelangelus.**  
**Typography-grade Vietnamese adaptation & 1-Click Installer toolkit for Michelangelus.**

*Việt hóa, tinh chỉnh glyph và đóng gói bởi **trungtypo**.*

[Tiếng Việt](#tiếng-việt) · [English](#english)

---

![Michelangelus VN — Chào nguyên xuân](assets/Michelangelus-VN-poster-color.png)

*Poster giới thiệu font chữ Michelangelus VN (trình bày tác phẩm "Chào nguyên xuân" - Bùi Giáng).*

---

> [!TIP]
> ### 📥 Quick Download
> - 👉 **[Bấm vào đây để tải trọn bộ từ Google Drive](https://drive.google.com/drive/folders/1hE8nc5wfGN0kCS44mlHzgg6-QP9CjUdz?usp=sharing)** *(Bao gồm đủ 4 file `.ttf` cho máy tính và 4 file `.cpfont` cho máy đọc sách)*.

---

## 📁 Cấu trúc thư mục / Repository Structure

```text
Michelangelus-VN/
├── windows/                     # 💻 Dành riêng cho Windows (1-Click)
│   ├── install.bat              # Nhấp đúp để tự động cài font vào Windows
│   ├── install.ps1              # Kịch bản PowerShell cài đặt & ghi Registry
│   ├── uninstall.bat            # Nhấp đúp để gỡ font sạch sẽ khỏi Windows
│   ├── uninstall.ps1            # Kịch bản PowerShell gỡ bỏ font
│   └── README.txt               # Hướng dẫn nhanh cho Windows
│
├── macos/                       # 🍎 Dành riêng cho macOS (1-Click)
│   ├── install.command          # Nhấp đúp để cài font vào ~/Library/Fonts
│   ├── uninstall.command        # Nhấp đúp để gỡ font khỏi macOS
│   └── README.txt               # Hướng dẫn nhanh cho macOS
│
├── assets/                      # 🎨 Poster, bảng chữ & hình nền máy đọc sách
│   ├── Michelangelus-VN-poster-color.png
│   ├── Michelangelus-VN-poster-BW.png
│   ├── preview-Regular.png
│   ├── Chao-nguyen-xuan-X3-BW.png
│   └── Chao-nguyen-xuan-X3-BW.bmp
│
├── vietnamese_builder.py        # 🛠️ Script tự động vá & tạo 4 font tiếng Việt
├── Michelangelus Fonts EULA.rtf  # 📄 Giấy phép bản quyền font gốc Microsoft
├── README.md                    # 📖 Tài liệu hướng dẫn sử dụng
└── SHA256SUMS.txt               # 🔒 Bảng mã băm kiểm tra tính toàn vẹn
```

---

## ⚠️ Thông báo Bản quyền & Pháp lý / Copyright & Legal Disclaimer

> [!WARNING]
> **Bản quyền font gốc thuộc Microsoft Corporation và Fabbrica di San Pietro (Tòa thánh Vatican), thiết kế bởi Studiogusto.**  
> Giấy phép người dùng cuối ([Michelangelus Fonts EULA](Michelangelus%20Fonts%20EULA.rtf)) **nghiêm cấm phân phối lại file font nhị phân (No Redistribution of Font Software)** và **không cho phép thương mại hóa**.

- **Cam kết của repository:** Kho lưu trữ này tuân thủ tuyệt đối bản quyền: **KHÔNG lưu trữ trực tiếp các file font nhị phân có bản quyền (`.ttf`, `.cpfont`) trong kho mã nguồn**.
- **Mục đích:** Dự án phi thương mại (non-commercial), phục vụ mục đích nghiên cứu typography, học tập cá nhân và thưởng thức văn học tiếng Việt trên máy tính và máy đọc sách e-ink.
- **Hai hình thức tiếp cận:**
  1. **Người dùng phổ thông:** Tải bản dựng sẵn qua [Google Drive](https://drive.google.com/drive/folders/1hE8nc5wfGN0kCS44mlHzgg6-QP9CjUdz?usp=sharing) cho mục đích sử dụng cá nhân phi thương mại.
  2. **Tự tạo (DIY Builder):** Dùng mã nguồn [`vietnamese_builder.py`](vietnamese_builder.py) để tự động vá dấu tiếng Việt vào font gốc tải từ Microsoft.

---

## Tiếng Việt

Michelangelus VN là dự án bổ sung toàn diện hệ thống dấu tiếng Việt cho font **Michelangelus** — bộ font kỷ niệm Năm Thánh Vatican 2025 mang phong cách Phục Hưng tinh tế do Microsoft Design và Studiogusto phát triển.

### Điểm nổi bật về Typography
- **Đầy đủ 146 ký tự tiếng Việt Unicode**: Bao gồm tất cả các chữ cái có dấu hoa và thường.
- **Dấu 2 tầng hài hòa**: Các tổ hợp phức tạp (`ấ, ầ, ẩ, ẫ, ậ`, `ắ, ằ, ẳ, ẵ, ặ`, `ế, ề, ể, ễ, ệ`, `ố, ồ, ổ, ỗ, ộ`) được căn chỉnh tỉ lệ quang học (optical proportion), đặt vát khéo léo theo dáng nón và trăng, không chạm trần ascender.
- **Râu móc Ơ / Ư cổ điển**: Nét móc uốn cong mềm mại với đầu giọt lệ đặc trưng của trường phái serif Phục Hưng.
- **Sửa lỗi ký tự Đ / đ**: Thay thế lỗi gán dấu caron (`Dcaron / dcaron`) của bản gốc bằng nét gạch ngang thân chuẩn mực.
- **Dấu tham chiếu nguồn mở**: Sử dụng dấu serif từ **EB Garamond** (giấy phép mở SIL Open Font License).

![Xem trước bảng chữ](assets/preview-Regular.png)

---

### Hướng dẫn Cài đặt & Sử dụng

Bạn có thể lựa chọn 1 trong 2 cách sau:

#### ⭐ Cách 1: Tải nhanh trọn bộ (Dành cho người dùng phổ thông — KHÔNG cần cài Python)
1. Tải toàn bộ font dựng sẵn tại: [Google Drive Folder](https://drive.google.com/drive/folders/1hE8nc5wfGN0kCS44mlHzgg6-QP9CjUdz?usp=sharing).
2. Giải nén và đặt các file font `.ttf` vào thư mục của repo này.
3. Thực hiện cài đặt 1-Click:
   - **Windows:** Vào thư mục `windows/` và nhấp đúp **`install.bat`**.
   - **macOS:** Vào thư mục `macos/` và nhấp đúp **`install.command`**.

---

#### 🛠️ Cách 2: Tự tạo font bằng script Python (Dành cho ai thích tự làm / DIY)

```
[1. Tải font gốc Microsoft] ──> [2. Chạy vietnamese_builder.py] ──> [3. Chạy file cài đặt trong windows/ hoặc macos/]
```

1. **Tải font gốc Microsoft:**
   - Tải file nén tại: [Microsoft Download Center (ID 108856)](https://www.microsoft.com/en-us/download/details.aspx?id=108856).
   - Giải nén lấy 4 file font gốc (`Michelangelus-Regular.ttf`, `Michelangelus-Bold.ttf`, `Michelangelus-Italic.ttf`, `Michelangelus-BoldItalic.ttf`) và đặt vào thư mục repo.
2. **Chạy script tạo font tiếng Việt:**
   ```bash
   pip install fonttools freetype-py pillow numpy
   python vietnamese_builder.py
   ```
   Script sẽ tự động vá dấu và tạo ra 4 file `Michelangelus-VN-*.ttf`.
3. **Cài đặt 1-Click:** Nhấp đúp chuột vào `windows/install.bat` hoặc `macos/install.command`.

---

### Dành cho Máy đọc sách (E-readers & E-ink)
- **Kindle, Kobo, Boox:** Sau khi có các file `Michelangelus-VN-*.ttf`, cắm cáp kết nối máy đọc sách với máy tính và chép file font vào thư mục `fonts` trên máy đọc sách.
- **Thiết bị chạy XtOS (xteink firmware):** Sử dụng các file `.cpfont` có sẵn trong [Google Drive](https://drive.google.com/drive/folders/1hE8nc5wfGN0kCS44mlHzgg6-QP9CjUdz?usp=sharing) chép vào thẻ nhớ/bộ nhớ máy.
- **Hình nền e-ink nghệ thuật:** Thư mục `assets/` cung cấp sẵn ảnh màn hình khóa e-ink 16 cấp độ xám tối ưu cho máy đọc sách: [`assets/Chao-nguyen-xuan-X3-BW.png`](assets/Chao-nguyen-xuan-X3-BW.png) và [`assets/Chao-nguyen-xuan-X3-BW.bmp`](assets/Chao-nguyen-xuan-X3-BW.bmp).

---

## English

Michelangelus VN is a typography-grade Vietnamese adaptation of the **Michelangelus** typeface, celebrating the Vatican Jubilee 2025, originally designed by Studiogusto and commissioned by Fabbrica di San Pietro & Microsoft Design.

### Typographic Highlights
- **Full Unicode Vietnamese support (146 glyphs)**: Complete coverage of uppercase and lowercase diacritical glyphs.
- **Harmonious stacked diacritics**: Complex accent combinations (`ấ, ầ, ẩ, ẫ, ậ`, `ắ, ằ, ẳ, ẵ, ặ`, `ế, ề, ể, ễ, ệ`, `ố, ồ, ổ, ỗ, ộ`) are optically scaled and angled alongside the circumflex/breve curves without ascender collision.
- **Renaissance horn diacritics (Ơ / Ư)**: Gentle curves with terminal teardrop serifs faithful to the original Italian Renaissance aesthetic.
- **Corrected Đ / đ**: Fixed the upstream font bug where `Đ / đ` had caron diacritics instead of proper typographic crossbars.
- **Open-source reference**: Accent contours adapted from **EB Garamond** (SIL Open Font License).

---

### How to Install & Use

Choose either of the two methods below:

#### ⭐ Method 1: Quick Download (For non-technical users — NO Python required)
1. Download the pre-built fonts from [Google Drive](https://drive.google.com/drive/folders/1hE8nc5wfGN0kCS44mlHzgg6-QP9CjUdz?usp=sharing).
2. Extract the font files (`.ttf`) into this repository folder.
3. Perform 1-Click Installation:
   - **Windows:** Open the `windows/` folder and double-click **`install.bat`**.
   - **macOS:** Open the `macos/` folder and double-click **`install.command`**.

---

#### 🛠️ Method 2: Build Locally with Python (For developers & DIY enthusiasts)

```
[1. Download Original Font] ──> [2. Run vietnamese_builder.py] ──> [3. Run installer in windows/ or macos/]
```

1. **Download original Microsoft fonts:**
   - Download the official archive from [Microsoft Download Center (ID 108856)](https://www.microsoft.com/en-us/download/details.aspx?id=108856).
   - Extract the 4 original TTF files (`Michelangelus-*.ttf`) into the repo root.
2. **Build Vietnamese fonts:**
   ```bash
   pip install fonttools freetype-py pillow numpy
   python vietnamese_builder.py
   ```
   The script outputs the 4 compiled `Michelangelus-VN-*.ttf` files.
3. **Install:** Double-click `windows/install.bat` or `macos/install.command`.

---

### E-Reader & E-ink Usage
- **Kindle, Kobo, Boox, etc.**: Copy the `Michelangelus-VN-*.ttf` files directly into your e-reader's `fonts` folder.
- **XtOS (xteink devices)**: Use the `.cpfont` files provided in the [Google Drive Folder](https://drive.google.com/drive/folders/1hE8nc5wfGN0kCS44mlHzgg6-QP9CjUdz?usp=sharing).
- **Included artwork**: High-contrast, 16-level grayscale lockscreen wallpapers are available in `assets/`: [`assets/Chao-nguyen-xuan-X3-BW.png`](assets/Chao-nguyen-xuan-X3-BW.png) and [`assets/Chao-nguyen-xuan-X3-BW.bmp`](assets/Chao-nguyen-xuan-X3-BW.bmp).

---

## Ghi công & Tham chiếu / Credits & Acknowledgments

- **Original Typeface**: **Michelangelus**, designed by **Studiogusto**, commissioned by **Fabbrica di San Pietro**, presented by **Microsoft Design**.
- **Reference Diacritics**: **EB Garamond**, designed by **Georg Duffner** and **Octavio Pardo** (licensed under the [SIL Open Font License](http://scripts.sil.org/OFL)).
- **Vietnamese Adaptation & Builder Tool**: **trungtypo**.
- **Integrity Check**: SHA-256 checksums of repository assets are recorded in [SHA256SUMS.txt](SHA256SUMS.txt).
