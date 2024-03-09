from typing import Union
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtCore import Signal, Qt
from qfluentwidgets import FluentIconBase, LineEdit, PrimaryPushButton, TableWidget, SearchLineEdit, SettingCardGroup
from app.component.setting_card import SettingCard


class PrimaryPushSettingCard_Giveall(SettingCard):
    give_materials = Signal()
    give_avatars = Signal()
    def __init__(self, meterials, avatars, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.button_materials = PrimaryPushButton(meterials, self)
        self.button_avatars = PrimaryPushButton(avatars, self)
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
        self.account_name.setPlaceholderText("账户名称")
        self.account_uid = LineEdit(self)
        self.account_uid.setPlaceholderText("UID(可选)")
        validator = QIntValidator(self)
        self.account_uid.setValidator(validator)
        self.button_create = PrimaryPushButton(create, self)
        self.button_delete = PrimaryPushButton(delete, self)
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
        validator = QIntValidator(self)
        self.account_uid.setValidator(validator)
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
        validator = QIntValidator(self)
        self.stucked_uid.setValidator(validator)
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
        validator = QIntValidator(1, 70, self)
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
        self.avatar_level.setPlaceholderText("角色等级")
        self.avatar_eidolon.setPlaceholderText("星魂等级")
        self.avatar_skill.setPlaceholderText("行迹等级")
        validator = QIntValidator(1, 80, self)
        self.avatar_level.setValidator(validator)
        self.avatar_eidolon.setValidator(validator)
        self.avatar_skill.setValidator(validator)

        self.button_avatar = PrimaryPushButton(avatar, self)
        self.hBoxLayout.addWidget(self.avatar_level, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.avatar_eidolon, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.avatar_skill, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_avatar, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_avatar.clicked.connect(self.avatar_set)


class Scene(QWidget):
    emit_scene_id = Signal(str)
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text.replace(' ', '-'))

        self.search_line = SearchLineEdit(self)
        self.search_line.setPlaceholderText("搜索场景")
        self.search_line.setFixedHeight(35)
        self.scene_table = TableWidget(self)
        self.scene_table.setFixedSize(1140, 420)
        self.scene_table.setBorderVisible(True)
        self.scene_table.setBorderRadius(8)
        self.scene_table.setWordWrap(False)
        self.scene_table.setColumnCount(2)
        self.scene_table.verticalHeader().hide()
        # self.scene_table.setSelectRightClickedRow(True)
        self.scene_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.scene_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.scene_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.scene_layout = QVBoxLayout()
        self.scene_layout.addSpacing(20)
        self.scene_layout.addWidget(self.search_line)
        self.scene_layout.addSpacing(20)
        self.scene_layout.addWidget(self.scene_table)
        self.setLayout(self.scene_layout)

        with open('src/data/scene.txt', 'r', encoding='utf-8') as file:
            scene = file.readlines()
        self.scene_table.setRowCount(len(scene))
        for i, line in enumerate(scene):
            parts = line.split()
            for j, part in enumerate(parts):
                self.scene_table.setItem(i, j, QTableWidgetItem(part))
        self.scene_table.setHorizontalHeaderLabels(['场景描述', '场景ID'])

        self.search_line.textChanged.connect(self.search_scene)
        self.scene_table.cellClicked.connect(self.scene_clicked)
    
    def scene_clicked(self, row, column):
        item = self.scene_table.item(row, 1)
        scene_id = item.text()
        self.emit_scene_id.emit(scene_id)
    
    def search_scene(self):
        keyword = self.search_line.text()
        for row in range(self.scene_table.rowCount()):
            item = self.scene_table.item(row, 0)
            if item.text().lower().find(keyword.lower()) != -1:
                self.scene_table.setRowHidden(row, False)
            else:
                self.scene_table.setRowHidden(row, True)


class Spawn(QWidget):
    emit_monster_id = Signal(str)
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text.replace(' ', '-'))

        self.line_container = QWidget(self)
        validator = QIntValidator(1, 99, self)
        self.search_line = SearchLineEdit(self)
        self.search_line.setPlaceholderText("搜索怪物")
        self.monster_num = LineEdit(self)
        self.monster_level = LineEdit(self)
        self.monster_round = LineEdit(self)
        self.monster_num.setPlaceholderText("怪物数量")
        self.monster_level.setPlaceholderText("怪物等级")
        self.monster_round.setPlaceholderText("怪物半径")
        self.search_line.setFixedHeight(35)
        self.monster_num.setFixedSize(82, 35)
        self.monster_level.setFixedSize(82, 35)
        self.monster_round.setFixedSize(82, 35)
        self.monster_num.setValidator(validator)
        self.monster_level.setValidator(validator)
        self.monster_round.setValidator(validator)

        self.spawn_table = TableWidget(self)
        self.spawn_table.setFixedSize(1140, 420)
        self.spawn_table.setBorderVisible(True)
        self.spawn_table.setBorderRadius(8)
        self.spawn_table.setWordWrap(False)
        self.spawn_table.setColumnCount(2)
        self.spawn_table.verticalHeader().hide()
        # self.spawn_table.setSelectRightClickedRow(True)
        self.spawn_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.spawn_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.spawn_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.line_layout = QHBoxLayout()
        self.line_layout.addWidget(self.search_line)
        self.line_layout.addSpacing(5)
        self.line_layout.addWidget(self.monster_num)
        self.line_layout.addSpacing(5)
        self.line_layout.addWidget(self.monster_level)
        self.line_layout.addSpacing(5)
        self.line_layout.addWidget(self.monster_round)
        self.line_container.setLayout(self.line_layout)
        self.spawn_layout = QVBoxLayout()
        self.spawn_layout.addWidget(self.line_container)
        self.spawn_layout.addWidget(self.spawn_table)
        self.setLayout(self.spawn_layout)

        with open('src/data/monster.txt', 'r', encoding='utf-8') as file:
            monster = file.readlines()
        self.spawn_table.setRowCount(len(monster))
        for i, line in enumerate(monster):
            parts = line.split()
            for j, part in enumerate(parts):
                self.spawn_table.setItem(i, j, QTableWidgetItem(part))
        self.spawn_table.setHorizontalHeaderLabels(['怪物名称', '怪物ID'])

        self.search_line.textChanged.connect(self.search_monster)
        self.spawn_table.cellClicked.connect(self.spawn_clicked)
    
    def spawn_clicked(self, row, column):
        item = self.spawn_table.item(row, 1)
        monster_id = item.text()
        self.emit_monster_id.emit(monster_id)
    
    def search_monster(self):
        keyword = self.search_line.text()
        for row in range(self.spawn_table.rowCount()):
            item = self.spawn_table.item(row, 0)
            if item.text().lower().find(keyword.lower()) != -1:
                self.spawn_table.setRowHidden(row, False)
            else:
                self.spawn_table.setRowHidden(row, True)


