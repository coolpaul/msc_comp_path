@echo off
echo ==============================================
echo       MsC COMPUTATIONAL PATHOLOGY ENVIRONMENT SETUP
echo ==============================================

:: 1. VS Code Installation
echo [1/5] Installing Visual Studio Code...
curl -L "https://update.code.visualstudio.com/latest/win32-x64-user/stable" -o vscode_setup.exe
start /wait vscode_setup.exe /verysilent /mergetasks=!runcode
del vscode_setup.exe

:: 2. Quarto Installation
echo [2/5] Installing Quarto (v1.9.36)...
curl -L "https://github.com/quarto-dev/quarto-cli/releases/download/v1.9.36/quarto-1.9.36-win.msi" -o quarto_setup.msi
start /wait msiexec /i quarto_setup.msi /quiet
del quarto_setup.msi

:: 3. Zotero Installation
echo [3/5] Installing Zotero...
curl -L "https://www.zotero.org/download/client/dl?channel=release&platform=win32" -o zotero_setup.exe
start /wait zotero_setup.exe /S
del zotero_setup.exe

:: 4. QuPath Portable
echo [4/5] Downloading QuPath (Portable)...
curl -L "https://github.com/qupath/qupath/releases/download/v0.7.0/QuPath-v0.7.0-Windows.zip" -o qupath.zip
powershell -command "Expand-Archive -Path qupath.zip -DestinationPath ."
del qupath.zip

:: 5. Conda Environment build
echo [5/5] Building Python Environment (This may take a few minutes)...
call conda env create -f environment.yml

echo SETUP COMPLETE. PLEASE RESTART YOUR COMPUTER.
pause