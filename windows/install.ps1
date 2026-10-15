
# Michelangelus VN - Windows Font Installer
$ErrorActionPreference = 'Stop'

Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "    CÀI ĐẶT FONT MICHELANGELUS VN (1-CLICK WINDOWS)" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""

$scriptDir = $PSScriptRoot
$fonts = @(
    @{ File = "Michelangelus-VN-Regular.ttf"; Name = "Michelangelus VN Regular (TrueType)" },
    @{ File = "Michelangelus-VN-Bold.ttf"; Name = "Michelangelus VN Bold (TrueType)" },
    @{ File = "Michelangelus-VN-Italic.ttf"; Name = "Michelangelus VN Italic (TrueType)" },
    @{ File = "Michelangelus-VN-BoldItalic.ttf"; Name = "Michelangelus VN Bold Italic (TrueType)" }
)

# Check if Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if ($isAdmin) {
    Write-Host "[*] Quyền: Administrator (Cài đặt cho toàn bộ hệ thống)" -ForegroundColor Cyan
    $targetDir = "$env:SystemRoot\Fonts"
    $regPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
} else {
    Write-Host "[*] Quyền: Standard User (Cài đặt cho người dùng hiện tại)" -ForegroundColor Cyan
    $targetDir = "$env:LOCALAPPDATA\Microsoft\Windows\Fonts"
    $regPath = "HKCU:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
    if (-not (Test-Path $targetDir)) {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    }
}

Write-Host "[*] Thư mục đích: $targetDir" -ForegroundColor DarkGray
Write-Host ""

$searchDirs = @($scriptDir, (Split-Path -Parent $scriptDir))

$installed = 0
foreach ($item in $fonts) {
    $srcPath = $null
    foreach ($d in $searchDirs) {
        $candidate = Join-Path $d $item.File
        if (Test-Path $candidate) {
            $srcPath = $candidate
            break
        }
    }
    if ($srcPath) {
        $destPath = Join-Path $targetDir $item.File
        
        $copied = $false
        try {
            Copy-Item -Path $srcPath -Destination $destPath -Force -ErrorAction Stop
            $copied = $true
        } catch {
            if (Test-Path $destPath) {
                # File already exists and is locked by a running process, still consider it installed
                $copied = $true
                Write-Host "  [i] File đang mở: $($item.File) (sử dụng bản đã cài)" -ForegroundColor DarkGray
            } else {
                Write-Host "  [!] Không thể ghi file: $($item.File)" -ForegroundColor Red
            }
        }
        
        if ($copied) {
            $regValue = if ($isAdmin) { $item.File } else { $destPath }
            Set-ItemProperty -Path $regPath -Name $item.Name -Value $regValue -Force
            Write-Host "  [OK] Đã cài đặt: $($item.Name)" -ForegroundColor Green
            $installed++
        }
    } else {
        Write-Host "  [!] Không tìm thấy file nguồn: $($item.File)" -ForegroundColor Yellow
    }
}

# Broadcast WM_FONTCHANGE
try {
    $win32 = Add-Type -MemberDefinition @"
[DllImport("gdi32.dll")]
public static extern int AddFontResource(string lpFileName);

[DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
public static extern bool SendMessageTimeout(IntPtr hWnd, uint Msg, UIntPtr wParam, IntPtr lParam, uint fuFlags, uint uTimeout, out UIntPtr lpdwResult);
"@ -Name "FontNative" -Namespace "FontInstaller" -PassThru -ErrorAction SilentlyContinue

    $HWND_BROADCAST = [IntPtr]0xffff
    $WM_FONTCHANGE = 0x001D
    $result = [UIntPtr]::Zero
    [FontInstaller.FontNative]::SendMessageTimeout($HWND_BROADCAST, $WM_FONTCHANGE, [UIntPtr]::Zero, [IntPtr]::Zero, 2, 1000, [ref]$result) | Out-Null
} catch {}

Write-Host ""
if ($installed -eq $fonts.Count) {
    Write-Host "[THÀNH CÔNG] Đã cài đặt đầy đủ $installed/4 font Michelangelus VN!" -ForegroundColor Green
    Write-Host "Bạn có thể mở Word, Photoshop, trình duyệt... và chọn font 'Michelangelus VN' ngay bây giờ." -ForegroundColor White
} elseif ($installed -gt 0) {
    Write-Host "[HOÀN TẤT] Đã cài đặt $installed font vào hệ thống." -ForegroundColor Yellow
} else {
    Write-Host "[NHẮC NHỞ] Chưa tìm thấy các file font Michelangelus-VN-*.ttf." -ForegroundColor Red
    Write-Host "Vui lòng chạy 'python vietnamese_builder.py' trước để tạo bộ font từ nguồn gốc Microsoft." -ForegroundColor Yellow
    Write-Host "Xem chi tiết hướng dẫn tại README.md" -ForegroundColor Cyan
}
