import os
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from PySide6.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import Pivot, qrouter, ScrollArea, PrimaryPushSettingCard, HyperlinkCard, InfoBar, InfoBarPosition
from app.model.config import cfg
from app.model.style_sheet import StyleSheet
from app.model.setting_group import SettingCardGroup
from app.model.download_message import (MessageDownload, MessageLunarCore, MessageLunarCoreRes, HyperlinkCard_LunarCore, HyperlinkCard_Tool,
                                       HyperlinkCard_Environment, MessageLauncher, MessageGit, MessageJava, MessageMongoDB, MessageFiddler,
                                       MessageMitmdump, HyperlinkCard_Launcher, MessageAudio)


class Download(ScrollArea):
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

        # 添加项
        self.LauncherInterface = SettingCardGroup(self.scrollWidget)
        self.LauncherRepoCard = HyperlinkCard_Launcher(
            'https://github.com/letheriver2007/Firefly-Launcher',
            'Firefly-Launcher',
            'https://github.com/letheriver2007/Firefly-Launcher-Res',
            'Firefly-Launcher-Res',
            FIF.LINK,
            '项目仓库',
            '打开Firefly-Launcher相关项目仓库'
        )
        self.AudioDownloadCard = PrimaryPushSettingCard(
            '详细信息',
            FIF.DOWNLOAD,
            'Firefly-Launcher-Audio',
            '下载流萤音频文件'
        )
        self.EnvironmentInterface = SettingCardGroup(self.scrollWidget)
        self.EnvironmentRepoCard = HyperlinkCard_Environment(
            'https://git-scm.com/download/win',
            'Git',
            'https://www.oracle.com/java/technologies/javase-downloads.html',
            'Java',
            'https://www.mongodb.com/try/download/community',
            'MongoDB',
            FIF.LINK,
            '项目仓库',
            '打开各环境仓库'
        )
        self.GitDownloadCard = PrimaryPushSettingCard(
            '详细信息',
            FIF.DOWNLOAD,
            'Git',
            '下载Git安装包'
        )
        self.JavaDownloadCard = PrimaryPushSettingCard(
            '详细信息',
            FIF.DOWNLOAD,
            'Java',
            '下载Java安装包'
        )
        self.MongoDBDownloadCard = PrimaryPushSettingCard(
            '详细信息',
            FIF.DOWNLOAD,
            'MongoDB',
            '下载MongoDB安装包'
        )
        self.LunarCoreInterface = SettingCardGroup(self.scrollWidget)
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
        self.ToolInterface = SettingCardGroup(self.scrollWidget)
        self.ToolRepoCard = HyperlinkCard_Tool(
            'https://www.telerik.com/fiddler#fiddler-classic',
            'Fiddler',
            'https://mitmproxy.org/',
            'Mitmdump',
            FIF.LINK,
            '项目仓库',
            '打开代理工具仓库'
        )
        self.DownloadFiddlerCard = PrimaryPushSettingCard(
            '详细信息',
            FIF.DOWNLOAD,
            'Fiddler',
            '下载代理工具Fiddler'
        )
        self.DownloadMitmdumpCard = PrimaryPushSettingCard(
            '详细信息',
            FIF.DOWNLOAD,
            'Mitmdump',
            '下载代理工具Mitmdump'
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
        self.LauncherInterface.addSettingCard(self.LauncherRepoCard)
        self.LauncherInterface.addSettingCard(self.AudioDownloadCard)
        self.EnvironmentInterface.addSettingCard(self.EnvironmentRepoCard)
        self.EnvironmentInterface.addSettingCard(self.GitDownloadCard)
        self.EnvironmentInterface.addSettingCard(self.JavaDownloadCard)
        self.EnvironmentInterface.addSettingCard(self.MongoDBDownloadCard)
        self.LunarCoreInterface.addSettingCard(self.LunarCoreRepoCard)
        self.LunarCoreInterface.addSettingCard(self.LunarCoreDownloadCard)
        self.LunarCoreInterface.addSettingCard(self.LunarCoreResDownloadCard)
        self.ToolInterface.addSettingCard(self.ToolRepoCard)
        self.ToolInterface.addSettingCard(self.DownloadFiddlerCard)
        self.ToolInterface.addSettingCard(self.DownloadMitmdumpCard)

        # 栏绑定界面
        self.addSubInterface(self.LauncherInterface, 'LauncherInterface','启动器', icon=FIF.TAG)
        self.addSubInterface(self.EnvironmentInterface, 'EnvironmentInterface','环境', icon=FIF.TAG)
        self.addSubInterface(self.LunarCoreInterface, 'LunarCoreInterface','LunarCore', icon=FIF.TAG)
        self.addSubInterface(self.ToolInterface, 'ToolInterface','工具', icon=FIF.TAG)

        # 初始化配置界面
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 10, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.LauncherInterface)
        self.pivot.setCurrentItem(self.LauncherInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.LauncherInterface.objectName())
        
    def __connectSignalToSlot(self):
        self.AudioDownloadCard.clicked.connect(lambda: self.download_check('audio'))
        self.GitDownloadCard.clicked.connect(lambda: self.download_check('git'))
        self.JavaDownloadCard.clicked.connect(lambda: self.download_check('java'))
        self.MongoDBDownloadCard.clicked.connect(lambda: self.download_check('mongodb'))
        self.LunarCoreDownloadCard.clicked.connect(lambda: self.download_check('lunarcore'))
        self.LunarCoreResDownloadCard.clicked.connect(lambda: self.download_check('lunarcoreres'))
        self.DownloadFiddlerCard.clicked.connect(lambda: self.download_check('fiddler'))
        self.DownloadMitmdumpCard.clicked.connect(lambda: self.download_check('mitmdump'))

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
    
    def generate_download_url(self, types, repo_url, mirror_url, repo_branch=None, mirror_branch=None, is_add=False):
        if types == 'url':
            file = os.path.join("temp", repo_url.split('/')[-1])
            url_cfg = f'curl -o {file} -L '
            if cfg.chinaStatus.value:
                return url_cfg + mirror_url
            elif cfg.proxyStatus.value:
                url_cfg = f'curl -x http://127.0.0.1:7890 -o {file} -L '
            return url_cfg + repo_url
        elif types == 'git':
            git_cfg = 'git clone --progress '
            if not is_add:
                if cfg.chinaStatus.value:
                    return git_cfg + mirror_branch + mirror_url
                elif cfg.proxyStatus.value:
                    git_cfg = 'git -c http.proxy=http://127.0.0.1:7890 -c https.proxy=http://127.0.0.1:7890 clone --progress '
                return git_cfg + repo_branch + repo_url
            else:
                if cfg.chinaStatus.value:
                    return ''
                elif cfg.proxyStatus.value:
                    git_cfg = 'git -c http.proxy=http://127.0.0.1:7890 -c https.proxy=http://127.0.0.1:7890 clone --progress '
                return ' && ' + git_cfg + repo_branch + repo_url

    def download_check(self, name):
        build_jar = ''
        if name == 'audio':
            w = MessageAudio(self)
            types = 'git'
            file_path = 'src\\audio'
            command = self.generate_download_url(types, cfg.DOWNLOAD_COMMANDS_AUDIO, cfg.DOWNLOAD_COMMANDS_AUDIO_MIRROR, '--branch audio ', '--branch audio ')
        elif name == 'git':
            w = MessageGit(self)
            types = 'url'
            file_path = os.path.join("temp", cfg.DOWNLOAD_COMMANDS_GIT.split('/')[-1])
            command = self.generate_download_url(types, cfg.DOWNLOAD_COMMANDS_GIT, cfg.DOWNLOAD_COMMANDS_GIT_MIRROR)
        elif name == 'java':
            w = MessageJava(self)
            types = 'url'
            file_path = os.path.join("temp", cfg.DOWNLOAD_COMMANDS_JAVA.split('/')[-1])
            command = self.generate_download_url(types, cfg.DOWNLOAD_COMMANDS_JAVA, cfg.DOWNLOAD_COMMANDS_JAVA_MIRROR)
        elif name =='mongodb':
            w = MessageMongoDB(self)
            types = 'url'
            file_path = os.path.join("temp", cfg.DOWNLOAD_COMMANDS_MONGODB.split('/')[-1])
            command = self.generate_download_url(types, cfg.DOWNLOAD_COMMANDS_MONGODB, cfg.DOWNLOAD_COMMANDS_MONGODB_MIRROR)
        elif name == 'lunarcore':
            w = MessageLunarCore(self)
            types = 'git'
            file_path = 'server\\LunarCore'
            command = self.generate_download_url(types, cfg.DOWNLOAD_COMMANDS_LUNARCORE, cfg.DOWNLOAD_COMMANDS_LUNARCORE_MIRROR, '', '--branch lunarcore ')
            build_jar = 'lunarcore'
        elif name == 'lunarcoreres':
            w = MessageLunarCoreRes(self)
            types = 'git'
            file_path = 'server\\LunarCore\\resources'
            command_1 = self.generate_download_url(types, cfg.DOWNLOAD_COMMANDS_LUNARCORE_RES_1, cfg.DOWNLOAD_COMMANDS_LUNARCORE_RES_MIRROR, '', '--branch lunarcoreres ')
            command_2 = self.generate_download_url(types, cfg.DOWNLOAD_COMMANDS_LUNARCORE_RES_2, '', '', '', True)
            command = command_1 + command_2
        elif name == 'fiddler':
            w = MessageFiddler(self)
            types = 'git'
            file_path = 'tool\\Fiddler'
            command = self.generate_download_url(types, cfg.DOWNLOAD_COMMANDS_FIDDLER, cfg.DOWNLOAD_COMMANDS_FIDDLER_MIRROR, '--branch fiddler ', '--branch fiddler ')
        elif name == 'mitmdump':
            w = MessageMitmdump(self)
            types = 'git'
            file_path = 'tool\\Mitmdump'
            command = self.generate_download_url(types, cfg.DOWNLOAD_COMMANDS_MITMDUMP, cfg.DOWNLOAD_COMMANDS_MITMDUMP_MIRROR, '--branch mitmdump ', '--branch mitmdump ')
        print(command)

        if w.exec():
            if not os.path.exists(file_path):
                x = MessageDownload(self)
                x.show()
                x.start_download(types, command, file_path, build_jar)
                if x.exec():
                    InfoBar.success(
                        title='下载成功！',
                        content="",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=1000,
                        parent=self
                        )
                else:
                    # x.runner.terminate()
                    # self.clean_task()
                    InfoBar.error(
                        title='下载失败！',
                        content="",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self
                        )
            else:
                InfoBar.error(
                title=f'该目录已存在文件,无法下载！',
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
                )
                subprocess.Popen('start ' + file_path, shell=True)
    
    def clean_task(self):
        output = subprocess.check_output('tasklist', shell=True)
        if 'curl.exe' in str(output):
            subprocess.run('taskkill /f /im curl.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif 'java.exe' in str(output):
            subprocess.run('taskkill /f /im java.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif 'git.exe' in str(output):
            subprocess.run('taskkill /f /im git.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)