import os
import json
from enum import Enum
from PySide6.QtCore import QLocale
from qfluentwidgets import qconfig, QConfig, Theme, ConfigItem, BoolValidator, OptionsValidator, OptionsConfigItem, ConfigSerializer

def get_json(file_path, key):
    with open(f'{file_path}', 'r') as file:
        json_data = json.load(file)
        return json_data[f"{key}"]

def get_version_type(version):
    if not os.path.exists('firefly-launcher.py'):
        return f'{version} REL'
    else:
        return f'{version} DEV'


class Language(Enum):
    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Chinese, QLocale.Taiwan)
    ENGLISH = QLocale(QLocale.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"
    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


class Config(QConfig):
    ############### APP CONFIG ###############
    dpiScale = OptionsConfigItem(
        "Style", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    language = OptionsConfigItem(
        "Style", "Language", Language.AUTO, OptionsValidator(Language), LanguageSerializer(), restart=True)
    autoCopy = ConfigItem("Function", "AutoCopy", True, BoolValidator())
    useLogin = ConfigItem("Function", "UseLogin", False, BoolValidator())
    useAudio = ConfigItem("Function", "UseAudio", True, BoolValidator())
    proxyStatus = ConfigItem("Proxy", "ProxyStatus", True, BoolValidator())
    chinaStatus = ConfigItem("Proxy", "ChinaStatus", False, BoolValidator())
    useRemote = ConfigItem("Command", "useRemote", False, BoolValidator())

    APP_NAME = "Firefly Launcher(Letheriver2007)"
    APP_VERSION = get_version_type(get_json('./config/version.json', 'APP_VERSION'))
    APP_FONT = "SDK_SC_Web"
    
    ############### DOWNLOAD CONFIG ###############
    URL_WRITER = "https://github.com/letheriver2007"
    URL_REPO = "https://github.com/letheriver2007/Firefly-Launcher"
    URL_RELEASES = "https://github.com/letheriver2007/Firefly-Launcher/releases"
    URL_ISSUES = "https://github.com/letheriver2007/Firefly-Launcher/issues"

    DOWNLOAD_COMMANDS_AUDIO = ('https://github.com/letheriver2007/Firefly-Launcher-Res.git src/audio')
    DOWNLOAD_COMMANDS_GIT = ('https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.exe')
    DOWNLOAD_COMMANDS_JAVA = ('https://download.oracle.com/java/17/latest/jdk-17_windows-x64_bin.msi')
    DOWNLOAD_COMMANDS_MONGODB = ('https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.6-signed.msi')
    DOWNLOAD_COMMANDS_LUNARCORE = ('https://github.com/Melledy/LunarCore.git server/LunarCore')
    DOWNLOAD_COMMANDS_LUNARCORE_RES_1 = ('https://github.com/Dimbreath/StarRailData.git server/LunarCore/resources')
    DOWNLOAD_COMMANDS_LUNARCORE_RES_2 = ('https://gitlab.com/Melledy/LunarCore-Configs.git server/LunarCore/resources/Config/Config && '
    'move "server/LunarCore/resources/Config/Config/Config/ConfigSummonUnit" "server/LunarCore/resources/Config/ConfigSummonUnit" && '
    'xcopy /s /e /y "server/LunarCore/resources/Config/Config/Config/LevelOutput" "server/LunarCore/resources/Config/LevelOutput" && '
    'rmdir /s /q "server/LunarCore/resources/Config/Config"')
    DOWNLOAD_COMMANDS_FIDDLER = ('https://github.com/Letheriver2007/Firefly-Launcher-Res.git tool/fiddler')
    DOWNLOAD_COMMANDS_MITMDUMP = ('https://github.com/Letheriver2007/Firefly-Launcher-Res.git tool/mitmdump')

    DOWNLOAD_COMMANDS_AUDIO_MIRROR = ('https://gitee.com/letheriver2007/Firefly-Launcher-Res.git src/audio')
    DOWNLOAD_COMMANDS_GIT_MIRROR = ('https://cdn.npmmirror.com/binaries/git-for-windows/v2.44.0.windows.1/Git-2.44.0-64-bit.exe')
    DOWNLOAD_COMMANDS_JAVA_MIRROR = ('https://d6.injdk.cn/oraclejdk/17/jdk-17_windows-x64_bin.msi')
    DOWNLOAD_COMMANDS_MONGODB_MIRROR = ('https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.6-signed.msi')
    DOWNLOAD_COMMANDS_LUNARCORE_MIRROR = ('https://gitee.com/kenny-pk/LunarCore.git server/LunarCore')
    DOWNLOAD_COMMANDS_LUNARCORE_RES_MIRROR = ('https://gitee.com/Letheriver2007/Firefly-Launcher-Res.git server/LunarCore/resources')
    DOWNLOAD_COMMANDS_FIDDLER_MIRROR = ('https://gitee.com/Letheriver2007/Firefly-Launcher-Res.git tool/fiddler')
    DOWNLOAD_COMMANDS_MITMDUMP_MIRROR = ('https://gitee.com/Letheriver2007/Firefly-Launcher-Res.git tool/mitmdump')

    ############### SERVER CONFIG ###############
    SERVER_NAMES = get_json('./config/config.json', 'SERVER_NAMES')
    SERVER_COMMANDS = get_json('./config/config.json', 'SERVER_COMMANDS')


cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load('./config/auto.json', cfg)