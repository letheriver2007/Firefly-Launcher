from typing import Union
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QVBoxLayout, QHBoxLayout, QButtonGroup
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtCore import Signal, Qt
from qfluentwidgets import (FluentIconBase, LineEdit, TogglePushButton, PrimaryPushButton, StrongBodyLabel,
                            TableWidget, SearchLineEdit, SettingCardGroup, SubtitleLabel, PrimaryToolButton)
from qfluentwidgets import FluentIcon as FIF
from app.model.setting_card import SettingCard


class Scene(QWidget):
    emit_scene_id = Signal(str)
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)

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
        self.setObjectName(text)

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
        self.setObjectName(text)

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
        self.button_all.setChecked(True)
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
    relic_id_signal = Signal(str)
    custom_relic_signal = Signal(str)
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)

        self.__initWidget()

    def __initWidget(self):
        # 遗物
        self.relic_search_line = SearchLineEdit(self)
        self.relic_search_line.setPlaceholderText("搜索遗器")
        self.relic_search_line.setFixedSize(238, 35)

        self.base_relic_button = TogglePushButton("基础", self)
        self.base_relic_button.setFixedSize(67, 35)
        self.custom_relic_button = TogglePushButton("预设", self)
        self.custom_relic_button.setFixedSize(67, 35)
        self.base_relic_button.setChecked(True)

        self.relic_type_button_group = QButtonGroup(self)
        self.relic_type_button_group.addButton(self.base_relic_button)
        self.relic_type_button_group.addButton(self.custom_relic_button)

        self.relic_table = TableWidget(self)
        self.relic_table.setColumnCount(4)
        self.relic_table.setFixedSize(385, 420)
        self.relic_table.setColumnWidth(0, 163)
        self.relic_table.setColumnWidth(1, 80)
        self.relic_table.setColumnWidth(2, 140)
        self.relic_table.setColumnWidth(3, 0) # 隐藏command列

        self.relic_table.setBorderVisible(True)
        self.relic_table.setBorderRadius(8)
        self.relic_table.setWordWrap(False)
        self.relic_table.verticalHeader().hide()
        self.relic_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.relic_table.setSelectionMode(QAbstractItemView.SingleSelection)

        # 词条
        self.entry_search_line = SearchLineEdit(self)
        self.entry_search_line.setPlaceholderText("搜索词条")
        self.entry_search_line.setFixedSize(180, 35)

        self.main_entry_button = TogglePushButton("主词条", self)
        self.side_entry_button = TogglePushButton("副词条", self)
        self.main_entry_button.setFixedSize(67, 35)
        self.side_entry_button.setFixedSize(67, 35)
        self.main_entry_button.setChecked(True)

        self.entry_type_button_group = QButtonGroup(self)
        self.entry_type_button_group.addButton(self.main_entry_button)
        self.entry_type_button_group.addButton(self.side_entry_button)

        self.entry_table = TableWidget(self)
        self.entry_table.setColumnCount(3)
        self.entry_table.setFixedSize(325, 420)
        self.entry_table.setColumnWidth(0, 168)
        self.entry_table.setColumnWidth(1, 80)
        self.entry_table.setColumnWidth(2, 75)

        self.entry_table.setBorderVisible(True)
        self.entry_table.setBorderRadius(8)
        self.entry_table.setWordWrap(False)
        self.entry_table.verticalHeader().hide()
        self.entry_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.entry_table.setSelectionMode(QAbstractItemView.SingleSelection)

        # 当前信息
        self.main_now_label = SubtitleLabel("当前主词条：", self)
        self.main_now_edit = LineEdit(self)
        self.main_now_edit.setReadOnly(True)
        self.side_now_label = SubtitleLabel("当前副词条：", self)

        self.now_table = TableWidget(self)
        self.now_table.setColumnCount(2)
        self.now_table.setFixedSize(365, 160)
        self.now_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.now_table.setBorderVisible(True)
        self.now_table.setWordWrap(False)
        self.now_table.setBorderRadius(8)
        self.now_table.verticalHeader().hide()
        self.now_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.now_table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.add_side_button = PrimaryToolButton(FIF.RIGHT_ARROW)
        self.add_side_button.setFixedSize(35, 35)
        self.add_num_button = PrimaryToolButton(FIF.ADD)
        self.add_num_button.setFixedSize(35, 35)
        self.minus_num_button = PrimaryToolButton(FIF.REMOVE)
        self.minus_num_button.setFixedSize(35, 35)
        self.set_num_edit = LineEdit(self)
        self.set_num_edit.setPlaceholderText("数量")
        self.set_num_edit.setFixedSize(55, 35)
        self.set_num_edit.setValidator(QIntValidator(1, 9999, self))
        self.set_num_button = PrimaryToolButton(FIF.SETTING)
        self.set_num_button.setFixedSize(35, 35)
        self.delete_num_button = PrimaryToolButton(FIF.DELETE)
        self.delete_num_button.setFixedSize(35, 35)

        self.level_label = SubtitleLabel("等级：", self)
        self.level_edit = LineEdit(self)
        self.level_edit.setPlaceholderText("请输入生成遗器的等级")
        self.level_edit.setValidator(QIntValidator(1, 99, self))

        self.__initLayout()
        self.__initInfo()
        self.__connectSignalToSlot()

    def __initLayout(self):
        # 遗物
        self.relic_button_layout = QHBoxLayout()
        self.relic_button_layout.addWidget(self.relic_search_line)
        self.relic_button_layout.addWidget(self.base_relic_button)
        self.relic_button_layout.addWidget(self.custom_relic_button)

        self.relic_layout = QVBoxLayout()
        self.relic_layout.addLayout(self.relic_button_layout)
        self.relic_layout.addWidget(self.relic_table)

        # 词条
        self.entry_button_layout = QHBoxLayout()
        self.entry_button_layout.addWidget(self.entry_search_line)
        self.entry_button_layout.addWidget(self.main_entry_button)
        self.entry_button_layout.addWidget(self.side_entry_button)
        self.entry_layout = QVBoxLayout()
        self.entry_layout.addLayout(self.entry_button_layout)
        self.entry_layout.addWidget(self.entry_table)

        # 当前信息
        self.now_layout = QVBoxLayout()
        self.now_layout.addSpacing(15)
        self.now_layout.addWidget(self.main_now_label)
        self.now_layout.addSpacing(5)
        self.now_layout.addWidget(self.main_now_edit)
        self.now_layout.addSpacing(20)
        self.now_layout.addWidget(self.side_now_label)
        self.now_layout.addSpacing(5)
        self.now_layout.addWidget(self.now_table)
        self.now_layout.addSpacing(14)

        self.now_tool_layout = QHBoxLayout()
        self.now_tool_layout.addWidget(self.add_side_button)
        self.now_tool_layout.addSpacing(67)
        self.now_tool_layout.addWidget(self.add_num_button)
        self.now_tool_layout.addSpacing(5)
        self.now_tool_layout.addWidget(self.minus_num_button)
        self.now_tool_layout.addSpacing(5)
        self.now_tool_layout.addWidget(self.set_num_edit)
        self.now_tool_layout.addSpacing(5)
        self.now_tool_layout.addWidget(self.set_num_button)
        self.now_tool_layout.addSpacing(5)
        self.now_tool_layout.addWidget(self.delete_num_button)

        self.now_layout.addLayout(self.now_tool_layout)
        self.now_layout.addSpacing(15)
        self.now_layout.addWidget(self.level_label)
        self.now_layout.addSpacing(5)
        self.now_layout.addWidget(self.level_edit)
        self.now_layout.addStretch(1)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.relic_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.entry_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.now_layout)
        self.setLayout(self.main_layout)

    def __initInfo(self):
        self.now_list = {}
        self.handleRelicTypeChanged()
        self.handleEntryLoad()
        self.handleNowLoad()

    def __connectSignalToSlot(self):
        self.relic_search_line.textChanged.connect(self.handleRelicSearch)
        self.base_relic_button.clicked.connect(self.handleRelicTypeChanged)
        self.custom_relic_button.clicked.connect(self.handleRelicTypeChanged)
        self.relic_table.cellClicked.connect(self.handleRelicTableClicked)

        self.entry_search_line.textChanged.connect(self.handleEntrySearch)
        self.main_entry_button.clicked.connect(self.handleEntryTypeChanged)
        self.side_entry_button.clicked.connect(self.handleEntryTypeChanged)
        self.entry_table.cellClicked.connect(self.handleEntryTableClicked)

        # 更新当前信息
        self.add_side_button.clicked.connect(self.handleAddSideClicked)
        self.add_side_button.clicked.connect(self.handleRelicSingal)
        self.add_num_button.clicked.connect(lambda: self.handleEntryNumChanged('add'))
        self.add_num_button.clicked.connect(self.handleRelicSingal)
        self.minus_num_button.clicked.connect(lambda: self.handleEntryNumChanged('remove'))
        self.minus_num_button.clicked.connect(self.handleRelicSingal)
        self.set_num_button.clicked.connect(lambda: self.handleEntryNumChanged('set'))
        self.delete_num_button.clicked.connect(lambda: self.handleEntryNumChanged('delete'))
        self.delete_num_button.clicked.connect(self.handleRelicSingal)

        self.main_now_edit.textChanged.connect(self.handleRelicSingal)
        self.level_edit.textChanged.connect(self.handleRelicSingal)

    # 信号
    def handleRelicSingal(self):
        selected_items = self.relic_table.selectedItems()
        if selected_items:
            if self.base_relic_button.isChecked():
                relic_id = selected_items[2].text()
                self.relic_id_signal.emit(relic_id)
            elif self.custom_relic_button.isChecked():
                command = selected_items[3].text()
                self.custom_relic_signal.emit(command)

    # 条件更新时切换显示状态相关
    def handleRelicSearch(self):
        keyword = self.relic_search_line.text()
        for row in range(self.relic_table.rowCount()):
            item_1 = self.relic_table.item(row, 0)
            item_2 = self.relic_table.item(row, 1)
            item_3 = self.relic_table.item(row, 2)
            iskeyword_1 = item_1 and item_1.text().lower().find(keyword.lower()) != -1
            iskeyword_2 = item_2 and item_2.text().lower().find(keyword.lower()) != -1
            iskeyword_3 = item_3 and item_3.text().lower().find(keyword.lower()) != -1
            if iskeyword_1 or iskeyword_2 or iskeyword_3:
                self.relic_table.setRowHidden(row, False)
            else:
                self.relic_table.setRowHidden(row, True)

    def handleEntrySearch(self):
        keyword = self.entry_search_line.text()
        for row in range(self.entry_table.rowCount()):
            item = self.entry_table.item(row, 0)
            if item.text().lower().find(keyword.lower()) != -1:
                self.entry_table.setRowHidden(row, False)
            else:
                self.entry_table.setRowHidden(row, True)

    def handleRelicTypeChanged(self):
        self.relic_search_line.clear()
        self.relic_table.clearSelection()
        self.entry_table.clearSelection()
        self.now_table.clearSelection()

        selected_base_relic = self.base_relic_button.isChecked()
        if selected_base_relic:
            self.handleBaseRelicLoad()
            self.handleEntryLoad()
            self.handleNowLoad()
        else:
            self.entry_table.clearContents()
            self.now_table.clearContents()
            self.handleCustomRelicLoad()

        layouts = [self.entry_layout, self.entry_button_layout, self.now_layout, self.now_tool_layout]
        for layout in layouts:
            for i in range(layout.count()):
                widget = layout.itemAt(i).widget()
                if widget is not None:
                    if selected_base_relic:
                        widget.setDisabled(False)
                    else:
                        widget.setDisabled(True)

    def handleEntryTypeChanged(self):
        selected_main_entry = self.main_entry_button.isChecked()
        for row in range(self.entry_table.rowCount()):
            entry_type = self.entry_table.item(row, 1).text()
            if selected_main_entry:
                if entry_type == '通用':
                    self.entry_table.setRowHidden(row, True)
                else:
                    self.entry_table.setRowHidden(row, False)
                self.__handleRelatedEntryUpdate()
            else:
                if entry_type == '通用':
                    self.entry_table.setRowHidden(row, False)
                else:
                    self.entry_table.setRowHidden(row, True)

    # 信息更新行为相关
    def handleRelicTableClicked(self):
        self.handleRelicSingal()
        self.__handleRelatedEntryUpdate()
        if self.base_relic_button.isChecked():
            self.main_now_edit.setText('')
    
    def handleEntryTableClicked(self):
        selected_entry = self.entry_table.selectedItems()
        selected_entry_type = self.entry_table.item(self.entry_table.currentRow(), 1).text()
        if selected_entry and selected_entry_type != '通用':
            self.main_now_edit.setText(selected_entry[0].text())

    def handleAddSideClicked(self):
        selected_side_entry = self.side_entry_button.isChecked()
        if selected_side_entry:
            selected_entry = self.entry_table.selectedItems()
            selected_entry_type = self.entry_table.item(self.entry_table.currentRow(), 1).text()
            entry_id = selected_entry[0].text()
            if selected_entry and selected_entry_type == '通用' and len(self.now_list) < 4 and entry_id not in self.now_list:
                self.now_list[entry_id] = 1
                self.handleNowLoad()

    def handleEntryNumChanged(self, types):
        selected_now = self.now_table.selectedItems()
        if selected_now:
            entry_name = selected_now[0].text()
            if types == 'add':
                self.now_list[entry_name] += 1
            elif types =='remove':
                if self.now_list[entry_name] > 1:
                    self.now_list[entry_name] -= 1
                else:
                    del self.now_list[entry_name]
            elif types =='set':
                num = int(self.set_num_edit.text())
                if num > 0:
                    self.now_list[entry_name] = num
                else:
                    del self.now_list[entry_name]
            elif types == 'delete':
                del self.now_list[entry_name]

            # 保存行数，在表格更新后仍然选中(支持连续更改)
            selected_row = self.now_table.currentRow()
            self.handleNowLoad()
            self.now_table.selectRow(selected_row)

    # 读取和加载页面信息相关
    def handleBaseRelicLoad(self):
        with open('src/data/relic.txt', 'r', encoding='utf-8') as file:
            relic = [line for line in file.readlines() if not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.relic_table.setRowCount(len(relic))
        for i, line in enumerate(relic):
            parts = line.split()
            self.relic_table.setRowHeight(i, 39)
            for j, part in enumerate(parts):
                self.relic_table.setItem(i, j, QTableWidgetItem(part))
        self.relic_table.setHorizontalHeaderLabels(['遗器名称', '部位', 'ID'])

    def handleCustomRelicLoad(self):
        with open('src/data/myrelic.txt', 'r', encoding='utf-8') as file:
            relic = [line for line in file.readlines() if not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.relic_table.setRowCount(len(relic))
        for i, line in enumerate(relic):
            parts = line.split()
            self.relic_table.setRowHeight(i, 39)
            for j, part in enumerate(parts):
                if j == 3:
                    item = ' '.join(parts[3:])
                    self.relic_table.setItem(i, j, QTableWidgetItem(item))
                    break
                else:
                    self.relic_table.setItem(i, j, QTableWidgetItem(part))
        self.relic_table.setHorizontalHeaderLabels(['遗器名称', '部位', '适用角色', 'command'])

    def handleEntryLoad(self):
        with open('src/data/entry.txt', 'r', encoding='utf-8') as file:
            entry = [line for line in file.readlines() if not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.entry_table.setRowCount(len(entry))
        for i, line in enumerate(entry):
            parts = line.split()
            self.entry_table.setRowHeight(i, 39)
            for j, part in enumerate(parts):
                self.entry_table.setItem(i, j, QTableWidgetItem(part))
        self.entry_table.setHorizontalHeaderLabels(['词条名称', '部位', 'ID'])

    def handleNowLoad(self):
        self.now_table.clearContents()
        self.now_table.setRowCount(len(self.now_list))
        for row, (key, value) in enumerate(self.now_list.items()):
            self.now_table.setRowHeight(row, 30)
            self.now_table.setItem(row, 0, QTableWidgetItem(key))
            self.now_table.setItem(row, 1, QTableWidgetItem(str(value)))
        self.now_table.setHorizontalHeaderLabels(['词条名称', '数量'])

    # 遗器条件更新时，更新对应词条
    def __handleRelatedEntryUpdate(self):
        selected_relic = self.relic_table.selectedItems()
        if selected_relic and self.base_relic_button.isChecked():
            self.main_entry_button.setChecked(True)
            relic_type = selected_relic[1].text()
            for row in range(self.entry_table.rowCount()):
                if self.entry_table.item(row, 1).text() == relic_type:
                    self.entry_table.setRowHidden(row, False)
                else:
                    self.entry_table.setRowHidden(row, True)
            self.handleEntryLoad()