@echo off
echo Checking for Conda...
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing Miniconda...
    curl -L https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda_installer.exe
    start /wait "" miniconda_installer.exe /S /D=%UserProfile%\miniconda3
    del miniconda_installer.exe
    set "PATH=%UserProfile%\miniconda3\Scripts;%UserProfile%\miniconda3\condabin;%PATH%"
)
echo Creating the environment...
call conda env create -f environment.yml
echo Done!
pause