import json
from qfluentwidgets import qconfig, QConfig, Theme, ConfigItem, BoolValidator

def get_json(file_path, key):
    with open(f'{file_path}', 'r') as file:
        json_data = json.load(file)
        return json_data[f"{key}"]


class Config(QConfig):
    autoCopy = ConfigItem("Function", "AutoCopy", True, BoolValidator())
    useLogin = ConfigItem("Function", "UseLogin", True, BoolValidator())
    useAudio = ConfigItem("Function", "UseAudio", True, BoolValidator())
    randomHomeBg = ConfigItem("Function", "RandomHomeBg", True, BoolValidator())
    proxyStatus = ConfigItem("Proxy", "ProxyStatus", False, BoolValidator())
    chinaStatus = ConfigItem("Proxy", "ChinaStatus", True, BoolValidator())

    APP_NAME = "Firefly Launcher"
    APP_VERSION = get_json('./config/version.json', 'version')
    APP_FONT = "SDK_SC_Web"

    URL_WRITER = "https://github.com/letheriver2007"
    URL_REPO = "https://github.com/letheriver2007/Firefly-Launcher"
    URL_RELEASES = "https://github.com/letheriver2007/Firefly-Launcher/releases"
    URL_ISSUES = "https://github.com/letheriver2007/Firefly-Launcher/issues"

    DOWNLOAD_COMMANDS_LAUNCHER = ('https://github.com/letheriver2007/Firefly-Launcher/releases/download/v1.3.0/Firefly-Launcher.zip')
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

    DOWNLOAD_COMMANDS_LAUNCHER_MIRROR = ('https://hub.gitmirror.com/https://github.com/letheriver2007/Firefly-Launcher/releases/download/v1.3.0/Firefly-Launcher.zip')
    DOWNLOAD_COMMANDS_AUDIO_MIRROR = ('https://gitee.com/letheriver2007/Firefly-Launcher-Res.git src/audio')
    DOWNLOAD_COMMANDS_GIT_MIRROR = ('https://cdn.npmmirror.com/binaries/git-for-windows/v2.44.0.windows.1/Git-2.44.0-64-bit.exe')
    DOWNLOAD_COMMANDS_JAVA_MIRROR = ('https://d6.injdk.cn/oraclejdk/17/jdk-17_windows-x64_bin.msi')
    DOWNLOAD_COMMANDS_MONGODB_MIRROR = ('https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.6-signed.msi')
    DOWNLOAD_COMMANDS_LUNARCORE_MIRROR = ('https://gitee.com/Letheriver2007/Firefly-Launcher-Res.git server/LunarCore')
    DOWNLOAD_COMMANDS_LUNARCORE_RES_MIRROR = ('https://gitee.com/Letheriver2007/Firefly-Launcher-Res.git server/LunarCore/resources')
    DOWNLOAD_COMMANDS_FIDDLER_MIRROR = ('https://gitee.com/Letheriver2007/Firefly-Launcher-Res.git tool/fiddler')
    DOWNLOAD_COMMANDS_MITMDUMP_MIRROR = ('https://gitee.com/Letheriver2007/Firefly-Launcher-Res.git tool/mitmdump')

    PROXY_PORT = get_json('./config/config.json', 'PROXY_PORT')
    SERVER_NAMES = get_json('./config/config.json', 'SERVER_NAMES')
    SERVER_COMMANDS = get_json('./config/config.json', 'SERVER_COMMANDS')


cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load('./config/auto.json', cfg)