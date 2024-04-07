import os
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from PySide6.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import Pivot, qrouter, ScrollArea, PrimaryPushSettingCard, InfoBar, InfoBarPosition
from app.model.style_sheet import StyleSheet
from app.lunarcore_command import LunarCoreCommand
from app.lunarcore_edit import LunarCoreEdit
from app.model.setting_card import SettingCardGroup, HyperlinkCard_LunarCore, PrimaryPushSettingCard_Sendcode, PrimaryPushSettingCard_Verifycode
from app.model.download_process import DownloadCMD
from app.model.open_command import ping, send_code, verify_token
from app.model.config import cfg


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
        self.OpencommandInterface = SettingCardGroup(self.scrollWidget)
        self.pingCard = PrimaryPushSettingCard(
            self.tr('执行'),
            FIF.SPEED_OFF,
            self.tr('确认插件连接状态'),
            'Ping Web Server'
        )
        self.sendcodeCard = PrimaryPushSettingCard_Sendcode(
            self.tr('发送验证码')
        )
        self.vertifycodeCard = PrimaryPushSettingCard_Verifycode(
            self.tr('验证验证码')
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
        self.OpencommandInterface.addSettingCard(self.pingCard)
        self.OpencommandInterface.addSettingCard(self.sendcodeCard)
        self.OpencommandInterface.addSettingCard(self.vertifycodeCard)

        # 栏绑定界面
        self.addSubInterface(self.LunarCoreDownloadInterface, 'LunarCoreDownloadInterface',self.tr('下载'), icon=FIF.DOWNLOAD)
        self.addSubInterface(self.ConfigInterface,'configInterface',self.tr('配置'), icon=FIF.EDIT)
        self.LunarCoreCommandInterface = LunarCoreCommand('CommandInterface', self)
        self.addSubInterface(self.LunarCoreCommandInterface, 'LunarCoreCommandInterface',self.tr('命令'), icon=FIF.COMMAND_PROMPT)
        self.LunarCoreEditInterface = LunarCoreEdit('EditInterface', self)
        self.addSubInterface(self.LunarCoreEditInterface, 'LunarCoreEditInterface',self.tr('编辑器'), icon=FIF.LAYOUT)
        self.addSubInterface(self.OpencommandInterface, 'OpencommandInterface',self.tr('远程'), icon=FIF.CONNECT)

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
        TEMP_TOKEN = ''
    
    def __connectSignalToSlot(self):
        DownloadCMDSelf = DownloadCMD(self)
        self.LunarCoreDownloadCard.clicked.connect(lambda: DownloadCMDSelf.handleDownloadStarted('lunarcore'))
        self.LunarCoreResDownloadCard.clicked.connect(lambda: DownloadCMDSelf.handleDownloadStarted('lunarcoreres'))
        self.LunarCoreBuildCard.clicked.connect(self.handleLunarCoreBuild)
        self.GiveDataConfigCard.clicked.connect(lambda: subprocess.run(['start', f'.\\src\\data\\mygive.txt'], shell=True))
        self.RelicDataConfigCard.clicked.connect(lambda: subprocess.run(['start', f'.\\src\\data\\{cfg.get(cfg.language).value.name()}\\myrelic.txt'], shell=True))
        self.pingCard.clicked.connect(lambda: self.handleOpencommandClicked('ping'))
        self.sendcodeCard.clicked_sendcode.connect(lambda uid: self.handleOpencommandClicked('sendcode', uid))
        self.vertifycodeCard.clicked_verifycode.connect(lambda code: self.handleOpencommandClicked('vertifycode', code))

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

    def handleLunarCoreBuild(self):
        if os.path.exists('server\\LunarCore\\LunarCore.jar'):
            InfoBar.error(
                title=self.tr("LunarCore已编译！"),
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
            return
        if not os.path.exists('server\\LunarCore'):
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
        if cfg.chinaStatus:
            subprocess.run('copy /y "src\\patch\\gradle\\gradle-wrapper.properties" "server\\LunarCore\\gradle\\wrapper\\gradle-wrapper.properties" && '
            'copy /y "src\\patch\\gradle\\build.gradle" "server\\LunarCore\\build.gradle"', shell=True)
        process = subprocess.run('start cmd /c "cd server\\LunarCore && gradlew jar && pause"', shell=True)

    def handleOpencommandClicked(self, command, info=None):
        if command == 'ping':
            status, response = ping()
            if status == 'success':
                self.pingCard.iconLabel.setIcon(FIF.SPEED_HIGH)
                self.sendcodeCard.setDisabled(False)
                self.vertifycodeCard.setDisabled(False)
                InfoBar.success(
                    title=self.tr("连接成功！"),
                    content=self.tr('请继续配置token'),
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=1000,
                    parent=self
                )
            else:
                InfoBar.error(
                    title=self.tr("连接失败！"),
                    content=str(response),
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
        if command =='sendcode':
            status, response = send_code(info)
            if status == 'success':
                self.TEMP_TOKEN = response
                self.sendcodeCard.iconLabel.setIcon(FIF.SEND_FILL)
                InfoBar.success(
                    title=self.tr("发送成功！"),
                    content=str(response),
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=1000,
                    parent=self
                )
            else:
                InfoBar.error(
                    title=self.tr("发送失败！"),
                    content=str(response),
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
        if command =='vertifycode':
            status, response = verify_token(self.TEMP_TOKEN, info)
            if status == 'success':
                self.save_token(response)
                InfoBar.success(
                    title=self.tr("验证成功！"),
                    content=self.tr('远程执行配置完成'),
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=1000,
                    parent=self
                )
            else:
                InfoBar.error(
                    title=self.tr("验证失败！"),
                    content=str(response),
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )

    def save_token(self, token):
        with open('config/config.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            data['TOKEN'] = token
        with open('config/config.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)