import os
import json
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from PySide6.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import Pivot, qrouter, ScrollArea, PrimaryPushSettingCard, InfoBar, InfoBarPosition
from app.model.style_sheet import StyleSheet
from app.model.setting_group import SettingCardGroup
from app.model.toolkit_message import MessageFiddler, PrimaryPushSettingCard_Fiddler, PrimaryPushSettingCard_Sendcode, PrimaryPushSettingCard_Verifycode
from app.model.open_command import ping, send_code, verify_token
from app.toolkit_download import ToolkitDownload


class Toolkit(ScrollArea):
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
        self.ProxyToolInterface = SettingCardGroup(self.scrollWidget)
        self.FiddlerCard = PrimaryPushSettingCard_Fiddler(
            '脚本打开',
            '原版打开',
            FIF.VPN,
            'Fiddler(外部)',
            '使用Fiddler Scripts代理'
        )
        self.mitmdumpCard = PrimaryPushSettingCard( 
            '打开',
            FIF.VPN,
            'Mitmdump(外部)',
            '使用Mitmdump代理'
        )
        self.ConfigInterface = SettingCardGroup(self.scrollWidget)
        self.settingConfigCard = PrimaryPushSettingCard(
            '打开文件',
            FIF.LABEL,
            '启动器设置',
            '自定义启动器配置'
        )
        self.OpencommandInterface = SettingCardGroup(self.scrollWidget)
        self.pingCard = PrimaryPushSettingCard(
            '执行',
            FIF.SPEED_OFF,
            '确认插件连接状态',
            '基于lc-opencommand-plugin'
        )
        self.sendcodeCard = PrimaryPushSettingCard_Sendcode(
            '执行',
            FIF.SEND,
            '发送验证码',
            '基于lc-opencommand-plugin'
        )
        self.vertifycodeCard = PrimaryPushSettingCard_Verifycode(
            '执行',
            FIF.FINGERPRINT,
            '验证验证码',
            '基于lc-opencommand-plugin'
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
        self.ProxyToolInterface.addSettingCard(self.FiddlerCard)
        self.ProxyToolInterface.addSettingCard(self.mitmdumpCard)
        self.ConfigInterface.addSettingCard(self.settingConfigCard)
        self.OpencommandInterface.addSettingCard(self.pingCard)
        self.OpencommandInterface.addSettingCard(self.sendcodeCard)
        self.OpencommandInterface.addSettingCard(self.vertifycodeCard)

        # 栏绑定界面
        self.ToolkitDownloadInterface = ToolkitDownload('ToolkitDownloadInterface', self.scrollWidget)
        self.addSubInterface(self.ToolkitDownloadInterface, 'ToolkitDownloadInterface','下载', icon=FIF.DOWNLOAD)
        self.addSubInterface(self.ProxyToolInterface, 'ProxyToolInterface','代理', icon=FIF.CERTIFICATE)
        self.addSubInterface(self.ConfigInterface,'configInterface','配置', icon=FIF.EDIT)
        self.addSubInterface(self.OpencommandInterface, 'OpencommandInterface','远程', icon=FIF.CONNECT)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 10, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.ToolkitDownloadInterface)
        self.pivot.setCurrentItem(self.ToolkitDownloadInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.ToolkitDownloadInterface.objectName())

    def __initInfo(self):
        TEMP_TOKEN = ''

    def __connectSignalToSlot(self):
        self.FiddlerCard.clicked_script.connect(lambda: self.proxy_fiddler('script'))
        self.FiddlerCard.clicked_old.connect(lambda: self.proxy_fiddler('old'))
        self.mitmdumpCard.clicked.connect(self.proxy_mitmdump)
        self.settingConfigCard.clicked.connect(lambda: self.open_file('config/config.json'))
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

    def proxy_fiddler(self, mode):
        if mode =='script':
            w = MessageFiddler(self)
            if w.exec():
                self.open_file('src/patch/yuanshen/update.exe')
                self.open_file('tool/Fiddler/Fiddler.exe')
            else:
                self.open_file('src/patch/starrail/update.exe')
                self.open_file('tool/Fiddler/Fiddler.exe')
        elif mode == 'old':
            self.open_file('tool/Fiddler/Fiddler.exe')

    def open_file(self, file_path):
        if os.path.exists(file_path):
            subprocess.run(['start', file_path], shell=True)
        else:
            InfoBar.error(
                title="找不到文件，请重新下载！",
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )

    def proxy_mitmdump(self):
        if os.path.exists('tool/Mitmdump'):
            subprocess.run('cd ./tool/Mitmdump && start /b Proxy.exe', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            InfoBar.error(
                title="找不到文件，请重新下载！",
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )

    def handleOpencommandClicked(self, command, info=None):
        if command == 'ping':
            status, response = ping()
            if status == 'success':
                self.pingCard.iconLabel.setIcon(FIF.SPEED_HIGH)
                self.sendcodeCard.setDisabled(False)
                self.vertifycodeCard.setDisabled(False)
                InfoBar.success(
                    title="连接成功！",
                    content='请继续配置token',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=1000,
                    parent=self
                )
            else:
                InfoBar.error(
                    title="连接失败！",
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
                    title="发送成功！",
                    content=f'请尽快验证token({response})',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=1000,
                    parent=self
                )
            else:
                InfoBar.error(
                    title="发送失败！",
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
                    title="验证成功！",
                    content='远程执行配置完成',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=1000,
                    parent=self
                )
            else:
                InfoBar.error(
                    title="验证失败！",
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