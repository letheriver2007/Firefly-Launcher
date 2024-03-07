@echo off
python -m pip install --upgrade pip
pip install pip install "PySide6-Fluent-Widgets" -i https://pypi.org/simple/
pip install PySide6==6.4.2
pip install PySideSix-Frameless-Window>=0.3.1
pip install pyinstaller
pyinstaller -w -i ./src/image/icon.ico ./main_page.py -n Firefly-Launcher
xcopy /s /e /y src\ dist\Firefly-Launcher\src\
start ./dist/Firefly-Launcher/Firefly-Launcher.exe
pause