@echo off
chcp 65001 > nul
echo [*] Deleting pre-version ...
rmdir /s /q build dist
del main.spec

echo [*] Building ...
%~dp0.venv\Scripts\pyinstaller.exe --onefile --noconsole main.py

echo [*] Success! New file on dist\
pause