class Give(QWidget):
    emit_item_id = Signal(str)
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text.replace(' ', '-'))

        self.search_line = SearchLineEdit(self)
        self.search_line.setPlaceholderText("搜索物品")
        self.search_line.setFixedHeight(35)

        self.give_table = TableWidget(self)
        self.give_table.setFixedSize(1140, 420)
        self.give_table.setBorderVisible(True)
        self.give_table.setBorderRadius(8)
        self.give_table.setWordWrap(False)
        self.give_table.setColumnCount(3)
        self.give_table.verticalHeader().hide()
        # self.give_table.setSelectRightClickedRow(True)
        self.give_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.give_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.give_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.give_layout = QVBoxLayout()
        self.give_layout.addSpacing(20)
        self.give_layout.addWidget(self.search_line)
        self.give_layout.addSpacing(20)
        self.give_layout.addWidget(self.give_table)
        self.setLayout(self.give_layout)

        with open('src/data/item.txt', 'r', encoding='utf-8') as file:
            item = file.readlines()
        self.give_table.setRowCount(len(item))
        for i, line in enumerate(item):
            parts = line.split()
            for j, part in enumerate(parts):
                self.give_table.setItem(i, j, QTableWidgetItem(part))
        self.give_table.setHorizontalHeaderLabels(['物品名称', '物品ID', '物品类型'])

        self.search_line.textChanged.connect(self.search_monster)
        self.give_table.cellClicked.connect(self.give_clicked)
    
    def give_clicked(self, row, column):
        item = self.give_table.item(row, 1)
        item_id = item.text()
        self.emit_item_id.emit(item_id)
    
    def search_monster(self):
        keyword = self.search_line.text()
        for row in range(self.give_table.rowCount()):
            item = self.give_table.item(row, 0)
            if item.text().lower().find(keyword.lower()) != -1:
                self.give_table.setRowHidden(row, False)
            else:
                self.give_table.setRowHidden(row, True)