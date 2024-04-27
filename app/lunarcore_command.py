import os
import shutil
from PySide6.QtWidgets import (QWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
                               QVBoxLayout, QHBoxLayout, QButtonGroup)
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Signal, Qt
from qfluentwidgets import (LineEdit, TogglePushButton, PrimaryPushButton, ComboBox, FluentIcon,
                            TableWidget, SearchLineEdit, SubtitleLabel, PrimaryToolButton)
from app.model.setting_card import SettingCard
from app.model.config import cfg, Info


class Account(SettingCard):
    create_account = Signal()
    delete_account = Signal()

    def __init__(self, title, icon=FluentIcon.TAG, content='/account {create | delete} [username]'):
        super().__init__(icon, title, content)
        self.account_name = LineEdit(self)
        self.account_uid = LineEdit(self)
        self.button_create = PrimaryPushButton(self.tr('添加'), self)
        self.button_delete = PrimaryPushButton(self.tr('删除'), self)
        self.account_name.setPlaceholderText(self.tr("名称"))
        self.account_uid.setPlaceholderText("UID")
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


class Kick(SettingCard):
    kick_player = Signal()

    def __init__(self, title, icon=FluentIcon.TAG, content='/kick @[player id]'):
        super().__init__(icon, title, content)
        self.account_uid = LineEdit(self)
        self.account_uid.setPlaceholderText("UID")
        self.account_uid.setValidator(QIntValidator(self))
        self.button_kick = PrimaryPushButton(self.tr('使用'), self)
        self.hBoxLayout.addWidget(self.account_uid, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_kick, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_kick.clicked.connect(self.kick_player)


class Unstuck(SettingCard):
    unstuck_player = Signal()

    def __init__(self, title, icon=FluentIcon.TAG, content='/unstuck @[player id]'):
        super().__init__(icon, title, content)
        self.stuck_uid = LineEdit(self)
        self.stuck_uid.setPlaceholderText("UID")
        self.stuck_uid.setValidator(QIntValidator(self))
        self.button_unstuck = PrimaryPushButton(self.tr('使用'), self)
        self.hBoxLayout.addWidget(self.stuck_uid, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_unstuck, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_unstuck.clicked.connect(self.unstuck_player)


class Custom(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)
        self.parent = parent

        self.__initWidget()

    def __initWidget(self):
        self.mycommand_search_line = SearchLineEdit(self)
        self.mycommand_search_line.setPlaceholderText(self.tr("搜索自定义命令"))
        self.mycommand_search_line.setFixedHeight(35)

        self.default_button = PrimaryPushButton(self.tr('恢复默认'), self)
        self.default_button.setFixedSize(100, 35)

        self.mycommand_table = TableWidget(self)
        self.mycommand_table.setFixedSize(1140, 420)
        self.mycommand_table.setColumnCount(2)

        self.mycommand_table.setBorderVisible(True)
        self.mycommand_table.setBorderRadius(8)
        self.mycommand_table.setWordWrap(False)
        self.mycommand_table.verticalHeader().hide()
        self.mycommand_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.mycommand_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.mycommand_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.__initLayout()
        self.__initInfo()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.line_layout = QHBoxLayout()
        self.line_layout.addWidget(self.mycommand_search_line)
        self.line_layout.addSpacing(5)
        self.line_layout.addWidget(self.default_button)

        self.mycommand_layout = QVBoxLayout()
        self.mycommand_layout.addLayout(self.line_layout)
        self.mycommand_layout.addWidget(self.mycommand_table)
        self.setLayout(self.mycommand_layout)

    def __initInfo(self):
        self.handleMycommandLoad()

    def __connectSignalToSlot(self):
        self.mycommand_search_line.textChanged.connect(self.handleMycommandSearch)
        self.default_button.clicked.connect(self.handleDefaultClicked)

        self.mycommand_table.cellClicked.connect(lambda: self.handleMycommandClicked('single'))
        self.mycommand_table.doubleClicked.connect(lambda: self.handleMycommandClicked('double'))
        self.mycommand_table.itemChanged.connect(self.handleNameChanged)

    def handleMycommandSearch(self):
        keyword = self.mycommand_search_line.text()
        for row in range(self.mycommand_table.rowCount()):
            item_1 = self.mycommand_table.item(row, 0)
            item_2 = self.mycommand_table.item(row, 1)
            iskeyword_1 = item_1.text().lower().find(keyword.lower()) != -1
            iskeyword_2 = item_2.text().lower().find(keyword.lower()) != -1
            if iskeyword_1 or iskeyword_2:
                self.mycommand_table.setRowHidden(row, False)
            else:
                self.mycommand_table.setRowHidden(row, True)

    def handleDefaultClicked(self):
        shutil.copy('src/data/mycommand-default.txt', 'src/data/mycommand.txt')
        Info(self.parent, 'S', 1000, self.tr('恢复默认成功！'))
        self.handleMycommandLoad()

    def handleMycommandClicked(self, types):
        row = self.mycommand_table.currentRow()
        column = self.mycommand_table.currentColumn()
        if types == 'single':
            if column == 0:
                self.mycommand_table.editItem(self.mycommand_table.item(row, 0))
            elif column == 1:
                command = self.mycommand_table.item(row, 1).text()
                self.parent.command_update.emit(command)
        elif types == 'double':
            self.mycommand_table.removeRow(row)
            with open(f'src/data/mycommand.txt', 'r', encoding='utf-8') as file:
                mycommand = file.readlines()
            with open(f'src/data/mycommand.txt', 'w', encoding='utf-8') as file:
                for i, line in enumerate(mycommand):
                    if i != row:
                        file.write(line)

    def handleNameChanged(self):
        selected_item = self.mycommand_table.selectedItems()
        if selected_item:
            rows = self.mycommand_table.rowCount()
            column = self.mycommand_table.currentColumn()
            if column == 0 and selected_item[0].text().strip() == '':
                selected_item[0].setText(self.tr('自定义命令'))
            data = []
            # 临时解决NoneType问题
            try:
                for row in range(rows):
                    first_col = self.mycommand_table.item(row, 0).text()
                    second_col = self.mycommand_table.item(row, 1).text()
                    data_row = f"{first_col} : {second_col}\n"
                    data.append(data_row)
                with open('src/data/mycommand.txt', 'w', encoding='utf-8') as file:
                    file.writelines(data)
            except:
                pass

    def handleMycommandLoad(self):
        self.mycommand_table.clearFocus()
        if not os.path.exists('src/data/mycommand.txt'):
            shutil.copy('src/data/mycommand-default.txt', 'src/data/mycommand.txt')

        with open(f'src/data/mycommand.txt', 'r', encoding='utf-8') as file:
            mycommand = file.readlines()
        self.mycommand_table.setRowCount(len(mycommand))
        for i, line in enumerate(mycommand):
            line = line.strip()
            parts = line.split(' : ')
            for j, part in enumerate(parts):
                self.mycommand_table.setItem(i, j, QTableWidgetItem(part))
        self.mycommand_table.setHorizontalHeaderLabels([self.tr('名称'), self.tr('命令')])


class Giveall(SettingCard):
    giveall_clicked = Signal(int)

    def __init__(self, title, icon=FluentIcon.TAG, content='/giveall {materials | avatars | lightcones | relics | icons}'):
        super().__init__(icon, title, content)
        self.texts = [self.tr('材料'), self.tr('角色'), self.tr('光锥'), self.tr('遗器'), self.tr('图标')]
        self.comboBox = ComboBox(self)
        self.comboBox.setPlaceholderText(self.tr('选择物品'))
        self.comboBox.addItems(self.texts)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.comboBox.setCurrentIndex(-1)
        self.comboBox.currentIndexChanged.connect(self.onSignalEmit)

    def onSignalEmit(self, index: int):
        self.giveall_clicked.emit(index)


class Clear(SettingCard):
    clear_clicked = Signal(int)

    def __init__(self, title, icon=FluentIcon.TAG, content='/clear {relics | lightcones | materials | all}'):
        super().__init__(icon, title, content)
        self.texts = [self.tr('遗器'), self.tr('光锥'), self.tr('材料'), self.tr('全部')]
        self.comboBox = ComboBox(self)
        self.comboBox.setPlaceholderText(self.tr('选择物品'))
        self.comboBox.addItems(self.texts)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.comboBox.setCurrentIndex(-1)
        self.comboBox.currentIndexChanged.connect(self.onSignalEmit)

    def onSignalEmit(self, index: int):
        self.clear_clicked.emit(index)


class WorldLevel(SettingCard):
    set_world_level = Signal(int)

    def __init__(self, title, icon=FluentIcon.TAG, content='/level [trailblaze level] || /worldlevel [world level]'):
        super().__init__(icon, title, content)
        self.texts = [self.tr('开拓'), self.tr('均衡')]
        self.world_types = ComboBox(self)
        self.world_types.setPlaceholderText(self.tr('类型'))
        self.world_types.addItems(self.texts)
        self.world_types.setCurrentIndex(-1)

        self.world_level = LineEdit(self)
        self.world_level.setPlaceholderText(self.tr("世界等级"))
        validator = QIntValidator(1, 99, self)
        self.world_level.setValidator(validator)

        self.hBoxLayout.addWidget(self.world_types, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.world_level, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.world_level.textChanged.connect(self.onSignalEmit)
        self.world_types.currentIndexChanged.connect(self.onSignalEmit)

    def onSignalEmit(self):
        index = self.world_types.currentIndex()
        self.set_world_level.emit(index)


class Avatar(SettingCard):
    avatar_set = Signal(int)

    def __init__(self, title, icon=FluentIcon.TAG, content='/avatar [lv(level)] [r(eidolon)] [s(skill level)]'):
        super().__init__(icon, title, content)
        self.avatar_level = LineEdit(self)
        self.avatar_eidolon = LineEdit(self)
        self.avatar_skill = LineEdit(self)
        self.avatar_level.setPlaceholderText(self.tr("等级"))
        self.avatar_eidolon.setPlaceholderText(self.tr("星魂"))
        self.avatar_skill.setPlaceholderText(self.tr("行迹"))
        validator = QIntValidator(1, 99, self)
        self.avatar_level.setValidator(validator)
        self.avatar_eidolon.setValidator(validator)
        self.avatar_skill.setValidator(validator)

        self.texts = [self.tr('当前'), self.tr('队伍'), self.tr('全部')]
        self.avatar_types = ComboBox(self)
        self.avatar_types.setPlaceholderText(self.tr('应用范围'))
        self.avatar_types.addItems(self.texts)
        self.avatar_types.setCurrentIndex(-1)

        self.hBoxLayout.addWidget(self.avatar_level, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.avatar_eidolon, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.avatar_skill, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.avatar_types, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.avatar_level.textChanged.connect(lambda: self.onSignalEmit(-1))
        self.avatar_eidolon.textChanged.connect(lambda: self.onSignalEmit(-1))
        self.avatar_skill.textChanged.connect(lambda: self.onSignalEmit(-1))
        self.avatar_types.currentIndexChanged.connect(lambda index: self.onSignalEmit(index))

    def onSignalEmit(self, index: int):
        self.avatar_set.emit(index)


class Gender(SettingCard):
    gender_male = Signal()
    gender_female = Signal()

    def __init__(self, title, icon=FluentIcon.TAG, content='/gender {male | female}'):
        super().__init__(icon, title, content)
        self.button_male = PrimaryPushButton(self.tr('星'), self)
        self.button_female = PrimaryPushButton(self.tr('穹'), self)
        self.hBoxLayout.addWidget(self.button_male, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_female, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_male.clicked.connect(self.gender_male)
        self.button_female.clicked.connect(self.gender_female)


class Scene(QWidget):
    scene_id_signal = Signal(str)

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)

        self.__initWidget()

    def __initWidget(self):
        self.scene_search_line = SearchLineEdit(self)
        self.scene_search_line.setPlaceholderText(self.tr("搜索场景"))
        self.scene_search_line.setFixedHeight(35)

        self.scene_table = TableWidget(self)
        self.scene_table.setFixedSize(1140, 420)
        self.scene_table.setColumnCount(2)

        self.scene_table.setBorderVisible(True)
        self.scene_table.setBorderRadius(8)
        self.scene_table.setWordWrap(False)
        self.scene_table.verticalHeader().hide()
        self.scene_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.scene_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.scene_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.__initLayout()
        self.__initInfo()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.scene_layout = QVBoxLayout()
        self.scene_layout.addWidget(self.scene_search_line)
        self.scene_layout.addWidget(self.scene_table)
        self.setLayout(self.scene_layout)

    def __initInfo(self):
        self.handleSceneLoad()

    def __connectSignalToSlot(self):
        self.scene_search_line.textChanged.connect(self.handleSceneSearch)
        self.scene_table.cellClicked.connect(self.handleSceneSignal)

    def handleSceneSignal(self, row):
        item = self.scene_table.item(row, 1)
        scene_id = item.text()
        self.scene_id_signal.emit(scene_id)

    def handleSceneSearch(self):
        keyword = self.scene_search_line.text()
        for row in range(self.scene_table.rowCount()):
            item_1 = self.scene_table.item(row, 0)
            item_2 = self.scene_table.item(row, 1)
            iskeyword_1 = item_1.text().lower().find(keyword.lower()) != -1
            iskeyword_2 = item_2.text().lower().find(keyword.lower()) != -1
            if iskeyword_1 or iskeyword_2:
                self.scene_table.setRowHidden(row, False)
            else:
                self.scene_table.setRowHidden(row, True)

    def handleSceneLoad(self):
        with open(f'src/data/{cfg.get(cfg.language).value.name()}/scene.txt', 'r', encoding='utf-8') as file:
            scene = [line for line in file.readlines() if
                     not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.scene_table.setRowCount(len(scene))
        for i, line in enumerate(scene):
            line = line.strip()
            parts = line.split(' : ')
            parts[0], parts[1] = parts[1], parts[0]
            scene[i] = ' : '.join(parts)
            for j, part in enumerate(parts):
                self.scene_table.setItem(i, j, QTableWidgetItem(part))
        self.scene_table.setHorizontalHeaderLabels([self.tr('场景描述'), 'ID'])


class Spawn(QWidget):
    monster_id_signal = Signal(str, str)

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)

        self.__initWidget()

    def __initWidget(self):
        self.monster_num_label = SubtitleLabel(self.tr("数量:"), self)
        self.monster_num_edit = LineEdit(self)
        self.monster_num_edit.setPlaceholderText(self.tr("请输入怪物数量"))
        self.monster_num_edit.setValidator(QIntValidator(1, 99, self))

        self.monster_level_label = SubtitleLabel(self.tr("等级:"), self)
        self.monster_level_edit = LineEdit(self)
        self.monster_level_edit.setPlaceholderText(self.tr("请输入怪物等级"))
        self.monster_level_edit.setValidator(QIntValidator(1, 99, self))

        self.monster_round_label = SubtitleLabel(self.tr("半径:"), self)
        self.monster_round_edit = LineEdit(self)
        self.monster_round_edit.setPlaceholderText(self.tr("请输入仇恨半径"))
        self.monster_round_edit.setValidator(QIntValidator(1, 99, self))

        self.monster_search_line = SearchLineEdit(self)
        self.monster_search_line.setPlaceholderText(self.tr("搜索显示怪物"))
        self.monster_search_line.setFixedSize(455, 35)

        self.monster_table = TableWidget(self)
        self.monster_table.setFixedSize(455, 420)
        self.monster_table.setColumnCount(2)

        self.monster_table.setBorderVisible(True)
        self.monster_table.setBorderRadius(8)
        self.monster_table.setWordWrap(False)
        self.monster_table.verticalHeader().hide()
        self.monster_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.monster_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.monster_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.stage_search_line = SearchLineEdit(self)
        self.stage_search_line.setPlaceholderText(self.tr("搜索局内怪物"))
        self.stage_search_line.setFixedSize(455, 35)

        self.stage_table = TableWidget(self)
        self.stage_table.setFixedSize(455, 420)
        self.stage_table.setColumnCount(2)

        self.stage_table.setBorderVisible(True)
        self.stage_table.setBorderRadius(8)
        self.stage_table.setWordWrap(False)
        self.stage_table.verticalHeader().hide()
        self.stage_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.stage_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.stage_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.__initLayout()
        self.__initInfo()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.monster_layout = QVBoxLayout()
        self.monster_layout.addWidget(self.monster_search_line)
        self.monster_layout.addWidget(self.monster_table)
        self.stage_layout = QVBoxLayout()
        self.stage_layout.addWidget(self.stage_search_line)
        self.stage_layout.addWidget(self.stage_table)

        self.set_layout = QVBoxLayout()
        self.set_layout.addSpacing(70)
        self.set_layout.addWidget(self.monster_num_label)
        self.set_layout.addSpacing(5)
        self.set_layout.addWidget(self.monster_num_edit)
        self.set_layout.addSpacing(20)
        self.set_layout.addWidget(self.monster_level_label)
        self.set_layout.addSpacing(5)
        self.set_layout.addWidget(self.monster_level_edit)
        self.set_layout.addSpacing(20)
        self.set_layout.addWidget(self.monster_round_label)
        self.set_layout.addSpacing(5)
        self.set_layout.addWidget(self.monster_round_edit)
        self.set_layout.addStretch(1)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.monster_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.stage_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.set_layout)
        self.setLayout(self.main_layout)

    def __initInfo(self):
        self.handleMonsterLoad()
        self.handleStageLoad()

    def __connectSignalToSlot(self):
        self.monster_search_line.textChanged.connect(self.handleMonsterSearch)
        self.monster_table.cellClicked.connect(self.handleSpawnSignal)
        self.stage_search_line.textChanged.connect(self.handleStageSearch)
        self.stage_table.cellClicked.connect(self.handleSpawnSignal)

        self.monster_num_edit.textChanged.connect(self.handleSpawnSignal)
        self.monster_level_edit.textChanged.connect(self.handleSpawnSignal)
        self.monster_round_edit.textChanged.connect(self.handleSpawnSignal)

    def handleSpawnSignal(self):
        selected_monster = self.monster_table.selectedItems()
        selected_stage = self.stage_table.selectedItems()
        if selected_monster and selected_stage:
            monster_id = selected_monster[1].text()
            stage_id = selected_stage[1].text()
            self.monster_id_signal.emit(monster_id, stage_id)

    def handleMonsterSearch(self):
        keyword = self.monster_search_line.text()
        for row in range(self.monster_table.rowCount()):
            item_1 = self.monster_table.item(row, 0)
            item_2 = self.monster_table.item(row, 1)
            iskeyword_1 = item_1.text().lower().find(keyword.lower()) != -1
            iskeyword_2 = item_2.text().lower().find(keyword.lower()) != -1
            if iskeyword_1 or iskeyword_2:
                self.monster_table.setRowHidden(row, False)
            else:
                self.monster_table.setRowHidden(row, True)

    def handleStageSearch(self):
        keyword = self.stage_search_line.text()
        for row in range(self.stage_table.rowCount()):
            item_1 = self.stage_table.item(row, 0)
            item_2 = self.stage_table.item(row, 1)
            iskeyword_1 = item_1.text().lower().find(keyword.lower()) != -1
            iskeyword_2 = item_2.text().lower().find(keyword.lower()) != -1
            if iskeyword_1 or iskeyword_2:
                self.stage_table.setRowHidden(row, False)
            else:
                self.stage_table.setRowHidden(row, True)

    def handleMonsterLoad(self):
        with open(f'src/data/{cfg.get(cfg.language).value.name()}/monster.txt', 'r', encoding='utf-8') as file:
            monster = [line for line in file.readlines() if
                     not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.monster_table.setRowCount(len(monster))
        for i, line in enumerate(monster):
            line = line.strip()
            parts = line.split(' : ')
            parts[0], parts[1] = parts[1], parts[0]
            monster[i] = ' : '.join(parts)
            for j, part in enumerate(parts):
                self.monster_table.setItem(i, j, QTableWidgetItem(part))
        self.monster_table.setHorizontalHeaderLabels([self.tr('显示怪物名称'), 'ID'])

    def handleStageLoad(self):
        with open(f'src/data/{cfg.get(cfg.language).value.name()}/stage.txt', 'r', encoding='utf-8') as file:
            stage = [line for line in file.readlines() if
                     not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.stage_table.setRowCount(len(stage))
        for i, line in enumerate(stage):
            line = line.strip()
            parts = line.split(' : ')
            parts[0], parts[1] = parts[1], parts[0]
            stage[i] = ' : '.join(parts)
            for j, part in enumerate(parts):
                self.stage_table.setItem(i, j, QTableWidgetItem(part))
        self.stage_table.setHorizontalHeaderLabels([self.tr('局内怪物名称'), 'ID'])


class Give(QWidget):
    item_id_signal = Signal(str, int)

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)

        self.__initWidget()

    def __initWidget(self):
        self.give_search_line = SearchLineEdit(self)
        self.give_search_line.setPlaceholderText(self.tr("搜索物品"))
        self.give_search_line.setFixedSize(804, 35)
        self.give_combobox = ComboBox(self)
        self.give_combobox.setFixedSize(100, 35)
        self.give_combobox.addItems(
            [self.tr("角色"), self.tr("光锥"), self.tr("物品"), self.tr("食物"), self.tr("头像")])

        self.give_table = TableWidget(self)
        self.give_table.setFixedSize(915, 420)
        self.give_table.setColumnCount(2)
        self.give_table.setColumnWidth(0, 613)
        self.give_table.setColumnWidth(1, 300)

        self.give_table.setBorderVisible(True)
        self.give_table.setBorderRadius(8)
        self.give_table.setWordWrap(False)
        self.give_table.verticalHeader().hide()
        self.give_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.give_table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.give_num_label = SubtitleLabel(self.tr("数量:"), self)
        self.give_num_edit = LineEdit(self)
        self.give_num_edit.setPlaceholderText(self.tr("请输入物品数量"))
        self.give_num_edit.setValidator(QIntValidator(self))

        self.give_level_label = SubtitleLabel(self.tr("等级:"), self)
        self.give_level_edit = LineEdit(self)
        self.give_level_edit.setPlaceholderText(self.tr("请输入等级"))
        self.give_level_edit.setValidator(QIntValidator(1, 99, self))

        self.give_eidolon_label = SubtitleLabel(self.tr("星魂/叠影:"), self)
        self.give_eidolon_edit = LineEdit(self)
        self.give_eidolon_edit.setPlaceholderText(self.tr("请输入星魂/叠影"))
        self.give_eidolon_edit.setValidator(QIntValidator(1, 9, self))

        self.__initLayout()
        self.__initInfo()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.give_line_layout = QHBoxLayout()
        self.give_line_layout.addWidget(self.give_search_line)
        self.give_line_layout.addSpacing(5)
        self.give_line_layout.addWidget(self.give_combobox)
        self.give_layout = QVBoxLayout()
        self.give_layout.addLayout(self.give_line_layout)
        self.give_layout.addWidget(self.give_table)

        self.set_layout = QVBoxLayout()
        self.set_layout.addSpacing(70)
        self.set_layout.addWidget(self.give_num_label)
        self.set_layout.addSpacing(5)
        self.set_layout.addWidget(self.give_num_edit)
        self.set_layout.addSpacing(20)
        self.set_layout.addWidget(self.give_level_label)
        self.set_layout.addSpacing(5)
        self.set_layout.addWidget(self.give_level_edit)
        self.set_layout.addSpacing(20)
        self.set_layout.addWidget(self.give_eidolon_label)
        self.set_layout.addSpacing(5)
        self.set_layout.addWidget(self.give_eidolon_edit)
        self.set_layout.addStretch(1)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.give_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.set_layout)
        self.setLayout(self.main_layout)

    def __initInfo(self):
        self.handleAvatarLoad()

    def __connectSignalToSlot(self):
        self.give_search_line.textChanged.connect(self.handleGiveSearch)
        self.give_table.cellClicked.connect(self.handleGiveSignal)
        self.give_combobox.currentIndexChanged.connect(lambda index: self.handleGiveTypeChanged(index))

        self.give_num_edit.textChanged.connect(self.handleGiveSignal)
        self.give_level_edit.textChanged.connect(self.handleGiveSignal)
        self.give_eidolon_edit.textChanged.connect(self.handleGiveSignal)

    def handleGiveSignal(self):
        selected_items = self.give_table.selectedItems()
        index = self.give_combobox.currentIndex()
        if selected_items:
            item_id = selected_items[1].text()
            self.item_id_signal.emit(item_id, index)

    def handleGiveSearch(self):
        keyword = self.give_search_line.text()
        for row in range(self.give_table.rowCount()):
            item_1 = self.give_table.item(row, 0)
            item_2 = self.give_table.item(row, 1)
            iskeyword_1 = item_1.text().lower().find(keyword.lower()) != -1
            iskeyword_2 = item_2.text().lower().find(keyword.lower()) != -1
            if iskeyword_1 or iskeyword_2:
                self.give_table.setRowHidden(row, False)
            else:
                self.give_table.setRowHidden(row, True)

    def handleGiveTypeChanged(self, index):
        interface = [
            self.handleAvatarLoad, self.handleLightconeLoad,
            self.handleItemLoad, self.handleFoodLoad, self.handleHeadLoad
        ]
        interface[index]()

    def handleAvatarLoad(self):
        with open(f'src/data/{cfg.get(cfg.language).value.name()}/avatar.txt', 'r', encoding='utf-8') as file:
            avatar = [line for line in file.readlines() if
                     not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.give_table.setRowCount(len(avatar))
        for i, line in enumerate(avatar):
            line = line.strip()
            parts = line.split(' : ')
            parts[0], parts[1] = parts[1], parts[0]
            avatar[i] = ' : '.join(parts)
            for j, part in enumerate(parts):
                self.give_table.setItem(i, j, QTableWidgetItem(part))
        self.give_table.setHorizontalHeaderLabels([self.tr('角色名称'), 'ID'])

    def handleLightconeLoad(self):
        with open(f'src/data/{cfg.get(cfg.language).value.name()}/lightcone.txt', 'r', encoding='utf-8') as file:
            lightcone = [line for line in file.readlines() if
                     not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.give_table.setRowCount(len(lightcone))
        for i, line in enumerate(lightcone):
            line = line.strip()
            parts = line.split(' : ')
            parts[0], parts[1] = parts[1], parts[0]
            lightcone[i] = ' : '.join(parts)
            for j, part in enumerate(parts):
                self.give_table.setItem(i, j, QTableWidgetItem(part))
        self.give_table.setHorizontalHeaderLabels([self.tr('光锥名称'), 'ID'])

    def handleItemLoad(self):
        with open(f'src/data/{cfg.get(cfg.language).value.name()}/item.txt', 'r', encoding='utf-8') as file:
            item = [line for line in file.readlines() if
                     not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.give_table.setRowCount(len(item))
        for i, line in enumerate(item):
            line = line.strip()
            parts = line.split(' : ')
            parts[0], parts[1] = parts[1], parts[0]
            item[i] = ' : '.join(parts)
            for j, part in enumerate(parts):
                self.give_table.setItem(i, j, QTableWidgetItem(part))
        self.give_table.setHorizontalHeaderLabels([self.tr('物品名称'), 'ID'])

    def handleFoodLoad(self):
        with open(f'src/data/{cfg.get(cfg.language).value.name()}/food.txt', 'r', encoding='utf-8') as file:
            food = [line for line in file.readlines() if
                     not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.give_table.setRowCount(len(food))
        for i, line in enumerate(food):
            line = line.strip()
            parts = line.split(' : ')
            parts[0], parts[1] = parts[1], parts[0]
            food[i] = ' : '.join(parts)
            for j, part in enumerate(parts):
                self.give_table.setItem(i, j, QTableWidgetItem(part))
        self.give_table.setHorizontalHeaderLabels([self.tr('食物名称'), 'ID'])

    def handleHeadLoad(self):
        with open(f'src/data/{cfg.get(cfg.language).value.name()}/head.txt', 'r', encoding='utf-8') as file:
            head = [line for line in file.readlines() if
                     not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.give_table.setRowCount(len(head))
        for i, line in enumerate(head):
            line = line.strip()
            parts = line.split(' : ')
            parts[0], parts[1] = parts[1], parts[0]
            head[i] = ' : '.join(parts)
            for j, part in enumerate(parts):
                self.give_table.setItem(i, j, QTableWidgetItem(part))
        self.give_table.setHorizontalHeaderLabels([self.tr('头像名称'), 'ID'])


class Relic(QWidget):
    relic_id_signal = Signal(str)
    custom_relic_signal = Signal(str)

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)

        self.__initWidget()

    def __initWidget(self):
        # 遗器
        self.relic_search_line = SearchLineEdit(self)
        self.relic_search_line.setPlaceholderText(self.tr("搜索遗器"))
        self.relic_search_line.setFixedSize(258, 35)

        self.base_relic_button = TogglePushButton(self.tr("基础"), self)
        self.base_relic_button.setFixedSize(67, 35)
        self.custom_relic_button = TogglePushButton(self.tr("预设"), self)
        self.custom_relic_button.setFixedSize(67, 35)
        self.base_relic_button.setChecked(True)

        self.relic_type_button_group = QButtonGroup(self)
        self.relic_type_button_group.addButton(self.base_relic_button)
        self.relic_type_button_group.addButton(self.custom_relic_button)

        self.relic_table = TableWidget(self)
        self.relic_table.setColumnCount(4)
        self.relic_table.setFixedSize(405, 420)
        self.relic_table.setColumnWidth(0, 190)
        self.relic_table.setColumnWidth(1, 78)
        self.relic_table.setColumnWidth(2, 135)
        self.relic_table.setColumnWidth(3, 0)  # 隐藏command列

        self.relic_table.setBorderVisible(True)
        self.relic_table.setBorderRadius(8)
        self.relic_table.setWordWrap(False)
        self.relic_table.verticalHeader().hide()
        self.relic_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.relic_table.setSelectionMode(QAbstractItemView.SingleSelection)

        # 词条
        self.entry_search_line = SearchLineEdit(self)
        self.entry_search_line.setPlaceholderText(self.tr("搜索词条"))
        self.entry_search_line.setFixedSize(160, 35)

        self.main_entry_button = TogglePushButton(self.tr("主词条"), self)
        self.side_entry_button = TogglePushButton(self.tr("副词条"), self)
        self.main_entry_button.setFixedSize(67, 35)
        self.side_entry_button.setFixedSize(67, 35)
        self.main_entry_button.setChecked(True)

        self.entry_type_button_group = QButtonGroup(self)
        self.entry_type_button_group.addButton(self.main_entry_button)
        self.entry_type_button_group.addButton(self.side_entry_button)

        self.entry_table = TableWidget(self)
        self.entry_table.setColumnCount(3)
        self.entry_table.setFixedSize(305, 420)
        self.entry_table.setColumnWidth(0, 148)
        self.entry_table.setColumnWidth(1, 80)
        self.entry_table.setColumnWidth(2, 75)

        self.entry_table.setBorderVisible(True)
        self.entry_table.setBorderRadius(8)
        self.entry_table.setWordWrap(False)
        self.entry_table.verticalHeader().hide()
        self.entry_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.entry_table.setSelectionMode(QAbstractItemView.SingleSelection)

        # 当前信息
        self.main_now_label = SubtitleLabel(self.tr("当前主词条:"), self)
        self.main_now_edit = LineEdit(self)
        self.main_now_edit.setReadOnly(True)
        self.side_now_label = SubtitleLabel(self.tr("当前副词条:"), self)

        self.now_table = TableWidget(self)
        self.now_table.setColumnCount(2)
        self.now_table.setFixedSize(365, 160)

        self.now_table.setBorderVisible(True)
        self.now_table.setWordWrap(False)
        self.now_table.setBorderRadius(8)
        self.now_table.verticalHeader().hide()
        self.now_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.now_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.now_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.add_num_button = PrimaryToolButton(FluentIcon.ADD)
        self.add_num_button.setFixedSize(35, 35)
        self.minus_num_button = PrimaryToolButton(FluentIcon.REMOVE)
        self.minus_num_button.setFixedSize(35, 35)
        self.set_num_edit = LineEdit(self)
        self.set_num_edit.setPlaceholderText(self.tr("数量"))
        self.set_num_edit.setFixedSize(55, 35)
        self.set_num_edit.setValidator(QIntValidator(1, 9999, self))

        self.level_label = SubtitleLabel(self.tr("等级:"), self)
        self.level_edit = LineEdit(self)
        self.level_edit.setPlaceholderText(self.tr("请输入生成遗器的等级"))
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
        self.now_tool_layout.addStretch(1)
        self.now_tool_layout.addWidget(self.add_num_button)
        self.now_tool_layout.addSpacing(5)
        self.now_tool_layout.addWidget(self.minus_num_button)
        self.now_tool_layout.addSpacing(5)
        self.now_tool_layout.addWidget(self.set_num_edit)
        self.now_tool_layout.addSpacing(12)

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
        self.entry_table.cellDoubleClicked.connect(self.handleAddSideClicked)

        self.now_table.cellDoubleClicked.connect(lambda: self.handleEntryNumChanged('delete'))
        self.add_num_button.clicked.connect(lambda: self.handleEntryNumChanged('add'))
        self.minus_num_button.clicked.connect(lambda: self.handleEntryNumChanged('remove'))
        self.set_num_edit.textChanged.connect(lambda: self.handleEntryNumChanged('set'))

        self.main_now_edit.textChanged.connect(self.handleRelicSignal)
        self.level_edit.textChanged.connect(self.handleRelicSignal)

    # 信号
    def handleRelicSignal(self):
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
        self.relic_table.setRowCount(0)
        self.entry_table.setRowCount(0)
        self.now_table.setRowCount(0)

        selected_base_relic = self.base_relic_button.isChecked()
        if selected_base_relic:
            self.handleBaseRelicLoad()
            self.handleEntryLoad()
            self.handleNowLoad()
        else:
            self.entry_table.setRowCount(0)
            self.now_table.setRowCount(0)
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
        self.entry_search_line.clear()
        selected_main_entry = self.main_entry_button.isChecked()
        for row in range(self.entry_table.rowCount()):
            entry_type = self.entry_table.item(row, 1).text()
            if selected_main_entry:
                if entry_type == self.tr('通用'):
                    self.entry_table.setRowHidden(row, True)
                else:
                    self.entry_table.setRowHidden(row, False)
                self.__handleRelatedEntryUpdate()
            else:
                if entry_type == self.tr('通用'):
                    self.entry_table.setRowHidden(row, False)
                else:
                    self.entry_table.setRowHidden(row, True)

    # 信息更新行为相关
    def handleRelicTableClicked(self):
        self.handleRelicSignal()
        self.__handleRelatedEntryUpdate()
        if self.base_relic_button.isChecked():
            self.main_now_edit.clear()

    def handleEntryTableClicked(self):
        selected_entry = self.entry_table.selectedItems()
        selected_entry_type = self.entry_table.item(self.entry_table.currentRow(), 1).text()
        if selected_entry and selected_entry_type != self.tr('通用'):
            self.main_now_edit.setText(selected_entry[0].text())
            self.side_entry_button.setChecked(True)
            self.handleEntryTypeChanged()

    def handleAddSideClicked(self):
        selected_side_entry = self.side_entry_button.isChecked()
        if selected_side_entry:
            selected_entry = self.entry_table.selectedItems()
            selected_entry_type = self.entry_table.item(self.entry_table.currentRow(), 1).text()
            entry_id = selected_entry[0].text()
            if selected_entry and selected_entry_type == self.tr('通用') and len(
                    self.now_list) < 4 and entry_id not in self.now_list:
                self.now_list[entry_id] = 1
                self.handleNowLoad()
            self.handleRelicSignal()

    def handleEntryNumChanged(self, types):
        selected_now = self.now_table.selectedItems()
        if selected_now:
            entry_name = selected_now[0].text()
            if types == 'add':
                self.now_list[entry_name] += 1
            elif types == 'remove':
                if self.now_list[entry_name] > 0:
                    self.now_list[entry_name] -= 1
            elif types == 'set':
                if self.set_num_edit.text() != '' and int(self.set_num_edit.text()) > 0:
                    self.now_list[entry_name] = int(self.set_num_edit.text())
                else:
                    self.now_list[entry_name] = 0
            elif types == 'delete':
                del self.now_list[entry_name]

            selected_row = self.now_table.currentRow()
            self.handleNowLoad()
            self.now_table.selectRow(selected_row)
            self.handleRelicSignal()

    # 读取和加载页面信息相关
    def handleBaseRelicLoad(self):
        with open(f'src/data/{cfg.get(cfg.language).value.name()}/relic.txt', 'r', encoding='utf-8') as file:
            relic = [line for line in file.readlines() if
                     not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.relic_table.setRowCount(len(relic))
        for i, line in enumerate(relic):
            line = line.strip()
            parts = line.split(" : ")
            parts[0], parts[1], parts[2] = parts[1], parts[2], parts[0]
            relic[i] = ' : '.join(parts)
            self.relic_table.setRowHeight(i, 39)
            for j, part in enumerate(parts):
                self.relic_table.setItem(i, j, QTableWidgetItem(part))
        self.relic_table.setHorizontalHeaderLabels([self.tr('遗器名称'), self.tr('部位'), 'ID'])

    def handleCustomRelicLoad(self):
        with open(f'src/data/{cfg.get(cfg.language).value.name()}/myrelic.txt', 'r', encoding='utf-8') as file:
            relic = [line for line in file.readlines() if
                     not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.relic_table.setRowCount(len(relic))
        for i, line in enumerate(relic):
            line = line.strip()
            parts = line.split(' : ')
            self.relic_table.setRowHeight(i, 39)
            for j, part in enumerate(parts):
                self.relic_table.setItem(i, j, QTableWidgetItem(part))
        self.relic_table.setHorizontalHeaderLabels(
            [self.tr('遗器名称'), self.tr('部位'), self.tr('适用角色'), 'command'])

    def handleEntryLoad(self):
        with open(f'src/data/{cfg.get(cfg.language).value.name()}/entry.txt', 'r', encoding='utf-8') as file:
            entry = [line for line in file.readlines() if
                     not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.entry_table.setRowCount(len(entry))
        for i, line in enumerate(entry):
            parts = line.split()
            self.entry_table.setRowHeight(i, 39)
            for j, part in enumerate(parts):
                self.entry_table.setItem(i, j, QTableWidgetItem(part))
        self.entry_table.setHorizontalHeaderLabels([self.tr('词条名称'), self.tr('部位'), 'ID'])

    def handleNowLoad(self):
        self.now_table.clearContents()
        self.now_table.setRowCount(len(self.now_list))
        for row, (key, value) in enumerate(self.now_list.items()):
            self.now_table.setRowHeight(row, 30)
            self.now_table.setItem(row, 0, QTableWidgetItem(key))
            self.now_table.setItem(row, 1, QTableWidgetItem(str(value)))
        self.now_table.setHorizontalHeaderLabels([self.tr('词条名称'), self.tr('数量')])

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
