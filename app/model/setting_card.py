from typing import Union, List
from PySide6.QtGui import QIcon, QPainter, QColor, QIntValidator
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (FluentIconBase, IconWidget, FluentStyleSheet, isDarkTheme, drawIcon,
                            ComboBox, HyperlinkButton,MessageBoxBase, TitleLabel, SubtitleLabel,
                             BodyLabel, LineEdit, PrimaryPushButton, ExpandLayout, PasswordLineEdit)


class SettingCardGroup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.cardLayout = ExpandLayout()
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setSpacing(0)
        self.cardLayout.setContentsMargins(0, 0, 0, 0)
        self.cardLayout.setSpacing(2)
        self.vBoxLayout.addLayout(self.cardLayout, 1)
        FluentStyleSheet.SETTING_CARD_GROUP.apply(self)

    def addSettingCard(self, card: QWidget):
        card.setParent(self)
        self.cardLayout.addWidget(card)
        self.adjustSize()

    def addSettingCards(self, cards: List[QWidget]):
        for card in cards:
            self.addSettingCard(card)

    def adjustSize(self):
        h = self.cardLayout.heightForWidth(self.width()) + 46
        return self.resize(self.width(), h)


class SettingCard(QFrame):
    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title=None, content=None, parent=None):
        super().__init__(parent=parent)
        self.iconLabel = SettingIconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(content or '', self)
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        if not content:
            self.contentLabel.hide()

        self.setFixedHeight(70 if content else 50)
        self.iconLabel.setFixedSize(16, 16)

        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(16, 0, 0, 0)
        self.hBoxLayout.setAlignment(Qt.AlignVCenter)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)

        self.hBoxLayout.addWidget(self.iconLabel, 0, Qt.AlignLeft)
        self.hBoxLayout.addSpacing(16)

        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignLeft)

        self.hBoxLayout.addSpacing(16)
        self.hBoxLayout.addStretch(1)

        self.contentLabel.setObjectName('contentLabel')
        FluentStyleSheet.SETTING_CARD.apply(self)

    def setTitle(self, title: str):
        self.titleLabel.setText(title)

    def setContent(self, content: str):
        self.contentLabel.setText(content)
        self.contentLabel.setVisible(bool(content))

    def setValue(self, value):
        pass

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        if isDarkTheme():
            painter.setBrush(QColor(255, 255, 255, 13))
            painter.setPen(QColor(0, 0, 0, 50))
        else:
            painter.setBrush(QColor(255, 255, 255, 170))
            painter.setPen(QColor(0, 0, 0, 19))

        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 6, 6)


class SettingIconWidget(IconWidget):
    def paintEvent(self, e):
        painter = QPainter(self)

        if not self.isEnabled():
            painter.setOpacity(0.36)

        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        drawIcon(self._icon, painter, self.rect())


############### Environment Interface ###############
class HyperlinkCard_Environment(SettingCard):
    def __init__(self, title, content=None, icon=FIF.LINK):
        super().__init__(icon, title, content)
        self.linkButton_git = HyperlinkButton('https://git-scm.com/download/win', 'Git', self)
        self.linkButton_jar = HyperlinkButton('https://www.oracle.com/java/technologies/javase-downloads.html', 'Java', self)
        self.linkButton_mongodb = HyperlinkButton('https://www.mongodb.com/try/download/community', 'MongoDB', self)
        self.hBoxLayout.addWidget(self.linkButton_git, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_jar, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_mongodb, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)


############### Launcher Interface ###############
class HyperlinkCard_Launcher(SettingCard):
    def __init__(self, title, content=None, icon=FIF.LINK):
        super().__init__(icon, title, content)
        self.linkButton_launcher = HyperlinkButton('https://github.com/letheriver2007/Firefly-Launcher', 'Firefly-Launcher', self)
        self.linkButton_audio = HyperlinkButton('https://github.com/letheriver2007/Firefly-Launcher-Res', 'Firefly-Launcher-Res', self)
        self.hBoxLayout.addWidget(self.linkButton_launcher, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_audio, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)


############### LunarCore Interface ###############
class HyperlinkCard_LunarCore(SettingCard):
    def __init__(self, title, content=None, icon=FIF.LINK):
        super().__init__(icon, title, content)
        self.linkButton_repo = HyperlinkButton('https://github.com/Melledy/LunarCore', 'LunarCore', self)
        self.linkButton_res1 = HyperlinkButton('https://github.com/Dimbreath/StarRailData', 'StarRailData', self)
        self.linkButton_res2 = HyperlinkButton('https://gitlab.com/Melledy/LunarCore-Configs', 'LunarCore-Configs', self)
        self.hBoxLayout.addWidget(self.linkButton_repo, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_res1, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_res2, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)


