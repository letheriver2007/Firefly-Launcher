import os
import json
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QAbstractItemView, QHeaderView, QHBoxLayout, QTableWidgetItem
from PySide6.QtCore import Qt
from qfluentwidgets import SearchLineEdit, TableWidget, PrimaryPushButton, InfoBar, InfoBarPosition, InfoBarIcon
from app.model.config import cfg, Info


class Warp(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)
        self.parent = parent

        self.__initWidget()

    def __initWidget(self):
        self.banner_search_line = SearchLineEdit(self)
        self.banner_search_line.setPlaceholderText(self.tr("搜索预设卡池"))
        self.banner_search_line.setFixedSize(420, 35)

        self.banner_table = TableWidget(self)
        self.banner_table.setFixedSize(420, 470)
        self.banner_table.setColumnCount(4)
        self.banner_table.setColumnWidth(0, 139)
        self.banner_table.setColumnWidth(1, 139)
        self.banner_table.setColumnWidth(2, 139)
        self.banner_table.setColumnWidth(3, 0)

        self.banner_table.setBorderVisible(True)
        self.banner_table.setBorderRadius(8)
        self.banner_table.setWordWrap(False)
        self.banner_table.verticalHeader().hide()
        self.banner_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.banner_table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.avatar_search_line = SearchLineEdit(self)
        self.avatar_search_line.setPlaceholderText(self.tr("搜索物品"))
        self.avatar_search_line.setFixedSize(330, 35)

        self.avatar_table = TableWidget(self)
        self.avatar_table.setFixedSize(330, 470)
        self.avatar_table.setColumnCount(2)

        self.avatar_table.setBorderVisible(True)
        self.avatar_table.setBorderRadius(8)
        self.avatar_table.setWordWrap(False)
        self.avatar_table.verticalHeader().hide()
        self.avatar_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.avatar_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.avatar_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.now_table = TableWidget(self)
        self.now_table.setFixedSize(330, 260)
        self.now_table.setColumnCount(3)
        self.now_table.setColumnWidth(0, 164)
        self.now_table.setColumnWidth(1, 164)
        self.now_table.setColumnWidth(2, 0)

        self.now_table.setBorderVisible(True)
        self.now_table.setBorderRadius(8)
        self.now_table.setWordWrap(False)
        self.now_table.verticalHeader().hide()
        self.now_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.now_table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.four_table = TableWidget(self)
        self.four_table.setFixedSize(330, 140)
        self.four_table.setColumnCount(2)

        self.four_table.setBorderVisible(True)
        self.four_table.setBorderRadius(8)
        self.four_table.setWordWrap(False)
        self.four_table.verticalHeader().hide()
        self.four_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.four_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.four_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.load_button = PrimaryPushButton(self.tr('加载配置'), self)
        self.load_button.setFixedSize(157, 36)
        self.save_button = PrimaryPushButton(self.tr('保存配置'), self)
        self.save_button.setFixedSize(157, 36)
        self.cancel_button = PrimaryPushButton(self.tr('恢复默认配置'), self)
        self.cancel_button.setFixedSize(330, 36)

        self.__initLayout()
        self.__initInfo()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.banner_layout = QVBoxLayout()
        self.banner_layout.addWidget(self.banner_search_line)
        self.banner_layout.addSpacing(10)
        self.banner_layout.addWidget(self.banner_table)
        self.banner_layout.addStretch(1)

        self.avatar_layout = QVBoxLayout()
        self.avatar_layout.addWidget(self.avatar_search_line)
        self.avatar_layout.addSpacing(10)
        self.avatar_layout.addWidget(self.avatar_table)
        self.avatar_layout.addStretch(1)

        now_button_layout = QHBoxLayout()
        now_button_layout.addWidget(self.load_button)
        now_button_layout.addSpacing(10)
        now_button_layout.addWidget(self.save_button)

        self.now_layout = QVBoxLayout()
        self.now_layout.addWidget(self.now_table)
        self.now_layout.addSpacing(10)
        self.now_layout.addWidget(self.four_table)
        self.now_layout.addSpacing(10)
        self.now_layout.addLayout(now_button_layout)
        self.now_layout.addSpacing(10)
        self.now_layout.addWidget(self.cancel_button)
        self.now_layout.addStretch(1)

        self.tool_layout = QVBoxLayout()
        self.tool_layout.addWidget(self.load_button)
        self.tool_layout.addSpacing(20)
        self.tool_layout.addWidget(self.save_button)
        self.tool_layout.addSpacing(20)
        self.tool_layout.addWidget(self.cancel_button)
        self.tool_layout.addStretch(1)

        self.tool_layout = QVBoxLayout()
        self.tool_layout.addWidget(self.load_button)
        self.tool_layout.addSpacing(10)
        self.tool_layout.addWidget(self.save_button)
        self.tool_layout.addSpacing(10)
        self.tool_layout.addWidget(self.cancel_button)
        self.tool_layout.addStretch(1)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.banner_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.avatar_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.now_layout)
        self.setLayout(self.main_layout)

    def __initInfo(self):
        self.config_data = {}
        self.config_gachaType = {'Normal': self.tr('常驻池'), 'AvatarUp': self.tr('角色池'),
                                 'WeaponUp': self.tr('武器池')}
        self.now_list = {}
        self.now_four_list = {}

        self.handleConfigLoad()
        self.handleDefaultBannerLoad()
        self.handleAvatarLoad()
        self.handleNowLoad()
        self.handleFourLoad()

    def __connectSignalToSlot(self):
        self.banner_search_line.textChanged.connect(self.handleBannerSearch)
        self.banner_table.doubleClicked.connect(self.handleBannerClicked)

        self.avatar_search_line.textChanged.connect(self.handleAvatarSearch)
        self.avatar_table.doubleClicked.connect(self.handleAvatarClicked)

        self.now_table.clicked.connect(lambda: self.handleNowClicked('single'))
        self.now_table.doubleClicked.connect(lambda: self.handleNowClicked('double'))
        self.four_table.doubleClicked.connect(self.handleFourClicked)

        self.load_button.clicked.connect(self.handleLoadClicked)
        self.save_button.clicked.connect(self.handleSaveClicked)
        self.cancel_button.clicked.connect(self.handleCancelClicked)

    # 从父对象信号处运行
    def handleEditDisabled(self):
        if self.parent.parent.stackedWidget.currentIndex() != 4:
            return

        for child in self.parent.children():
            if isinstance(child, InfoBar):
                child.close()

        layouts = [self.banner_layout, self.avatar_layout, self.now_layout, self.tool_layout]
        if not os.path.exists(f'.\\server\\LunarCore\\data\\Banners.json'):
            for layout in layouts:
                for i in range(layout.count()):
                    widget = layout.itemAt(i).widget()
                    if widget is not None:
                        widget.setDisabled(True)

            file_error = InfoBar(
                icon=InfoBarIcon.ERROR,
                title=self.tr('找不到文件!'),
                content='',
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=-1,
                parent=self.parent
            )
            file_error_button = PrimaryPushButton(self.tr('前往下载'))
            file_error_button.clicked.connect(lambda: self.parent.parent.stackedWidget.setCurrentIndex(0))
            file_error.addWidget(file_error_button)
            file_error.show()
        else:
            for layout in layouts:
                for i in range(layout.count()):
                    widget = layout.itemAt(i).widget()
                    if widget is not None:
                        widget.setDisabled(False)

    def handleBannerSearch(self):
        keyword = self.banner_search_line.text()
        for row in range(self.banner_table.rowCount()):
            item_1 = self.banner_table.item(row, 0)
            item_2 = self.banner_table.item(row, 1)
            item_3 = self.banner_table.item(row, 2)
            iskeyword_1 = item_1 and item_1.text().lower().find(keyword.lower()) != -1
            iskeyword_2 = item_2 and item_2.text().lower().find(keyword.lower()) != -1
            iskeyword_3 = item_3 and item_3.text().lower().find(keyword.lower()) != -1
            if iskeyword_1 or iskeyword_2 or iskeyword_3:
                self.banner_table.setRowHidden(row, False)
            else:
                self.banner_table.setRowHidden(row, True)

    def handleAvatarSearch(self):
        keyword = self.avatar_search_line.text()
        for row in range(self.avatar_table.rowCount()):
            item_1 = self.avatar_table.item(row, 0)
            item_2 = self.avatar_table.item(row, 1)
            iskeyword_1 = item_1 and item_1.text().lower().find(keyword.lower()) != -1
            iskeyword_2 = item_2 and item_2.text().lower().find(keyword.lower()) != -1
            if iskeyword_1 or iskeyword_2:
                self.avatar_table.setRowHidden(row, False)
            else:
                self.avatar_table.setRowHidden(row, True)

    def handleBannerClicked(self):
        selected_banner = self.banner_table.selectedItems()
        rateUpItems4 = eval(selected_banner[3].text())
        rateUpItems5 = selected_banner[0].text()
        bannerid = int(selected_banner[2].text())

        if bannerid not in self.now_list:
            self.now_list[bannerid] = ([], [])
            self.now_list[bannerid][0].append(rateUpItems5)
            self.now_list[bannerid][1].extend(rateUpItems4)

        self.handleNowLoad()

    def handleAvatarClicked(self):
        selected_now = self.now_table.selectedItems()
        selected_avatar = self.avatar_table.selectedItems()
        selected_id = int(selected_avatar[1].text())
        if selected_now:
            selected_row = selected_now[0].row()
            selected_bannerid = int(selected_now[1].text())

            if selected_bannerid != 1001 and len(self.now_list[selected_bannerid][1]) < 3:
                self.now_list[selected_bannerid][1].append(selected_id)

                self.handleNowLoad()
                self.now_table.selectRow(selected_row)
                self.handleFourLoad()

    def handleNowClicked(self, types):
        if types == 'single':
            self.handleFourLoad()
        elif types == 'double':
            selected_now = self.now_table.selectedItems()
            selected_id = int(selected_now[1].text())
            if selected_id in self.now_list:
                del self.now_list[selected_id]
            self.handleNowLoad()

    def handleFourClicked(self):
        selected_now = self.now_table.selectedItems()
        selected_four = self.four_table.selectedItems()
        if selected_now:
            selected_row = selected_now[0].row()
            selected_id = int(selected_now[1].text())
            selected_fourid = int(selected_four[1].text())
            if selected_id != 1001:
                self.now_list[selected_id][1].remove(selected_fourid)

                self.handleNowLoad()
                self.now_table.selectRow(selected_row)
                self.handleFourLoad()

    def handleLoadClicked(self, iscancel=False):
        try:
            with open('server/LunarCore/data/Banners.json', 'r', encoding='utf-8') as file:
                lcbanner = json.load(file)
        except FileNotFoundError:
            Info(self.parent, 'E', 1000, self.tr('找不到文件!'))
            return

        self.now_list.clear()
        for row, item in enumerate(lcbanner):
            bannerid = item['id']
            rateUpItems4 = item['rateUpItems4']

            if len(item['rateUpItems5']) > 1:
                rateUpItems5 = self.tr('常驻池')
            else:
                rateUpItems5 = self.config_data[str(item['rateUpItems5'][0])]

            if bannerid not in self.now_list:
                self.now_list[bannerid] = ([], [])
                self.now_list[bannerid][0].append(rateUpItems5)
                self.now_list[bannerid][1].extend(rateUpItems4)

        self.handleNowLoad()

        if not iscancel:
            Info(self.parent, 'S', 1000, self.tr('加载成功!'))
        else:
            Info(self.parent, 'S', 1000, self.tr('恢复默认配置成功!'))

    def handleSaveClicked(self):
        with open('src/warp/Banners.json', 'r', encoding='utf-8') as file:
            banner = json.load(file)

        now_banners = []
        for item in banner:
            bannerid = item['id']
            for key, value in self.now_list.items():
                rateUpItems5, rateUpItems4 = value
                if key == bannerid:
                    item['rateUpItems4'] = rateUpItems4
                    now_banners.append(item)
                    break

        with open('server/LunarCore/data/Banners.json', 'w', encoding='utf-8') as file:
            json.dump(now_banners, file, indent=2, ensure_ascii=False)

        Info(self.parent, 'S', 1000, self.tr('保存成功!'))

    def handleCancelClicked(self):
        subprocess.run('copy src\\warp\\Banners.json server\\LunarCore\\data\\Banners.json', shell=True)
        self.handleLoadClicked(True)

    def handleConfigLoad(self):
        self.config_data.clear()
        with open(f'src/data/{cfg.get(cfg.language).value.name()}/avatar.txt', 'r', encoding='utf-8') as file:
            avatar = [line for line in file.readlines() if
                      not (line.strip().startswith("//") or line.strip().startswith("#"))]
        for i, line in enumerate(avatar):
            line = line.strip()
            parts = line.split(' : ')
            self.config_data[parts[0]] = parts[1]

        with open(f'src/data/{cfg.get(cfg.language).value.name()}/lightcone.txt', 'r', encoding='utf-8') as file:
            lightcone = file.readlines()
        for i, line in enumerate(lightcone):
            line = line.strip()
            parts = line.split(' : ')
            self.config_data[parts[0]] = parts[1]

    def handleDefaultBannerLoad(self):
        with open('src/warp/Banners.json', 'r', encoding='utf-8') as file:
            banner = json.load(file)

        self.banner_table.setRowCount(len(banner))
        for row, item in enumerate(banner):
            gachaTypeRes = item['gachaType']
            gachaType = self.config_gachaType[gachaTypeRes]
            bannerid = item['id']
            rateUpItems4 = item['rateUpItems4']
            if len(item['rateUpItems5']) > 1:
                rateUpItems5 = self.tr('常驻池')
            else:
                rateUpItems5 = self.config_data[str(item['rateUpItems5'][0])]

            self.banner_table.setItem(row, 0, QTableWidgetItem(rateUpItems5))
            self.banner_table.setItem(row, 1, QTableWidgetItem(gachaType))
            self.banner_table.setItem(row, 2, QTableWidgetItem(str(bannerid)))
            self.banner_table.setItem(row, 3, QTableWidgetItem(str(rateUpItems4)))
            self.banner_table.setRowHeight(row, 39)
        self.banner_table.setHorizontalHeaderLabels([self.tr('卡池名称'), self.tr('卡池类型'), 'ID', 'FourID'])

    def handleAvatarLoad(self):
        self.avatar_table.setRowCount(len(self.config_data))
        for row, (ids, name) in enumerate(self.config_data.items()):
            self.avatar_table.setItem(row, 0, QTableWidgetItem(name))
            self.avatar_table.setItem(row, 1, QTableWidgetItem(ids))
            self.avatar_table.setRowHeight(row, 39)
        self.avatar_table.setHorizontalHeaderLabels([self.tr('物品名称'), 'ID'])

    def handleFourLoad(self):
        selected_now = self.now_table.selectedItems()
        if selected_now:
            selected_fourid = eval(selected_now[2].text())
            display_data = []
            for ids in selected_fourid:
                display_data.append((self.config_data[str(ids)], str(ids)))

            self.four_table.clearContents()
            self.four_table.setRowCount(len(display_data))
            for row, (name, ids) in enumerate(display_data):
                self.four_table.setItem(row, 0, QTableWidgetItem(name))
                self.four_table.setItem(row, 1, QTableWidgetItem(ids))
                self.four_table.setRowHeight(row, 30)
        self.four_table.setHorizontalHeaderLabels([self.tr('当前角色'), 'ID'])

    def handleNowLoad(self):
        self.now_table.clearContents()
        self.now_table.setRowCount(len(self.now_list))
        self.four_table.setRowCount(0)

        row = 0
        for key, value in self.now_list.items():
            self.now_table.setItem(row, 0, QTableWidgetItem(value[0][0]))
            self.now_table.setItem(row, 1, QTableWidgetItem(str(key)))
            self.now_table.setItem(row, 2, QTableWidgetItem(str(value[1])))
            self.now_table.setRowHeight(row, 30)
            row += 1
        self.now_table.setHorizontalHeaderLabels([self.tr('当前卡池'), 'ID', 'FourID'])
