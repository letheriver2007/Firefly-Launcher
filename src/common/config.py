import json
import urllib.request
from qfluentwidgets import qconfig, QConfig, Theme, ConfigItem, BoolValidator
import src.common.url as url

def get_json(file_path, key):
    with open(f'{file_path}', 'r') as file:
        json_data = json.load(file)
        return json_data[f"{key}"]


class Config(QConfig):
    proxyStatus = ConfigItem("Proxy", "ProxyStatus", False, BoolValidator())
    chinaStatus = ConfigItem("China", "ChinaStatus", True, BoolValidator())

    APP_NAME = "Firefly Launcher"
    APP_VERSION = get_json('./config/version.json', 'version')
    APP_FONT = "SDK_SC_Web"

    URL_WRITER = "https://github.com/letheriver2007"
    URL_REPO = "https://github.com/letheriver2007/Firefly-Launcher"
    URL_RELEASES = "https://github.com/letheriver2007/Firefly-Launcher/releases"
    URL_ISSUES = "https://github.com/letheriver2007/Firefly-Launcher/issues"

    DOWNLOAD_COMMANDS_TOOL = ('Letheriver2007/Firefly-Launcher-Res.git tool')
    DOWNLOAD_COMMANDS_LUNARCORE = ('git clone --progress https://github.com/Melledy/LunarCore.git server/LunarCore && '
    'xcopy /s /e /y "src\\download\\.gradle" "server\\LunarCore\\.gradle\\"')
    DOWNLOAD_COMMANDS_LUNARCORE_RES = ('git clone --progress https://github.com/Dimbreath/StarRailData.git server/LunarCore/resources && '
    'git clone --progress https://gitlab.com/Melledy/LunarCore-Configs.git server/LunarCore/resources/Config/Config && '
    'move "server/LunarCore/resources/Config/Config/Config/ConfigSummonUnit" "server/LunarCore/resources/Config/ConfigSummonUnit" && '
    'xcopy /s /e /y "server/LunarCore/resources/Config/Config/Config/LevelOutput" "server/LunarCore/resources/Config/LevelOutput" && '
    'rmdir /s /q "server/LunarCore/resources/Config/Config"')

    PROXY_PORT = get_json('./config/config.json', 'PROXY_PORT')
    SERVER_NAMES = get_json('./config/config.json', 'SERVER_NAMES')
    SERVER_COMMANDS = get_json('./config/config.json', 'SERVER_COMMANDS')


cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load('./config/auto.json', cfg)