<# :
@echo off
setlocal
echo ============================================================
echo   AI HARNESS BUNDLER
echo ============================================================
echo.
echo Packaging all harness files into ai_harness_bundle.txt...
echo.
powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((Get-Content '%~f0' | Out-String))"
echo.
echo ============================================================
echo   SUCCESS: ai_harness_bundle.txt has been created.
echo ============================================================
echo.
pause
exit /b
#>

$outfile = "ai_harness_bundle.txt"
$exclude = @("logs", "bin", ".git", "node_modules", "__pycache__")
$extensions = @(".json", ".md", ".py", ".bat", ".ps1", ".txt", ".yml", ".yaml", ".sh", ".skill", ".workflow")

$files = Get-ChildItem -Path . -Recurse -File | Where-Object {
    $path = $_.FullName
    $name = $_.Name
    $ext = $_.Extension
    
    $shouldSkip = $false
    foreach ($ex in $exclude) {
        if ($path -like "*\$ex\*") { $shouldSkip = $true; break }
    }
    
    if ($name -eq $outfile -or $name -eq "bundle_harness.bat") { $shouldSkip = $true }
    
    -not $shouldSkip -and ($extensions -contains $ext)
}

$header = "AI HARNESS COMPLETE BUNDLE - Generated on $(Get-Date)"
$header | Out-File -FilePath $outfile -Encoding utf8

$total = $files.Count
$count = 0

foreach ($file in $files) {
    $count++
    $relPath = Resolve-Path $file.FullName -Relative
    $relPath = $relPath -replace '^\.\\', ''
    
    Write-Host "[$count/$total] Adding $relPath" -ForegroundColor Cyan
    
    "--------------------------------------------------------------------------------" | Out-File -FilePath $outfile -Append -Encoding utf8
    "FILE: $relPath" | Out-File -FilePath $outfile -Append -Encoding utf8
    "--------------------------------------------------------------------------------" | Out-File -FilePath $outfile -Append -Encoding utf8
    
    try {
        Get-Content $file.FullName -Raw | Out-File -FilePath $outfile -Append -Encoding utf8
    } catch {
        "ERROR: Could not read file content." | Out-File -FilePath $outfile -Append -Encoding utf8
    }
    
    "`n`n" | Out-File -FilePath $outfile -Append -Encoding utf8
}
