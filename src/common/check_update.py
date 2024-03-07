import json
import winreg
import urllib.request
from PySide6.QtCore import QThread, Signal
import src.common.config as cfgurl
from src.common.config import cfg

def get_latest_version():
    if cfg.chinaStatus.value:
        url = 'https://raw.gitmirror.com/letheriver2007/Firefly-Launcher/main/config/version.json'
        proxy_support = urllib.request.ProxyHandler()
    elif cfg.proxyStatus.value:
        url = 'https://raw.githubusercontent.com/letheriver2007/Firefly-Launcher/main/config/version.json'
        proxy_support = urllib.request.ProxyHandler({'http': f'http://127.0.0.1:{cfg.PROXY_PORT}', 'https': f'https://127.0.0.1:{cfg.PROXY_PORT}'})
    else:
        url = 'https://raw.githubusercontent.com/letheriver2007/Firefly-Launcher/main/config/version.json'
        proxy_support = urllib.request.ProxyHandler()

    opener = urllib.request.build_opener(proxy_support)
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            if response.getcode() == 200:
                html = response.read()
                latest_version_info = json.loads(html)
                return latest_version_info["version"]
            else:
                return None
    except Exception as e:
        return None

def get_installed_version():
    with open('./config/version.json', 'r') as file:
        installed_version_info = json.load(file)
        return installed_version_info["version"]

def checkUpdate(self):
    self.check_thread = UpdateThread()
    self.check_thread._update_signal.connect(self.handleUpdate)
    self.check_thread.start()

class UpdateThread(QThread):
    _update_signal = Signal(int, str)
    def __init__(self):
        super().__init__()
    
    def run(self):
        latest_version = get_latest_version()
        installed_version = get_installed_version()
        if latest_version and installed_version:
            if latest_version > installed_version:
                self._update_signal.emit(2, str(latest_version))
            elif latest_version == installed_version:
                self._update_signal.emit(1, str(latest_version))
            else:
                self._update_signal.emit(0, '版本信息错误')
        else:
            self._update_signal.emit(0, '网络访问错误')