from typing import Union, List
from PySide6.QtGui import QIcon, QPainter, QColor, QIntValidator
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QWidget
from qfluentwidgets import (FluentIconBase, IconWidget, FluentStyleSheet, isDarkTheme, drawIcon, ComboBox, HyperlinkButton,
                            MessageBoxBase, TitleLabel, SubtitleLabel, BodyLabel, LineEdit, PrimaryPushButton, ExpandLayout)


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
    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
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


############### Download Interface ###############
class HyperlinkCard_Launcher(SettingCard):
    def __init__(self, url_launcher, text_launcher, url_audio, text_audio, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.linkButton_launcher = HyperlinkButton(url_launcher, text_launcher, self)
        self.linkButton_audio = HyperlinkButton(url_audio, text_audio, self)
        self.hBoxLayout.addWidget(self.linkButton_launcher, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_audio, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)


class HyperlinkCard_Environment(SettingCard):
    def __init__(self, url_git, text_git ,url_jar, text_jar,url_mongodb, text_mongodb, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.linkButton_git = HyperlinkButton(url_git, text_git, self)
        self.linkButton_jar = HyperlinkButton(url_jar, text_jar, self)
        self.linkButton_mongodb = HyperlinkButton(url_mongodb, text_mongodb, self)
        self.hBoxLayout.addWidget(self.linkButton_git, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_jar, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_mongodb, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)


class HyperlinkCard_LunarCore(SettingCard):
    def __init__(self, url_repo, text_repo, url_res_1, text_res_1, url_res_2, text_res_2, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.linkButton_repo = HyperlinkButton(url_repo, text_repo, self)
        self.linkButton_res1 = HyperlinkButton(url_res_1, text_res_1, self)
        self.linkButton_res2 = HyperlinkButton(url_res_2, text_res_2, self)
        self.hBoxLayout.addWidget(self.linkButton_repo, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_res1, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_res2, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)


class HyperlinkCard_Tool(SettingCard):
    def __init__(self, url_fiddler, text_fiddler, url_mitmdump, text_mitmdump, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.linkButton_fiddler = HyperlinkButton(url_fiddler, text_fiddler, self)
        self.linkButton_mitmdump = HyperlinkButton(url_mitmdump, text_mitmdump, self)
        self.hBoxLayout.addWidget(self.linkButton_fiddler, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_mitmdump, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)


############### LunarCore Interface ###############
class PrimaryPushSettingCard_Giveall(SettingCard):
    give_materials = Signal()
    give_avatars = Signal()
    def __init__(self, meterials, avatars, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.line_level = LineEdit(self)
        self.line_eidolon = LineEdit(self)
        self.line_skill = LineEdit(self)
        self.button_materials = PrimaryPushButton(meterials, self)
        self.button_avatars = PrimaryPushButton(avatars, self)
        self.line_level.setFixedWidth(60)
        self.line_eidolon.setFixedWidth(60)
        self.line_skill.setFixedWidth(60)
        self.line_level.setPlaceholderText("等级")
        self.line_eidolon.setPlaceholderText("叠/魂")
        self.line_skill.setPlaceholderText("行迹")
        self.line_level.setValidator(QIntValidator(1,99,self))
        self.line_eidolon.setValidator(QIntValidator(1,9,self))
        self.line_skill.setValidator(QIntValidator(1,99,self))
        self.hBoxLayout.addWidget(self.line_level, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.line_eidolon, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.line_skill, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_materials, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_avatars, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_materials.clicked.connect(self.give_materials)
        self.button_avatars.clicked.connect(self.give_avatars)


class PrimaryPushSettingCard_Account(SettingCard):
    create_account = Signal()
    delete_account = Signal()
    def __init__(self, create, delete, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.account_name = LineEdit(self)
        self.account_uid = LineEdit(self)
        self.button_create = PrimaryPushButton(create, self)
        self.button_delete = PrimaryPushButton(delete, self)
        self.account_name.setPlaceholderText("名称")
        self.account_uid.setPlaceholderText("UID")
        self.account_name.setFixedWidth(60)
        self.account_uid.setFixedWidth(60)
        self.account_uid.setValidator(QIntValidator(self))
        self.hBoxLayout.addWidget(self.account_name, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.account_uid, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_create, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_delete, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_create.clicked.connect(self.create_account)
        self.button_delete.clicked.connect(self.delete_account)


class PrimaryPushSettingCard_Kick(SettingCard):
    kick_player = Signal()
    def __init__(self, kick, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.account_uid = LineEdit(self)
        self.account_uid.setPlaceholderText("UID")
        self.account_uid.setFixedWidth(60)
        self.account_uid.setValidator(QIntValidator(self))
        self.button_kick = PrimaryPushButton(kick, self)
        self.hBoxLayout.addWidget(self.account_uid, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_kick, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_kick.clicked.connect(self.kick_player)


class PrimaryPushSettingCard_Unstuck(SettingCard):
    unstuck_player = Signal()
    def __init__(self, unstuck, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.stucked_uid = LineEdit(self)
        self.stucked_uid.setPlaceholderText("UID")
        self.stucked_uid.setFixedWidth(60)
        self.stucked_uid.setValidator(QIntValidator(self))
        self.button_unstuck = PrimaryPushButton(unstuck, self)
        self.hBoxLayout.addWidget(self.stucked_uid, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_unstuck, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_unstuck.clicked.connect(self.unstuck_player)


class PrimaryPushSettingCard_Gender(SettingCard):
    gender_male = Signal()
    gender_female = Signal()
    def __init__(self, male, female, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.button_male = PrimaryPushButton(male, self)
        self.button_female = PrimaryPushButton(female, self)
        self.hBoxLayout.addWidget(self.button_male, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_female, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_male.clicked.connect(self.gender_male)
        self.button_female.clicked.connect(self.gender_female)


class PrimaryPushSettingCard_WorldLevel(SettingCard):
    set_level = Signal()
    def __init__(self, worldlevel, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.world_level = LineEdit(self)
        self.world_level.setPlaceholderText("开拓等级")
        self.world_level.setFixedWidth(85)
        validator = QIntValidator(1, 99, self)
        self.world_level.setValidator(validator)
        self.hBoxLayout.addWidget(self.world_level, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.world_level.textChanged.connect(self.set_level)


class PrimaryPushSettingCard_Avatar(SettingCard):
    avatar_set = Signal()
    def __init__(self, avatar, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.avatar_level = LineEdit(self)
        self.avatar_eidolon = LineEdit(self)
        self.avatar_skill = LineEdit(self)
        self.avatar_level.setPlaceholderText("等级")
        self.avatar_eidolon.setPlaceholderText("星魂")
        self.avatar_skill.setPlaceholderText("行迹")
        self.avatar_level.setFixedWidth(60)
        self.avatar_eidolon.setFixedWidth(60)
        self.avatar_skill.setFixedWidth(60)
        validator = QIntValidator(1, 99, self)
        self.avatar_level.setValidator(validator)
        self.avatar_eidolon.setValidator(validator)
        self.avatar_skill.setValidator(validator)
        self.hBoxLayout.addWidget(self.avatar_level, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.avatar_eidolon, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.avatar_skill, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.avatar_level.textChanged.connect(self.avatar_set)
        self.avatar_eidolon.textChanged.connect(self.avatar_set)
        self.avatar_skill.textChanged.connect(self.avatar_set)


class ComboBoxSettingCard_Quickgive(SettingCard):
    quickgive_clicked = Signal(int)
    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, texts=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.comboBox = ComboBox(self)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.comboBox.setPlaceholderText('选择物品')
        self.comboBox.addItems(texts)
        self.comboBox.setCurrentIndex(-1)
        self.comboBox.currentIndexChanged.connect(self._onCurrentIndexChanged)

    def _onCurrentIndexChanged(self, index: int):
        self.quickgive_clicked.emit(index)


class ComboBoxSettingCard__Clear(SettingCard):
    clear_clicked = Signal(int)
    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, texts=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.comboBox = ComboBox(self)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.comboBox.setPlaceholderText('选择物品')
        self.comboBox.addItems(texts)
        self.comboBox.setCurrentIndex(-1)
        self.comboBox.currentIndexChanged.connect(self._onCurrentIndexChanged)

    def _onCurrentIndexChanged(self, index: int):
        self.clear_clicked.emit(index)


############### Setting Interface ###############
class LineEditSettingCard(SettingCard):
    set_port = Signal()
    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.port_edit = LineEdit(self)
        self.port_edit.setFixedWidth(85)
        self.port_edit.setPlaceholderText("端口")
        self.port_edit.setValidator(QIntValidator(1,99999,self))
        self.set_port_button = PrimaryPushButton('设置', self)

        self.hBoxLayout.addWidget(self.port_edit, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.set_port_button, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.set_port_button.clicked.connect(self.set_port)


############### Proxy Interface ###############
class PrimaryPushSettingCard_Fiddler(SettingCard):
    clicked_script = Signal()
    clicked_old = Signal()
    def __init__(self, text_script, text_old, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.button_script = PrimaryPushButton(text_script, self)
        self.button_old = PrimaryPushButton(text_old, self)
        self.hBoxLayout.addWidget(self.button_script, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_old, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_script.clicked.connect(self.clicked_script)
        self.button_old.clicked.connect(self.clicked_old)


class PrimaryPushSettingCard_Sendcode(SettingCard):
    clicked_sendcode = Signal(int)
    def __init__(self, text_sendcode, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.lineedit_sendcode = LineEdit(self)
        self.lineedit_sendcode.setPlaceholderText("UID")
        self.lineedit_sendcode.setFixedWidth(60)
        self.lineedit_sendcode.setValidator(QIntValidator(self))
        self.button_sendcode = PrimaryPushButton(text_sendcode, self)
        self.hBoxLayout.addWidget(self.lineedit_sendcode, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_sendcode, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_sendcode.clicked.connect(lambda: self.clicked_sendcode.emit(int(self.lineedit_sendcode.text())))
        self.setDisabled(True)


class PrimaryPushSettingCard_Verifycode(SettingCard):
    clicked_verifycode = Signal(int)
    def __init__(self, text_verifycode, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.lineedit_verifycode = LineEdit(self)
        self.lineedit_verifycode.setPlaceholderText("验证码")
        self.lineedit_verifycode.setFixedWidth(70)
        self.lineedit_verifycode.setValidator(QIntValidator(1, 9999, self))
        self.button_verifycode = PrimaryPushButton(text_verifycode, self)
        self.hBoxLayout.addWidget(self.lineedit_verifycode, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_verifycode, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_verifycode.clicked.connect(lambda: self.clicked_verifycode.emit(int(self.lineedit_verifycode.text())))
        self.setDisabled(True)


class MessageFiddler(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel('选择需要使用Fiddler Scripts的服务端:    ')
        self.label1 = SubtitleLabel('    目前支持的服务端列表:')
        self.label2 = BodyLabel('        Yuanshen: Hutao-GS')
        self.label3 = BodyLabel('        StarRail: LunarCore')

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.label1)
        self.viewLayout.addWidget(self.label2)
        self.viewLayout.addWidget(self.label3)

        self.yesButton.setText('Yuanshen')
        self.cancelButton.setText('StarRail')