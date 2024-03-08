from typing import Union
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QPushButton
from qfluentwidgets import MessageBoxBase, TitleLabel, SubtitleLabel, BodyLabel, FluentIconBase
from app.component.setting_card import SettingCard


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
