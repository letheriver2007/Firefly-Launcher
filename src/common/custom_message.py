import subprocess
from PySide6.QtCore import QThread, Signal, QSize
from qfluentwidgets import MessageBoxBase, TitleLabel, SubtitleLabel, BodyLabel, PlainTextEdit, PasswordLineEdit
from src.common.login_message_base import LoginMessageBase


class MessageLogin(LoginMessageBase):
    passwordEntered = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel('你的老婆是？    ')
        self.passwordLabel = PasswordLineEdit(self)
        self.passwordLabel.setFixedWidth(300)
        self.passwordLabel.setPlaceholderText('请输入TA的英文名')
        self.cancelButton.setHidden(True)
        self.yesButton.setText('登录')
        self.yesButton.clicked.connect(self.emitPassword)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.passwordLabel)

    def emitPassword(self, password):
        password = self.passwordLabel.text()
        self.passwordEntered.emit(password)


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


class MessageTool(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel('确认当前下载项目:                ')
        self.label1 = SubtitleLabel('    当前内容包含以下项目:')
        self.label2 = BodyLabel('        Fiddler: 用于Hutao-GS和LunarCore')
        self.label3 = BodyLabel('        Mitmdump: 用于Grasscutter')

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.label1)
        self.viewLayout.addWidget(self.label2)
        self.viewLayout.addWidget(self.label3)

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


class MessageDownload(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel('下载进程：')
        self.commandOutput = PlainTextEdit()
        self.commandOutput.setReadOnly(True)
        self.commandOutput.setFixedSize(QSize(600, 450))
        self.cancelButton.clicked.connect(self.cancel_download)
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.commandOutput)

    def start_download(self, command, jar=False):
        self.jar = jar
        self.yesButton.setHidden(True)
        self.runner = CommandRunner(command)
        self.runner.output_updated.connect(self.update_output)
        self.runner.download_finished.connect(self.download_finished)
        self.runner.start()

    def update_output(self, output):
        self.commandOutput.appendPlainText(output)

    def download_finished(self, success):
        if success:
            if self.jar:
                self.update_output('LunarCore编译完成')
                subprocess.run('cd server/LunarCore && gradlew jar', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.yesButton.setText('完成')
            self.cancelButton.setHidden(True)
            self.yesButton.setHidden(False)

    def cancel_download(self):
        self.runner.terminate()


class CommandRunner(QThread):
    output_updated = Signal(str)
    download_finished = Signal(bool)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
        for line in process.stdout:
            self.output_updated.emit(line.rstrip('\n'))
        process.communicate()
        success = process.returncode == 0
        self.download_finished.emit(success)