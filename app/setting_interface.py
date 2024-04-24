import sys
import json
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QDesktopServices, QFont, QIntValidator
from PySide6.QtCore import Qt, QUrl, QSize, QProcess, Signal
from qfluentwidgets import (Pivot, qrouter, ScrollArea, CustomColorSettingCard, PushButton,
                            PrimaryPushSettingCard, setCustomStyleSheet, SwitchSettingCard,
                            ComboBoxSettingCard, LineEdit, PrimaryPushButton, FluentIcon, setThemeColor)
from app.model.setting_card import SettingCard, SettingCardGroup
from app.model.style_sheet import StyleSheet
from app.model.check_update import checkUpdate
from app.model.config import cfg, get_json, Info


class LineEditSettingCard_Port(SettingCard):
    set_port = Signal()

    def __init__(self, title, icon=FluentIcon.SETTING):
        super().__init__(icon, title)
        self.port_edit = LineEdit(self)
        self.port_edit.setFixedWidth(85)
        self.port_edit.setPlaceholderText(self.tr("端口"))
        self.port_edit.setValidator(QIntValidator(1, 99999, self))
        self.set_port_button = PrimaryPushButton(self.tr('设置'), self)

        self.hBoxLayout.addWidget(self.port_edit, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.set_port_button, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.set_port_button.clicked.connect(self.set_port)


class Setting(ScrollArea):
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
        self.PersonalInterface = SettingCardGroup(self.scrollWidget)
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor,
            FluentIcon.PALETTE,
            self.tr('主题色'),
            self.tr('默认流萤主题色，开拓者你不会改的吧?')
        )
        self.zoomCard = ComboBoxSettingCard(
            cfg.dpiScale,
            FluentIcon.ZOOM,
            self.tr("DPI调整"),
            self.tr("调整全局缩放"),
            texts=["100%", "125%", "150%", "175%", "200%", self.tr("跟随系统设置")]
        )
        self.languageCard = ComboBoxSettingCard(
            cfg.language,
            FluentIcon.LANGUAGE,
            self.tr('语言'),
            self.tr('设置UI界面显示语言'),
            texts=['简体中文', '繁體中文', 'English', self.tr('跟随系统设置')]
        )
        self.updateOnStartUpCard = PrimaryPushSettingCard(
            self.tr('检查更新'),
            FluentIcon.UPDATE,
            self.tr('手动检查更新'),
            self.tr('当前版本 : ') + cfg.APP_VERSION
        )
        self.restartCard = PrimaryPushSettingCard(
            self.tr('重启程序'),
            FluentIcon.ROTATE,
            self.tr('重启程序'),
            self.tr('无奖竞猜，存在即合理')
        )
        self.FunctionInterface = SettingCardGroup(self.scrollWidget)
        self.autoCopyCard = SwitchSettingCard(
            FluentIcon.COPY,
            self.tr('命令自动复制'),
            self.tr('选择命令时，自动复制命令到剪贴板'),
            configItem=cfg.autoCopy
        )
        self.useLoginCard = SwitchSettingCard(
            FluentIcon.PENCIL_INK,
            self.tr('启用登录功能'),
            self.tr('使用自定义登陆彩蛋'),
            configItem=cfg.useLogin
        )
        self.useAudioCard = SwitchSettingCard(
            FluentIcon.MUSIC,
            self.tr('启用流萤语音'),
            self.tr('使用随机流萤语音彩蛋'),
            configItem=cfg.useAudio
        )
        self.ProxyInterface = SettingCardGroup(self.scrollWidget)
        self.proxyCard = SwitchSettingCard(
            FluentIcon.CERTIFICATE,
            self.tr('使用代理端口'),
            self.tr('启用代理，在配置文件里更改地址'),
            configItem=cfg.proxyStatus
        )
        self.proxyPortCard = LineEditSettingCard_Port(
            self.tr('代理端口')
        )
        self.chinaCard = SwitchSettingCard(
            FluentIcon.CALORIES,
            self.tr('使用国内镜像'),
            self.tr('为Github下载启用国内镜像站链接'),
            configItem=cfg.chinaStatus
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
        self.__initInfo()
        self.__connectSignalToSlot()

    def __initLayout(self):
        # 项绑定到栏目
        self.PersonalInterface.addSettingCard(self.themeColorCard)
        self.PersonalInterface.addSettingCard(self.zoomCard)
        self.PersonalInterface.addSettingCard(self.languageCard)
        self.PersonalInterface.addSettingCard(self.updateOnStartUpCard)
        self.PersonalInterface.addSettingCard(self.restartCard)
        self.FunctionInterface.addSettingCard(self.autoCopyCard)
        self.FunctionInterface.addSettingCard(self.useLoginCard)
        self.FunctionInterface.addSettingCard(self.useAudioCard)
        self.ProxyInterface.addSettingCard(self.proxyCard)
        self.ProxyInterface.addSettingCard(self.proxyPortCard)
        self.ProxyInterface.addSettingCard(self.chinaCard)

        # 栏绑定界面
        self.addSubInterface(self.PersonalInterface, 'PersonalInterface', self.tr('程序'), icon=FluentIcon.SETTING)
        self.addSubInterface(self.FunctionInterface, 'FunctionInterface', self.tr('功能'), icon=FluentIcon.TILES)
        self.addSubInterface(self.ProxyInterface, 'ProxyInterface', self.tr('代理'), icon=FluentIcon.CERTIFICATE)
        self.AboutInterface = About('AboutInterface', self)
        self.addSubInterface(self.AboutInterface, 'AboutInterface', self.tr('关于'), icon=FluentIcon.INFO)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 10, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.PersonalInterface)
        self.pivot.setCurrentItem(self.PersonalInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.PersonalInterface.objectName())

    def __initInfo(self):
        port = get_json('./config/config.json', 'PROXY_PORT')
        self.proxyPortCard.titleLabel.setText(self.tr('代理端口 (当前: ') + port + ')')
        self.proxyPortCard.setDisabled(not cfg.proxyStatus.value)

    def __connectSignalToSlot(self):
        self.themeColorCard.colorChanged.connect(lambda c: setThemeColor(c, lazy=True))
        self.zoomCard.comboBox.currentIndexChanged.connect(self.restart_application)
        self.languageCard.comboBox.currentIndexChanged.connect(self.restart_application)
        self.updateOnStartUpCard.clicked.connect(lambda: checkUpdate(self.parent))
        self.restartCard.clicked.connect(self.restart_application)

        self.autoCopyCard.checkedChanged.connect(
            lambda: self.handleChoiceChanged(cfg.autoCopy.value, self.tr('自动复制已开启!'), self.tr('自动复制已关闭!')))
        self.useLoginCard.checkedChanged.connect(
            lambda: self.handleChoiceChanged(cfg.useLogin.value, self.tr('登录功能已开启!'), self.tr('登录功能已关闭!')))
        self.useAudioCard.checkedChanged.connect(
            lambda: self.handleChoiceChanged(cfg.useAudio.value, self.tr('流萤语音已开启!'), self.tr('流萤语音已关闭!')))

        self.proxyCard.checkedChanged.connect(
            lambda: self.handleProxyChanged(cfg.proxyStatus.value, self.tr('代理端口已开启!'), self.tr('代理端口已关闭!')))
        self.chinaCard.checkedChanged.connect(
            lambda: self.handleProxyChanged(cfg.chinaStatus.value, self.tr('国内镜像已开启!'), self.tr('国内镜像已关闭!')))
        self.proxyPortCard.set_port.connect(self.handleSetProxyPort)

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

    def handleChoiceChanged(self, status, title_true, title_false):
        if status:
            Info(self, 'S', 1000, title_true)
        else:
            Info(self, 'S', 1000, title_false)

    def handleProxyChanged(self, status, title_true, title_false):
        if status:
            Info(self, 'S', 1000, title_true)
        else:
            Info(self, 'S', 1000, title_false)

        if cfg.chinaStatus.value and cfg.proxyStatus.value:
            Info(self, 'W', 3000, self.tr("代理设置冲突,优先使用国内镜像!"))

        self.__initInfo()

    def handleSetProxyPort(self):
        new_port = self.proxyPortCard.port_edit.text()
        if new_port != '':
            with open('config/config.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                data['PROXY_PORT'] = new_port
            with open('config/config.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        
        self.__initInfo()


class About_Background(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pixmap = QPixmap("./src/image/bg_about.png")
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 20, 20)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, self.width(), self.height(), pixmap)

        painter.setPen(Qt.white)
        painter.setFont(QFont(cfg.APP_FONT, 45))
        painter.drawText(self.rect().adjusted(0, -30, 0, 0), Qt.AlignHCenter | Qt.AlignVCenter, cfg.APP_NAME)
        painter.setFont(QFont(cfg.APP_FONT, 30))
        painter.drawText(self.rect().adjusted(0, 120, 0, 0), Qt.AlignHCenter | Qt.AlignVCenter, cfg.APP_VERSION)


class About(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)

        self.__initWidget()

    def __initWidget(self):
        self.about_image = About_Background()
        self.about_image.setFixedSize(1100, 500)

        self.link_writer = PushButton(FluentIcon.HOME, self.tr('   作者主页'))
        self.link_repo = PushButton(FluentIcon.GITHUB, self.tr('   Github项目'))
        self.link_releases = PushButton(FluentIcon.MESSAGE, self.tr('   版本发布'))
        self.link_issues = PushButton(FluentIcon.HELP, self.tr('   反馈交流'))

        for link_button in [self.link_writer, self.link_repo, self.link_releases, self.link_issues]:
            link_button.setFixedSize(260, 70)
            link_button.setIconSize(QSize(16, 16))
            link_button.setFont(QFont(f'{cfg.APP_FONT}', 12))
            setCustomStyleSheet(link_button, 'PushButton{border-radius: 12px}', 'PushButton{border-radius: 12px}')

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.image_layout = QVBoxLayout()
        self.image_layout.addWidget(self.about_image, alignment=Qt.AlignHCenter)

        self.info_button_layout = QHBoxLayout()
        self.info_button_layout.addWidget(self.link_writer)
        self.info_button_layout.addWidget(self.link_repo)
        self.info_button_layout.addWidget(self.link_releases)
        self.info_button_layout.addWidget(self.link_issues)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(self.image_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.info_button_layout)
        self.setLayout(self.main_layout)

    def __connectSignalToSlot(self):
        self.link_writer.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(cfg.URL_WRITER)))
        self.link_repo.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(cfg.URL_REPO)))
        self.link_releases.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(cfg.URL_RELEASES)))
        self.link_issues.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(cfg.URL_ISSUES)))
