from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget
from PySide6.QtGui import QPixmap, Qt, QPainter, QPainterPath, QDesktopServices, QFont
from PySide6.QtCore import Qt, QUrl
from qfluentwidgets import (TitleLabel, SubtitleLabel, Pivot, qrouter, ScrollArea, SettingCardGroup,
                            CustomColorSettingCard, PushButton, setThemeColor)
from qfluentwidgets import FluentIcon as FIF
from functools import partial
import webbrowser
from home_page import Home
from config import cfg
from src.common.style_sheet import StyleSheet

class Setting(ScrollArea):
    Nav = Pivot
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setObjectName(text.replace(' ', '-'))
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)

        self.pivot = self.Nav(self)
        self.stackedWidget = QStackedWidget(self)

        self.personalGroup = SettingCardGroup('个性化', self.scrollWidget)
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            '主题色',
            '选择一个你喜欢的主题颜色显示',
            self.personalGroup
        )

        self.__initWidget()

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(20, 0, 20, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        
        self.scrollWidget.setObjectName('scrollWidget')
        StyleSheet.SETTING_INTERFACE.apply(self)    #使用qss

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):

        self.personalGroup.addSettingCard(self.themeColorCard)

        self.addSubInterface(self.personalGroup,'personalGroup','一般设置', icon=FIF.SETTING)
        self.AboutInterface = About('About Interface', self)
        self.addSubInterface(self.AboutInterface, 'AboutInterface','关于', icon=FIF.INFO)

        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.personalGroup)
        self.pivot.setCurrentItem(self.personalGroup.objectName())

        qrouter.setDefaultRouteKey(self.stackedWidget, self.personalGroup.objectName())

        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setContentsMargins(0, 10, 10, 10)

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

    def __connectSignalToSlot(self):
        self.themeColorCard.colorChanged.connect(lambda c: setThemeColor(c, lazy=True))


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
        label1 = QLabel(cfg.APP_NAME)
        label2 = QLabel(cfg.APP_VERSION)
        label1.setContentsMargins(0, 20, 0, 0)
        label2.setContentsMargins(0, 10, 0, 20)
        label1.setStyleSheet("font-family: SDK_SC_Web; font-size: 35px;")
        label2.setStyleSheet("font-family: SDK_SC_Web; font-size: 20px;")
        info_layout.addWidget(label1, alignment=Qt.AlignHCenter)
        info_layout.addWidget(label2, alignment=Qt.AlignHCenter)

        # Github链接
        info_button_layout = QHBoxLayout()
        button1 = PushButton(FIF.HOME, '   作者主页')
        button2 = PushButton(FIF.GITHUB, '   Github项目')
        button3 = PushButton(FIF.MESSAGE, '   更新日志')
        button4 = PushButton(FIF.HELP, '   反馈交流')
        button1.setFixedSize(270, 70)
        button2.setFixedSize(270, 70)
        button3.setFixedSize(270, 70)
        button4.setFixedSize(270, 70)
        info_button_layout.addWidget(button1)
        info_button_layout.addWidget(button2)
        info_button_layout.addWidget(button3)
        info_button_layout.addWidget(button4)
    
        main_layout.addLayout(image_layout)
        main_layout.addLayout(info_layout)
        main_layout.addLayout(info_button_layout)

        button1.clicked.connect(self.WriterUrl)
        button2.clicked.connect(self.RepoUrl)
        button3.clicked.connect(self.ReleasesUrl)
        button4.clicked.connect(self.IssuesUrl)

    def WriterUrl(self):
        QDesktopServices.openUrl(QUrl(cfg.URL_WRITER))
    def RepoUrl(self):
        QDesktopServices.openUrl(QUrl(cfg.URL_REPO))
    def ReleasesUrl(self):
        QDesktopServices.openUrl(QUrl(cfg.URL_RELEASES))
    def IssuesUrl(self):
        QDesktopServices.openUrl(QUrl(cfg.URL_ISSUES))
    

