import os
import json
import subprocess
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import Pivot, qrouter, ScrollArea, PrimaryPushSettingCard, InfoBar, InfoBarPosition, SwitchSettingCard
from app.model.style_sheet import StyleSheet
from app.lunarcore_command import LunarCoreCommand
from app.lunarcore_edit import LunarCoreEdit
from app.model.setting_card import (SettingCardGroup, HyperlinkCard_LunarCore, PrimaryPushSettingCard_UID, PrimaryPushSettingCard_API,
                                    PrimaryPushSettingCard_URL, PrimaryPushSettingCard_KEY, PrimaryPushSettingCard_Verify)
from app.model.download_process import SubDownloadCMD
from app.model.config import cfg, get_json, open_file
from app.model.remote import handleApply, handleVerify


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
        self.CommandConfigCard = PrimaryPushSettingCard(
            self.tr('打开文件'),
            FIF.LABEL,
            self.tr('自定义命令设置'),
            self.tr('手动配置自定义命令')
        )
        self.RelicDataConfigCard = PrimaryPushSettingCard(
            self.tr('打开文件'),
            FIF.LABEL,
            self.tr('遗器命令设置'),
            self.tr('自定义遗器命令配置')
        )
        self.BannerConfigCard = PrimaryPushSettingCard(
            self.tr('打开文件'),
            FIF.LABEL,
            self.tr('卡池设置'),
            self.tr('手动LC卡池数据配置')
        )
        self.RemoteInterface = SettingCardGroup(self.scrollWidget)
        self.patchCard = PrimaryPushSettingCard(
            self.tr('补丁'),
            FIF.ERASE_TOOL,
            'LunarCore-Patch',
            self.tr('魔改LunarCore核心, 以支持远程执行')
        )
        self.useRemoteCard = SwitchSettingCard(
            FIF.CODE,
            self.tr('启用远程执行'),
            self.tr('启用远程执行功能, 并接受可能存在的安全风险'),
            configItem=cfg.useRemote
        )
        self.setURLCard = PrimaryPushSettingCard_URL(
            self.tr('配置服务端地址'),
            self.tr('设置远程执行服务端地址')
        )
        self.setAPICard = PrimaryPushSettingCard_API(
            self.tr('配置服务端API'),
            self.tr('设置用于远程执行命令的地址, 适应不兼容服务端')
        )
        self.setUIDCard = PrimaryPushSettingCard_UID(
            self.tr('配置UID'),
            self.tr('设置默认远程目标玩家的UID')
        )
        self.VerifyCard = PrimaryPushSettingCard_Verify(
            self.tr('配置密码'),
            self.tr('通过验证码验证身份并设置密码')
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
        self.ConfigInterface.addSettingCard(self.CommandConfigCard)
        self.ConfigInterface.addSettingCard(self.RelicDataConfigCard)
        self.ConfigInterface.addSettingCard(self.BannerConfigCard)
        self.RemoteInterface.addSettingCard(self.patchCard)
        self.RemoteInterface.addSettingCard(self.useRemoteCard)
        self.RemoteInterface.addSettingCard(self.setURLCard)
        self.RemoteInterface.addSettingCard(self.setAPICard)
        self.RemoteInterface.addSettingCard(self.setUIDCard)
        self.RemoteInterface.addSettingCard(self.VerifyCard)

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
            self.setURLCard.setDisabled(True)
            self.setAPICard.setDisabled(True)
            self.setUIDCard.setDisabled(True)
            self.VerifyCard.setDisabled(True)
        url = get_json('./config/config.json', 'SERVER_URL')
        self.uid = get_json('./config/config.json', 'UID')
        key = get_json('./config/config.json', 'KEY')
        self.setURLCard.titleLabel.setText(self.tr('配置服务端地址 (当前: ') + url + ')')
        self.setUIDCard.titleLabel.setText(self.tr('配置UID (当前: ') + self.uid + ')')
        self.VerifyCard.titleLabel.setText(self.tr('配置密码 (当前: ') + key + ')')
    
    def __connectSignalToSlot(self):
        SubDownloadCMDSelf = SubDownloadCMD(self)
        self.LunarCoreDownloadCard.clicked.connect(lambda: SubDownloadCMDSelf.handleDownloadStarted('lunarcore'))
        self.LunarCoreResDownloadCard.clicked.connect(lambda: SubDownloadCMDSelf.handleDownloadStarted('lunarcoreres'))
        self.LunarCoreBuildCard.clicked.connect(self.handleLunarCoreBuild)

        self.CommandConfigCard.clicked.connect(lambda: open_file(self, f'.\\src\\data\\mycommand.txt'))
        self.RelicDataConfigCard.clicked.connect(lambda: open_file(self, f'.\\src\\data\\{cfg.get(cfg.language).value.name()}\\myrelic.txt'))
        self.BannerConfigCard.clicked.connect(lambda: open_file(self, f'.\\server\\LunarCore\\data\\Banners.json'))

        self.patchCard.clicked.connect(self.handlePatch)
        self.useRemoteCard.checkedChanged.connect(self.handleRemoteChanged)
        self.setURLCard.clicked_seturl.connect(lambda: self.handleRemoteClicked('seturl'))
        self.setAPICard.clicked_setapi.connect(lambda: self.handleRemoteClicked('setapi'))
        self.setUIDCard.clicked_setuid.connect(lambda: self.handleRemoteClicked('setuid'))
        self.VerifyCard.clicked_apply.connect(lambda: self.handleRemoteClicked('apply'))
        self.VerifyCard.clicked_verify.connect(lambda: self.handleRemoteClicked('verify'))

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
        'copy /y "src\\patch\\remote\\HttpServer.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\HttpServer.java" && '
        'copy /y "src\\patch\\remote\\ApplyHandler.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\handlers\\ApplyHandler.java" && '
        'copy /y "src\\patch\\remote\\CodeHandler.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\handlers\\CodeHandler.java" && '
        'copy /y "src\\patch\\remote\\PasswordHandler.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\handlers\\PasswordHandler.java" && '
        'copy /y "src\\patch\\remote\\RemoteHandler.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\handlers\\RemoteHandler.java" && '
        'copy /y "src\\patch\\remote\\VerifyHandler.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\handlers\\VerifyHandler.java" && '
        'copy /y "src\\patch\\remote\\JsonRequest.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\objects\\JsonRequest.java" && '
        'copy /y "src\\patch\\remote\\JsonResponse.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\objects\\JsonResponse.java" && '
        'copy /y "src\\patch\\remote\\Utils.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\util\\Utils.java"', shell=True)
        if os.path.exists('server\\LunarCore\\config.json'):
            subprocess.run('del /f /q "server\\LunarCore\\config.json"', shell=True)

        self.handleLunarCoreBuild(True)

    def handleRemoteChanged(self):
        if cfg.useRemote.value:
            self.setURLCard.setDisabled(False)
            self.setAPICard.setDisabled(False)
            self.setUIDCard.setDisabled(False)
            self.VerifyCard.setDisabled(False)
        else:
            self.setURLCard.setDisabled(True)
            self.setAPICard.setDisabled(True)
            self.setUIDCard.setDisabled(True)
            self.VerifyCard.setDisabled(True)

    def handleRemoteClicked(self, command):
        if command =='seturl':
            tmp_url = self.setURLCard.lineedit_seturl.text()
            if tmp_url != '':
                self.save(tmp_url, 'SERVER_URL')
                InfoBar.success(
                    title=self.tr("服务端地址设置成功！"),
                    content='',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=1000,
                    parent=self
                )
            else:
                InfoBar.error(
                    title=self.tr("服务端地址为空！"),
                    content='',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
        if command =='setapi':
            open_file(self, 'config/config.json')
        if command =='setuid':
            tmp_uid = self.setUIDCard.lineedit_setuid.text()
            if tmp_uid != '':
                self.save(tmp_uid, 'UID')
                InfoBar.success(
                    title=self.tr("UID设置成功！"),
                    content='',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=1000,
                    parent=self
                )
            else:
                InfoBar.error(
                    title=self.tr("UID为空！"),
                    content='',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
        if command =='apply':
            status, message = handleApply(self.uid)
            if status == "success":
                InfoBar.success(
                    title=self.tr("验证码发送成功！"),
                    content=self.tr("请在游戏内查收验证码"),
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=1000,
                    parent=self
                )
            elif status == "error":
                InfoBar.error(
                    title=self.tr("验证码发送失败！"),
                    content=str(message),
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
        if command =='verify':
            tmp_code = self.VerifyCard.lineedit_code.text()
            tmp_key = self.VerifyCard.lineedit_key.text()
            if tmp_code == '' or tmp_key == '':
                InfoBar.error(
                    title=self.tr("验证码或密码为空！"),
                    content='',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
                return

            status, message = handleVerify(self.uid, tmp_code, tmp_key)
            if status == "success":
                InfoBar.success(
                    title=self.tr("密码设置成功！"),
                    content='',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=1000,
                    parent=self
                )
            elif status == "error":
                InfoBar.error(
                    title=self.tr("验证失败！"),
                    content=str(message),
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
                
        self.__initInfo()

    def save(self, data, types):
        with open('config/config.json', 'r', encoding='utf-8') as file:
            info = json.load(file)
            info[types] = data
        with open('config/config.json', 'w', encoding='utf-8') as file:
            json.dump(info, file, indent=2, ensure_ascii=False)