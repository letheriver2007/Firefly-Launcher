from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QApplication, QTableWidgetItem
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import Pivot, qrouter, ScrollArea, LineEdit, PrimaryPushButton, InfoBar, InfoBarPosition, PrimaryPushSettingCard
from app.component.style_sheet import StyleSheet
from app.component.message_command import (PrimaryPushSettingCard_Giveall, PrimaryPushSettingCard_Clear, PrimaryPushSettingCard_Account,
                                           PrimaryPushSettingCard_Kick, PrimaryPushSettingCard_Unstuck, PrimaryPushSettingCard_Gender,
                                           PrimaryPushSettingCard_WorldLevel, PrimaryPushSettingCard_Avatar, Scene, Spawn, Give)
from app.component.setting_group import SettingCardGroup
from app.module.config import cfg


class Command(ScrollArea):
    Nav = Pivot
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setObjectName(text.replace(' ', '-'))
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)

        # 栏定义
        self.pivot = self.Nav(self)
        self.stackedWidget = QStackedWidget(self)

        self.__initWidget()

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)     # 水平滚动条关闭
        self.setViewportMargins(20, 0, 20, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)    # 必须设置！！！

        self.updateText = LineEdit()
        self.updateText.setFixedSize(930, 35)
        self.clearButton = PrimaryPushButton('清空')
        self.copyButton = PrimaryPushButton('复制')
        self.clearButton.setFixedSize(80, 35)
        self.copyButton.setFixedSize(80, 35)
        self.updateContainer = QWidget()
        
        # 使用qss设置样式
        self.scrollWidget.setObjectName('scrollWidget')
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        # 栏绑定界面
        self.LunarCoreInterface = LunarCore('About Interface', self)
        self.addSubInterface(self.LunarCoreInterface, 'LunarCoreInterface','LunarCore', icon=FIF.COMMAND_PROMPT)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(0, 10, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.LunarCoreInterface)
        self.pivot.setCurrentItem(self.LunarCoreInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.LunarCoreInterface.objectName())

        self.updateLayout = QHBoxLayout(self.updateContainer)
        self.updateLayout.addWidget(self.updateText, alignment=Qt.AlignCenter)
        self.updateLayout.addStretch(1)
        self.updateLayout.addWidget(self.clearButton, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(5)
        self.updateLayout.addWidget(self.copyButton, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(15)
        self.vBoxLayout.addWidget(self.updateContainer)

    def __connectSignalToSlot(self):
        self.LunarCoreInterface.buttonClicked.connect(self.handlebuttonClicked)
        self.clearButton.clicked.connect(lambda: self.updateText.clear())
        self.copyButton.clicked.connect(self.copyToClipboard)

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
            self.copyToClipboard()
    
    def copyToClipboard(self):
        text = self.updateText.text()
        app = QApplication.instance()
        try:
            if text != '':
                clipboard = app.clipboard()
                clipboard.setText(text)
                InfoBar.success(
                    title='复制成功！',
                    content='',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=1000,
                    parent=self
                )
            else:
                InfoBar.error(
                    title='复制失败！',
                    content='',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
        except:
            InfoBar.error(
                title='复制失败！',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )


class LunarCore(ScrollArea):
    Nav = Pivot
    buttonClicked = Signal(str)
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setObjectName(text.replace(' ', '-'))
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)

        # 栏定义
        self.pivot = self.Nav(self)
        self.stackedWidget = QStackedWidget(self)

        # 添加项
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
        self.CustomInterface = SettingCardGroup(self.scrollWidget)
        self.giveallCard = PrimaryPushSettingCard_Giveall(
            '物品',
            '角色',
            FIF.TAG,
            '给予全部',
            '/giveall {items | avatars}'
        )
        self.clearCard = PrimaryPushSettingCard_Clear(
            '遗器',
            '光锥',
            '材料',
            '物品',
            FIF.TAG,
            '清空物品',
            '/clear {relics | lightcones | materials | items}'
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
        self.SpawnInterface = SettingCardGroup(self.scrollWidget)
        self.GiveInterface = SettingCardGroup(self.scrollWidget)
        self.MailInterface = SettingCardGroup(self.scrollWidget)

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
        self.ServerInterface.addSettingCard(self.helpCard)
        self.ServerInterface.addSettingCard(self.reloadCard)
        self.ServerInterface.addSettingCard(self.accountCard)
        self.ServerInterface.addSettingCard(self.kickCard)
        self.ServerInterface.addSettingCard(self.unstuckCard)
        self.CustomInterface.addSettingCard(self.giveallCard)
        self.CustomInterface.addSettingCard(self.clearCard)
        self.CustomInterface.addSettingCard(self.refillCard)
        self.CustomInterface.addSettingCard(self.healCard)
        self.PersonalInterface.addSettingCard(self.genderCard)
        self.PersonalInterface.addSettingCard(self.worldLevelCard)
        self.PersonalInterface.addSettingCard(self.avatarCard)

        # 栏绑定界面
        self.addSubInterface(self.ServerInterface, 'ServerInterface','服务端', icon=FIF.TAG)
        self.addSubInterface(self.CustomInterface, 'CustomInterface','快捷', icon=FIF.TAG)
        self.addSubInterface(self.PersonalInterface, 'PersonalInterface','账号', icon=FIF.TAG)
        self.SceneInterface = Scene('Scene Interface', self)
        self.addSubInterface(self.SceneInterface, 'SceneInterface','场景', icon=FIF.TAG)
        self.SpawnInterface = Spawn('Spawn Interface', self)
        self.addSubInterface(self.SpawnInterface, 'SpawnInterface','生成', icon=FIF.TAG)
        self.GiveInterface = Give('Give Interface', self)
        self.addSubInterface(self.SpawnInterface, 'SpawnInterface','生成', icon=FIF.TAG)
        self.addSubInterface(self.GiveInterface, 'GiveInterface','给予', icon=FIF.TAG)
        self.addSubInterface(self.MailInterface, 'MailInterface','邮件', icon=FIF.TAG)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.ServerInterface)
        self.pivot.setCurrentItem(self.ServerInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.ServerInterface.objectName())
        
    def __connectSignalToSlot(self):
        self.refillCard.clicked.connect(lambda: self.buttonClicked.emit('/refill'))
        self.healCard.clicked.connect(lambda: self.buttonClicked.emit('/heal'))
        self.helpCard.clicked.connect(lambda: self.buttonClicked.emit('/help'))
        self.reloadCard.clicked.connect(lambda: self.buttonClicked.emit('/reload'))
        self.accountCard.create_account.connect(lambda: self.handleAccountClicked('create'))
        self.accountCard.delete_account.connect(lambda: self.handleAccountClicked('delete'))
        self.kickCard.kick_player.connect(self.handleKickClicked)
        self.unstuckCard.unstuck_player.connect(self.handleUnstuckClicked)
        self.giveallCard.give_materials.connect(lambda: self.buttonClicked.emit('/giveall materials'))
        self.giveallCard.give_avatars.connect(lambda: self.buttonClicked.emit('/giveall avatars'))
        self.clearCard.clear_relics.connect(lambda: self.buttonClicked.emit('/clear relics'))
        self.clearCard.clear_lightcones.connect(lambda: self.buttonClicked.emit('/clear lightcones'))
        self.clearCard.clear_materials.connect(lambda: self.buttonClicked.emit('/clear materials'))
        self.clearCard.clear_items.connect(lambda: self.buttonClicked.emit('/clear items'))
        self.genderCard.gender_male.connect(lambda: self.buttonClicked.emit('/gender male'))
        self.genderCard.gender_female.connect(lambda: self.buttonClicked.emit('/gender female'))
        self.worldLevelCard.set_level.connect(self.handleWorldLevelClicked)
        self.avatarCard.avatar_set.connect(self.handleAvatarClicked)
        self.SceneInterface.emit_scene_id.connect(lambda id: self.buttonClicked.emit('/scene '+ id))

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
    
    def handleAccountClicked(self, types):
        if self.accountCard.account_name.text() != '':
            if types == 'create' and self.accountCard.account_uid.text() != '' and int(self.accountCard.account_uid.text())>0:
                self.buttonClicked.emit(f'/account {types} ' + self.accountCard.account_name.text() + ' ' + self.accountCard.account_uid.text())
            else:
                self.buttonClicked.emit(f'/account {types} ' + self.accountCard.account_name.text())
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
        if self.kickCard.account_uid.text() != '' and int(self.kickCard.account_uid.text())>0:
            self.buttonClicked.emit('/kick @' + self.kickCard.account_uid.text())
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
        if self.unstuckCard.stucked_uid.text() != '' and int(self.unstuckCard.stucked_uid.text())>0:
            self.buttonClicked.emit('/unstuck @' + self.unstuckCard.stucked_uid.text())
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
        if self.worldLevelCard.world_level.text() != '' and int(self.worldLevelCard.world_level.text())>0 and int(self.worldLevelCard.world_level.text())<=70:
            self.buttonClicked.emit('/worldlevel ' + self.worldLevelCard.world_level.text())
        else:
            InfoBar.error(
                title='请输入正确的开拓等级！',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent
            )
    
    def handleAvatarClicked(self):
        if (self.avatarCard.avatar_level.text() != '' and self.avatarCard.avatar_eidolon.text() != '' and self.avatarCard.avatar_skill.text() != '' and
            int(self.avatarCard.avatar_level.text())>0 and int(self.avatarCard.avatar_level.text())<=80 and
            int(self.avatarCard.avatar_eidolon.text())>0 and int(self.avatarCard.avatar_eidolon.text())<=6 and
            int(self.avatarCard.avatar_skill.text())>0 and int(self.avatarCard.avatar_skill.text())<=12):
            self.buttonClicked.emit('/avatar lv' + self.avatarCard.avatar_level.text() + ' r' + self.avatarCard.avatar_eidolon.text() + ' s' + self.avatarCard.avatar_skill.text())
        else:
            InfoBar.error(
                title='请输入正确的等级！',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent
            )
            