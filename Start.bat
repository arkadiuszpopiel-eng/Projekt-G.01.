@echo off
REM ============================================================
REM  GATE DOMINION - Master Build Script
REM  One command to rule them all.
REM  This script verifies dependencies, downloads Godot if needed,
REM  generates the entire project, builds, and launches the game.
REM ============================================================

setlocal enabledelayedexpansion

echo ============================================================
echo   GATE DOMINION - AI Game Development Studio
echo   Initializing build pipeline...
echo ============================================================
echo.

REM ----------------------------------------------------------
REM  STEP 0: Configuration
REM ----------------------------------------------------------
set "PROJECT_ROOT=%~dp0"
set "ENGINE_DIR=%PROJECT_ROOT%engine"
set "PROJECT_DIR=%PROJECT_ROOT%project"
set "TOOLS_DIR=%PROJECT_ROOT%tools"
set "BUILD_DIR=%PROJECT_ROOT%build"
set "GODOT_VERSION=4.2.2-stable"
set "GODOT_ZIP=Godot_v%GODOT_VERSION%_win64.exe.zip"
set "GODOT_URL=https://github.com/godotengine/godot/releases/download/%GODOT_VERSION%/Godot_v%GODOT_VERSION%_win64.exe.zip"
set "GODOT_EXE=%ENGINE_DIR%\Godot_v%GODOT_VERSION%_win64.exe"

REM ----------------------------------------------------------
REM  STEP 1: Verify Python Installation
REM ----------------------------------------------------------
echo [1/9] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYTHON_VER=%%v
echo   Found Python %PYTHON_VER%
echo.

REM ----------------------------------------------------------
REM  STEP 2: Create Directory Structure
REM ----------------------------------------------------------
echo [2/9] Creating directory structure...
if not exist "%ENGINE_DIR%" mkdir "%ENGINE_DIR%"
if not exist "%PROJECT_DIR%" mkdir "%PROJECT_DIR%"
if not exist "%PROJECT_DIR%\scripts" mkdir "%PROJECT_DIR%\scripts"
if not exist "%PROJECT_DIR%\scenes" mkdir "%PROJECT_DIR%\scenes"
if not exist "%PROJECT_DIR%\ui" mkdir "%PROJECT_DIR%\ui"
if not exist "%PROJECT_DIR%\data" mkdir "%PROJECT_DIR%\data"
if not exist "%PROJECT_DIR%\assets" mkdir "%PROJECT_DIR%\assets"
if not exist "%PROJECT_DIR%\assets\audio" mkdir "%PROJECT_DIR%\assets\audio"
if not exist "%TOOLS_DIR%" mkdir "%TOOLS_DIR%"
if not exist "%BUILD_DIR%" mkdir "%BUILD_DIR%"
echo   Directory tree created.
echo.

REM ----------------------------------------------------------
REM  STEP 3: Download Godot Engine if missing
REM ----------------------------------------------------------
echo [3/9] Checking Godot Engine...
if exist "%GODOT_EXE%" (
    echo   Godot Engine found at %GODOT_EXE%
) else (
    echo   Godot Engine not found. Downloading...
    echo   URL: %GODOT_URL%

    REM Try PowerShell download
    powershell -Command "& { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%GODOT_URL%' -OutFile '%ENGINE_DIR%\%GODOT_ZIP%' }" 2>nul

    if not exist "%ENGINE_DIR%\%GODOT_ZIP%" (
        REM Fallback to certutil
        echo   PowerShell download failed, trying certutil...
        certutil -urlcache -split -f "%GODOT_URL%" "%ENGINE_DIR%\%GODOT_ZIP%" >nul 2>&1
    )

    if not exist "%ENGINE_DIR%\%GODOT_ZIP%" (
        echo   ERROR: Failed to download Godot Engine.
        echo   Please manually download from: %GODOT_URL%
        echo   Place the zip in: %ENGINE_DIR%\
        pause
        exit /b 1
    )

    echo   Extracting Godot Engine...
    powershell -Command "Expand-Archive -Path '%ENGINE_DIR%\%GODOT_ZIP%' -DestinationPath '%ENGINE_DIR%' -Force"

    if not exist "%GODOT_EXE%" (
        echo   ERROR: Extraction failed or executable not found.
        echo   Expected: %GODOT_EXE%
        pause
        exit /b 1
    )

    echo   Godot Engine ready.
)
echo.

