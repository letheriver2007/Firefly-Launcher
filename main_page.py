import sys
from PySide6.QtWidgets import QApplication, QHBoxLayout, QFrame
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt, QLocale
from qfluentwidgets import MSFluentWindow, SubtitleLabel, setFont, NavigationItemPosition, setTheme, Theme, FluentTranslator
from qfluentwidgets import FluentIcon as FIF
from config import cfg
from home_page import Home
from setting_page import Setting
from config import cfg

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

        self.homeInterface = Home('Home Interface', self)
        self.commandInterface = TempPage('Command Interface', self)
        self.downloadInterface = TempPage('Download Interface', self)
        self.settingInterface = Setting('Setting Interface', self)

        self.initNavigation()
        self.initMainWindow()
        setTheme(cfg.themeMode.value)


    def changeTheme(self):
        if cfg.themeMode.value == Theme.LIGHT:
            setTheme(Theme.DARK)
            cfg.themeMode.value = Theme.DARK
            cfg.save()
        elif cfg.themeMode.value == Theme.DARK:
            setTheme(Theme.LIGHT)
            cfg.themeMode.value = Theme.LIGHT
            cfg.save()
        else:
            setTheme(Theme.DARK)    # config丢失
            cfg.themeMode.value = Theme.DARK
            cfg.save()


    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页', FIF.HOME_FILL)
        self.addSubInterface(self.commandInterface, FIF.COMMAND_PROMPT, '命令', FIF.COMMAND_PROMPT)
        self.addSubInterface(self.downloadInterface, FIF.DOWNLOAD, '下载', FIF.DOWNLOAD)
        self.navigationInterface.addItem(
            routeKey='theme',
            icon=FIF.VIEW,
            text='主题',
            onClick=self.changeTheme,
            selectable=False,
            position=NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', FIF.SETTING, NavigationItemPosition.BOTTOM)
        #font = QFont("Microsoft YaHei UI")
        #self.setFont(font)


    # 居中显示窗口
    def initMainWindow(self):
        self.setWindowTitle('Firefly Launcher')
        self.setFixedSize(1280, 768)
        icon = QIcon('./src/image/icon.ico')
        self.setWindowIcon(icon)
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)


app = QApplication(sys.argv)
translator = FluentTranslator(QLocale(QLocale.Chinese, QLocale.China))
app.installTranslator(translator)
#app.setFont(QFont("SDK_SC_Web"))
window = MainApp()
window.show()
sys.exit(app.exec())
