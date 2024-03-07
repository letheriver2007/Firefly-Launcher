import urllib.request
import json
from PySide6.QtCore import QThread, Signal
from app.src.common.config import cfg
import winreg

def get_proxy_port():
    reg_path = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings'
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ)
    
    try:
        proxy_enable, _ = winreg.QueryValueEx(reg_key, 'ProxyEnable')
        if proxy_enable == 1:  # 代理已启用
            proxy_server, _ = winreg.QueryValueEx(reg_key, 'ProxyServer')
            if proxy_server.strip() != '':
                proxy_parts = proxy_server.split(':')
                if len(proxy_parts) > 1:
                    proxy_port = proxy_parts[1]
                    return proxy_port
                else:
                    return None
            else:
                return None  # 代理为空
        else:
            return None  # 代理已关闭
    except FileNotFoundError:
        return None  # 未找到注册表

def get_latest_version():
    if get_proxy_port() == None:
        if cfg.proxyStatus.value:
            url = 'https://raw.githubusercontent.com/letheriver2007/Firefly-Launcher/main/config/version.json'
            proxy_support = urllib.request.ProxyHandler({'http': f'http://127.0.0.1:{cfg.PROXY_PORT}', 'https': f'https://127.0.0.1:{cfg.PROXY_PORT}'})
        else:
            url = 'https://raw.gitmirror.com/letheriver2007/Firefly-Launcher/main/config/version.json'
            proxy_support = urllib.request.ProxyHandler()
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
        print(e)
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
            if get_proxy_port() != cfg.PROXY_PORT:
                self._update_signal.emit(0, '代理设置错误')
            else:
                self._update_signal.emit(0, '网络访问错误')