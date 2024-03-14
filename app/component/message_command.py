from typing import Union
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QVBoxLayout, QHBoxLayout, QButtonGroup
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtCore import Signal, Qt
from qfluentwidgets import (FluentIconBase, LineEdit, TogglePushButton, PrimaryPushButton, StrongBodyLabel,
                            TableWidget, SearchLineEdit, SettingCardGroup, SubtitleLabel, PrimaryToolButton)
from qfluentwidgets import FluentIcon as FIF
from app.component.setting_card import SettingCard


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


class Scene(QWidget):
    emit_scene_id = Signal(str)
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text.replace(' ', '-'))

        self.__initWidget()

    def __initWidget(self):
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

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.scene_layout = QVBoxLayout()
        self.scene_layout.addWidget(self.search_line)
        self.scene_layout.addWidget(self.scene_table)
        self.setLayout(self.scene_layout)

        self.load_scene()

    def __connectSignalToSlot(self):
        self.search_line.textChanged.connect(self.search_scene)
        self.scene_table.cellClicked.connect(self.scene_clicked)
    
    def load_scene(self):
        with open('src/data/scene.txt', 'r', encoding='utf-8') as file:
            scene = file.readlines()
        self.scene_table.setRowCount(len(scene))
        for i, line in enumerate(scene):
            parts = line.split()
            for j, part in enumerate(parts):
                self.scene_table.setItem(i, j, QTableWidgetItem(part))
        self.scene_table.setHorizontalHeaderLabels(['场景描述', '场景ID'])
    
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

        self.__initWidget()

    def __initWidget(self):
        validator = QIntValidator(1, 99, self)
        self.monster_num = LineEdit(self)
        self.monster_level = LineEdit(self)
        self.monster_round = LineEdit(self)
        self.monster_num.setPlaceholderText("请输入怪物数量")
        self.monster_level.setPlaceholderText("请输入怪物等级")
        self.monster_round.setPlaceholderText("请输入仇恨半径")
        self.monster_num.setValidator(validator)
        self.monster_level.setValidator(validator)
        self.monster_round.setValidator(validator)

        self.monster_num_label = SubtitleLabel("数量：", self)
        self.monster_level_label = SubtitleLabel("等级：", self)
        self.monster_round_label = SubtitleLabel("半径：", self)

        self.search_line = SearchLineEdit(self)
        self.search_line.setPlaceholderText("搜索怪物")
        self.search_line.setFixedSize(915, 35)
        self.spawn_table = TableWidget(self)
        self.spawn_table.setFixedSize(915, 420)
        self.spawn_table.setBorderVisible(True)
        self.spawn_table.setBorderRadius(8)
        self.spawn_table.setWordWrap(False)
        self.spawn_table.setColumnCount(2)
        self.spawn_table.verticalHeader().hide()
        # self.spawn_table.setSelectRightClickedRow(True)
        self.spawn_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.spawn_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.spawn_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.set_layout = QVBoxLayout()
        self.set_layout.addSpacing(70)
        self.set_layout.addWidget(self.monster_num_label)
        self.set_layout.addSpacing(5)
        self.set_layout.addWidget(self.monster_num)
        self.set_layout.addSpacing(20)
        self.set_layout.addWidget(self.monster_level_label)
        self.set_layout.addSpacing(5)
        self.set_layout.addWidget(self.monster_level)
        self.set_layout.addSpacing(20)
        self.set_layout.addWidget(self.monster_round_label)
        self.set_layout.addSpacing(5)
        self.set_layout.addWidget(self.monster_round)
        self.set_layout.addStretch(1)

        self.spawn_layout = QVBoxLayout()
        self.spawn_layout.addWidget(self.search_line)
        self.spawn_layout.addWidget(self.spawn_table)
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.spawn_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.set_layout)
        self.setLayout(self.main_layout)

        self.load_monster()

    def __connectSignalToSlot(self):
        self.search_line.textChanged.connect(self.search_monster)
        self.spawn_table.cellClicked.connect(self.spawn_clicked)
        self.monster_num.textChanged.connect(self.spawn_clicked)
        self.monster_level.textChanged.connect(self.spawn_clicked)
        self.monster_round.textChanged.connect(self.spawn_clicked)
    
    def load_monster(self):
        with open('src/data/monster.txt', 'r', encoding='utf-8') as file:
            monster = file.readlines()
        self.spawn_table.setRowCount(len(monster))
        for i, line in enumerate(monster):
            parts = line.split()
            for j, part in enumerate(parts):
                self.spawn_table.setItem(i, j, QTableWidgetItem(part))
        self.spawn_table.setHorizontalHeaderLabels(['怪物名称', '怪物ID'])

    def spawn_clicked(self):
        selected_items = self.spawn_table.selectedItems()
        if selected_items:
            monster_id = selected_items[1].text()
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
    emit_item_id = Signal(str, str)
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text.replace(' ', '-'))

        self.__initWidget()

    def __initWidget(self):
        self.search_line = SearchLineEdit(self)
        self.search_line.setPlaceholderText("搜索物品")
        self.search_line.setFixedSize(915, 35)
        self.give_table = TableWidget(self)
        self.give_table.setFixedSize(915, 420)
        self.give_table.setBorderVisible(True)
        self.give_table.setBorderRadius(8)
        self.give_table.setWordWrap(False)
        self.give_table.setColumnCount(3)
        self.give_table.verticalHeader().hide()
        # self.give_table.setSelectRightClickedRow(True)
        self.give_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.give_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.give_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.button_group = QButtonGroup(self)
        self.button_all = TogglePushButton("全部", self)
        self.button_avatar = TogglePushButton("角色", self)
        self.button_lightcone = TogglePushButton("光锥", self)
        self.button_item = TogglePushButton("物品", self)
        self.button_food = TogglePushButton("食物", self)
        self.button_head = TogglePushButton("头像", self)
        self.button_all.setFixedSize(60, 35)
        self.button_avatar.setFixedSize(60, 35)
        self.button_lightcone.setFixedSize(60, 35)
        self.button_item.setFixedSize(60, 35)
        self.button_food.setFixedSize(60, 35)
        self.button_head.setFixedSize(60, 35)
        self.button_group.addButton(self.button_all)
        self.button_group.addButton(self.button_avatar)
        self.button_group.addButton(self.button_lightcone)
        self.button_group.addButton(self.button_item)
        self.button_group.addButton(self.button_food)
        self.button_group.addButton(self.button_head)
        
        self.search_num = LineEdit(self)
        self.search_level = LineEdit(self)
        self.search_eidolon = LineEdit(self)
        self.search_num.setPlaceholderText("请输入物品数量")
        self.search_level.setPlaceholderText("请输入角色/光锥等级")
        self.search_eidolon.setPlaceholderText("请输入角色星魂/光锥叠影")
        self.search_num.setValidator(QIntValidator(self))
        self.search_level.setValidator(QIntValidator(1, 99, self))
        self.search_eidolon.setValidator(QIntValidator(1, 9, self))

        self.item_num_label = SubtitleLabel("数量：", self)
        self.item_level_label = SubtitleLabel("等级：", self)
        self.item_eidolon_label = SubtitleLabel("星魂/叠影：", self)

        self.__initLayout()
        self.__connectSignalToSlot()
    
    def __initLayout(self):
        self.give_layout = QVBoxLayout()
        self.give_layout.addWidget(self.search_line)
        self.give_layout.addWidget(self.give_table)

        horizontal_layout1 = QHBoxLayout()
        horizontal_layout1.addWidget(self.button_all)
        horizontal_layout1.addWidget(self.button_avatar)
        horizontal_layout1.addWidget(self.button_lightcone)
        horizontal_layout2 = QHBoxLayout()
        horizontal_layout2.addWidget(self.button_item)
        horizontal_layout2.addWidget(self.button_food)
        horizontal_layout2.addWidget(self.button_head)
        vertical_layout = QVBoxLayout()
        vertical_layout.addSpacing(65)
        vertical_layout.addLayout(horizontal_layout1)
        vertical_layout.addSpacing(5)
        vertical_layout.addLayout(horizontal_layout2)

        self.set_layout = QVBoxLayout()
        self.set_layout.addLayout(vertical_layout)
        self.set_layout.addSpacing(20)
        self.set_layout.addWidget(self.item_num_label)
        self.set_layout.addSpacing(5)
        self.set_layout.addWidget(self.search_num)
        self.set_layout.addSpacing(20)
        self.set_layout.addWidget(self.item_level_label)
        self.set_layout.addSpacing(5)
        self.set_layout.addWidget(self.search_level)
        self.set_layout.addSpacing(20)
        self.set_layout.addWidget(self.item_eidolon_label)
        self.set_layout.addSpacing(5)
        self.set_layout.addWidget(self.search_eidolon)
        self.set_layout.addStretch(1)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.give_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.set_layout)
        self.setLayout(self.main_layout)

        self.load_item()

    def __connectSignalToSlot(self):
        self.button_all.clicked.connect(lambda: self.search_give("all"))
        self.search_line.textChanged.connect(lambda: self.search_give("text"))
        self.button_avatar.clicked.connect(lambda: self.search_give("avatar"))
        self.button_lightcone.clicked.connect(lambda: self.search_give("lightcone"))
        self.button_item.clicked.connect(lambda: self.search_give("item"))
        self.button_food.clicked.connect(lambda: self.search_give("food"))
        self.button_head.clicked.connect(lambda: self.search_give("head"))
        self.give_table.cellClicked.connect(self.give_clicked)
        self.search_num.textChanged.connect(self.give_clicked)
        self.search_level.textChanged.connect(self.give_clicked)
        self.search_eidolon.textChanged.connect(self.give_clicked)

    def load_item(self):
        with open('src/data/item.txt', 'r', encoding='utf-8') as file:
            item = file.readlines()
        self.give_table.setRowCount(len(item))
        for i, line in enumerate(item):
            parts = line.split()
            for j, part in enumerate(parts):
                self.give_table.setItem(i, j, QTableWidgetItem(part))
        self.give_table.setHorizontalHeaderLabels(['物品名称', '物品ID', '物品类型'])
        self.types_dict = {'avatar': '角色', 'lightcone': '光锥', 'item': '物品', 'food': '食物', 'head': '头像'}
    
    def give_clicked(self):
        selected_items = self.give_table.selectedItems()
        if selected_items:
            item_id = selected_items[1].text()
            value = selected_items[2].text()
            keys = [key for key, val in self.types_dict.items() if val == value]
            self.emit_item_id.emit(item_id, keys[0])

    def search_give(self, types):
        if types == 'all':
            for row in range(self.give_table.rowCount()):
                self.give_table.setRowHidden(row, False)
        elif types == 'text':
            keyword = self.search_line.text()
            for row in range(self.give_table.rowCount()):
                item = self.give_table.item(row, 0)
                if item.text().lower().find(keyword.lower()) != -1:
                    self.give_table.setRowHidden(row, False)
                else:
                    self.give_table.setRowHidden(row, True)
        elif types in self.types_dict:
            for row in range(self.give_table.rowCount()):
                item = self.give_table.item(row, 2)
                if item.text() == self.types_dict[types]:
                    self.give_table.setRowHidden(row, False)
                else:
                    self.give_table.setRowHidden(row, True)


