import os
import json
import subprocess
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QApplication
from qfluentwidgets import (Pivot, qrouter, ScrollArea, PrimaryPushSettingCard, InfoBar, HyperlinkButton,
                            InfoBarPosition, SwitchSettingCard, LineEdit, PrimaryPushButton, FluentIcon,
                            PasswordLineEdit, InfoBarIcon)
from app.model.style_sheet import StyleSheet
from app.lunarcore_command import (Account, Kick, Unstuck, Custom, Giveall, Clear, WorldLevel,
                                   Avatar, Gender, Scene, Spawn, Give, Relic)
from app.lunarcore_edit import Warp
from app.model.setting_card import SettingCard, SettingCardGroup
from app.model.download_process import SubDownloadCMD
from app.model.config import cfg, get_json, open_file, save_json, Info
from app.model.remote import handleApply, handleVerify, handleCommandSend


class HyperlinkCard_LunarCore(SettingCard):
    def __init__(self, title, content=None, icon=FluentIcon.LINK):
        super().__init__(icon, title, content)
        self.linkButton_repo = HyperlinkButton('https://github.com/Melledy/LunarCore', 'LunarCore', self)
        self.linkButton_res1 = HyperlinkButton('https://github.com/Dimbreath/StarRailData', 'StarRailData', self)
        self.linkButton_res2 = HyperlinkButton('https://gitlab.com/Melledy/LunarCore-Configs', 'LunarCore-Configs',
                                               self)
        self.hBoxLayout.addWidget(self.linkButton_repo, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_res1, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_res2, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)


