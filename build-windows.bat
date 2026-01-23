@echo off
REM Build script for Windows executable
REM Run this on a Windows machine

echo ========================================
echo PC CamTouch Windows Build Script
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Install PyInstaller
echo.
echo Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

REM Clean previous builds
echo.
echo Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM Build executable
echo.
echo Building executable...
pyinstaller pc-camtouch.spec
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

REM Create ZIP archive
echo.
echo Creating distribution archive...
powershell -Command "Compress-Archive -Path 'dist\PC CamTouch' -DestinationPath 'PC-CamTouch-Windows.zip' -Force"
if errorlevel 1 (
    echo WARNING: Failed to create ZIP archive
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Executable location: dist\PC CamTouch\PC CamTouch.exe
echo ZIP archive: PC-CamTouch-Windows.zip
echo.
echo You can now test the application by running:
echo   dist\PC CamTouch\PC CamTouch.exe
echo.
pause