class Relic(QWidget):
    emit_relic_id = Signal(str)
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text.replace(' ', '-'))

        self.__initWidget()

    def __initWidget(self):
        self.search_line = SearchLineEdit(self)
        self.search_line.setPlaceholderText("搜索遗器")
        self.search_line.setFixedSize(210, 35)
        self.relic_base_button = PrimaryPushButton("基础", self)
        self.relic_base_button.setFixedSize(68, 35)
        self.relic_custom_button = PrimaryPushButton("预设", self)
        self.relic_custom_button.setFixedSize(68, 35)
        self.relic_table = TableWidget(self)
        self.relic_table.setFixedSize(355, 420)
        self.relic_table.setBorderVisible(True)
        self.relic_table.setBorderRadius(8)
        self.relic_table.setWordWrap(False)
        self.relic_table.setColumnCount(4)
        self.relic_table.verticalHeader().hide()
        # self.relic_table.setSelectRightClickedRow(True)
        self.relic_table.setColumnWidth(0, 198)
        self.relic_table.setColumnWidth(1, 80)
        self.relic_table.setColumnWidth(2, 75)
        self.relic_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.relic_table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.entry_search_line = SearchLineEdit(self)
        self.entry_search_line.setPlaceholderText("搜索词条")
        self.entry_search_line.setFixedSize(210, 35)
        self.entry_main_button = PrimaryPushButton("主词条", self)
        self.entry_main_button.setFixedSize(68, 35)
        self.entry_side_button = PrimaryPushButton("副词条", self)
        self.entry_side_button.setFixedSize(68, 35)
        self.entry_table = TableWidget(self)
        self.entry_table.setFixedSize(355, 420)
        self.entry_table.setBorderVisible(True)
        self.entry_table.setBorderRadius(8)
        self.entry_table.setWordWrap(False)
        self.entry_table.setColumnCount(4)
        self.entry_table.verticalHeader().hide()
        # self.entry_table.setSelectRightClickedRow(True)
        self.entry_table.setColumnWidth(0, 198)
        self.entry_table.setColumnWidth(1, 80)
        self.entry_table.setColumnWidth(2, 75)
        self.entry_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.entry_table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.now_entry_label1 = SubtitleLabel("当前主词条：", self)
        self.now_entry_label = LineEdit(self)
        self.now_entry_label.setReadOnly(True)
        self.now_entry_label2 = SubtitleLabel("当前副词条：", self)
        self.now_entry_table = TableWidget(self)
        self.now_entry_table.setFixedSize(365, 160)
        self.now_entry_table.setBorderVisible(True)
        self.now_entry_table.setBorderRadius(8)
        self.now_entry_table.setWordWrap(False)
        self.now_entry_table.setColumnCount(2)
        self.now_entry_table.verticalHeader().hide()
        # self.now_entry_table.setSelectRightClickedRow(True)
        self.now_entry_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.now_entry_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.now_entry_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.toright_button = PrimaryToolButton(FIF.RIGHT_ARROW)
        self.toright_button.setFixedSize(35, 35)
        self.num_edit = LineEdit(self)
        self.num_edit.setPlaceholderText("数量")
        self.num_edit.setFixedSize(65, 35)
        self.num_edit.setValidator(QIntValidator(self))
        self.set_button = PrimaryToolButton(FIF.UP)
        self.set_button.setFixedSize(35, 35)
        self.add_button = PrimaryToolButton(FIF.ADD)
        self.add_button.setFixedSize(35, 35)
        self.remove_button = PrimaryToolButton(FIF.REMOVE)
        self.remove_button.setFixedSize(35, 35)
        self.delete_button = PrimaryToolButton(FIF.DELETE)
        self.delete_button.setFixedSize(35, 35)

        self.level_label = SubtitleLabel("等级：", self)
        self.level_edit = LineEdit(self)
        self.level_edit.setPlaceholderText("请输入生成遗器的等级")
        self.level_edit.setValidator(QIntValidator(1, 99, self))

        self.now_entry_list = {}

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.relic_button_layout = QHBoxLayout()
        self.relic_button_layout.addWidget(self.search_line)
        self.relic_button_layout.addWidget(self.relic_base_button)
        self.relic_button_layout.addWidget(self.relic_custom_button)
        self.relic_layout = QVBoxLayout()
        self.relic_layout.addLayout(self.relic_button_layout)
        self.relic_layout.addWidget(self.relic_table)

        self.entry_button_layout = QHBoxLayout()
        self.entry_button_layout.addWidget(self.entry_search_line)
        self.entry_button_layout.addWidget(self.entry_main_button)
        self.entry_button_layout.addWidget(self.entry_side_button)
        self.entry_layout = QVBoxLayout()
        self.entry_layout.addLayout(self.entry_button_layout)
        self.entry_layout.addWidget(self.entry_table)

        self.now_entry_tool_layout = QHBoxLayout()
        self.now_entry_tool_layout.addWidget(self.toright_button)
        self.now_entry_tool_layout.addSpacing(60)
        self.now_entry_tool_layout.addWidget(self.num_edit)
        self.now_entry_tool_layout.addSpacing(5)
        self.now_entry_tool_layout.addWidget(self.set_button)
        self.now_entry_tool_layout.addSpacing(5)
        self.now_entry_tool_layout.addWidget(self.add_button)
        self.now_entry_tool_layout.addSpacing(5)
        self.now_entry_tool_layout.addWidget(self.remove_button)
        self.now_entry_tool_layout.addSpacing(5)
        self.now_entry_tool_layout.addWidget(self.delete_button)
        self.now_entry_layout = QVBoxLayout()
        self.now_entry_layout.addSpacing(15)
        self.now_entry_layout.addWidget(self.now_entry_label1)
        self.now_entry_layout.addSpacing(5)
        self.now_entry_layout.addWidget(self.now_entry_label)
        self.now_entry_layout.addSpacing(20)
        self.now_entry_layout.addWidget(self.now_entry_label2)
        self.now_entry_layout.addSpacing(5)
        self.now_entry_layout.addWidget(self.now_entry_table)
        self.now_entry_layout.addSpacing(14)
        self.now_entry_layout.addLayout(self.now_entry_tool_layout)
        self.now_entry_layout.addSpacing(15)
        self.now_entry_layout.addWidget(self.level_label)
        self.now_entry_layout.addSpacing(5)
        self.now_entry_layout.addWidget(self.level_edit)
        self.now_entry_layout.addStretch(1)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.relic_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.entry_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.now_entry_layout)
        self.setLayout(self.main_layout)

        self.load_relic()
        self.load_entry()
        self.load_now_entry()

    def __connectSignalToSlot(self):
        self.search_line.textChanged.connect(lambda: self.search_relic('line'))
        self.relic_base_button.clicked.connect(lambda: self.search_relic('base'))
        self.relic_custom_button.clicked.connect(lambda: self.search_relic('custom'))

        self.entry_search_line.textChanged.connect(lambda: self.search_entry('line'))
        self.entry_main_button.clicked.connect(lambda: self.search_entry('main'))
        self.entry_side_button.clicked.connect(lambda: self.search_entry('side'))
        self.entry_table.cellClicked.connect(lambda: self.move_to_right('cell'))
        self.toright_button.clicked.connect(lambda: self.move_to_right('button'))

        self.add_button.clicked.connect(lambda: self.entry_num_changed('add'))
        self.remove_button.clicked.connect(lambda: self.entry_num_changed('remove'))
        self.delete_button.clicked.connect(lambda: self.entry_num_changed('delete'))

        self.relic_table.cellClicked.connect(self.show_relic_entry)
        self.relic_table.cellClicked.connect(self.relic_clicked)
        self.now_entry_label.textChanged.connect(self.relic_clicked)
        self.toright_button.clicked.connect(self.relic_clicked)
        self.add_button.clicked.connect(self.relic_clicked)
        self.remove_button.clicked.connect(self.relic_clicked)
        self.delete_button.clicked.connect(self.relic_clicked)
        self.level_edit.textChanged.connect(self.relic_clicked)

    def load_relic(self):
        with open('src/data/relic.txt', 'r', encoding='utf-8') as file:
            relic = file.readlines()
        self.relic_table.setRowCount(len(relic))
        for i, line in enumerate(relic):
            parts = line.split()
            for j, part in enumerate(parts):
                self.relic_table.setItem(i, j, QTableWidgetItem(part))
        self.relic_table.setHorizontalHeaderLabels(['遗器名称', '部位', 'ID', 'types'])
        self.relic_table.setColumnHidden(3, True)
    
    def load_entry(self):
        with open('src/data/entry.txt', 'r', encoding='utf-8') as file:
            entry = file.readlines()
        self.entry_table.setRowCount(len(entry))
        for i, line in enumerate(entry):
            parts = line.split()
            for j, part in enumerate(parts):
                self.entry_table.setItem(i, j, QTableWidgetItem(part))
        self.entry_table.setHorizontalHeaderLabels(['词条名称', '部位', 'ID', 'types'])
        self.entry_table.setColumnHidden(3, True)
    
    def load_now_entry(self):
        self.now_entry_table.clearContents()
        self.now_entry_table.setRowCount(len(self.now_entry_list))
        for row, (key, value) in enumerate(self.now_entry_list.items()):
            self.now_entry_table.setItem(row, 0, QTableWidgetItem(key))
            self.now_entry_table.setItem(row, 1, QTableWidgetItem(str(value)))
        self.now_entry_table.setHorizontalHeaderLabels(['词条名称', '数量'])

    def search_relic(self, types):
        if types == 'line':
            keyword = self.search_line.text()
            for row in range(self.relic_table.rowCount()):
                item = self.relic_table.item(row, 0)
                if item.text().lower().find(keyword.lower()) != -1:
                    self.relic_table.setRowHidden(row, False)
                else:
                    self.relic_table.setRowHidden(row, True)
        else:
            for row in range(self.relic_table.rowCount()):
                item = self.relic_table.item(row, 3)
                if types == 'base':
                    if item.text() != 'base':
                        self.relic_table.setRowHidden(row, True)
                    else:
                        self.relic_table.setRowHidden(row, False)
                elif types == 'custom':
                    if item.text() != 'custom':
                        self.relic_table.setRowHidden(row, True)
                    else:
                        self.relic_table.setRowHidden(row, False)
    
    def search_entry(self, types):
        if types == 'line':
            keyword = self.entry_search_line.text()
            for row in range(self.entry_table.rowCount()):
                item = self.entry_table.item(row, 0)
                if item.text().lower().find(keyword.lower()) != -1:
                    self.entry_table.setRowHidden(row, False)
                else:
                    self.entry_table.setRowHidden(row, True)
        else:
            for row in range(self.entry_table.rowCount()):
                item = self.entry_table.item(row, 3)
                if types == 'main':
                    if item.text() != 'main':
                        self.entry_table.setRowHidden(row, True)
                    else:
                        self.entry_table.setRowHidden(row, False)
                    self.show_relic_entry()
                elif types =='side':
                    if item.text() !='side':
                        self.entry_table.setRowHidden(row, True)
                    else:
                        self.entry_table.setRowHidden(row, False)
    
    def move_to_right(self, types):
        selected_entry = self.entry_table.selectedItems()
        if selected_entry:
            selected_row = self.entry_table.currentRow()
            if self.entry_table.item(selected_row, 3).text() == 'main' and types == 'cell':
                self.now_entry_label.setText(selected_entry[0].text())
            elif self.entry_table.item(selected_row, 3).text() == 'side' and types == 'button':
                if len(self.now_entry_list) < 4:
                    entry_id = selected_entry[0].text()
                    if entry_id not in self.now_entry_list:
                        self.now_entry_list[entry_id] = 1
                    self.load_now_entry()

    def entry_num_changed(self, types):
        selected_entry = self.now_entry_table.selectedItems()
        if selected_entry:
            entry_name = selected_entry[0].text()
            if types == 'add':
                self.now_entry_list[entry_name] += 1
            elif types =='remove':
                if self.now_entry_list[entry_name] > 1:
                    self.now_entry_list[entry_name] -= 1
                else:
                    del self.now_entry_list[entry_name]
            elif types == 'delete':
                del self.now_entry_list[entry_name]

            selected_row = self.now_entry_table.currentRow()
            self.load_now_entry()
            self.now_entry_table.selectRow(selected_row)
    
    def show_relic_entry(self):
        selected_relic = self.relic_table.selectedItems()
        relic_type = selected_relic[1].text()
        for row in range(self.entry_table.rowCount()):
            if self.entry_table.item(row, 1).text() == relic_type:
                self.entry_table.setRowHidden(row, False)
            else:
                self.entry_table.setRowHidden(row, True)
        self.load_entry()

    def relic_clicked(self):
        selected_items = self.relic_table.selectedItems()
        if selected_items:
            relic_id = selected_items[2].text()
            self.emit_relic_id.emit(relic_id)