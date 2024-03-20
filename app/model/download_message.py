import os
import subprocess
from typing import Union
from PySide6.QtGui import QIcon
from PySide6.QtCore import QThread, Signal, QSize, Qt
from qfluentwidgets import (MessageBoxBase, TitleLabel, SubtitleLabel, BodyLabel, InfoBar, InfoBarPosition,
                            PlainTextEdit, FluentIconBase, HyperlinkButton, IndeterminateProgressBar)
from app.model.config import cfg
from app.model.setting_card import SettingCard


class HyperlinkCard_Launcher(SettingCard):
    def __init__(self, url_launcher, text_launcher, url_audio, text_audio, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.linkButton_launcher = HyperlinkButton(url_launcher, text_launcher, self)
        self.linkButton_audio = HyperlinkButton(url_audio, text_audio, self)
        self.hBoxLayout.addWidget(self.linkButton_launcher, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_audio, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)


class HyperlinkCard_Environment(SettingCard):
    def __init__(self, url_git, text_git ,url_jar, text_jar,url_mongodb, text_mongodb, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.linkButton_git = HyperlinkButton(url_git, text_git, self)
        self.linkButton_jar = HyperlinkButton(url_jar, text_jar, self)
        self.linkButton_mongodb = HyperlinkButton(url_mongodb, text_mongodb, self)
        self.hBoxLayout.addWidget(self.linkButton_git, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_jar, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_mongodb, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)


class HyperlinkCard_LunarCore(SettingCard):
    def __init__(self, url_repo, text_repo, url_res_1, text_res_1, url_res_2, text_res_2, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.linkButton_repo = HyperlinkButton(url_repo, text_repo, self)
        self.linkButton_res1 = HyperlinkButton(url_res_1, text_res_1, self)
        self.linkButton_res2 = HyperlinkButton(url_res_2, text_res_2, self)
        self.hBoxLayout.addWidget(self.linkButton_repo, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_res1, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_res2, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)


class HyperlinkCard_Tool(SettingCard):
    def __init__(self, url_fiddler, text_fiddler, url_mitmdump, text_mitmdump, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.linkButton_fiddler = HyperlinkButton(url_fiddler, text_fiddler, self)
        self.linkButton_mitmdump = HyperlinkButton(url_mitmdump, text_mitmdump, self)
        self.hBoxLayout.addWidget(self.linkButton_fiddler, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton_mitmdump, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)


class MessageLauncher(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel('选择启动器版本:                ')
        self.label1 = SubtitleLabel('    当前内容包含以下项目:')
        self.label2 = BodyLabel(f'        Firefly-Launcher:{cfg.APP_VERSION}')

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.label1)
        self.viewLayout.addWidget(self.label2)

        self.yesButton.setText('下载')
        self.cancelButton.setText('取消')


class MessageAudio(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel('选择音频版本:                ')
        self.label1 = SubtitleLabel('    当前内容包含以下项目:')
        self.label2 = BodyLabel('        Firefly-Launcher-Audio: 流萤语音')

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.label1)
        self.viewLayout.addWidget(self.label2)

        self.yesButton.setText('下载')
        self.cancelButton.setText('取消')


class MessageGit(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel('确认当前下载项目:                ')
        self.label1 = SubtitleLabel('    当前内容包含以下项目:')
        self.label2 = BodyLabel('        Git: Git环境')

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.label1)
        self.viewLayout.addWidget(self.label2)

        self.yesButton.setText('下载')
        self.cancelButton.setText('取消')


class MessageJava(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel('确认当前下载项目:                ')
        self.label1 = SubtitleLabel('    当前内容包含以下项目:')
        self.label2 = BodyLabel('        Java: Java环境')

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.label1)
        self.viewLayout.addWidget(self.label2)

        self.yesButton.setText('下载')
        self.cancelButton.setText('取消')


class MessageMongoDB(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel('确认当前下载项目:                ')
        self.label1 = SubtitleLabel('    当前内容包含以下项目:')
        self.label2 = BodyLabel('        MongoDB: MongoDB数据库')

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.label1)
        self.viewLayout.addWidget(self.label2)

        self.yesButton.setText('下载')
        self.cancelButton.setText('取消')


class MessageLunarCore(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel('确认当前下载项目:                ')
        self.label1 = SubtitleLabel('    当前内容包含以下项目:')
        self.label2 = BodyLabel('        LunarCore: LunarCore项目本体')

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.label1)
        self.viewLayout.addWidget(self.label2)

        self.yesButton.setText('下载')
        self.cancelButton.setText('取消')


class MessageLunarCoreRes(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel('确认当前下载项目:                ')
        self.label1 = SubtitleLabel('    当前内容包含以下项目:')
        self.label2 = BodyLabel('        LunarCoreRes: StarRailData和Configs')

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.label1)
        self.viewLayout.addWidget(self.label2)

        self.yesButton.setText('下载')
        self.cancelButton.setText('取消')


class MessageFiddler(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel('确认当前下载项目:                ')
        self.label1 = SubtitleLabel('    当前内容包含以下项目:')
        self.label2 = BodyLabel('        Fiddler: 用于Hutao-GS和LunarCore')

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.label1)
        self.viewLayout.addWidget(self.label2)

        self.yesButton.setText('下载')
        self.cancelButton.setText('取消')


class MessageMitmdump(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel('确认当前下载项目:                ')
        self.label1 = SubtitleLabel('    当前内容包含以下项目:')
        self.label2 = BodyLabel('        Mitmdump: 用于Grasscutter')

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.label1)
        self.viewLayout.addWidget(self.label2)

        self.yesButton.setText('下载')
        self.cancelButton.setText('取消')


class MessageDownload(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel('下载进程：')
        self.yesButton.setHidden(True)
        self.cancelButton.setHidden(True)
        self.progressBar = IndeterminateProgressBar(self)
        self.progressBar.setFixedHeight(6)
        self.commandOutput = PlainTextEdit()
        self.commandOutput.setReadOnly(True)
        self.commandOutput.setFixedSize(QSize(600, 450))
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.commandOutput)
        self.buttonLayout.addWidget(self.progressBar)

    def start_download(self, types, command, file_path, build_jar):
        self.runner = CommandRunner(types, command, file_path, build_jar)
        self.runner.output_updated.connect(self.update_output)
        self.runner.download_finished.connect(self.download_finished)
        self.runner.start()

    def update_output(self, output):
        self.commandOutput.appendPlainText(output)

    def download_finished(self, success, file_path):
        self.progressBar.setHidden(True)
        if success:
            self.yesButton.setHidden(False)
            self.yesButton.setText('完成')
            self.yesButton.clicked.connect(lambda: subprocess.Popen('start ' + file_path, shell=True))
        else:
            self.cancelButton.setHidden(False)
            self.cancelButton.setText('退出')


class CommandRunner(QThread):
    output_updated = Signal(str)
    download_finished = Signal(bool, str)
    def __init__(self, types, command, check, build_jar):
        super().__init__()
        self.types = types
        self.command = command
        self.check = check
        self.build_jar = build_jar

    def run(self):
        if self.types == 'url' and not os.path.exists('temp'):
            subprocess.run('mkdir temp', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
        for line in process.stdout:
            self.output_updated.emit(line.rstrip('\n'))
        process.communicate()
        if self.build_jar == 'lunarcore':
            self.output_updated.emit('正在编译LunarCore...')
            if cfg.chinaStatus:
                subprocess.run('copy /y "src\\patch\\gradle\\gradle-wrapper.properties" "server\\LunarCore\\gradle\\wrapper\\gradle-wrapper.properties" && '
                'copy /y "src\\patch\\gradle\\build.gradle" "server\\LunarCore\\build.gradle"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run('cd server/LunarCore && gradlew jar', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if process.returncode == 0:
                self.output_updated.emit('LunarCore编译完成！')
            else:
                self.output_updated.emit('LunarCore编译失败！')
        self.download_finished.emit(process.returncode == 0, self.check)


def generate_download_url(types, repo_url, mirror_url, repo_branch=None, mirror_branch=None, is_add=False):
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
        command = generate_download_url(types, cfg.DOWNLOAD_COMMANDS_AUDIO, cfg.DOWNLOAD_COMMANDS_AUDIO_MIRROR, '--branch audio ', '--branch audio ')
    elif name == 'git':
        w = MessageGit(self)
        types = 'url'
        file_path = os.path.join("temp", cfg.DOWNLOAD_COMMANDS_GIT.split('/')[-1])
        command = generate_download_url(types, cfg.DOWNLOAD_COMMANDS_GIT, cfg.DOWNLOAD_COMMANDS_GIT_MIRROR)
    elif name == 'java':
        w = MessageJava(self)
        types = 'url'
        file_path = os.path.join("temp", cfg.DOWNLOAD_COMMANDS_JAVA.split('/')[-1])
        command = generate_download_url(types, cfg.DOWNLOAD_COMMANDS_JAVA, cfg.DOWNLOAD_COMMANDS_JAVA_MIRROR)
    elif name =='mongodb':
        w = MessageMongoDB(self)
        types = 'url'
        file_path = os.path.join("temp", cfg.DOWNLOAD_COMMANDS_MONGODB.split('/')[-1])
        command = generate_download_url(types, cfg.DOWNLOAD_COMMANDS_MONGODB, cfg.DOWNLOAD_COMMANDS_MONGODB_MIRROR)
    elif name == 'lunarcore':
        w = MessageLunarCore(self)
        types = 'git'
        file_path = 'server\\LunarCore'
        command = generate_download_url(types, cfg.DOWNLOAD_COMMANDS_LUNARCORE, cfg.DOWNLOAD_COMMANDS_LUNARCORE_MIRROR, '', '--branch development ')
        build_jar = 'lunarcore'
    elif name == 'lunarcoreres':
        w = MessageLunarCoreRes(self)
        types = 'git'
        file_path = 'server\\LunarCore\\resources'
        command_1 = generate_download_url(types, cfg.DOWNLOAD_COMMANDS_LUNARCORE_RES_1, cfg.DOWNLOAD_COMMANDS_LUNARCORE_RES_MIRROR, '', '--branch lunarcoreres ')
        command_2 = generate_download_url(types, cfg.DOWNLOAD_COMMANDS_LUNARCORE_RES_2, '', '', '', True)
        command = command_1 + command_2
    elif name == 'fiddler':
        w = MessageFiddler(self)
        types = 'git'
        file_path = 'tool\\Fiddler'
        command = generate_download_url(types, cfg.DOWNLOAD_COMMANDS_FIDDLER, cfg.DOWNLOAD_COMMANDS_FIDDLER_MIRROR, '--branch fiddler ', '--branch fiddler ')
    elif name == 'mitmdump':
        w = MessageMitmdump(self)
        types = 'git'
        file_path = 'tool\\Mitmdump'
        command = generate_download_url(types, cfg.DOWNLOAD_COMMANDS_MITMDUMP, cfg.DOWNLOAD_COMMANDS_MITMDUMP_MIRROR, '--branch mitmdump ', '--branch mitmdump ')
    print(command)

    if w.exec():
        if not os.path.exists(file_path):
            x = MessageDownload(self)
            x.show()
            x.start_download(types, command, file_path, build_jar)
            if x.exec():
                self.clean_task()
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
    
def clean_task():
    output = subprocess.check_output('tasklist', shell=True)
    if 'curl.exe' in str(output):
        subprocess.run('taskkill /f /im curl.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif 'java.exe' in str(output):
        subprocess.run('taskkill /f /im java.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif 'git.exe' in str(output):
        subprocess.run('taskkill /f /im git.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)