REM ----------------------------------------------------------
REM  STEP 4: Generate Project (project.godot + folder structure)
REM ----------------------------------------------------------
echo [4/9] Generating Godot project...
python "%TOOLS_DIR%\generate_project.py" "%PROJECT_DIR%" "%GODOT_EXE%"
if errorlevel 1 (
    echo   ERROR: Project generation failed.
    pause
    exit /b 1
)
echo.

REM ----------------------------------------------------------
REM  STEP 5: Generate Game Code (GDScript files)
REM ----------------------------------------------------------
echo [5/9] Generating game code...
python "%TOOLS_DIR%\generate_code.py" "%PROJECT_DIR%"
if errorlevel 1 (
    echo   ERROR: Code generation failed.
    pause
    exit /b 1
)
echo.

REM ----------------------------------------------------------
REM  STEP 6: Generate Assets (textures, sprites, etc.)
REM ----------------------------------------------------------
echo [6/9] Generating assets...
python "%TOOLS_DIR%\generate_assets.py" "%PROJECT_DIR%"
if errorlevel 1 (
    echo   ERROR: Asset generation failed.
    pause
    exit /b 1
)
echo.

REM ----------------------------------------------------------
REM  STEP 7: Generate Scenes (.tscn files)
REM ----------------------------------------------------------
echo [7/9] Generating scenes and UI...
python "%TOOLS_DIR%\generate_scenes.py" "%PROJECT_DIR%"
if errorlevel 1 (
    echo   ERROR: Scene generation failed.
    pause
    exit /b 1
)
python "%TOOLS_DIR%\generate_ui.py" "%PROJECT_DIR%"
if errorlevel 1 (
    echo   ERROR: UI generation failed.
    pause
    exit /b 1
)
echo.

REM ----------------------------------------------------------
REM  STEP 8: Generate Data (JSON configs, balance data)
REM ----------------------------------------------------------
echo [8/9] Generating game data...
python "%TOOLS_DIR%\generate_data.py" "%PROJECT_DIR%"
if errorlevel 1 (
    echo   ERROR: Data generation failed.
    pause
    exit /b 1
)
echo.

REM ----------------------------------------------------------
REM  STEP 9: Build and Launch
REM ----------------------------------------------------------
echo [9/9] Building and launching Gate Dominion...
python "%TOOLS_DIR%\build_game.py" "%PROJECT_DIR%" "%GODOT_EXE%" "%BUILD_DIR%"
if errorlevel 1 (
    echo   WARNING: Build failed. Attempting to run from editor...
)

REM Launch the game directly with Godot
echo.
echo ============================================================
echo   GATE DOMINION - Launching...
echo ============================================================
echo.

echo   Godot: %GODOT_EXE%
echo   Project: %PROJECT_DIR%
echo.
if not exist "%GODOT_EXE%" (
    echo   ERROR: Godot engine not found at: %GODOT_EXE%
    echo   Please download Godot 4.2.2 manually and place it in the engine\ folder.
    echo.
    pause
    exit /b 1
)

echo   Starting Godot Engine...
echo.
"%GODOT_EXE%" --path "%PROJECT_DIR%"
set GODOT_EXIT=%errorlevel%
echo.
echo   Godot exited with code: %GODOT_EXIT%

if %GODOT_EXIT% neq 0 (
    echo   Godot returned an error. Trying alternative launch...
    "%GODOT_EXE%" --main-pack "%PROJECT_DIR%"
)

echo.
echo ============================================================
echo   GATE DOMINION - Session ended.
echo   Press any key to close this window.
echo ============================================================
pause

endlocal
