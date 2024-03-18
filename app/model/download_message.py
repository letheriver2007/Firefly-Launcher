import os
import subprocess
from typing import Union
from PySide6.QtGui import QIcon
from PySide6.QtCore import QThread, Signal, QSize, Qt
from qfluentwidgets import (MessageBoxBase, TitleLabel, SubtitleLabel, BodyLabel,
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