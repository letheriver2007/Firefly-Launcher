import json
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QApplication, QTableWidgetItem
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import Pivot, qrouter, ScrollArea, LineEdit, PrimaryPushButton, InfoBar, InfoBarPosition, PrimaryPushSettingCard
from app.model.style_sheet import StyleSheet
from app.lunarcore_command import Scene, Spawn, Give, Relic
from app.lunarcore_edit import LunarCoreEdit
from app.model.lunarcore_message import (PrimaryPushSettingCard_Giveall, ComboBoxSettingCard__Clear, PrimaryPushSettingCard_Account,
                                           PrimaryPushSettingCard_Kick, PrimaryPushSettingCard_Unstuck, PrimaryPushSettingCard_Gender,
                                           PrimaryPushSettingCard_WorldLevel, PrimaryPushSettingCard_Avatar, ComboBoxSettingCard_Quickgive)
from app.model.download_message import MessageLunarCore, MessageLunarCoreRes, HyperlinkCard_LunarCore, download_check
from app.model.setting_group import SettingCardGroup
from app.model.config import cfg
from app.model.open_command import send_command


class LunarCore(ScrollArea):
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

        self.LunarCoreDownloadInterface = SettingCardGroup(self.scrollWidget)
        self.LunarCoreRepoCard = HyperlinkCard_LunarCore(
            'https://github.com/Melledy/LunarCore',
            'LunarCore',
            'https://github.com/Dimbreath/StarRailData',
            'StarRailData',
            'https://gitlab.com/Melledy/LunarCore-Configs',
            'LunarCore-Configs',
            FIF.LINK,
            '项目仓库',
            '打开LunarCore相关仓库'
        )
        self.LunarCoreDownloadCard = PrimaryPushSettingCard(
            '详细信息',
            FIF.DOWNLOAD,
            'LunarCore',
            '下载LunarCore并编译'
        )
        self.LunarCoreResDownloadCard = PrimaryPushSettingCard(
            '详细信息',
            FIF.DOWNLOAD,
            'LunarCore-Res',
            '下载LunarCore资源文件'
        )
        self.ConfigInterface = SettingCardGroup(self.scrollWidget)
        self.CommandDataConfigCard = PrimaryPushSettingCard(
            '打开文件夹',
            FIF.LABEL,
            '命令数据设置',
            '自定义命令数据配置'
        )

        self.__initWidget()

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)     # 水平滚动条关闭
        self.setViewportMargins(20, 0, 20, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)    # 必须设置！！！
        
        # 使用qss设置样式
        self.scrollWidget.setObjectName('scrollWidget')
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        # 项绑定到栏目
        self.LunarCoreDownloadInterface.addSettingCard(self.LunarCoreRepoCard)
        self.LunarCoreDownloadInterface.addSettingCard(self.LunarCoreDownloadCard)
        self.LunarCoreDownloadInterface.addSettingCard(self.LunarCoreResDownloadCard)
        self.ConfigInterface.addSettingCard(self.CommandDataConfigCard)

        # 栏绑定界面
        self.addSubInterface(self.LunarCoreDownloadInterface, 'LunarCoreDownloadInterface','下载', icon=FIF.DOWNLOAD)
        self.LunarCoreCommandInterface = LunarCoreCommand('CommandInterface', self)
        self.addSubInterface(self.ConfigInterface,'configInterface','配置', icon=FIF.EDIT)
        self.addSubInterface(self.LunarCoreCommandInterface, 'LunarCoreCommandInterface','命令', icon=FIF.COMMAND_PROMPT)
        self.LunarCoreEditInterface = LunarCoreEdit('EditInterface', self)
        self.addSubInterface(self.LunarCoreEditInterface, 'LunarCoreEditInterface','编辑器', icon=FIF.LAYOUT)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 10, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.LunarCoreDownloadInterface)
        self.pivot.setCurrentItem(self.LunarCoreDownloadInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.LunarCoreDownloadInterface.objectName())

    def __connectSignalToSlot(self):
        self.LunarCoreDownloadCard.clicked.connect(lambda: download_check(self, 'lunarcore'))
        self.LunarCoreResDownloadCard.clicked.connect(lambda: download_check(self, 'lunarcoreres'))
        self.CommandDataConfigCard.clicked.connect(lambda: subprocess.run(['start', '.\\src\\data\\'], shell=True))

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


class LunarCoreCommand(ScrollArea):
    Nav = Pivot
    buttonClicked = Signal(str)
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
        self.CustomInterface = SettingCardGroup(self.scrollWidget)
        self.giveallCard = PrimaryPushSettingCard_Giveall(
            '物品',
            '角色',
            FIF.TAG,
            '给予全部',
            '/giveall {items | avatars}'
        )
        self.quickgiveCard = ComboBoxSettingCard_Quickgive(
            FIF.TAG,
            '物品快捷给予',
            '选择你想要快捷得到的物品',
            texts=['1000专票', '1000通票']
        )
        self.refillCard = PrimaryPushSettingCard(
            '使用',
            FIF.TAG,
            '秘技点补充',
            '/refill'
        )
        self.healCard = PrimaryPushSettingCard(
            '使用',
            FIF.TAG,
            '治疗全部队伍角色',
            '/heal'
        )
        self.ServerInterface = SettingCardGroup(self.scrollWidget)
        self.helpCard = PrimaryPushSettingCard(
            '使用',
            FIF.TAG,
            '查看服务端命令帮助',
            '/help'
        )
        self.reloadCard = PrimaryPushSettingCard(
            '使用',
            FIF.TAG,
            '重载服务端',
            '/reload'
        )
        self.accountCard = PrimaryPushSettingCard_Account(
            '添加',
            '删除',
            FIF.TAG,
            '添加或删除账号',
            '/account {create | delete} [username]'
        )
        self.kickCard = PrimaryPushSettingCard_Kick(
            '使用',
            FIF.TAG,
            '踢出玩家',
            '/kick @[player id]'
        )
        self.unstuckCard = PrimaryPushSettingCard_Unstuck(
            '使用',
            FIF.TAG,
            '解除场景未加载造成的卡死',
            '/unstuck'
        )
        self.PersonalInterface = SettingCardGroup(self.scrollWidget)
        self.genderCard = PrimaryPushSettingCard_Gender(
            '星',
            '穹',
            FIF.TAG,
            '设置开拓者性别',
            '/gender {male | female}'
        )
        self.worldLevelCard = PrimaryPushSettingCard_WorldLevel(
            '使用',
            FIF.TAG,
            '设置开拓等级',
            '/worldlevel [world level]'
        )
        self.avatarCard = PrimaryPushSettingCard_Avatar(
            '使用',
            FIF.TAG,
            '设置当前角色属性',
            '/avatar [lv(level)] [r(eidolon)] [s(skill level)]'
        )
        self.clearCard = ComboBoxSettingCard__Clear(
            FIF.TAG,
            '清空物品',
            '/clear {all | relics | lightcones | materials | items}',
            texts=['全部', '遗器', '光锥', '材料', '物品']
        )
        self.RelicInterface = SettingCardGroup(self.scrollWidget)

        self.__initWidget()

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)     # 水平滚动条关闭
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)    # 必须设置！！！
        
        self.updateText = LineEdit()
        self.updateText.setFixedSize(845, 35)
        self.clearButton = PrimaryPushButton('清空')
        self.copyButton = PrimaryPushButton('复制')
        self.actionButton = PrimaryPushButton('执行')
        self.clearButton.setFixedSize(80, 35)
        self.copyButton.setFixedSize(80, 35)
        self.actionButton.setFixedSize(80, 35)
        self.updateContainer = QWidget()
        
        # 使用qss设置样式
        self.scrollWidget.setObjectName('scrollWidget')
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        # 项绑定到栏目
        self.CustomInterface.addSettingCard(self.giveallCard)
        self.CustomInterface.addSettingCard(self.quickgiveCard)
        self.CustomInterface.addSettingCard(self.refillCard)
        self.CustomInterface.addSettingCard(self.healCard)
        self.ServerInterface.addSettingCard(self.helpCard)
        self.ServerInterface.addSettingCard(self.reloadCard)
        self.ServerInterface.addSettingCard(self.accountCard)
        self.ServerInterface.addSettingCard(self.kickCard)
        self.ServerInterface.addSettingCard(self.unstuckCard)
        self.PersonalInterface.addSettingCard(self.genderCard)
        self.PersonalInterface.addSettingCard(self.worldLevelCard)
        self.PersonalInterface.addSettingCard(self.avatarCard)
        self.PersonalInterface.addSettingCard(self.clearCard)

        # 栏绑定界面
        self.addSubInterface(self.CustomInterface, 'CustomInterface','快捷', icon=FIF.COMMAND_PROMPT)
        self.addSubInterface(self.ServerInterface, 'ServerInterface','服务端', icon=FIF.COMMAND_PROMPT)
        self.addSubInterface(self.PersonalInterface, 'PersonalInterface','账号', icon=FIF.COMMAND_PROMPT)

        self.SceneInterface = Scene('SceneInterface', self)
        self.addSubInterface(self.SceneInterface, 'SceneInterface','场景', icon=FIF.COMMAND_PROMPT)
        self.SpawnInterface = Spawn('SpawnInterface', self)
        self.addSubInterface(self.SpawnInterface, 'SpawnInterface','生成', icon=FIF.COMMAND_PROMPT)
        self.GiveInterface = Give('GiveInterface', self)
        self.addSubInterface(self.GiveInterface, 'GiveInterface','给予', icon=FIF.COMMAND_PROMPT)
        self.RelicInterface = Relic('RelicInterface', self)
        self.addSubInterface(self.RelicInterface, 'RelicInterface','遗器', icon=FIF.COMMAND_PROMPT)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.CustomInterface)
        self.pivot.setCurrentItem(self.CustomInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.CustomInterface.objectName())

        self.updateLayout = QHBoxLayout(self.updateContainer)
        self.updateLayout.addWidget(self.updateText, alignment=Qt.AlignCenter)
        self.updateLayout.addStretch(1)
        self.updateLayout.addWidget(self.clearButton, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(5)
        self.updateLayout.addWidget(self.copyButton, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(5)
        self.updateLayout.addWidget(self.actionButton, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(15)
        self.vBoxLayout.addWidget(self.updateContainer)
        
    def __connectSignalToSlot(self):
        self.buttonClicked.connect(self.handlebuttonClicked)
        self.clearButton.clicked.connect(lambda: self.updateText.clear())
        self.copyButton.clicked.connect(lambda: self.copyToClipboard('show'))
        self.actionButton.clicked.connect(self.handleOpencommandActionCkicked)

        self.accountCard.create_account.connect(lambda: self.handleAccountClicked('create'))
        self.accountCard.delete_account.connect(lambda: self.handleAccountClicked('delete'))
        self.kickCard.kick_player.connect(self.handleKickClicked)
        self.unstuckCard.unstuck_player.connect(self.handleUnstuckClicked)

        self.refillCard.clicked.connect(lambda: self.buttonClicked.emit('/refill'))
        self.healCard.clicked.connect(lambda: self.buttonClicked.emit('/heal'))
        self.helpCard.clicked.connect(lambda: self.buttonClicked.emit('/help'))
        self.reloadCard.clicked.connect(lambda: self.buttonClicked.emit('/reload'))

        self.giveallCard.give_materials.connect(lambda: self.handleGiveallClicked('materials'))
        self.giveallCard.give_avatars.connect(lambda: self.handleGiveallClicked('avatars'))
        self.quickgiveCard.quickgive_clicked.connect(lambda itemid: self.handleQuickgiveClicked(itemid))

        self.genderCard.gender_male.connect(lambda: self.buttonClicked.emit('/gender male'))
        self.genderCard.gender_female.connect(lambda: self.buttonClicked.emit('/gender female'))
        self.worldLevelCard.set_level.connect(self.handleWorldLevelClicked)
        self.avatarCard.avatar_set.connect(self.handleAvatarClicked)
        self.clearCard.clear_clicked.connect(lambda itemid: self.handleClearClicked(itemid))

        self.SceneInterface.scene_id_signal.connect(lambda scene_id: self.buttonClicked.emit('/scene '+ scene_id))
        self.SpawnInterface.monster_id_signal.connect(lambda monster_id: self.handleSpawnClicked(monster_id))
        self.GiveInterface.item_id_signal.connect(lambda item_id, types: self.handleGiveClicked(item_id, types))
        self.RelicInterface.relic_id_signal.connect(lambda relic_id: self.handleRelicClicked(relic_id))
        self.RelicInterface.custom_relic_signal.connect(lambda command: self.buttonClicked.emit(command))

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
    
    def handlebuttonClicked(self, text):
        self.updateText.clear()
        self.updateText.setText(text)
        if cfg.autoCopy.value:
            self.copyToClipboard('hide')
    
    def handleOpencommandActionCkicked(self):
        with open('config/config.json', 'r') as file:
            data = json.load(file)
            token = data['TOKEN']
        command = self.updateText.text().replace('/', '')
        if token != '':
            if self.updateText.text() != '':
                try:
                    response = send_command(token, command)
                    InfoBar.success(
                        title='执行完成！',
                        content=response,
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=1000,
                        parent=self.parent
                    )
                except Exception as e:
                    InfoBar.error(
                        title='执行失败！',
                        content=str(e),
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self.parent
                    )
        else:
            InfoBar.error(
                title='执行失败！',
                content='请先配置远程执行！',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent
            )

    def copyToClipboard(self, status):
        text = self.updateText.text()
        app = QApplication.instance()
        try:
            if text != '':
                clipboard = app.clipboard()
                clipboard.setText(text)
                if status == 'show':
                    InfoBar.success(
                        title='复制成功！',
                        content='',
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=1000,
                        parent=self.parent
                    )
            else:
                if status == 'show':
                    InfoBar.error(
                        title='复制失败！',
                        content='',
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self.parent
                    )
        except:
            InfoBar.error(
                title='复制失败！',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent
            )

    def handleGiveallClicked(self, types):
        line_level = self.giveallCard.line_level.text()
        line_eidolon = self.giveallCard.line_eidolon.text()
        line_skill = self.giveallCard.line_skill.text()
        command = '/giveall '+ types
        if types == 'materials':
            if line_level != '':
                command += ' lv' + line_level
            if line_eidolon != '':
                command += ' r' + line_eidolon
        elif types == 'avatars':
            if line_level != '':
                command += ' lv' + line_level
            if line_eidolon != '':
                command += ' r' + line_eidolon
            if line_skill != '':
                command +=' s' + line_skill
        self.buttonClicked.emit(command)

    def handleQuickgiveClicked(self, itemid):
        if itemid == 0:
            self.buttonClicked.emit('/give 102 x1000')
        elif itemid == 1:
            self.buttonClicked.emit('/give 101 x1000')
    
    def handleClearClicked(self, itemid):
        if itemid == 0:
            self.buttonClicked.emit('/clear all')
        elif itemid == 1:
            self.buttonClicked.emit('/clear relics')
        elif itemid == 2:
            self.buttonClicked.emit('/clear lightcones')
        elif itemid == 3:
            self.buttonClicked.emit('/clear materials')
        elif itemid == 4:
            self.buttonClicked.emit('/clear items')
    
    def handleAccountClicked(self, types):
        account_name = self.accountCard.account_name.text()
        account_uid = self.accountCard.account_uid.text()
        if account_name != '':
            account = f'/account {types} {account_name}'
            if types == 'create' and account_uid != '':
                account += ' ' + account_uid
            self.buttonClicked.emit(account)
        else:
            InfoBar.error(
                title='请输入正确的用户名！',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent
            )
    
    def handleKickClicked(self):
        account_uid = self.kickCard.account_uid.text()
        if account_uid != '':
            self.buttonClicked.emit('/kick @' + account_uid)
        else:
            InfoBar.error(
                title='请输入正确的UID！',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent
            )

    def handleUnstuckClicked(self):
        stucked_uid = self.unstuckCard.stucked_uid.text()
        if stucked_uid != '' :
            self.buttonClicked.emit('/unstuck @' + stucked_uid)
        else:
            InfoBar.error(
                title='请输入正确的UID！',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent
            )
    
    def handleWorldLevelClicked(self):
        world_level = self.worldLevelCard.world_level.text()
        if world_level != '':
            self.buttonClicked.emit('/worldlevel ' + world_level)
        else:
            self.buttonClicked.emit('')
    
    def handleAvatarClicked(self):
        avatar_level = self.avatarCard.avatar_level.text()
        avatar_eidolon = self.avatarCard.avatar_eidolon.text()
        avatar_skill = self.avatarCard.avatar_skill.text()
        command = '/avatar'
        if avatar_level != '':
            command += ' lv' + avatar_level
        if avatar_eidolon != '':
            command += ' r' + avatar_eidolon
        if avatar_skill != '':
            command +=' s' + avatar_skill
        if command != '/avatar':
            self.buttonClicked.emit(command)
        else:
            self.buttonClicked.emit('')

    def handleSpawnClicked(self, monster_id):
        monster_num_edit = self.SpawnInterface.monster_num_edit.text()
        monster_level_edit = self.SpawnInterface.monster_level_edit.text()
        monster_round_edit = self.SpawnInterface.monster_round_edit.text()
        command = '/spawn ' + monster_id
        if monster_num_edit != '':
            command += ' x' + monster_num_edit
        if monster_level_edit != '':
            command += ' lv' + monster_level_edit
        if monster_round_edit != '':
            command += ' r' + monster_round_edit
        self.buttonClicked.emit(command)
    
    def handleGiveClicked(self, item_id, types):
        give_level_edit = self.GiveInterface.give_level_edit.text()
        give_eidolon_edit = self.GiveInterface.give_eidolon_edit.text()
        give_num_edit = self.GiveInterface.give_num_edit.text()
        command = '/give ' + item_id
        if types == 'avatar':
            if give_level_edit != '':
                command += ' lv' + give_level_edit
            if give_eidolon_edit != '':
                command += ' r' + give_eidolon_edit
        elif types == 'lightcone':
            if give_num_edit != '':
                command += ' x' + give_num_edit
            if give_level_edit != '':
                command += ' lv' + give_level_edit
            if give_eidolon_edit != '':
                command += ' r' + give_eidolon_edit
        elif types == 'item' or types == 'food':
            if give_num_edit != '':
                command += ' x' + give_num_edit
        self.buttonClicked.emit(command)
    
    def handleRelicClicked(self, relic_id):
        relic_level = self.RelicInterface.level_edit.text()
        main_entry_name = self.RelicInterface.main_now_edit.text()
        side_entry_name = self.RelicInterface.now_list
        entry_table = self.RelicInterface.entry_table
        command = '/give ' + relic_id

        if relic_level != '':
            command += ' lv' + relic_level

        if main_entry_name != '':
            entry_index = 0
            for i in range(entry_table.rowCount()):
                if entry_table.item(i, 0).text() == main_entry_name and entry_table.item(i, 1).text() != '通用':
                    entry_index = i
                    break
            main_entry = entry_table.item(entry_index, 2).text()
            command += ' s' + main_entry
        
        for entry_name, entry_num in side_entry_name.items():
            if entry_name != '':
                entry_index = 0
                for i in range(entry_table.rowCount()):
                    if entry_table.item(i, 0).text() == entry_name and entry_table.item(i, 1).text() =='通用':
                        entry_index = i
                        break
                side_entry = entry_table.item(entry_index, 2).text()
                command += ' ' + side_entry + ':' + str(entry_num)

        self.buttonClicked.emit(command)