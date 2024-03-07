import time
from PySide6.QtWidgets import QApplication, QHBoxLayout, QFrame
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QProcess, QSize
from qfluentwidgets import MSFluentWindow, SubtitleLabel, setFont, NavigationItemPosition, setTheme, Theme, InfoBar, InfoBarPosition, SplashScreen
from qfluentwidgets import FluentIcon as FIF
from app.home_interface import Home
from app.setting_interface import Setting
from app.src.common.config import cfg
from app.src.common.check_update import checkUpdate


class TempPage(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))

class MainApp(MSFluentWindow):
    def __init__(self):
        super().__init__()
        setTheme(cfg.themeMode.value)
        self.initMainWindow()

        self.homeInterface = Home('Home Interface', self)
        self.commandInterface = TempPage('Command Interface', self)
        self.downloadInterface = TempPage('Download Interface', self)
        self.settingInterface = Setting('Setting Interface', self)

        self.initNavigation()

        # 加载界面结束(3)
        self.splashScreen.finish()
        
        checkUpdate(self)

    def changeTheme(self):
        if cfg.themeMode.value == Theme.DARK:
            setTheme(Theme.LIGHT)
            cfg.themeMode.value = Theme.LIGHT
            cfg.save()
        else:
            setTheme(Theme.DARK)
            cfg.themeMode.value = Theme.DARK
            cfg.save()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页', FIF.HOME_FILL)
        self.addSubInterface(self.commandInterface, FIF.COMMAND_PROMPT, '命令', FIF.COMMAND_PROMPT)
        self.addSubInterface(self.downloadInterface, FIF.DOWNLOAD, '下载', FIF.DOWNLOAD)
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
        self.setResizeEnabled(False)
        self.setWindowTitle(cfg.APP_NAME)
        self.setFixedSize(1280, 768)
        self.setWindowIcon(QIcon('./app/src/image/icon.ico'))

        # 启用加载界面(1)
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(128, 128))
        self.splashScreen.raise_()

        # 居中显示
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        # 显示加载界面(2)
        self.show()
        QApplication.processEvents()
        time.sleep(1)   #别问 , 问就是没充VIP

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