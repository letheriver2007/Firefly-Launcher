import sys
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QDesktopServices, QFont
from PySide6.QtCore import Qt, QUrl, QSize, QProcess
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (Pivot, qrouter, ScrollArea, SettingCardGroup, CustomColorSettingCard, PushButton,
                            setThemeColor, PrimaryPushSettingCard, TitleLabel, SubtitleLabel, setCustomStyleSheet,
                            SwitchSettingCard, InfoBar, InfoBarPosition)
from src.module.config import cfg
from src.component.style_sheet import StyleSheet
from src.module.check_update import checkUpdate


class Setting(ScrollArea):
    Nav = Pivot
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setObjectName(text.replace(' ', '-'))
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)

        # 栏定义
        self.pivot = self.Nav(self)
        self.stackedWidget = QStackedWidget(self)

        # 添加项 , 名字会隐藏(1)
        self.PersonalInterface = SettingCardGroup('程序', self.scrollWidget)
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            '主题色',
            '默认流萤主题色，开拓者你不会改的吧？'
        )
        self.updateOnStartUpCard = PrimaryPushSettingCard(
            '检查更新',
            FIF.UPDATE,
            '手动检查更新',
            '当前版本 : '+ cfg.APP_VERSION
        )
        self.restartCard = PrimaryPushSettingCard(
            '重启程序',
            FIF.ROTATE,
            '重启程序',
            '无奖竞猜，存在即合理'
        )
        self.QuickInterface = SettingCardGroup('配置', self.scrollWidget)
        self.settingConfigCard = PrimaryPushSettingCard(
            '打开文件',
            FIF.LABEL,
            '设置配置',
            '自定义设置选项'
        )
        self.personalConfigCard = PrimaryPushSettingCard(
            '打开文件',
            FIF.LABEL,
            '个性化配置',
            '自定义个性化选项'
        )
        self.ProxyInterface = SettingCardGroup('代理', self.scrollWidget)
        self.proxyCard = SwitchSettingCard(
            FIF.CERTIFICATE,
            '使用代理端口',
            '启用代理，在配置文件里更改地址',
            configItem=cfg.proxyStatus
        )
        self.chinaCard = SwitchSettingCard(
            FIF.CALORIES,
            '使用国内镜像',
            '为Github下载启用国内镜像站链接',
            configItem=cfg.chinaStatus
        )
        self.noproxyCard = PrimaryPushSettingCard(
            '重置',
            FIF.POWER_BUTTON,
            '重置代理',
            '重置部分服务端未关闭的代理'
        )

        self.__initWidget()

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)     # 水平滚动条关闭
        self.setViewportMargins(20, 0, 20, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)    # 必须设置！！！
        
        # 使用qss设置样式
        self.scrollWidget.setObjectName('scrollWidget')
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        # 项绑定到栏目
        self.PersonalInterface.addSettingCard(self.themeColorCard)
        self.PersonalInterface.addSettingCard(self.updateOnStartUpCard)
        self.PersonalInterface.addSettingCard(self.restartCard)
        self.ProxyInterface.addSettingCard(self.proxyCard)
        self.ProxyInterface.addSettingCard(self.chinaCard)
        self.ProxyInterface.addSettingCard(self.noproxyCard)

        # 目前无法做到导航栏各个页面独立分组 , 故隐藏组标题
        self.QuickInterface.titleLabel.setHidden(True)
        self.PersonalInterface.titleLabel.setHidden(True)
        self.ProxyInterface.titleLabel.setHidden(True)

        # 栏绑定界面
        self.addSubInterface(self.PersonalInterface,'PersonalInterface','程序', icon=FIF.SETTING)
        self.addSubInterface(self.ProxyInterface, 'ProxyInterface','代理', icon=FIF.CERTIFICATE)
        self.AboutInterface = About('About Interface', self)
        self.addSubInterface(self.AboutInterface, 'AboutInterface','关于', icon=FIF.INFO)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(28)
        self.vBoxLayout.setContentsMargins(0, 10, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.PersonalInterface)
        self.pivot.setCurrentItem(self.PersonalInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.PersonalInterface.objectName())
        
    def __connectSignalToSlot(self):
        self.themeColorCard.colorChanged.connect(lambda c: setThemeColor(c, lazy=True))
        self.updateOnStartUpCard.clicked.connect(lambda: checkUpdate(self.parent))
        self.restartCard.clicked.connect(self.restart_application)
        self.proxyCard.checkedChanged.connect(self.proxy_changed)
        self.chinaCard.checkedChanged.connect(self.china_changed)
        self.noproxyCard.clicked.connect(self.disable_global_proxy)

    def addSubInterface(self, widget: QLabel, objectName, text, icon=None):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            icon=icon,
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())
        qrouter.push(self.stackedWidget, widget.objectName())

    def restart_application(self):
        current_process = QProcess()
        current_process.startDetached(sys.executable, sys.argv)
        sys.exit()

    def proxy_changed(self):
        if cfg.proxyStatus.value == True:
            InfoBar.success(
                title=f'已使用代理端口{cfg.PROXY_PORT},可在配置更改',
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
        self.china_proxy_check()

    def china_changed(self):
        if cfg.chinaStatus.value == True:
            InfoBar.success(
                title='国内镜像已开启！',
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
        self.china_proxy_check()
                
    def china_proxy_check(self):
        if cfg.chinaStatus.value == True and cfg.proxyStatus.value == True:
            InfoBar.warning(
                    title="已同时启用代理端口和国内镜像,默认使用国内镜像！",
                    content="",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=1000,
                    parent=self
                )

    def disable_global_proxy(self):
        try:
            if cfg.proxyStatus.value:
                subprocess.run('reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(f'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /d "127.0.0.1:{cfg.PROXY_PORT}" /f', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.run('reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run('reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /d "" /f', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            InfoBar.success(
                title=f'全局代理已更改！',
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
        except:
            InfoBar.error(
                title=f'全局代理关闭失败！',
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )


class About(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        
        main_layout = QVBoxLayout(self)
        self.setObjectName(text.replace(' ', '-'))
        
        image_layout = QVBoxLayout()
        image_widget = RoundedImageWidget("./src/image/bg_about.png")
        image_layout.addWidget(image_widget)
        image_widget.setFixedSize(1080, 540)
        image_layout.setAlignment(Qt.AlignHCenter)

        # APP信息
        info_layout = QVBoxLayout()
        self.info_name = TitleLabel(cfg.APP_NAME)
        self.info_version = SubtitleLabel(cfg.APP_VERSION)
        self.info_name.setFont(QFont(f'{cfg.APP_FONT}', 35))
        self.info_version.setFont(QFont(f'{cfg.APP_FONT}', 20))
        self.info_name.setContentsMargins(0, 25, 0, 0)
        self.info_version.setContentsMargins(0, 10, 0, 20)
        info_layout.addWidget(self.info_name, alignment=Qt.AlignHCenter)
        info_layout.addWidget(self.info_version, alignment=Qt.AlignHCenter)

        # Github链接
        info_button_layout = QHBoxLayout()
        link_writer = PushButton(FIF.HOME, '   作者主页')
        link_repo = PushButton(FIF.GITHUB, '   Github项目')
        link_releases = PushButton(FIF.MESSAGE, '   版本发布')
        link_issues = PushButton(FIF.HELP, '   反馈交流')

        for link_button_name in ['link_writer', 'link_repo', 'link_releases', 'link_issues']:
            eval(link_button_name).setFixedSize(270, 70)
            eval(link_button_name).setIconSize(QSize(18, 18))
            eval(link_button_name).setFont(QFont(f'{cfg.APP_FONT}', 12))
            setCustomStyleSheet(eval(link_button_name), 'PushButton{border-radius: 12px}', 'PushButton{border-radius: 12px}')
            info_button_layout.addWidget(eval(link_button_name))
            eval(link_button_name).clicked.connect(eval('self.' + link_button_name))

        main_layout.addLayout(image_layout)
        main_layout.addLayout(info_layout)
        main_layout.addLayout(info_button_layout)

    def link_writer(self):
        QDesktopServices.openUrl(QUrl(cfg.URL_WRITER))
    def link_repo(self):
        QDesktopServices.openUrl(QUrl(cfg.URL_REPO))
    def link_releases(self):
        QDesktopServices.openUrl(QUrl(cfg.URL_RELEASES))
    def link_issues(self):
        QDesktopServices.openUrl(QUrl(cfg.URL_ISSUES))


class RoundedImageWidget(QWidget):
    def __init__(self, image_path: str, parent=None):
        super().__init__(parent=parent)
        self.image_path = image_path

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pixmap = QPixmap(self.image_path)

        path = QPainterPath()
        path.addRoundedRect(self.rect(), 20, 20)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, self.width(), self.height(), pixmap)