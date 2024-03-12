from typing import Union
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QVBoxLayout, QHBoxLayout, QButtonGroup
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtCore import Signal, Qt
from qfluentwidgets import FluentIconBase, LineEdit, TogglePushButton, PrimaryPushButton, TableWidget, SearchLineEdit, SettingCardGroup, SubtitleLabel
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
        self.scene_layout.addSpacing(20)
        self.scene_layout.addWidget(self.search_line)
        self.scene_layout.addSpacing(20)
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
        self.search_line.setFixedSize(925, 35)
        self.spawn_table = TableWidget(self)
        self.spawn_table.setFixedSize(925, 420)
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
        self.search_line.setFixedSize(925, 35)
        self.give_table = TableWidget(self)
        self.give_table.setFixedSize(925, 420)
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