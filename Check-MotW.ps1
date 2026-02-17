# Check-MotW.ps1
# Safe Research Tool for Verifying Mark of the Web (MotW) Integrity

param (
    [Parameter(Mandatory=$true)]
    [string]$FilePath
)

if (-not (Test-Path $FilePath)) {
    Write-Host "[-] File not found: $FilePath" -ForegroundColor Red
    exit
}

# Check for the Zone.Identifier Alternate Data Stream
$stream = Get-Item -Path $FilePath -Stream Zone.Identifier -ErrorAction SilentlyContinue

if ($stream) {
    Write-Host "[+] SAFE: Mark of the Web FOUND on: $FilePath" -ForegroundColor Green
    Write-Host "    ZoneId Details:" -ForegroundColor Cyan
    Get-Content -Path $FilePath -Stream Zone.Identifier
} else {
    Write-Host "[!] VULNERABLE: No Mark of the Web found on: $FilePath" -ForegroundColor Red
    Write-Host "    Root Cause: The browser failed to apply the 'Internet Zone' tag." -ForegroundColor Yellow
    Write-Host "    Impact: The OS will treat this file as trusted local content." -ForegroundColor Yellow
}
