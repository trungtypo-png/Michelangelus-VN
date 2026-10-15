# Michelangelus VN

**Quick Vietnamese adaptation — modified and edited by trungtypo.**  
**Bản Việt hóa nhanh — chỉnh sửa và edit by trungtypo.**

[English](#english) · [Tiếng Việt](#tiếng-việt)

![Michelangelus VN — Chào nguyên xuân](Michelangelus-VN-poster-color.png)

[Desktop glyph preview / Xem bảng chữ trên máy tính](preview-Regular.png)

---

## ⚠️ Thông báo Bản quyền & Pháp lý / Copyright & Legal Disclaimer

> [!WARNING]
> **Font nguyên bản Michelangelus là tài sản sở hữu trí tuệ có bản quyền độc quyền của Microsoft Corporation và Fabbrica di San Pietro (Tòa thánh Vatican), thiết kế bởi Studiogusto.**  
> Giấy phép sử dụng kèm theo ([Michelangelus Fonts EULA](Michelangelus%20Fonts%20EULA.rtf)) **KHÔNG CẤP QUYỀN PHÂN PHỐI LẠI (No Distribution Rights)** và **KHÔNG CHO PHÉP THƯƠNG MẠI HÓA**.

* **Mục đích dự án:** Đây là dự án phi thương mại (non-commercial), phục vụ mục đích nghiên cứu typography, học tập cá nhân và hỗ trợ hiển thị tiếng Việt trên các thiết bị đọc sách e-ink cá nhân.
* **Tôn trọng bản quyền:** Dự án khuyến khích người dùng tải bản font gốc chính thức từ Microsoft tại [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=108856) hoặc xem bài giới thiệu tại [Microsoft Design — Designing Michelangelus](https://microsoft.design/articles/designing-michelangelus/).
* **Tự xây dựng (DIY):** Chúng tôi cung cấp mã nguồn [`vietnamese_builder.py`](vietnamese_builder.py) để người dùng có thể tự áp dụng bản vá tiếng Việt trực tiếp từ bộ font gốc tải về từ Microsoft trên máy tính của mình mà không cần phụ thuộc vào bản dựng sẵn.

---

## English

Michelangelus VN is a quick, unofficial Vietnamese adaptation of Michelangelus, optimized for desktop reading and e-readers.

### Credits & Licenses
- Vietnamese glyph engineering, kerning & accents: **trungtypo**.
- Original typeface: **Michelangelus**, designed by **Studiogusto**, commissioned by **Fabbrica di San Pietro**, and presented by **Microsoft Design**.
- Reference serif accents: **EB Garamond** (SIL Open Font License).
- Original source: [Designing Michelangelus — Microsoft Design](https://microsoft.design/articles/designing-michelangelus/).
- Original font download: [Microsoft Download Center (ID 108856)](https://www.microsoft.com/en-us/download/details.aspx?id=108856).

### 1-Click Installation (Windows & macOS)

| Operating System | How to Install | How to Uninstall |
| :--- | :--- | :--- |
| **Windows** 💻 | Double-click **`install-windows.bat`** | Double-click **`uninstall-windows.bat`** |
| **macOS** 🍎 | Double-click **`install-macos.command`** | Double-click **`uninstall-macos.command`** |

* On **Windows**: The script automatically copies the 4 TTF files to your font library, registers them in Windows Registry (supports both Standard User and Administrator), and broadcasts a cache refresh signal. You can open Word, Photoshop, or browsers immediately.
* On **macOS**: The script installs the fonts directly into `~/Library/Fonts/` for immediate system-wide use.

### DIY: Self-Build Vietnamese Fonts from Original Source

If you prefer building the Vietnamese font locally from the official Microsoft download:

1. Download the official font archive from [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=108856).
2. Extract the 4 original TTF files into an `original/` folder (or in the repository root).
3. Install required Python packages:
   ```bash
   pip install fonttools freetype-py pillow numpy
   ```
4. Run the builder script:
   ```bash
   python vietnamese_builder.py
   ```
   The script will automatically fetch reference serif diacritics from EB Garamond (OFL), generate all 94 Vietnamese glyphs, fix the `Đ/đ` stroke crossbars, and output the compiled `Michelangelus-VN-*.ttf` files.

### Downloads

| Format | Files | Intended use |
| --- | --- | --- |
| TTF · version 2.010 | [Regular](Michelangelus-VN-Regular.ttf), [Bold](Michelangelus-VN-Bold.ttf), [Italic](Michelangelus-VN-Italic.ttf), [Bold Italic](Michelangelus-VN-BoldItalic.ttf) | Desktop applications that support TrueType fonts |
| CP · .cpfont | [12](Michelangelus-vn_12.cpfont), [14](Michelangelus-vn_14.cpfont), [16](Michelangelus-vn_16.cpfont), [18](Michelangelus-vn_18.cpfont) | E-readers running firmware that supports .cpfont |

---

## Tiếng Việt

Michelangelus VN là **bản Việt hóa nhanh, không chính thức** của font chữ Michelangelus. Bộ font gồm 4 kiểu TrueType dùng trên máy tính và 4 file CP dành cho máy đọc sách (XtOS / e-readers).

### Ghi công & Bản quyền
- Việt hóa, chỉnh sửa glyph và kerning: **trungtypo**.
- Font gốc: **Michelangelus**, do **Studiogusto** thiết kế, được **Fabbrica di San Pietro** đặt thực hiện và giới thiệu bởi **Microsoft Design**.
- Dấu serif tham chiếu: **EB Garamond** (Giấy phép mã nguồn mở SIL OFL).
- Tải font nguyên bản: [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=108856).

### Cài đặt 1-Click (Dễ dàng cho người dùng)

| Hệ điều hành | Cách cài đặt | Cách gỡ bỏ |
| :--- | :--- | :--- |
| **Windows** 💻 | Nhấp đúp chuột vào **`install-windows.bat`** | Nhấp đúp chuột vào **`uninstall-windows.bat`** |
| **macOS** 🍎 | Nhấp đúp chuột vào **`install-macos.command`** | Nhấp đúp chuột vào **`uninstall-macos.command`** |

* **Windows:** Tự động cài đặt cả 4 kiểu font, đăng ký vào Registry Windows (hỗ trợ cả quyền User thường lẫn Admin) và làm mới cache font ngay lập tức.
* **macOS:** Tự động chép 4 font vào thư mục font cá nhân `~/Library/Fonts/`, mở app (Word, Pages, Photoshop, v.v.) là có font dùng ngay.

### Hướng dẫn Tự Việt hóa từ Font gốc của Microsoft (Tự làm / DIY)

Để bảo đảm 100% về mặt bản quyền cá nhân, bạn có thể tự chạy script để vá tiếng Việt từ file gốc Microsoft:

1. Tải bộ font gốc từ Microsoft: [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=108856).
2. Giải nén 4 file TTF gốc vào thư mục `original/` (hoặc để cùng thư mục với script).
3. Cài đặt các thư viện Python cần thiết:
   ```bash
   pip install fonttools freetype-py pillow numpy
   ```
4. Chạy script tạo font:
   ```bash
   python vietnamese_builder.py
   ```
   Script sẽ tự động:
   * Tải các nét dấu móc, râu serif từ EB Garamond (nguồn mở OFL).
   * Căn chỉnh quang học (optical center) theo từng biến thể (Regular, Bold, Italic, BoldItalic).
   * Tạo 94 glyphs tiếng Việt có dấu, tổ hợp 2 tầng và sửa nét gạch ngang chuẩn cho chữ `Đ / đ`.
   * Xuất ra bộ font hoàn chỉnh `Michelangelus-VN-*.ttf`.

### Tải và sử dụng

| Định dạng | File | Mục đích |
| --- | --- | --- |
| TTF · phiên bản 2.010 | [Regular](Michelangelus-VN-Regular.ttf), [Bold](Michelangelus-VN-Bold.ttf), [Italic](Michelangelus-VN-Italic.ttf), [Bold Italic](Michelangelus-VN-BoldItalic.ttf) | Ứng dụng trên máy tính hỗ trợ TrueType |
| CP · .cpfont | [12](Michelangelus-vn_12.cpfont), [14](Michelangelus-vn_14.cpfont), [16](Michelangelus-vn_16.cpfont), [18](Michelangelus-vn_18.cpfont) | Máy đọc sách dùng firmware hỗ trợ .cpfont |

### Tình trạng & Điểm cải tiến
- Đã bổ sung trọn vẹn 146 ký tự tiếng Việt chuẩn Unicode.
- Dấu thanh và dấu kép 2 tầng (như ấ, ầ, ắ, ằ, ố, ồ...) được scale tỉ lệ hài hòa và đặt vát theo sườn nón/lòng trăng, không chạm trần ascender.
- Nét móc râu `ơ, ư` uốn cong tự nhiên theo thân chữ với đầu giọt lệ Phục hưng.
- Sửa lỗi font gốc gán nhầm chữ `Đ / đ` thành `Dcaron / dcaron`, thay bằng dấu gạch ngang thân chuẩn xác.
- Mã kiểm tra SHA-256 nằm trong [SHA256SUMS.txt](SHA256SUMS.txt).
