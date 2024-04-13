import os
import json
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from PySide6.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import Pivot, qrouter, ScrollArea, PrimaryPushSettingCard, InfoBar, InfoBarPosition, SwitchSettingCard
from app.model.style_sheet import StyleSheet
from app.lunarcore_command import LunarCoreCommand
from app.lunarcore_edit import LunarCoreEdit
from app.model.setting_card import (SettingCardGroup, HyperlinkCard_LunarCore, PrimaryPushSettingCard_UID,
                                    PrimaryPushSettingCard_API, PrimaryPushSettingCard_PWD)
from app.model.download_process import SubDownloadCMD
from app.model.config import cfg, get_json


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
            self.tr('项目仓库'),
            self.tr('打开LunarCore相关仓库')
        )
        self.LunarCoreDownloadCard = PrimaryPushSettingCard(
            self.tr('下载'),
            FIF.DOWNLOAD,
            'LunarCore',
            self.tr('下载LunarCore')
        )
        self.LunarCoreResDownloadCard = PrimaryPushSettingCard(
            self.tr('下载'),
            FIF.DOWNLOAD,
            'LunarCore-Res',
            self.tr('下载LunarCore资源文件')
        )
        self.LunarCoreBuildCard = PrimaryPushSettingCard(
            self.tr('编译'),
            FIF.ZIP_FOLDER,
            'LunarCore-Build',
            self.tr('编译LunarCore')
        )
        self.ConfigInterface = SettingCardGroup(self.scrollWidget)
        self.GiveDataConfigCard = PrimaryPushSettingCard(
            self.tr('打开文件'),
            FIF.LABEL,
            self.tr('给予命令设置'),
            self.tr('自定义给予命令配置')
        )
        self.RelicDataConfigCard = PrimaryPushSettingCard(
            self.tr('打开文件'),
            FIF.LABEL,
            self.tr('遗器命令设置'),
            self.tr('自定义遗器命令配置')
        )
        self.RemoteInterface = SettingCardGroup(self.scrollWidget)
        self.useRemoteCard = SwitchSettingCard(
            FIF.CODE,
            self.tr('启用远程执行'),
            self.tr('启用远程执行功能, 并接受可能存在的安全风险'),
            configItem=cfg.useRemote
        )
        self.patchCard = PrimaryPushSettingCard(
            self.tr('补丁'),
            FIF.ERASE_TOOL,
            'LunarCore-Patch',
            self.tr('魔改LunarCore核心, 以支持远程执行')
        )
        self.setUIDCard = PrimaryPushSettingCard_UID(
            self.tr('配置UID'),
            self.tr('设置默认远程目标玩家的UID')
        )
        self.setPWDCard = PrimaryPushSettingCard_PWD(
            self.tr('配置密码'),
            self.tr('复制config.json中gm_public密码')
        )
        self.setAPICard = PrimaryPushSettingCard_API(
            self.tr('配置服务器API地址'),
            self.tr('设置服务器用于远程执行命令的API地址')
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
        self.__initInfo()
        self.__connectSignalToSlot()

    def __initLayout(self):
        # 项绑定到栏目
        self.LunarCoreDownloadInterface.addSettingCard(self.LunarCoreRepoCard)
        self.LunarCoreDownloadInterface.addSettingCard(self.LunarCoreDownloadCard)
        self.LunarCoreDownloadInterface.addSettingCard(self.LunarCoreResDownloadCard)
        self.LunarCoreDownloadInterface.addSettingCard(self.LunarCoreBuildCard)
        self.ConfigInterface.addSettingCard(self.GiveDataConfigCard)
        self.ConfigInterface.addSettingCard(self.RelicDataConfigCard)
        self.RemoteInterface.addSettingCard(self.useRemoteCard)
        self.RemoteInterface.addSettingCard(self.patchCard)
        self.RemoteInterface.addSettingCard(self.setUIDCard)
        self.RemoteInterface.addSettingCard(self.setPWDCard)
        self.RemoteInterface.addSettingCard(self.setAPICard)

        # 栏绑定界面
        self.addSubInterface(self.LunarCoreDownloadInterface, 'LunarCoreDownloadInterface',self.tr('下载'), icon=FIF.DOWNLOAD)
        self.addSubInterface(self.ConfigInterface,'configInterface',self.tr('配置'), icon=FIF.EDIT)
        self.addSubInterface(self.RemoteInterface, 'RemoteInterface',self.tr('远程'), icon=FIF.CONNECT)
        self.LunarCoreCommandInterface = LunarCoreCommand('CommandInterface', self)
        self.addSubInterface(self.LunarCoreCommandInterface, 'LunarCoreCommandInterface',self.tr('命令'), icon=FIF.COMMAND_PROMPT)
        self.LunarCoreEditInterface = LunarCoreEdit('EditInterface', self)
        self.addSubInterface(self.LunarCoreEditInterface, 'LunarCoreEditInterface',self.tr('编辑器'), icon=FIF.LAYOUT)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 10, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.LunarCoreDownloadInterface)
        self.pivot.setCurrentItem(self.LunarCoreDownloadInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.LunarCoreDownloadInterface.objectName())
    
    def __initInfo(self):
        if not cfg.useRemote.value:
            self.setUIDCard.setDisabled(True)
            self.setPWDCard.setDisabled(True)
            self.setAPICard.setDisabled(True)
        uid = get_json('./config/config.json', 'UID')
        pwd = get_json('./config/config.json', 'PWD')
        api = get_json('./config/config.json', 'SERVER_API')
        self.setUIDCard.titleLabel.setText(self.tr('配置UID (当前: ') + uid + ')')
        self.setPWDCard.titleLabel.setText(self.tr('配置密码 (当前: ') + pwd + ')')
        self.setAPICard.titleLabel.setText(self.tr('配置服务器API地址 (当前: ') + api + ')')
    
    def __connectSignalToSlot(self):
        SubDownloadCMDSelf = SubDownloadCMD(self)
        self.LunarCoreDownloadCard.clicked.connect(lambda: SubDownloadCMDSelf.handleDownloadStarted('lunarcore'))
        self.LunarCoreResDownloadCard.clicked.connect(lambda: SubDownloadCMDSelf.handleDownloadStarted('lunarcoreres'))
        self.LunarCoreBuildCard.clicked.connect(self.handleLunarCoreBuild)
        self.GiveDataConfigCard.clicked.connect(lambda: subprocess.run(['start', f'.\\src\\data\\mygive.txt'], shell=True))
        self.RelicDataConfigCard.clicked.connect(lambda: subprocess.run(['start', f'.\\src\\data\\{cfg.get(cfg.language).value.name()}\\myrelic.txt'], shell=True))
        self.useRemoteCard.checkedChanged.connect(self.handleRemoteChanged)
        self.patchCard.clicked.connect(self.handlePatch)
        self.setUIDCard.clicked_setuid.connect(lambda uid: self.handleRemoteClicked('setuid', uid))
        self.setPWDCard.clicked_setpwd.connect(lambda pwd: self.handleRemoteClicked('setpwd', pwd))
        self.setAPICard.clicked_setapi.connect(lambda api: self.handleRemoteClicked('setapi', api))

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

    def handleLunarCoreBuild(self, patch=False):

        if not patch and not os.path.exists('server\\LunarCore'):
            InfoBar.error(
                title=self.tr("LunarCore不存在, 请先下载！"),
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
            return

        if os.path.exists('server\\LunarCore\\LunarCore.jar'):
            subprocess.run('del /f /q "server\\LunarCore\\LunarCore.jar"', shell=True)

        if patch == False and cfg.chinaStatus:
            subprocess.run('copy /y "src\\patch\\gradle\\normal\\gradle-wrapper.properties" "server\\LunarCore\\gradle\\wrapper\\gradle-wrapper.properties" && '
            'copy /y "src\\patch\\gradle\\normal\\build.gradle" "server\\LunarCore\\build.gradle"', shell=True)
        elif patch and cfg.chinaStatus:
            subprocess.run('copy /y "src\\patch\\gradle\\normal\\gradle-wrapper.properties" "server\\LunarCore\\gradle\\wrapper\\gradle-wrapper.properties" && '
            'copy /y "src\\patch\\gradle\\patch\\build-zh_CN.gradle" "server\\LunarCore\\build.gradle"', shell=True)
        elif patch and not cfg.chinaStatus:
            subprocess.run('copy /y "src\\patch\\gradle\\normal\\gradle-wrapper.properties" "server\\LunarCore\\gradle\\wrapper\\gradle-wrapper.properties" && '
            'copy /y "src\\patch\\gradle\\patch\\build.gradle" "server\\LunarCore\\build.gradle"', shell=True)

        process = subprocess.run('start cmd /c "cd server\\LunarCore && gradlew jar && pause"', shell=True)

    def handleRemoteChanged(self):
        if cfg.useRemote.value:
            self.setUIDCard.setDisabled(False)
            self.setPWDCard.setDisabled(False)
            self.setAPICard.setDisabled(False)
        else:
            self.setUIDCard.setDisabled(True)
            self.setPWDCard.setDisabled(True)
            self.setAPICard.setDisabled(True)
    
    def handlePatch(self):
        if not os.path.exists('server\\LunarCore\\src'):
            InfoBar.error(
                title=self.tr("找不到Patch路径, 请勿使用预编译版本!"),
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
            return

        subprocess.run('copy /y "src\\patch\\remote\\Config.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\Config.java" && '
        'copy /y "src\\patch\\remote\\GameServer.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\game\\GameServer.java" && '
        'copy /y "src\\patch\\remote\\GMHandler.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\handlers\\GMHandler.java" && '
        'copy /y "src\\patch\\remote\\HttpServer.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\HttpServer.java" && '
        'copy /y "src\\patch\\remote\\JsonRequest.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\objects\\JsonRequest.java" && '
        'copy /y "src\\patch\\remote\\JsonResponse.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\objects\\JsonResponse.java" && '
        'copy /y "src\\patch\\remote\\Utils.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\util\\Utils.java"', shell=True)
    
        self.handleLunarCoreBuild(True)

    
    def handleRemoteClicked(self, command, data):
        if command =='setuid':
            self.save(data, 'UID')
            InfoBar.success(
                title=self.tr("UID设置成功！"),
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
        if command =='setpwd':
            self.save(data, 'PWD')
            InfoBar.success(
                title=self.tr("密码设置成功！"),
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
        if command =='setapi':
            self.save(data, 'SERVER_API')
            InfoBar.success(
                title=self.tr("API地址设置成功！"),
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
        self.__initInfo()

    def save(self, data, types):
        with open('config/config.json', 'r', encoding='utf-8') as file:
            info = json.load(file)
            info[types] = data
        with open('config/config.json', 'w', encoding='utf-8') as file:
            json.dump(info, file, indent=2, ensure_ascii=False)