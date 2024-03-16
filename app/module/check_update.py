import os
import json
import winreg
import urllib.request
from PySide6.QtCore import QThread, Signal, Qt
from qfluentwidgets import InfoBar, InfoBarPosition
from app.module.config import cfg

def get_latest_version():
    if cfg.chinaStatus.value:
        url = 'https://api.github.com/repos/letheriver2007/Firefly-Launcher/releases/latest'
        proxy_support = urllib.request.ProxyHandler()
    elif cfg.proxyStatus.value:
        url = 'https://api.github.com/repos/letheriver2007/Firefly-Launcher/releases/latest'
        proxy_support = urllib.request.ProxyHandler({'http': f'http://127.0.0.1:{cfg.PROXY_PORT}', 'https': f'https://127.0.0.1:{cfg.PROXY_PORT}'})
    else:
        url = 'https://api.github.com/repos/letheriver2007/Firefly-Launcher/releases/latest'
        proxy_support = urllib.request.ProxyHandler()

    opener = urllib.request.build_opener(proxy_support)
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    try:
        with urllib.request.urlopen(url) as response:
            if response.getcode() == 200:
                data = response.read()
                release_info = json.loads(data)
                latest_tag = release_info['tag_name']
                return latest_tag
            else:
                return None
    except:
        return None

def checkUpdate(self):
    self.check_thread = UpdateThread()
    self.check_thread._update_signal.connect(self.handleUpdate)
    self.check_thread.start()

class UpdateThread(QThread):
    _update_signal = Signal(int, str)
    def __init__(self):
        super().__init__()
    
    def run(self):
        if not os.path.exists('main.py'):
            latest_version = get_latest_version()
            installed_version = cfg.APP_VERSION
            if latest_version and installed_version:
                if latest_version > installed_version:
                    self._update_signal.emit(2, str(latest_version))
                elif latest_version == installed_version:
                    self._update_signal.emit(1, str(latest_version))
                else:
                    self._update_signal.emit(0, '版本信息错误')
            else:
                self._update_signal.emit(0, '网络访问错误')
        else:
            self._update_signal.emit(0, '当前为Dev版本')