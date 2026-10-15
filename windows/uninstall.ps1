
# Michelangelus VN - Windows Font Uninstaller
$ErrorActionPreference = 'SilentlyContinue'

$fonts = @(
    @{ File = "Michelangelus-VN-Regular.ttf"; Name = "Michelangelus VN Regular (TrueType)" },
    @{ File = "Michelangelus-VN-Bold.ttf"; Name = "Michelangelus VN Bold (TrueType)" },
    @{ File = "Michelangelus-VN-Italic.ttf"; Name = "Michelangelus VN Italic (TrueType)" },
    @{ File = "Michelangelus-VN-BoldItalic.ttf"; Name = "Michelangelus VN Bold Italic (TrueType)" }
)

Write-Host "Đang gỡ bỏ font Michelangelus VN khỏi Windows..." -ForegroundColor Cyan

# Remove from per-user location
$userFontsDir = "$env:LOCALAPPDATA\Microsoft\Windows\Fonts"
$userReg = "HKCU:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"

# Remove from system location
$sysFontsDir = "$env:SystemRoot\Fonts"
$sysReg = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"

foreach ($item in $fonts) {
    # Delete from HKCU
    Remove-ItemProperty -Path $userReg -Name $item.Name -ErrorAction SilentlyContinue
    $userFile = Join-Path $userFontsDir $item.File
    if (Test-Path $userFile) {
        Remove-Item -Path $userFile -Force -ErrorAction SilentlyContinue
    }
    
    # Delete from HKLM
    Remove-ItemProperty -Path $sysReg -Name $item.Name -ErrorAction SilentlyContinue
    $sysFile = Join-Path $sysFontsDir $item.File
    if (Test-Path $sysFile) {
        Remove-Item -Path $sysFile -Force -ErrorAction SilentlyContinue
    }
    
    Write-Host "  [-] Đã gỡ: $($item.Name)" -ForegroundColor Yellow
}

# Broadcast font change
try {
    $win32 = Add-Type -MemberDefinition @"
[DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
public static extern bool SendMessageTimeout(IntPtr hWnd, uint Msg, UIntPtr wParam, IntPtr lParam, uint fuFlags, uint uTimeout, out UIntPtr lpdwResult);
"@ -Name "FontNativeUninst" -Namespace "FontUninstaller" -PassThru -ErrorAction SilentlyContinue

    $HWND_BROADCAST = [IntPtr]0xffff
    $WM_FONTCHANGE = 0x001D
    $result = [UIntPtr]::Zero
    [FontUninstaller.FontNativeUninst]::SendMessageTimeout($HWND_BROADCAST, $WM_FONTCHANGE, [UIntPtr]::Zero, [IntPtr]::Zero, 2, 1000, [ref]$result) | Out-Null
} catch {}

Write-Host ""
Write-Host "[HOÀN TẤT] Đã gỡ bỏ toàn bộ font Michelangelus VN khỏi hệ thống." -ForegroundColor Green
