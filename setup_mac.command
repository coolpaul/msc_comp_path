#!/bin/bash
cd "$(dirname "$0")"
ARCH=$(uname -m)

echo "--- Starting Msc Computational Pathology Setup ---"

# 1. VS Code (Auto-detects Apple Silicon vs Intel)
echo "Installing VS Code..."
curl -L "https://update.code.visualstudio.com/latest/darwin$( [[ "$ARCH" == "arm64" ]] && echo "-arm64" )/stable" -o vscode.zip
unzip -q vscode.zip && mv "Visual Studio Code.app" /Applications && rm vscode.zip

# 2. Quarto
echo "Installing Quarto..."
curl -L "https://github.com/quarto-dev/quarto-cli/releases/download/v1.9.36/quarto-1.9.36-macos.pkg" -o quarto.pkg
sudo installer -pkg quarto.pkg -target /
rm quarto.pkg

# 3. Zotero
echo "Installing Zotero..."
curl -L "https://www.zotero.org/download/client/dl?channel=release&platform=mac$( [[ "$ARCH" == "arm64" ]] && echo "" )" -o zotero.dmg
hdiutil mount zotero.dmg -quiet
cp -R "/Volumes/Zotero/Zotero.app" /Applications
hdiutil unmount "/Volumes/Zotero"
rm zotero.dmg

# 4. QuPath
[[ "$ARCH" == "arm64" ]] && Q_VER="arm64" || Q_VER="x64"
curl -L "https://github.com/qupath/qupath/releases/download/v0.7.0/QuPath-v0.7.0-Mac-$Q_VER.pkg" -o qupath.pkg
sudo installer -pkg qupath.pkg -target /
rm qupath.pkg

# 5. Conda Environment
echo "Building Conda environment..."
conda env create -f environment.yml

echo "--- DONE! Please restart your Terminal. ---"