############### Setting Interface ###############
class LineEditSettingCard_Port(SettingCard):
    set_port = Signal()
    def __init__(self, title, icon=FIF.SETTING):
        super().__init__(icon, title)
        self.port_edit = LineEdit(self)
        self.port_edit.setFixedWidth(85)
        self.port_edit.setPlaceholderText(self.tr("端口"))
        self.port_edit.setValidator(QIntValidator(1,99999,self))
        self.set_port_button = PrimaryPushButton(self.tr('设置'), self)

        self.hBoxLayout.addWidget(self.port_edit, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.set_port_button, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.set_port_button.clicked.connect(self.set_port)


############### Proxy Interface ###############
class HyperlinkCard_Tool(SettingCard):
    def __init__(self, title, content=None, icon=FIF.LINK):
        super().__init__(icon, title, content)
        self.linkButton_fiddler = HyperlinkButton('https://www.telerik.com/fiddler#fiddler-classic', 'Fiddler', self)
        self.linkButton_mitmdump = HyperlinkButton('https://mitmproxy.org/', 'Mitmdump', self)
        self.hBoxLayout.addWidget(self.linkButton_fiddler, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_mitmdump, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)


class PrimaryPushSettingCard_Fiddler(SettingCard):
    clicked_script = Signal()
    clicked_old = Signal()
    def __init__(self, title, content=None, icon=FIF.VPN):
        super().__init__(icon, title, content)
        self.button_script = PrimaryPushButton(self.tr('脚本打开'), self)
        self.button_old = PrimaryPushButton(self.tr('原版打开'), self)
        self.hBoxLayout.addWidget(self.button_script, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_old, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_script.clicked.connect(self.clicked_script)
        self.button_old.clicked.connect(self.clicked_old)


class MessageFiddler(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel(self.tr('选择需要使用Fiddler Scripts的服务端:    '))
        self.label1 = SubtitleLabel(self.tr('    目前支持的服务端列表:'))
        self.label2 = BodyLabel('        Yuanshen: Hutao-GS')
        self.label3 = BodyLabel('        StarRail: LunarCore')

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.label1)
        self.viewLayout.addWidget(self.label2)
        self.viewLayout.addWidget(self.label3)

        self.yesButton.setText('Yuanshen')
        self.cancelButton.setText('StarRail')


############### Remote Interface ###############
class PrimaryPushSettingCard_URL(SettingCard):
    clicked_seturl = Signal()
    def __init__(self, title, content, icon=FIF.WIFI):
        super().__init__(icon, title, content)
        self.lineedit_seturl = LineEdit(self)
        self.lineedit_seturl.setPlaceholderText(self.tr("服务端地址"))
        self.lineedit_seturl.setFixedWidth(150)
        self.button_seturl = PrimaryPushButton(self.tr('设置'), self)
        self.hBoxLayout.addWidget(self.lineedit_seturl, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_seturl, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_seturl.clicked.connect(self.clicked_seturl)


class PrimaryPushSettingCard_API(SettingCard):
    clicked_setapi = Signal()
    def __init__(self, title, content, icon=FIF.LABEL):
        super().__init__(icon, title, content)
        self.button_seturl = PrimaryPushButton(self.tr('打开文件'), self)
        self.hBoxLayout.addWidget(self.button_seturl, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_seturl.clicked.connect(self.clicked_setapi)


class PrimaryPushSettingCard_UID(SettingCard):
    clicked_setuid = Signal()
    def __init__(self, title, content, icon=FIF.QUICK_NOTE):
        super().__init__(icon, title, content)
        self.lineedit_setuid = LineEdit(self)
        self.lineedit_setuid.setPlaceholderText("UID")
        self.lineedit_setuid.setFixedWidth(150)
        self.lineedit_setuid.setValidator(QIntValidator(self))
        self.button_setuid = PrimaryPushButton(self.tr('设置'), self)
        self.hBoxLayout.addWidget(self.lineedit_setuid, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_setuid, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_setuid.clicked.connect(self.clicked_setuid)


class PrimaryPushSettingCard_Verify(SettingCard):
    clicked_apply = Signal()
    clicked_verify = Signal()
    def __init__(self, title, content, icon=FIF.FINGERPRINT):
        super().__init__(icon, title, content)
        self.button_apply = PrimaryPushButton(self.tr('发送'), self)
        self.lineedit_code = LineEdit(self)
        self.lineedit_code.setPlaceholderText(self.tr("验证码"))
        self.lineedit_code.setFixedWidth(100)
        self.lineedit_code.setValidator(QIntValidator(self))
        self.lineedit_key = PasswordLineEdit(self)
        self.lineedit_key.setPlaceholderText(self.tr("密码"))
        self.lineedit_key.setFixedWidth(150)
        self.button_verify = PrimaryPushButton(self.tr('设置'), self)
        self.hBoxLayout.addWidget(self.lineedit_code, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_apply, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.hBoxLayout.addWidget(self.lineedit_key, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_verify, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_apply.clicked.connect(self.clicked_apply)
        self.button_verify.clicked.connect(self.clicked_verify)


class PrimaryPushSettingCard_KEY(SettingCard):
    clicked_setkey = Signal(str)
    def __init__(self, title, content, icon=FIF.FINGERPRINT):
        super().__init__(icon, title, content)
        self.lineedit_setkey = PasswordLineEdit(self)
        self.lineedit_setkey.setPlaceholderText(self.tr("密码"))
        self.button_setkey = PrimaryPushButton(self.tr('设置'), self)
        self.hBoxLayout.addWidget(self.lineedit_setkey, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_setkey, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_setkey.clicked.connect(lambda: self.clicked_setkey.emit(self.lineedit_setkey.text()))