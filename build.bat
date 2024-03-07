@echo off
xcopy /s /e /y Firefly-Launcher\ Firefly-Launcher_backup\
rd /s /q Firefly-Launcher\

python -m pip install --upgrade pip
pip install pip install "PySide6-Fluent-Widgets" -i https://pypi.org/simple/
pip install PySide6==6.4.2
pip install PySideSix-Frameless-Window>=0.3.1
pip install pyinstaller
pyinstaller -w -i ./app/src/image/icon.ico ./main.py -n Firefly-Launcher

xcopy  /s /e /y dist\Firefly-Launcher\ Firefly-Launcher\
xcopy /s /e /y app\src\common\qss\ Firefly-Launcher\app\src\common\qss\
xcopy /s /e /y app\src\image\ Firefly-Launcher\app\src\image\
xcopy /s /e /y app\src\script\  Firefly-Launcher\app\src\script\
xcopy /s /e /y config\ Firefly-Launcher\config\
rd /s /q dist\
rd /s /q build\
del /f /q 0.3.1
del /f /q Firefly-Launcher.spec
rd /s /q __pycache__\
rd /s /q app\__pycache__\
rd /s /q app\src\common\__pycache__\
rd /s /q config__pycache__\
rd  /s /q Firefly-Launcher_backup\

start ./Firefly-Launcher/Firefly-Launcher.exe