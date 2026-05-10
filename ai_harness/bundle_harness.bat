<# :
@echo off
setlocal
echo ============================================================
echo   AI HARNESS BUNDLER
echo ============================================================
echo.
echo Packaging all harness files into ai_harness_bundle.txt...
echo.
powershell -NoProfile -ExecutionPolicy Bypass -Command "iex (Get-Content -LiteralPath '%~f0' -Raw -Encoding UTF8)"
echo.
echo ============================================================
echo   SUCCESS: ai_harness_bundle.txt has been created.
echo ============================================================
echo.
pause
exit /b
#>

$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$outfile = "ai_harness_bundle.txt"
$exclude = @("logs", "bin", ".git", "node_modules", "__pycache__")
$runtimeSubtrees = @(
    ".agent\Loop_Flow",
    ".agent\state\sessions"
)
$runtimeFiles = @(
    ".agent\state\studio_loop.lock"
)
$extensions = @(".json", ".md", ".py", ".bat", ".ps1", ".txt", ".yml", ".yaml", ".sh", ".skill", ".workflow")

function Normalize-AsciiText([string]$text) {
    if ($null -eq $text) { return "" }
    $text = $text.Replace([string][char]0x2018, "'")
    $text = $text.Replace([string][char]0x2019, "'")
    $text = $text.Replace([string][char]0x201C, '"')
    $text = $text.Replace([string][char]0x201D, '"')
    $text = $text.Replace([string][char]0x2014, "-")
    $text = $text.Replace([string][char]0x2013, "-")
    $text = $text.Replace([string][char]0x2026, "...")
    $text = $text.Replace([string][char]0x00A0, " ")
    return $text
}

function Add-BundleText([string]$text) {
    $normalized = Normalize-AsciiText $text
    [System.IO.File]::AppendAllText((Resolve-Path $outfile), $normalized + [Environment]::NewLine, $OutputEncoding)
}

$files = Get-ChildItem -Path . -Recurse -File | Where-Object {
    $path = $_.FullName
    $name = $_.Name
    $ext = $_.Extension
    $relPath = Resolve-Path $_.FullName -Relative
    $relPath = $relPath -replace '^\.\\', ''
    
    $shouldSkip = $false
    foreach ($ex in $exclude) {
        if ($path -like "*\$ex\*") { $shouldSkip = $true; break }
    }

    foreach ($subtree in $runtimeSubtrees) {
        if ($relPath -eq $subtree -or $relPath.StartsWith($subtree + "\")) {
            $shouldSkip = $true
            break
        }
    }

    if ($runtimeFiles -contains $relPath) { $shouldSkip = $true }
    
    if ($name -eq $outfile -or $name -eq "bundle_harness.bat") { $shouldSkip = $true }
    
    -not $shouldSkip -and ($extensions -contains $ext)
}

$header = "AI HARNESS COMPLETE BUNDLE - Generated on $(Get-Date)"
[System.IO.File]::WriteAllText((Join-Path (Get-Location) $outfile), $header + [Environment]::NewLine, $OutputEncoding)

$total = $files.Count
$count = 0

foreach ($file in $files) {
    $count++
    $relPath = Resolve-Path $file.FullName -Relative
    $relPath = $relPath -replace '^\.\\', ''
    
    Write-Host "[$count/$total] Adding $relPath" -ForegroundColor Cyan
    
    Add-BundleText "--------------------------------------------------------------------------------"
    Add-BundleText "FILE: $relPath"
    Add-BundleText "--------------------------------------------------------------------------------"
    
    try {
        $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
        Add-BundleText $content
    } catch {
        Add-BundleText "ERROR: Could not read file content."
    }
    
    Add-BundleText "`n"
}
