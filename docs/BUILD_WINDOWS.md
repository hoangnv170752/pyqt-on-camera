# Building Windows Executable

This guide explains how to package the PC CamTouch application as a standalone Windows executable (.exe).

## Prerequisites

**You must build on a Windows machine** (or Windows VM). Cross-compilation from macOS/Linux is not reliable for PyQt6 applications.

### Required Software

1. **Python 3.10 or higher** for Windows
2. **Git** (optional, for cloning)
3. **Visual C++ Redistributable** (usually already installed)

## Installation Steps

### 1. Install Dependencies

On Windows, open PowerShell or Command Prompt:

```powershell
# Clone or copy the project to Windows machine
cd path\to\pyqt-on-camera

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install PyInstaller
pip install pyinstaller
```

### 2. Build the Executable

#### Option A: Using the spec file (Recommended)

```powershell
pyinstaller pc-camtouch.spec
```

#### Option B: Using command line

```powershell
pyinstaller --name "PC CamTouch" ^
    --windowed ^
    --onedir ^
    --add-data "config;config" ^
    --add-data "data;data" ^
    --hidden-import PyQt6.QtCore ^
    --hidden-import PyQt6.QtGui ^
    --hidden-import PyQt6.QtWidgets ^
    --hidden-import pygame ^
    --hidden-import cv2 ^
    --hidden-import loguru ^
    --hidden-import psutil ^
    --hidden-import pyvidplayer2 ^
    --exclude-module tkinter ^
    --exclude-module matplotlib ^
    main.py
```

### 3. Locate Your Application

After building, your application will be in:
```
dist\PC CamTouch\PC CamTouch.exe
```

### 4. Test the Application

```powershell
cd dist\PC CamTouch
"PC CamTouch.exe"
```

## Distribution

### Option 1: ZIP Archive (Simple)

1. Compress the entire `dist\PC CamTouch` folder
2. Share the .zip file with users
3. Users extract and run `PC CamTouch.exe`

```powershell
# Using PowerShell
Compress-Archive -Path "dist\PC CamTouch" -DestinationPath "PC-CamTouch-Windows.zip"
```

### Option 2: Installer (Professional)

Use **Inno Setup** to create a Windows installer:

1. Download and install [Inno Setup](https://jrsoftware.org/isinfo.php)
2. Create an installer script (see `installer.iss` example below)
3. Compile with Inno Setup

#### Example Inno Setup Script (`installer.iss`):

```ini
[Setup]
AppName=PC CamTouch
AppVersion=1.0.0
DefaultDirName={autopf}\PC CamTouch
DefaultGroupName=PC CamTouch
OutputDir=installer
OutputBaseFilename=PC-CamTouch-Setup
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "dist\PC CamTouch\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\PC CamTouch"; Filename: "{app}\PC CamTouch.exe"
Name: "{autodesktop}\PC CamTouch"; Filename: "{app}\PC CamTouch.exe"

[Run]
Filename: "{app}\PC CamTouch.exe"; Description: "Launch PC CamTouch"; Flags: postinstall nowait skipifsilent
```

### Option 3: Single File Executable

For a single .exe file (larger, slower startup):

```powershell
pyinstaller --name "PC CamTouch" ^
    --windowed ^
    --onefile ^
    --add-data "config;config" ^
    --add-data "data;data" ^
    main.py
```

**Note**: Single file mode is NOT recommended for large apps like this (200-300MB).

## Troubleshooting

### Issue: "Missing DLL" errors

**Solution**: Install Visual C++ Redistributable
- Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe

### Issue: App crashes on startup

**Solution**: Run with console to see errors:
```powershell
# Edit pc-camtouch.spec: change console=False to console=True
# Rebuild and check console output
```

### Issue: "Failed to execute script"

**Solution**: Check hidden imports in spec file. Add missing modules:
```python
hiddenimports=[
    'missing_module_name',
    # ... other imports
]
```

### Issue: Large file size (>500MB)

**Solution**: This is normal for Python apps with PyQt6, OpenCV, and pygame. To reduce:
- Use `--exclude-module` for unused packages
- Use UPX compression (already enabled)
- Remove test/documentation files from dependencies

### Issue: Antivirus flags the .exe

**Solution**: 
1. This is common for PyInstaller executables
2. Submit to antivirus vendors as false positive
3. Or: Code sign the executable (requires certificate, ~$100-500/year)

## File Structure

After building, your distribution folder contains:

```
dist/PC CamTouch/
├── PC CamTouch.exe          # Main executable
├── python313.dll            # Python runtime
├── _internal/               # Python libraries and dependencies
│   ├── PyQt6/
│   ├── pygame/
│   ├── cv2/
│   └── ... (other packages)
├── config/                  # Configuration files
└── data/                    # Database and data files
```

## System Requirements

The built application requires:
- **Windows 10 or later** (64-bit)
- **~500MB disk space**
- **4GB RAM minimum** (8GB recommended)
- **DirectX 9.0c or later** (for pygame)

## Advanced: Code Signing

To avoid Windows SmartScreen warnings:

1. Purchase a code signing certificate
2. Sign the executable:
   ```powershell
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com "dist\PC CamTouch\PC CamTouch.exe"
   ```

## CI/CD Build (GitHub Actions)

Create `.github/workflows/build-windows.yml`:

```yaml
name: Build Windows

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller
      
      - name: Build executable
        run: pyinstaller pc-camtouch.spec
      
      - name: Create ZIP
        run: Compress-Archive -Path "dist\PC CamTouch" -DestinationPath "PC-CamTouch-Windows.zip"
      
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: windows-build
          path: PC-CamTouch-Windows.zip
```

## Notes

- First launch may take 10-20 seconds (Python runtime initialization)
- Database and logs are stored in the app directory
- The app is portable - can be run from USB drive
- No installation required (unless using Inno Setup installer)

## Clean Build

To start fresh:

```powershell
# Remove build artifacts
Remove-Item -Recurse -Force build, dist
Remove-Item *.spec

# Rebuild
pyinstaller pc-camtouch.spec
```
