#!/bin/bash
cd "$(dirname "$0")"
if ! command -v conda &> /dev/null; then
    echo "Installing Miniconda..."
    ARCH=$(uname -m)
    OS_TYPE="MacOSX"
    [[ "$ARCH" == "arm64" ]] && INSTALLER="Miniconda3-latest-${OS_TYPE}-arm64.sh" || INSTALLER="Miniconda3-latest-${OS_TYPE}-x86_64.sh"
    curl -O "https://repo.anaconda.com/miniconda/$INSTALLER"
    bash "$INSTALLER" -b -p "$HOME/miniconda"
    rm "$INSTALLER"
    source "$HOME/miniconda/bin/activate"
    conda init zsh
fi
conda env create -f environment.yml --yes
echo "Done! Restart your terminal to begin."