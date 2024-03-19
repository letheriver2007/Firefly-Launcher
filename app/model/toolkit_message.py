from typing import Union
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QPushButton
from qfluentwidgets import MessageBoxBase, TitleLabel, SubtitleLabel, BodyLabel, FluentIconBase, LineEdit
from app.model.setting_card import SettingCard


class PushSettingCard_Fiddler(SettingCard):
    clicked_script = Signal()
    clicked_old = Signal()
    def __init__(self, text_script, text_old, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.button_script = QPushButton(text_script, self)
        self.button_old = QPushButton(text_old, self)
        self.hBoxLayout.addWidget(self.button_script, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_old, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_script.clicked.connect(self.clicked_script)
        self.button_old.clicked.connect(self.clicked_old)


class PrimaryPushSettingCard_Fiddler(PushSettingCard_Fiddler):
    def __init__(self, text_script, text_old, icon, title, content=None, parent=None):
        super().__init__(text_script, text_old, icon, title, content, parent)
        self.button_script.setObjectName('primaryButton')
        self.button_old.setObjectName('primaryButton')


class PushSettingCard_Sendcode(SettingCard):
    clicked_sendcode = Signal(int)
    def __init__(self, text_sendcode, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.lineedit_sendcode = LineEdit(self)
        self.lineedit_sendcode.setPlaceholderText("UID")
        self.lineedit_sendcode.setFixedWidth(60)
        self.lineedit_sendcode.setValidator(QIntValidator(self))
        self.button_sendcode = QPushButton(text_sendcode, self)
        self.hBoxLayout.addWidget(self.lineedit_sendcode, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_sendcode, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_sendcode.clicked.connect(lambda: self.clicked_sendcode.emit(self.lineedit_sendcode.text()))
        self.setDisabled(True)


class PrimaryPushSettingCard_Sendcode(PushSettingCard_Sendcode):
    def __init__(self, text_sendcode, icon, title, content=None, parent=None):
        super().__init__(text_sendcode, icon, title, content, parent)
        self.button_sendcode.setObjectName('primaryButton')


class PushSettingCard_Verifycode(SettingCard):
    clicked_verifycode = Signal(int)
    def __init__(self, text_verifycode, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.lineedit_verifycode = LineEdit(self)
        self.lineedit_verifycode.setPlaceholderText("验证码")
        self.lineedit_verifycode.setFixedWidth(70)
        self.lineedit_verifycode.setValidator(QIntValidator(1, 9999, self))
        self.button_verifycode = QPushButton(text_verifycode, self)
        self.hBoxLayout.addWidget(self.lineedit_verifycode, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_verifycode, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_verifycode.clicked.connect(lambda: self.clicked_verifycode.emit(self.lineedit_verifycode.text()))
        self.setDisabled(True)


class PrimaryPushSettingCard_Verifycode(PushSettingCard_Verifycode):
    def __init__(self, text_verifycode, icon, title, content=None, parent=None):
        super().__init__(text_verifycode, icon, title, content, parent)
        self.button_verifycode.setObjectName('primaryButton')


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
