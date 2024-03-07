@echo off
rd /s /q Firefly-Launcher\
rd /s /q __pycache__\
rd /s /q app\__pycache__\
rd /s /q src\component\__pycache__\
rd /s /q src\module\__pycache__\
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install "PySide6-Fluent-Widgets" -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install PySide6==6.4.2 -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install PySideSix-Frameless-Window>=0.3.1 -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple/
pyinstaller -w -i ./src/image/icon.ico ./main.py -n Firefly-Launcher
xcopy  /s /e /y dist\Firefly-Launcher\ Firefly-Launcher\
xcopy /s /e /y src\qss\ Firefly-Launcher\src\qss\
xcopy /s /e /y src\image\ Firefly-Launcher\src\image\
xcopy /s /e /y src\patch\starrail\ Firefly-Launcher\src\patch\starrail\
xcopy /s /e /y src\patch\yuanshen\  Firefly-Launcher\src\patch\yuanshen\
xcopy /s /e /y src\patch\gradle\ Firefly-Launcher\src\patch\gradle\
xcopy /s /e /y src\patch\font\ Firefly-Launcher\src\patch\font\
xcopy /s /e /y config\ Firefly-Launcher\config\
rd /s /q dist\
rd /s /q build\
del /f /q 0.3.1
del /f /q Firefly-Launcher.spec
rd /s /q __pycache__\
rd /s /q app\__pycache__\
rd /s /q src\component\__pycache__\
rd /s /q src\module\__pycache__\
start ./Firefly-Launcher/Firefly-Launcher.exe