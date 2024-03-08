from typing import Union
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QPushButton
from qfluentwidgets import FluentIconBase
from app.component.setting_card import SettingCard


class PushSettingCard_Giveall(SettingCard):
    give_materials = Signal()
    give_avatars = Signal()
    def __init__(self, meterials, avatars, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.button_materials = QPushButton(meterials, self)
        self.button_avatars = QPushButton(avatars, self)
        self.hBoxLayout.addWidget(self.button_materials, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_avatars, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_materials.clicked.connect(self.give_materials)
        self.button_avatars.clicked.connect(self.give_avatars)


class PrimaryPushSettingCard_Giveall(PushSettingCard_Giveall):
    def __init__(self, meterials, avatars, icon, title, content=None, parent=None):
        super().__init__(meterials, avatars, icon, title, content, parent)
        self.button_materials.setObjectName('primaryButton')
        self.button_avatars.setObjectName('primaryButton')


class PushSettingCard_Clear(SettingCard):
    clear_relics = Signal()
    clear_lightcones = Signal()
    clear_materials = Signal()
    clear_items = Signal()
    def __init__(self, relics, lightcones, meterials, items, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.button_relics = QPushButton(relics, self)
        self.button_lightcones = QPushButton(lightcones, self)
        self.button_materials = QPushButton(meterials, self)
        self.button_items = QPushButton(items, self)
        self.hBoxLayout.addWidget(self.button_relics, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_lightcones, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_materials, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_items, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_relics.clicked.connect(self.clear_relics)
        self.button_lightcones.clicked.connect(self.clear_lightcones)
        self.button_materials.clicked.connect(self.clear_materials)
        self.button_items.clicked.connect(self.clear_items)


class PrimaryPushSettingCard_Clear(PushSettingCard_Clear):
    def __init__(self, relics, lightcones, meterials, items, icon, title, content=None, parent=None):
        super().__init__(relics, lightcones, meterials, items, icon, title, content, parent)
        self.button_relics.setObjectName('primaryButton')
        self.button_lightcones.setObjectName('primaryButton')
        self.button_materials.setObjectName('primaryButton')
        self.button_items.setObjectName('primaryButton')