class PrimaryPushSettingCard_URL(SettingCard):
    clicked_seturl = Signal()

    def __init__(self, title, content, icon=FluentIcon.WIFI):
        super().__init__(icon, title, content)
        self.lineedit_seturl = LineEdit(self)
        self.lineedit_seturl.setPlaceholderText(self.tr("服务端地址"))
        self.lineedit_seturl.setFixedWidth(150)
        self.button_seturl = PrimaryPushButton(self.tr('设置'), self)
        self.hBoxLayout.addWidget(self.lineedit_seturl, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_seturl, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_seturl.clicked.connect(self.clicked_seturl)


class PrimaryPushSettingCard_API(SettingCard):
    clicked_setapi = Signal()

    def __init__(self, title, content, icon=FluentIcon.LABEL):
        super().__init__(icon, title, content)
        self.button_seturl = PrimaryPushButton(self.tr('打开文件'), self)
        self.hBoxLayout.addWidget(self.button_seturl, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_seturl.clicked.connect(self.clicked_setapi)


class PrimaryPushSettingCard_UID(SettingCard):
    clicked_setuid = Signal()

    def __init__(self, title, content, icon=FluentIcon.QUICK_NOTE):
        super().__init__(icon, title, content)
        self.lineedit_setuid = LineEdit(self)
        self.lineedit_setuid.setPlaceholderText("UID")
        self.lineedit_setuid.setFixedWidth(150)
        self.lineedit_setuid.setValidator(QIntValidator(self))
        self.button_setuid = PrimaryPushButton(self.tr('设置'), self)
        self.hBoxLayout.addWidget(self.lineedit_setuid, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_setuid, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_setuid.clicked.connect(self.clicked_setuid)


class PrimaryPushSettingCard_Verify(SettingCard):
    clicked_apply = Signal()
    clicked_verify = Signal()

    def __init__(self, title, content, icon=FluentIcon.FINGERPRINT):
        super().__init__(icon, title, content)
        self.button_apply = PrimaryPushButton(self.tr('发送'), self)
        self.lineedit_code = LineEdit(self)
        self.lineedit_code.setPlaceholderText(self.tr("验证码"))
        self.lineedit_code.setFixedWidth(100)
        self.lineedit_code.setValidator(QIntValidator(self))
        self.lineedit_key = PasswordLineEdit(self)
        self.lineedit_key.setPlaceholderText(self.tr("密码"))
        self.lineedit_key.setFixedWidth(150)
        self.button_verify = PrimaryPushButton(self.tr('设置'), self)
        self.hBoxLayout.addWidget(self.lineedit_code, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_apply, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.hBoxLayout.addWidget(self.lineedit_key, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_verify, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_apply.clicked.connect(self.clicked_apply)
        self.button_verify.clicked.connect(self.clicked_verify)


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
            FluentIcon.DOWNLOAD,
            'LunarCore',
            self.tr('下载LunarCore')
        )
        self.LunarCoreResDownloadCard = PrimaryPushSettingCard(
            self.tr('下载'),
            FluentIcon.DOWNLOAD,
            'LunarCore-Res',
            self.tr('下载LunarCore资源文件')
        )
        self.LunarCoreBuildCard = PrimaryPushSettingCard(
            self.tr('编译'),
            FluentIcon.ZIP_FOLDER,
            'LunarCore-Build',
            self.tr('编译LunarCore')
        )
        self.ConfigInterface = SettingCardGroup(self.scrollWidget)
        self.CommandConfigCard = PrimaryPushSettingCard(
            self.tr('打开文件'),
            FluentIcon.LABEL,
            self.tr('自定义命令设置'),
            self.tr('手动配置自定义命令')
        )
        self.RelicDataConfigCard = PrimaryPushSettingCard(
            self.tr('打开文件'),
            FluentIcon.LABEL,
            self.tr('遗器命令设置'),
            self.tr('自定义遗器命令配置')
        )
        self.BannerConfigCard = PrimaryPushSettingCard(
            self.tr('打开文件'),
            FluentIcon.LABEL,
            self.tr('卡池设置'),
            self.tr('手动LC卡池数据配置')
        )
        self.RemoteInterface = SettingCardGroup(self.scrollWidget)
        self.patchCard = PrimaryPushSettingCard(
            self.tr('补丁'),
            FluentIcon.ERASE_TOOL,
            'LunarCore-Patch',
            self.tr('魔改LunarCore核心, 以支持远程执行')
        )
        self.useRemoteCard = SwitchSettingCard(
            FluentIcon.CODE,
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
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 水平滚动条关闭
        self.setViewportMargins(20, 0, 20, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)  # 必须设置！！！

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
        self.addSubInterface(self.LunarCoreDownloadInterface, 'LunarCoreDownloadInterface', self.tr('下载'),
                             icon=FluentIcon.DOWNLOAD)
        self.addSubInterface(self.ConfigInterface, 'configInterface', self.tr('配置'), icon=FluentIcon.EDIT)
        self.addSubInterface(self.RemoteInterface, 'RemoteInterface', self.tr('远程'), icon=FluentIcon.CONNECT)
        self.LunarCoreCommandInterface = LunarCoreCommand('CommandInterface', self)
        self.addSubInterface(self.LunarCoreCommandInterface, 'LunarCoreCommandInterface', self.tr('命令'),
                             icon=FluentIcon.COMMAND_PROMPT)
        self.LunarCoreEditInterface = LunarCoreEdit('EditInterface', self)
        self.addSubInterface(self.LunarCoreEditInterface, 'LunarCoreEditInterface', self.tr('编辑器'),
                             icon=FluentIcon.LAYOUT)

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
        self.RelicDataConfigCard.clicked.connect(
            lambda: open_file(self, f'.\\src\\data\\{cfg.get(cfg.language).value.name()}\\myrelic.txt'))
        self.BannerConfigCard.clicked.connect(self.handleOpenLCBanner)

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

    def handleOpenLCBanner(self):
        if os.path.exists(f'.\\server\\LunarCore\\data\\Banners.json'):
            subprocess.run(['start', f'.\\server\\LunarCore\\data\\Banners.json'], shell=True)
            Info(self, "S", 1000, self.tr("文件已打开！"))
        else:
            file_error = InfoBar(
                icon=InfoBarIcon.ERROR,
                title=self.tr('找不到文件!'),
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            file_error_button = PrimaryPushButton(self.tr('前往下载'))
            file_error_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
            file_error.addWidget(file_error_button)
            file_error.show()
    
    def handleLunarCoreBuild(self, patch=False):
        if not patch and not os.path.exists('server\\LunarCore'):
            Info(self, 'E', 3000, self.tr('找不到服务端LunarCore!'))
            return

        if os.path.exists('server\\LunarCore\\LunarCore.jar'):
            subprocess.run('del /f /q "server\\LunarCore\\LunarCore.jar"', shell=True)

        if not patch and cfg.chinaStatus:
            subprocess.run(
                'copy /y "src\\patch\\gradle\\normal\\gradle-wrapper.properties" "server\\LunarCore\\gradle\\wrapper\\gradle-wrapper.properties" && '
                'copy /y "src\\patch\\gradle\\normal\\build.gradle" "server\\LunarCore\\build.gradle"', shell=True)
        elif patch and cfg.chinaStatus:
            subprocess.run(
                'copy /y "src\\patch\\gradle\\normal\\gradle-wrapper.properties" "server\\LunarCore\\gradle\\wrapper\\gradle-wrapper.properties" && '
                'copy /y "src\\patch\\gradle\\patch\\build-zh_CN.gradle" "server\\LunarCore\\build.gradle"', shell=True)
        elif patch and not cfg.chinaStatus:
            subprocess.run(
                'copy /y "src\\patch\\gradle\\normal\\gradle-wrapper.properties" "server\\LunarCore\\gradle\\wrapper\\gradle-wrapper.properties" && '
                'copy /y "src\\patch\\gradle\\patch\\build.gradle" "server\\LunarCore\\build.gradle"', shell=True)

        subprocess.run('start cmd /c "cd server\\LunarCore && gradlew jar && pause"', shell=True)

    def handlePatch(self):
        if not os.path.exists('server\\LunarCore\\src'):
            Info(self, 'E', 3000, self.tr('找不到Patch路径, 请勿使用预编译版本!'))
            return

        subprocess.run(
            'copy /y "src\\patch\\remote\\Config.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\Config.java" && '
            'copy /y "src\\patch\\remote\\GameServer.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\game\\GameServer.java" && '
            'copy /y "src\\patch\\remote\\HttpServer.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\HttpServer.java" && '
            'copy /y "src\\patch\\remote\\ApplyHandler.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\handlers\\ApplyHandler.java" && '
            'copy /y "src\\patch\\remote\\CodeHandler.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\handlers\\CodeHandler.java" && '
            'copy /y "src\\patch\\remote\\PasswordHandler.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\handlers\\PasswordHandler.java" && '
            'copy /y "src\\patch\\remote\\RemoteHandler.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\handlers\\RemoteHandler.java" && '
            'copy /y "src\\patch\\remote\\VerifyHandler.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\handlers\\VerifyHandler.java" && '
            'copy /y "src\\patch\\remote\\JsonRequest.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\objects\\JsonRequest.java" && '
            'copy /y "src\\patch\\remote\\JsonResponse.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\server\\http\\objects\\JsonResponse.java" && '
            'copy /y "src\\patch\\remote\\Utils.java" "server\\LunarCore\\src\\main\\java\\emu\\lunarcore\\util\\Utils.java"',
            shell=True)
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
        if command == 'seturl':
            tmp_url = self.setURLCard.lineedit_seturl.text()
            if tmp_url != '':
                save_json(tmp_url, 'SERVER_URL')
                Info(self, 'S', 1000, self.tr('服务端地址设置成功!'))
            else:
                Info(self, 'E', 3000, self.tr('服务端地址为空!'))
        if command == 'setapi':
            open_file(self, 'config/config.json')
        if command == 'setuid':
            tmp_uid = self.setUIDCard.lineedit_setuid.text()
            if tmp_uid != '':
                save_json(tmp_uid, 'UID')
                Info(self, 'S', 1000, self.tr('UID设置成功!'))
            else:
                Info(self, 'E', 3000, self.tr('UID为空!'))
        if command == 'apply':
            status, message = handleApply(self.uid)
            if status == "success":
                Info(self, 'S', 1000, self.tr('验证码发送成功!'), self.tr("请在游戏内查收验证码!"))
            elif status == "error":
                Info(self, 'E', 3000, self.tr('验证码发送失败!'), str(message))
        if command == 'verify':
            tmp_code = self.VerifyCard.lineedit_code.text()
            tmp_key = self.VerifyCard.lineedit_key.text()
            if tmp_code == '' or tmp_key == '':
                Info(self, 'E', 3000, self.tr('验证码或密码为空!'))
                return

            status, message = handleVerify(self.uid, tmp_code, tmp_key)
            if status == "success":
                Info(self, 'S', 1000, self.tr('密码设置成功!'))
            elif status == "error":
                Info(self, 'E', 3000, self.tr('验证码或密码错误!'), str(message))

        self.__initInfo()


class LunarCoreCommand(ScrollArea):
    Nav = Pivot
    command_update = Signal(str)

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
        self.ServerInterface = SettingCardGroup(self.scrollWidget)
        self.helpCard = PrimaryPushSettingCard(
            self.tr('使用'),
            FluentIcon.TAG,
            self.tr('查看服务端命令帮助'),
            '/help'
        )
        self.reloadCard = PrimaryPushSettingCard(
            self.tr('使用'),
            FluentIcon.TAG,
            self.tr('重载服务端'),
            '/reload'
        )
        self.accountCard = Account(
            self.tr('添加或删除账号')
        )
        self.kickCard = Kick(
            self.tr('踢出玩家')
        )
        self.unstuckCard = Unstuck(
            self.tr('解除场景未加载造成的卡死')
        )
        self.AccountInterface = SettingCardGroup(self.scrollWidget)
        self.giveallCard = Giveall(
            self.tr('给予全部')
        )
        self.clearCard = Clear(
            self.tr('清空物品')
        )
        self.worldLevelCard = WorldLevel(
            self.tr('设置世界等级')
        )
        self.refillCard = PrimaryPushSettingCard(
            self.tr('使用'),
            FluentIcon.TAG,
            self.tr('秘技点补充'),
            '/refill'
        )
        self.healCard = PrimaryPushSettingCard(
            self.tr('使用'),
            FluentIcon.TAG,
            self.tr('治疗全部队伍角色'),
            '/heal'
        )
        self.AvatarInterface = SettingCardGroup(self.scrollWidget)
        self.avatarCard = Avatar(
            self.tr('设置角色属性')
        )
        self.genderCard = Gender(
            self.tr('设置开拓者性别')
        )

        self.__initWidget()

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 水平滚动条关闭
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)  # 必须设置！！！

        self.updateText = LineEdit()
        self.updateText.setFixedSize(740, 35)
        self.clearButton = PrimaryPushButton(self.tr('清空'))
        self.saveButton = PrimaryPushButton(self.tr('保存'))
        self.copyButton = PrimaryPushButton(self.tr('复制'))
        self.actionButton = PrimaryPushButton(self.tr('执行'))
        self.clearButton.setFixedSize(80, 35)
        self.saveButton.setFixedSize(80, 35)
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
        self.ServerInterface.addSettingCard(self.helpCard)
        self.ServerInterface.addSettingCard(self.reloadCard)
        self.ServerInterface.addSettingCard(self.accountCard)
        self.ServerInterface.addSettingCard(self.kickCard)
        self.ServerInterface.addSettingCard(self.unstuckCard)

        self.AccountInterface.addSettingCard(self.giveallCard)
        self.AccountInterface.addSettingCard(self.clearCard)
        self.AccountInterface.addSettingCard(self.worldLevelCard)
        self.AccountInterface.addSettingCard(self.refillCard)
        self.AccountInterface.addSettingCard(self.healCard)

        self.AvatarInterface.addSettingCard(self.avatarCard)
        self.AvatarInterface.addSettingCard(self.genderCard)

        # 栏绑定界面
        self.addSubInterface(self.ServerInterface, 'ServerInterface', self.tr('服务端'), icon=FluentIcon.COMMAND_PROMPT)

        self.CustomInterface = Custom('CustomInterface', self)
        self.addSubInterface(self.CustomInterface, 'CustomInterface', self.tr('自定义'), icon=FluentIcon.COMMAND_PROMPT)

        self.addSubInterface(self.AccountInterface, 'AccountInterface', self.tr('账号'), icon=FluentIcon.COMMAND_PROMPT)
        self.addSubInterface(self.AvatarInterface, 'AvatarInterface', self.tr('角色'), icon=FluentIcon.COMMAND_PROMPT)

        self.SceneInterface = Scene('SceneInterface', self)
        self.addSubInterface(self.SceneInterface, 'SceneInterface', self.tr('场景'), icon=FluentIcon.COMMAND_PROMPT)
        self.SpawnInterface = Spawn('SpawnInterface', self)
        self.addSubInterface(self.SpawnInterface, 'SpawnInterface', self.tr('生成'), icon=FluentIcon.COMMAND_PROMPT)
        self.GiveInterface = Give('GiveInterface', self)
        self.addSubInterface(self.GiveInterface, 'GiveInterface', self.tr('给予'), icon=FluentIcon.COMMAND_PROMPT)
        self.RelicInterface = Relic('RelicInterface', self)
        self.addSubInterface(self.RelicInterface, 'RelicInterface', self.tr('遗器'), icon=FluentIcon.COMMAND_PROMPT)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.ServerInterface)
        self.pivot.setCurrentItem(self.ServerInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.ServerInterface.objectName())

        self.updateLayout = QHBoxLayout(self.updateContainer)
        self.updateLayout.addWidget(self.updateText, alignment=Qt.AlignCenter)
        self.updateLayout.addStretch(1)
        self.updateLayout.addWidget(self.clearButton, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(5)
        self.updateLayout.addWidget(self.saveButton, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(5)
        self.updateLayout.addWidget(self.copyButton, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(5)
        self.updateLayout.addWidget(self.actionButton, alignment=Qt.AlignCenter)
        self.updateLayout.addSpacing(15)
        self.vBoxLayout.addWidget(self.updateContainer)

    def __connectSignalToSlot(self):
        self.command_update.connect(self.handleCommandUpdate)
        self.clearButton.clicked.connect(lambda: self.updateText.clear())
        self.saveButton.clicked.connect(self.handleSaveClicked)
        self.copyButton.clicked.connect(lambda: self.handleCopyToClipboard('show'))
        self.actionButton.clicked.connect(self.handleActionClicked)

        self.helpCard.clicked.connect(lambda: self.command_update.emit('/help'))
        self.reloadCard.clicked.connect(lambda: self.command_update.emit('/reload'))

        self.accountCard.create_account.connect(lambda: self.handleAccountClicked('create'))
        self.accountCard.delete_account.connect(lambda: self.handleAccountClicked('delete'))
        self.kickCard.kick_player.connect(self.handleKickClicked)
        self.unstuckCard.unstuck_player.connect(self.handleUnstuckClicked)

        self.giveallCard.giveall_clicked.connect(lambda itemid: self.handleGiveallClicked(itemid))
        self.clearCard.clear_clicked.connect(lambda itemid: self.handleClearClicked(itemid))
        self.worldLevelCard.set_world_level.connect(lambda index: self.handleWorldLevelClicked(index))
        self.refillCard.clicked.connect(lambda: self.command_update.emit('/refill'))
        self.healCard.clicked.connect(lambda: self.command_update.emit('/heal'))

        self.avatarCard.avatar_set.connect(lambda index: self.handleAvatarClicked(index))
        self.genderCard.gender_male.connect(lambda: self.command_update.emit('/gender male'))
        self.genderCard.gender_female.connect(lambda: self.command_update.emit('/gender female'))

        self.SceneInterface.scene_id_signal.connect(lambda scene_id: self.command_update.emit('/scene ' + scene_id))
        self.SpawnInterface.monster_id_signal.connect(
            lambda monster_id, stage_id: self.handleSpawnClicked(monster_id, stage_id))
        self.GiveInterface.item_id_signal.connect(lambda item_id, index: self.handleGiveClicked(item_id, index))
        self.RelicInterface.relic_id_signal.connect(lambda relic_id: self.handleRelicClicked(relic_id))
        self.RelicInterface.custom_relic_signal.connect(lambda command: self.command_update.emit(command))

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
        self.updateText.clear()

    def handleCommandUpdate(self, text):
        self.updateText.clear()
        self.updateText.setText(text)
        if cfg.autoCopy.value:
            self.handleCopyToClipboard('hide')

    def handleSaveClicked(self):
        text = self.updateText.text()
        current_widget = self.stackedWidget.currentWidget()
        if text != '' and current_widget != self.CustomInterface:
            formatted_text = f"自定义命令 : {text}\n"
            with open('src/data/mycommand.txt', 'a', encoding='utf-8') as file:
                file.write(formatted_text)
            
            Info(self.parent, 'S', 1000, self.tr('保存成功!'))

            self.CustomInterface.handleMycommandLoad()

    def handleActionClicked(self):
        if not cfg.useRemote.value:
            remote_error = InfoBar(
                icon=InfoBarIcon.ERROR,
                title=self.tr('远程执行未启用!'),
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent
            )
            remote_error_button = PrimaryPushButton(self.tr('前往开启'))
            remote_error_button.clicked.connect(lambda: self.parent.stackedWidget.setCurrentIndex(2))
            remote_error.addWidget(remote_error_button)
            remote_error.show()
            return

        uid = get_json('./config/config.json', 'UID')
        key = get_json('./config/config.json', 'KEY')

        if uid != '' and key != '' and self.updateText.text() != '':
            try:
                status, response = handleCommandSend(uid, key, self.updateText.text())
                if status == 'success':
                    Info(self.parent, 'S', 1000, self.tr('执行成功!'), self.tr('请自行查看执行结果!'))
                else:
                    Info(self.parent, 'E', 3000, self.tr('执行失败!'), str(response))
            except Exception as e:
                Info(self.parent, 'E', 3000, self.tr('执行失败!'), str(e))
        else:
            Info(self.parent, 'E', 3000, self.tr('执行失败!'))

    def handleCopyToClipboard(self, status):
        text = self.updateText.text()
        app = QApplication.instance()
        if text != '':
            clipboard = app.clipboard()
            clipboard.setText(text)
            if status == 'show':
                Info(self.parent, 'S', 1000, self.tr('已复制到剪贴板!'))

    def handleAccountClicked(self, types):
        account_name = self.accountCard.account_name.text()
        account_uid = self.accountCard.account_uid.text()
        if account_name != '':
            account = f'/account {types} {account_name}'
            if types == 'create' and account_uid != '':
                account += ' ' + account_uid
            self.command_update.emit(account)
        else:
            Info(self.parent, 'E', 3000, self.tr('请输入正确的用户名!'))

    def handleKickClicked(self):
        account_uid = self.kickCard.account_uid.text()
        if account_uid != '':
            self.command_update.emit('/kick @' + account_uid)
        else:
            Info(self.parent, 'E', 3000, self.tr('请输入正确的UID!'))

    def handleUnstuckClicked(self):
        stuck_uid = self.unstuckCard.stuck_uid.text()
        if stuck_uid != '':
            self.command_update.emit('/unstuck @' + stuck_uid)
        else:
            Info(self.parent, 'E', 3000, self.tr('请输入正确的UID!'))

    def handleGiveallClicked(self, itemid):
        types = ['materials', 'avatars', 'lightcones', 'relics', 'icons']
        self.command_update.emit('/giveall ' + types[itemid])

    def handleClearClicked(self, itemid):
        types = ['relics', 'lightcones', 'lightcones', 'all']
        self.command_update.emit('/clear ' + types[itemid])

    def handleWorldLevelClicked(self, index):
        world_level = self.worldLevelCard.world_level.text()
        if world_level != '':
            if index == 0:
                self.command_update.emit('/level ' + world_level)
            elif index == 1:
                self.command_update.emit('/worldlevel ' + world_level)
        else:
            self.command_update.emit('')

    def handleAvatarClicked(self, index):
        avatar_level = self.avatarCard.avatar_level.text()
        avatar_eidolon = self.avatarCard.avatar_eidolon.text()
        avatar_skill = self.avatarCard.avatar_skill.text()
        types = ['', ' lineup', ' all']
        command = '/avatar'
        if index > -1:
            command += types[index]
        if avatar_level != '':
            command += ' lv' + avatar_level
        if avatar_eidolon != '':
            command += ' r' + avatar_eidolon
        if avatar_skill != '':
            command += ' s' + avatar_skill
        if command != '/avatar':
            self.command_update.emit(command)
        else:
            self.command_update.emit('')

    def handleSpawnClicked(self, monster_id, stage_id):
        monster_num_edit = self.SpawnInterface.monster_num_edit.text()
        monster_level_edit = self.SpawnInterface.monster_level_edit.text()
        monster_round_edit = self.SpawnInterface.monster_round_edit.text()
        command = '/spawn ' + monster_id + ' ' + stage_id
        if monster_num_edit != '':
            command += ' x' + monster_num_edit
        if monster_level_edit != '':
            command += ' lv' + monster_level_edit
        if monster_round_edit != '':
            command += ' r' + monster_round_edit
        self.command_update.emit(command)

    def handleGiveClicked(self, item_id, index):
        give_level_edit = self.GiveInterface.give_level_edit.text()
        give_eidolon_edit = self.GiveInterface.give_eidolon_edit.text()
        give_num_edit = self.GiveInterface.give_num_edit.text()
        command = '/give ' + item_id
        if index == 0:
            if give_level_edit != '':
                command += ' lv' + give_level_edit
            if give_eidolon_edit != '':
                command += ' r' + give_eidolon_edit
        elif index == 1:
            if give_num_edit != '':
                command += ' x' + give_num_edit
            if give_level_edit != '':
                command += ' lv' + give_level_edit
            if give_eidolon_edit != '':
                command += ' r' + give_eidolon_edit
        elif index == 2 or index == 3:
            if give_num_edit != '':
                command += ' x' + give_num_edit
        self.command_update.emit(command)

    def handleRelicClicked(self, relic_id):
        relic_level = self.RelicInterface.level_edit.text()
        main_entry_name = self.RelicInterface.main_now_edit.text()
        now_list_nozero = {k: v for k, v in self.RelicInterface.now_list.items() if v > 0}
        entry_table = self.RelicInterface.entry_table
        command = '/give ' + relic_id

        if relic_level != '':
            command += ' lv' + relic_level

        if main_entry_name != '':
            entry_index = 0
            for i in range(entry_table.rowCount()):
                if entry_table.item(i, 0).text() == main_entry_name and entry_table.item(i, 1).text() != self.tr(
                        '通用'):
                    entry_index = i
                    break
            main_entry = entry_table.item(entry_index, 2).text()
            command += ' s' + main_entry

        for entry_name, entry_num in now_list_nozero.items():
            if entry_name != '':
                entry_index = 0
                for i in range(entry_table.rowCount()):
                    if entry_table.item(i, 0).text() == entry_name and entry_table.item(i, 1).text() == self.tr('通用'):
                        entry_index = i
                        break
                side_entry = entry_table.item(entry_index, 2).text()
                command += ' ' + side_entry + ':' + str(entry_num)

        self.command_update.emit(command)


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
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 水平滚动条关闭
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)  # 必须设置！！！

        # 使用qss设置样式
        self.scrollWidget.setObjectName('scrollWidget')
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        # 项绑定到栏目

        # 栏绑定界面
        self.WarpInterface = Warp('WarpInterface', self)
        self.addSubInterface(self.WarpInterface, 'WarpInterface', self.tr('跃迁'), icon=FluentIcon.LABEL)

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
        self.parent.stackedWidget.currentChanged.connect(self.WarpInterface.handleEditDisabled)

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
