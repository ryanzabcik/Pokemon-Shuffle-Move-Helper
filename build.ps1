Write-Host "Removing existing zip files, build, and dist folders..."
Remove-Item -Path "Shuffle_Move_Helper*.zip" -ErrorAction SilentlyContinue
if (Test-Path "dist") { Remove-Item -Path "dist" -Recurse -Force }
if (Test-Path "build") { Remove-Item -Path "build" -Recurse -Force }

Write-Host "Executing pyinstaller..."
pyinstaller main.spec
if ($LASTEXITCODE -ne 0) {
    Write-Error "PyInstaller failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

Write-Host "Copying assets folder to dist..."
New-Item -ItemType Directory -Path "dist\main\assets" -Force | Out-Null
Copy-Item -Path "assets\*" -Destination "dist\main\assets" -Recurse -Force

Write-Host "Extracting Version Number..."
$versionContent = Get-Content -Path "app\src\version.py" -Raw
if ($versionContent -match '(?m)^\s*current_version\s*=\s*["'']([^"'']+)["'']') {
    $version = $Matches[1].Trim()
} else {
    Write-Error "Failed to extract current_version from app\src\version.py"
    exit 1
}

Write-Host "Zipping contents of dist\main..."
Compress-Archive -Path "dist\main\*" -DestinationPath "Shuffle_Move_Helper_$version.zip" -Force

Write-Host "Done."
Pause
