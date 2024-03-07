@echo off
rd /s /q Firefly-Launcher\

python -m pip install --upgrade pip
pip install pip install "PySide6-Fluent-Widgets" -i https://pypi.org/simple/
pip install PySide6==6.4.2
pip install PySideSix-Frameless-Window>=0.3.1
pip install pyinstaller
pyinstaller -w -i ./src/image/icon.ico ./main.py -n Firefly-Launcher

xcopy  /s /e /y dist\Firefly-Launcher\ Firefly-Launcher\
xcopy /s /e /y src\common\qss\ Firefly-Launcher\src\common\qss\
xcopy /s /e /y src\download\ Firefly-Launcher\src\download\
xcopy /s /e /y src\image\ Firefly-Launcher\src\image\
xcopy /s /e /y src\script\starrail\ Firefly-Launcher\src\script\starrail\
xcopy /s /e /y src\script\yuanshen\  Firefly-Launcher\src\script\yuanshen\
xcopy /s /e /y config\ Firefly-Launcher\config\
rd /s /q dist\
rd /s /q build\
del /f /q 0.3.1
del /f /q Firefly-Launcher.spec
rd /s /q __pycache__\
rd /s /q app\__pycache__\
rd /s /q src\common\__pycache__\
rd /s /q config\__pycache__\

start ./Firefly-Launcher/Firefly-Launcher.exe