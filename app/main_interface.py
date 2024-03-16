import os
import sys
import glob
import random
import hashlib
import subprocess
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from qfluentwidgets import MSFluentWindow, NavigationItemPosition, setTheme, Theme, InfoBar, InfoBarPosition, SplashScreen
from qfluentwidgets import FluentIcon as FIF
from app.home_interface import Home
from app.download_interface import Download
from app.config_interface import Config
from app.toolkit_interface import Toolkit
from app.command_interface import Command
from app.setting_interface import Setting
from app.module.config import cfg
from app.module.check_update import checkUpdate
from app.component.message_login import MessageLogin


class Main(MSFluentWindow):
    def __init__(self):
        super().__init__()
        setTheme(cfg.themeMode.value)
        self.initMainWindow()

        self.homeInterface = Home('Home Interface', self)
        self.downloadInterface = Download('Download Interface', self)
        self.configInterface = Config('Config Interface', self)
        self.toolkitInterface = Toolkit('Toolkit Interface', self)
        self.commandInterface = Command('Command Interface', self)
        self.settingInterface = Setting('Setting Interface', self)

        self.initNavigation()
        self.checkFont()
        # 加载界面结束
        self.splashScreen.finish()
        checkUpdate(self)
        if cfg.useLogin.value:
            self.incorrect_count = 1
            self.w = MessageLogin(self)
            self.w.show()
            self.w.passwordEntered.connect(self.checkLogin)
        else:
            if cfg.useAudio.value:
                self.mediaPlay('success')
    
    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页', FIF.HOME_FILL)
        self.addSubInterface(self.downloadInterface, FIF.DOWNLOAD, '下载', FIF.DOWNLOAD)
        self.addSubInterface(self.configInterface, FIF.SEARCH_MIRROR, '配置', FIF.SEARCH_MIRROR)
        self.addSubInterface(self.toolkitInterface, FIF.APPLICATION, '工具', FIF.APPLICATION)
        self.addSubInterface(self.commandInterface, FIF.COMMAND_PROMPT, '命令', FIF.COMMAND_PROMPT)
        self.navigationInterface.addItem(
            routeKey='theme',
            icon=FIF.CONSTRACT,
            text='主题',
            onClick=self.changeTheme,
            selectable=False,
            position=NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', FIF.SETTING, NavigationItemPosition.BOTTOM)

    def initMainWindow(self):
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
        self.splashScreen.setIconSize(QSize(128, 128))
        self.splashScreen.raise_()

        # 居中显示
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        # 显示加载界面
        self.show()
        QApplication.processEvents()

    def checkFont(self):
        font_path = os.path.expandvars('%UserProfile%\AppData\Local\Microsoft\Windows\Fonts\zh-cn.ttf')
        if not os.path.exists(font_path):
            subprocess.run('cd src/patch/font && start zh-cn.ttf', shell=True)
            sys.exit()

    def checkLogin(self, password):
        md5_hash = hashlib.md5(password.encode()).hexdigest()[8:24].upper()
        # if md5_hash == 'EE1FC4FB7AD2BE1C':
        if password == '':
            InfoBar.success(
                title='登录成功',
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
                title=f'密码错误{self.incorrect_count}次',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            self.incorrect_count += 1
            if cfg.useAudio.value:
                self.mediaPlay('error')

    def changeTheme(self):
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
            InfoBar.warning(
                title=f'检测到新版本: {info}',
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
        elif status == 1:
            InfoBar.success(
                title=f'当前是最新版本: {info}',
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
        elif status == 0:
            InfoBar.error(
                title=f'检测更新失败: {info}',
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
    
    def mediaPlay(self, status):
        try:
            self.player = QMediaPlayer()
            self.audioOutput = QAudioOutput()
            self.player.setAudioOutput(self.audioOutput)
            self.audioOutput.setVolume(1)
            audio_list = glob.glob(f'src\\audio\\{status}\\*.wav')
            audio_play = QUrl.fromLocalFile(random.choice(audio_list))
            self.player.setSource(audio_play)
            self.player.play()
        except:
            InfoBar.error(
                title='未找到语音，请重新下载！',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )