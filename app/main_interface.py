import sys
import glob
import random
import winreg
import hashlib
import subprocess
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from qfluentwidgets import (MSFluentWindow, NavigationItemPosition, setTheme, Theme, InfoBar,
                            InfoBarPosition, SplashScreen, HyperlinkButton, InfoBarIcon, FluentIcon)
from app.home_interface import Home
from app.launcher_interface import Launcher
from app.environment_interface import Environment
from app.lunarcore_interface import LunarCore
from app.proxy_interface import Proxy
from app.setting_interface import Setting
from app.model.config import cfg
from app.model.check_update import checkUpdate
from app.model.login_card import MessageLogin


class Main(MSFluentWindow):
    def __init__(self):
        super().__init__()
        setTheme(cfg.themeMode.value)

        self.__initMainWindow()
        self.__initNavigation()
        self.handleFontCheck()

        # 加载界面结束
        self.splashScreen.finish()

        checkUpdate(self)
        if cfg.useLogin.value:
            self.incorrect_count = 1
            self.login_card = MessageLogin(self)
            self.login_card.show()
            self.login_card.passwordEntered.connect(self.handleLogin)
        else:
            if cfg.useAudio.value:
                self.handleMideaPlay('success')

    def __initNavigation(self):
        self.homeInterface = Home('HomeInterface', self)
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, self.tr('主页'), FluentIcon.HOME_FILL)
        self.launcherInterface = Launcher('LauncherInterface', self)
        self.addSubInterface(self.launcherInterface, FluentIcon.PLAY, self.tr('启动器'), FluentIcon.PLAY)
        self.environmentInterface = Environment('EnvironmentInterface', self)
        self.addSubInterface(self.environmentInterface, FluentIcon.DICTIONARY, self.tr('环境'), FluentIcon.DICTIONARY)
        self.lunarcoreInterface = LunarCore('LunarCoreInterface', self)
        self.addSubInterface(self.lunarcoreInterface, FluentIcon.CAFE, 'LunarCore', FluentIcon.CAFE)
        self.proxyInterface = Proxy('ProxyInterface', self)
        self.addSubInterface(self.proxyInterface, FluentIcon.CERTIFICATE, self.tr('代理'), FluentIcon.CERTIFICATE)

        self.navigationInterface.addItem(
            routeKey='theme',
            icon=FluentIcon.CONSTRACT,
            text=self.tr('主题'),
            onClick=self.handleThemeChanged,
            selectable=False,
            position=NavigationItemPosition.BOTTOM
        )

        self.settingInterface = Setting('SettingInterface', self)
        self.addSubInterface(self.settingInterface, FluentIcon.SETTING, self.tr('设置'), FluentIcon.SETTING,
                             NavigationItemPosition.BOTTOM)

    def __initMainWindow(self):
        self.titleBar.maxBtn.setHidden(True)
        self.titleBar.maxBtn.setDisabled(True)
        self.titleBar.setDoubleClickEnabled(False)
        self.setResizeEnabled(False)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        self.setWindowTitle(cfg.APP_NAME)
        self.setFixedSize(1280, 768)
        self.setWindowIcon(QIcon('./src/image/icon.ico'))

        # 启用加载界面
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(200, 200))
        self.splashScreen.raise_()

        # 居中显示
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        # 显示加载界面
        self.show()
        QApplication.processEvents()

    def handleFontCheck(self):
        isSetupFont = False
        registry_keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows NT\CurrentVersion\Fonts")
        ]
        try:
            for hkey, sub_key in registry_keys:
                reg = winreg.ConnectRegistry(None, hkey)
                reg_key = winreg.OpenKey(reg, sub_key)
                i = 0
                while True:
                    try:
                        name, data, types = winreg.EnumValue(reg_key, i)
                        if cfg.APP_FONT.lower() in name.lower():
                            isSetupFont = True
                        i += 1
                    except OSError:
                        break
                winreg.CloseKey(reg_key)
        except Exception as e:
            InfoBar.error(
                title=self.tr('检查字体失败: '),
                content=str(e),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )

        if not isSetupFont:
            subprocess.run('cd src/patch/font && start zh-cn.ttf', shell=True)
            sys.exit()

    def handleLogin(self, password):
        md5_hash = hashlib.md5(password.encode()).hexdigest()[8:24].upper()
        if md5_hash == 'EE1FC4FB7AD2BE1C':
            InfoBar.success(
                title=self.tr('登录成功'),
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
            if cfg.useAudio.value:
                self.mediaPlay('success')
            self.w.close()
        else:
            InfoBar.error(
                title=self.tr('密码错误!'),
                content=self.tr('次数: ') + self.incorrect_count,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            self.incorrect_count += 1
            if cfg.useAudio.value:
                self.mediaPlay('error')

    def handleThemeChanged(self):
        if cfg.themeMode.value == Theme.DARK:
            setTheme(Theme.LIGHT)
            cfg.themeMode.value = Theme.LIGHT
            cfg.save()
        else:
            setTheme(Theme.DARK)
            cfg.themeMode.value = Theme.DARK
            cfg.save()

    def handleUpdate(self, status, info):
        if status == 2:
            self.update_button = HyperlinkButton(cfg.URL_LATEST, self.tr('前往下载'))
            update_info = InfoBar(
                icon=InfoBarIcon.WARNING,
                title=self.tr('检测到新版本: ') + info,
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=-1,
                parent=self
            )
            update_info.addWidget(self.update_button)
            update_info.show()
        elif status == 1:
            InfoBar.success(
                title=self.tr('当前是最新版本: ') + info,
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
        elif status == 0:
            InfoBar.error(
                title=self.tr('检测更新失败: ') + info,
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )

    def handleMideaPlay(self, status):
        try:
            self.player = QMediaPlayer()
            self.audioOutput = QAudioOutput()
            self.player.setAudioOutput(self.audioOutput)
            self.audioOutput.setVolume(1)
            audio_list = glob.glob(f'src\\audio\\{status}\\*.wav')
            audio_play = QUrl.fromLocalFile(random.choice(audio_list))
            self.player.setSource(audio_play)
            self.player.play()
        except Exception as e:
            InfoBar.error(
                title=self.tr('未找到语音, 请重新下载!'),
                content=str(e),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
