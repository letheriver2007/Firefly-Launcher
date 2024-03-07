import os
import subprocess
from typing import Union
from PySide6.QtGui import QIcon, QPainter, QColor
from PySide6.QtCore import QThread, Signal, QSize, Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from qfluentwidgets import (MessageBoxBase, TitleLabel, SubtitleLabel, BodyLabel, PlainTextEdit, PasswordLineEdit,
                            FluentIconBase, HyperlinkButton, IconWidget, FluentStyleSheet, isDarkTheme, drawIcon,
                            IndeterminateProgressBar)
from app.module.config import cfg


class SettingCard(QFrame):
    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(parent=parent)
        self.iconLabel = SettingIconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(content or '', self)
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        if not content:
            self.contentLabel.hide()

        self.setFixedHeight(70 if content else 50)
        self.iconLabel.setFixedSize(16, 16)

        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(16, 0, 0, 0)
        self.hBoxLayout.setAlignment(Qt.AlignVCenter)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)

        self.hBoxLayout.addWidget(self.iconLabel, 0, Qt.AlignLeft)
        self.hBoxLayout.addSpacing(16)

        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignLeft)

        self.hBoxLayout.addSpacing(16)
        self.hBoxLayout.addStretch(1)

        self.contentLabel.setObjectName('contentLabel')
        FluentStyleSheet.SETTING_CARD.apply(self)

    def setTitle(self, title: str):
        self.titleLabel.setText(title)

    def setContent(self, content: str):
        self.contentLabel.setText(content)
        self.contentLabel.setVisible(bool(content))

    def setValue(self, value):
        pass

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        if isDarkTheme():
            painter.setBrush(QColor(255, 255, 255, 13))
            painter.setPen(QColor(0, 0, 0, 50))
        else:
            painter.setBrush(QColor(255, 255, 255, 170))
            painter.setPen(QColor(0, 0, 0, 19))

        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 6, 6)


class SettingIconWidget(IconWidget):
    def paintEvent(self, e):
        painter = QPainter(self)

        if not self.isEnabled():
            painter.setOpacity(0.36)

        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        drawIcon(self._icon, painter, self.rect())


class PushSettingCard_Fiddler(SettingCard):
    clicked_script = Signal()
    clicked_old = Signal()
    def __init__(self, text_script, text_old, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.button_script = QPushButton(text_script, self)
        self.button_old = QPushButton(text_old, self)
        self.hBoxLayout.addWidget(self.button_script, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_old, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_script.clicked.connect(self.clicked_script)
        self.button_old.clicked.connect(self.clicked_old)


class PrimaryPushSettingCard_Fiddler(PushSettingCard_Fiddler):
    def __init__(self, text_script, text_old, icon, title, content=None, parent=None):
        super().__init__(text_script, text_old, icon, title, content, parent)
        self.button_script.setObjectName('primaryButton')
        self.button_old.setObjectName('primaryButton')


class PushSettingCard_Giveall(SettingCard):
    give_materials = Signal()
    give_avatars = Signal()
    def __init__(self, meterials, avatars, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.button_materials = QPushButton(meterials, self)
        self.button_avatars = QPushButton(avatars, self)
        self.hBoxLayout.addWidget(self.button_materials, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_avatars, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_materials.clicked.connect(self.give_materials)
        self.button_avatars.clicked.connect(self.give_avatars)


class PrimaryPushSettingCard_Giveall(PushSettingCard_Giveall):
    def __init__(self, meterials, avatars, icon, title, content=None, parent=None):
        super().__init__(meterials, avatars, icon, title, content, parent)
        self.button_materials.setObjectName('primaryButton')
        self.button_avatars.setObjectName('primaryButton')


class HyperlinkCard_Environment(SettingCard):
    def __init__(self, url_py, text_py,url_git, text_git ,url_jar, text_jar,url_mongodb, text_mongodb, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.linkButton_py = HyperlinkButton(url_py, text_py, self)
        self.linkButton_git = HyperlinkButton(url_git, text_git, self)
        self.linkButton_jar = HyperlinkButton(url_jar, text_jar, self)
        self.linkButton_mongodb = HyperlinkButton(url_mongodb, text_mongodb, self)
        self.hBoxLayout.addWidget(self.linkButton_py, 0, Qt.AlignRight)
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


class MessageFiddler(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel('选择需要使用Fiddler Scripts的服务端:    ')
        self.label1 = SubtitleLabel('    目前支持的服务端列表:')
        self.label2 = BodyLabel('        Yuanshen: Hutao-GS')
        self.label3 = BodyLabel('        StarRail: LunarCore')

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.label1)
        self.viewLayout.addWidget(self.label2)
        self.viewLayout.addWidget(self.label3)

        self.yesButton.setText('Yuanshen')
        self.cancelButton.setText('StarRail')


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


class MessagePython(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel('确认当前下载项目:                ')
        self.label1 = SubtitleLabel('    当前内容包含以下项目:')
        self.label2 = BodyLabel('        Python: Python环境')

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

    def clean_task(self):
        if self.runner.isRunning():
            self.runner.terminate()
        output = subprocess.check_output('tasklist', shell=True)
        if 'curl.exe' in str(output):
            subprocess.run('taskkill /f /im curl.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif 'java.exe' in str(output):
            subprocess.run('taskkill /f /im java.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif 'git.exe' in str(output):
            subprocess.run('taskkill /f /im git.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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