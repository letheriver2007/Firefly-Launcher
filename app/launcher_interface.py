from PySide6.QtWidgets import QWidget, QLabel, QStackedWidget, QVBoxLayout
from PySide6.QtCore import Qt
from qfluentwidgets import Pivot, qrouter, ScrollArea, PrimaryPushSettingCard, HyperlinkButton, FluentIcon
from app.model.style_sheet import StyleSheet
from app.model.setting_card import SettingCard, SettingCardGroup
from app.model.download_process import SubDownloadCMD
from app.model.config import open_file


class HyperlinkCard_Launcher(SettingCard):
    def __init__(self, title, content=None, icon=FluentIcon.LINK):
        super().__init__(icon, title, content)
        self.linkButton_launcher = HyperlinkButton('https://github.com/letheriver2007/Firefly-Launcher',
                                                   'Firefly-Launcher', self)
        self.linkButton_audio = HyperlinkButton('https://github.com/letheriver2007/Firefly-Launcher-Res',
                                                'Firefly-Launcher-Res', self)
        self.hBoxLayout.addWidget(self.linkButton_launcher, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_audio, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)


class Launcher(ScrollArea):
    Nav = Pivot

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setObjectName(text)
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)

        # 栏定义
        self.pivot = self.Nav(self)
        self.stackedWidget = QStackedWidget(self)

        # 添加项
        self.LauncherDownloadInterface = SettingCardGroup(self.scrollWidget)
        self.LauncherRepoCard = HyperlinkCard_Launcher(
            self.tr('项目仓库'),
            self.tr('打开Firefly-Launcher相关项目仓库')
        )
        self.AudioDownloadCard = PrimaryPushSettingCard(
            self.tr('下载'),
            FluentIcon.DOWNLOAD,
            'Firefly-Launcher-Audio',
            self.tr('下载流萤音频文件')
        )
        self.ConfigInterface = SettingCardGroup(self.scrollWidget)
        self.settingConfigCard = PrimaryPushSettingCard(
            self.tr('打开文件'),
            FluentIcon.LABEL,
            self.tr('启动器设置'),
            self.tr('自定义启动器配置')
        )

        self.__initWidget()

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 水平滚动条关闭
        self.setViewportMargins(20, 0, 20, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)  # 必须设置！！！

        # 使用qss设置样式
        self.scrollWidget.setObjectName('scrollWidget')
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        # 项绑定到栏目
        self.LauncherDownloadInterface.addSettingCard(self.LauncherRepoCard)
        self.LauncherDownloadInterface.addSettingCard(self.AudioDownloadCard)
        self.ConfigInterface.addSettingCard(self.settingConfigCard)

        # 栏绑定界面
        self.addSubInterface(self.LauncherDownloadInterface, 'LauncherDownloadInterface', self.tr('下载'),
                             icon=FluentIcon.DOWNLOAD)
        self.addSubInterface(self.ConfigInterface, 'configInterface', self.tr('配置'), icon=FluentIcon.EDIT)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 10, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.LauncherDownloadInterface)
        self.pivot.setCurrentItem(self.LauncherDownloadInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.LauncherDownloadInterface.objectName())

    def __connectSignalToSlot(self):
        SubDownloadCMDSelf = SubDownloadCMD(self)
        self.AudioDownloadCard.clicked.connect(lambda: SubDownloadCMDSelf.handleDownloadStarted('audio'))
        self.settingConfigCard.clicked.connect(lambda: open_file(self, 'config/config.json'))

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
