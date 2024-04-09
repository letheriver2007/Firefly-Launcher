import json
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QAbstractItemView, QHeaderView, QHBoxLayout, QButtonGroup, QTableWidgetItem
from PySide6.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import Pivot, qrouter, ScrollArea, SearchLineEdit, TableWidget, TogglePushButton, PrimaryPushButton, InfoBar, InfoBarPosition
from app.model.style_sheet import StyleSheet
from app.model.setting_card import SettingCardGroup
from app.model.config import cfg


class LunarCoreEdit(ScrollArea):
    Nav = Pivot
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setObjectName(text)
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)

        # 栏定义
        self.pivot = self.Nav(self)
        self.stackedWidget = QStackedWidget(self)

        # 添加项
        self.WarpInterface = SettingCardGroup(self.scrollWidget)

        self.__initWidget()

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)     # 水平滚动条关闭
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)    # 必须设置！！！

        # 使用qss设置样式
        self.scrollWidget.setObjectName('scrollWidget')
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        # 项绑定到栏目

        # 栏绑定界面
        self.WarpInterface = Warp('WarpInterface', self)
        self.addSubInterface(self.WarpInterface, 'WarpInterface',self.tr('跃迁'), icon=FIF.LABEL)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.WarpInterface)
        self.pivot.setCurrentItem(self.WarpInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.WarpInterface.objectName())

    def __connectSignalToSlot(self):
        pass

    def addSubInterface(self, widget: QLabel, objectName, text, icon=None):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            icon=icon,
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())
        qrouter.push(self.stackedWidget, widget.objectName())


