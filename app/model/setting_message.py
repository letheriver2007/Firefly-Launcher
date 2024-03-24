from typing import Union
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QVBoxLayout, QHBoxLayout, QButtonGroup
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtCore import Signal, Qt
from qfluentwidgets import (FluentIconBase, LineEdit, TogglePushButton, PrimaryPushButton, StrongBodyLabel, ComboBox,
                            TableWidget, SearchLineEdit, SettingCardGroup, SubtitleLabel, PrimaryToolButton, ConfigItem)
from qfluentwidgets import FluentIcon as FIF
from app.model.setting_card import SettingCard
from app.model.config import cfg


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