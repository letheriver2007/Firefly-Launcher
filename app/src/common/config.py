from qfluentwidgets import qconfig, QConfig, Theme, ConfigItem, BoolValidator
import json

def get_json(file_path, key):
    with open(f'{file_path}', 'r') as file:
        json_data = json.load(file)
        return json_data[f"{key}"]

class Config(QConfig):
    proxyStatus = ConfigItem("Proxy", "ProxyStatus", True, BoolValidator())

    APP_NAME = "Firefly Launcher"
    APP_VERSION = get_json('./config/version.json', 'version')
    APP_FONT = "SDK_SC_Web"
    URL_WRITER = "https://github.com/letheriver2007"
    URL_REPO = "https://github.com/letheriver2007/Firefly-Launcher"
    URL_RELEASES = "https://github.com/letheriver2007/Firefly-Launcher/releases"
    URL_ISSUES = "https://github.com/letheriver2007/Firefly-Launcher/issues"
    PROXY_PORT = get_json('./config/config.json', 'PROXY_PORT')
    SERVER_NAMES = get_json('./config/config.json', 'SERVER_NAMES')
    SERVER_COMMANDS = get_json('./config/config.json', 'SERVER_COMMANDS')


cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load('./config/auto.json', cfg)