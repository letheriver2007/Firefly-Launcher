from typing import Union
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QVBoxLayout, QHBoxLayout, QButtonGroup
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtCore import Signal, Qt
from qfluentwidgets import (FluentIconBase, LineEdit, TogglePushButton, PrimaryPushButton, StrongBodyLabel,
                            TableWidget, SearchLineEdit, SettingCardGroup, SubtitleLabel, PrimaryToolButton)
from qfluentwidgets import FluentIcon as FIF
from app.model.setting_card import SettingCard


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


class PrimaryPushSettingCard_Clear(SettingCard):
    clear_relics = Signal()
    clear_lightcones = Signal()
    clear_materials = Signal()
    clear_items = Signal()
    def __init__(self, relics, lightcones, meterials, items, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.button_relics = PrimaryPushButton(relics, self)
        self.button_lightcones = PrimaryPushButton(lightcones, self)
        self.button_materials = PrimaryPushButton(meterials, self)
        self.button_items = PrimaryPushButton(items, self)
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
        self.button_set = PrimaryPushButton(worldlevel, self)
        self.hBoxLayout.addWidget(self.world_level, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_set, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_set.clicked.connect(self.set_level)


class PrimaryPushSettingCard_Avatar(SettingCard):
    avatar_set = Signal()
    def __init__(self, avatar, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.avatar_level = LineEdit(self)
        self.avatar_eidolon = LineEdit(self)
        self.avatar_skill = LineEdit(self)
        self.button_avatar = PrimaryPushButton(avatar, self)
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
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_avatar, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_avatar.clicked.connect(self.avatar_set)