class Warp(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)
        self.parent = parent

        self.__initWidget()

    def __initWidget(self):
        self.banner_search_line = SearchLineEdit(self)
        self.banner_search_line.setPlaceholderText(self.tr("搜索预设卡池"))
        self.banner_search_line.setFixedSize(350, 35)

        self.banner_table = TableWidget(self)
        self.banner_table.setFixedSize(350, 455)
        self.banner_table.setColumnCount(3)

        self.banner_table.setBorderVisible(True)
        self.banner_table.setBorderRadius(8)
        self.banner_table.setWordWrap(False)
        self.banner_table.verticalHeader().hide()
        self.banner_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.banner_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.banner_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.now_table = TableWidget(self)
        self.now_table.setFixedSize(350, 506)
        self.now_table.setColumnCount(2)

        self.now_table.setBorderVisible(True)
        self.now_table.setBorderRadius(8)
        self.now_table.setWordWrap(False)
        self.now_table.verticalHeader().hide()
        self.now_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.now_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.now_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.load_button = PrimaryPushButton(FIF.FOLDER_ADD, self.tr('加载配置'), self)
        self.load_button.setFixedSize(220, 40)
        self.save_button = PrimaryPushButton(FIF.SAVE, self.tr('保存配置'), self)
        self.save_button.setFixedSize(220, 40)
        self.cancel_button = PrimaryPushButton(FIF.CANCEL, self.tr('恢复默认配置'), self)
        self.cancel_button.setFixedSize(220, 40)

        self.__initLayout()
        self.__initInfo()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.banner_layout = QVBoxLayout()
        self.banner_layout.addWidget(self.banner_search_line)
        self.banner_layout.addSpacing(10)
        self.banner_layout.addWidget(self.banner_table)
        self.banner_layout.addStretch(1)

        self.now_layout = QVBoxLayout()
        self.now_layout.addWidget(self.now_table)
        self.now_layout.addStretch(1)

        self.tool_layout = QVBoxLayout()
        self.tool_layout.addWidget(self.load_button)
        self.tool_layout.addSpacing(20)
        self.tool_layout.addWidget(self.save_button)
        self.tool_layout.addSpacing(20)
        self.tool_layout.addWidget(self.cancel_button)
        self.tool_layout.addStretch(1)
        
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.banner_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.now_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.tool_layout)
        self.setLayout(self.main_layout)

    def __initInfo(self):
        self.now_list = {}
        self.handleConfigLoad()
        self.handleDefaultBannerLoad()
        self.handleNowLoad()

    def __connectSignalToSlot(self):
        self.banner_search_line.textChanged.connect(self.handleBannerSearch)
        self.banner_table.doubleClicked.connect(self.handleBannerClicked)
        self.now_table.doubleClicked.connect(self.handleNowClicked)

        self.load_button.clicked.connect(self.handleLoadClicked)
        self.save_button.clicked.connect(self.handleSaveClicked)
        self.cancel_button.clicked.connect(self.handleCancelClicked)

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
    
    def handleBannerClicked(self):
        selected_banner = self.banner_table.selectedItems()
        banner_name = selected_banner[0].text()
        banner_id = selected_banner[2].text()
        if selected_banner and banner_name not in self.now_list:
            self.now_list[banner_name] = banner_id
            self.handleNowLoad()

    def handleNowClicked(self):
        selected_now = self.now_table.selectedItems()
        selected_name = selected_now[0].text()
        if selected_now:
            del self.now_list[selected_name]
            self.handleNowLoad()

    def handleLoadClicked(self, flag=True):
        try:
            with open('server/LunarCore/data/Banners.json', 'r', encoding='utf-8') as file:
                lcbanner = json.load(file)
            self.now_table.setRowCount(len(lcbanner))
            for row, item in enumerate(lcbanner):
                if len(item['rateUpItems5']) > 1:
                    rateUpItems5 = self.tr('多物品')
                else:
                    rateUpItems5 = self.config_data[str(item['rateUpItems5'][0])]
                bannerid = str(item['id'])
                self.now_list[rateUpItems5] = bannerid
            self.handleNowLoad()

            if flag:
                InfoBar.success(
                    title=self.tr('加载成功!'),
                    content='',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self.parent
                )
        except:
            self.now_table.setRowCount(0)
            InfoBar.error(
                title=self.tr('找不到文件, 请重新下载!'),
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent
            )

    def handleSaveClicked(self):
        with open('src/warp/Banners.json', 'r', encoding='utf-8') as file:
            all_banners = json.load(file)

        filtered_banners = [banner for banner in all_banners if str(banner['id']) in self.now_list.values()]

        with open('server/LunarCore/data/Banners.json', 'w', encoding='utf-8') as file:
            json.dump(filtered_banners, file, indent=2, ensure_ascii=False)

        InfoBar.success(
            title=self.tr('保存成功!'),
            content='',
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self.parent
        )

    def handleCancelClicked(self):
        subprocess.run('copy src\\warp\\Banners.json server\\LunarCore\\data\\Banners.json', shell=True)
        self.handleLoadClicked(False)
        self.handleNowLoad()

    def handleConfigLoad(self):
        self.config_data = {}
        self.config_gachaType = {'Normal': self.tr('常驻池'), 'AvatarUp': self.tr('角色池'), 'WeaponUp': self.tr('武器池')}
        with open(f'src/data/{cfg.get(cfg.language).value.name()}/avatar.txt', 'r', encoding='utf-8') as file:
            avatar = file.readlines()
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
            if len(item['rateUpItems5']) > 1:
                rateUpItems5 = self.tr('常驻池')
            else:
                rateUpItems5 = self.config_data[str(item['rateUpItems5'][0])]
            gachaTypeRes = item['gachaType']
            gachaType = self.config_gachaType[gachaTypeRes]
            bannerid = str(item['id'])
            self.banner_table.setItem(row, 0, QTableWidgetItem(rateUpItems5))
            self.banner_table.setItem(row, 1, QTableWidgetItem(gachaType))
            self.banner_table.setItem(row, 2, QTableWidgetItem(bannerid))
            self.banner_table.setRowHeight(row, 39)
        self.banner_table.setHorizontalHeaderLabels([self.tr('卡池名称'), self.tr('卡池类型'), self.tr('ID')])

    def handleNowLoad(self):
        print(self.now_list)
        self.now_table.clearContents()
        self.now_table.setRowCount(len(self.now_list))
        for row, (key, value) in enumerate(self.now_list.items()):
            self.now_table.setItem(row, 0, QTableWidgetItem(key))
            self.now_table.setItem(row, 1, QTableWidgetItem(str(value)))
            self.now_table.setRowHeight(row, 39)
        self.now_table.setHorizontalHeaderLabels([self.tr('当前卡池'), self.tr('ID')])