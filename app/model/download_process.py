import os
import time
import subprocess
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QDialog, QVBoxLayout
from PySide6.QtCore import QThread, Signal, Qt
from qfluentwidgets import PlainTextEdit
from app.model.config import cfg, Info


class SubDownloadCMD(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.palette = self.palette()
        self.palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0))
        self.setPalette(self.palette)
        self.setFixedSize(960, 512)
        self.setCursor(Qt.CrossCursor)
        self.setWindowTitle(cfg.APP_NAME)

        self.commandOutput = PlainTextEdit()
        self.commandOutput.setReadOnly(True)
        self.commandOutput.setStyleSheet(
            "color: #FFFFFF; background-color: #000000; font-family: Cascadia Mono; font-size: 13pt;")

        self.viewLayout = QVBoxLayout(self)
        self.viewLayout.addWidget(self.commandOutput)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)

    def handleDownloadStarted(self, name):
        types, command, file_path = handleDownloadGenerate(name)
        if not os.path.exists(file_path):
            self.show()
            self.runner = CommandRunner(types, command, file_path)
            self.runner.command_updated.connect(self.handleTextUpdate)
            self.runner.download_finished.connect(self.handleDownloadFinished)
            self.success = False
            self.commandOutput.clear()
            self.runner.start()
            if self.exec_() == 0:
                self.runner.download_finished.emit(-1, file_path)
        else:
            Info(self.parent, 'E', 3000, self.tr('该目录已存在文件！'))
            subprocess.Popen('start ' + file_path, shell=True)

    def handleTextUpdate(self, text):
        self.commandOutput.appendPlainText(text)

    def handleDownloadFinished(self, returncode, file_path):
        if returncode == 0:
            Info(self.parent, 'S', 2000, self.tr('下载成功！'))
            self.success = True
            self.commandOutput.clear()
            self.close()
            subprocess.Popen('start ' + file_path, shell=True)
        if not self.success:
            if returncode == -1:
                Info(self.parent, 'E', 3000, self.tr('下载取消！'))
            else:
                Info(self.parent, 'E', 3000, self.tr('下载失败！'))
        self.runner.process.kill()
        self.runner.terminate()
        output = subprocess.check_output('tasklist', shell=True)
        if 'curl.exe' in str(output):
            subprocess.run('taskkill /f /im curl.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if 'java.exe' in str(output):
            subprocess.run('taskkill /f /im java.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if 'git.exe' in str(output):
            subprocess.run('taskkill /f /im git.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


class CommandRunner(QThread):
    command_updated = Signal(str)
    download_finished = Signal(int, str)

    def __init__(self, types, command, check):
        super().__init__()
        self.types = types
        self.command = command
        self.check = check

    def run(self):
        if self.types == 'url' and not os.path.exists('temp'):
            subprocess.run('mkdir temp', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        self.process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True,
                                        text=True)
        for line in self.process.stdout:
            self.command_updated.emit(line.rstrip('\n'))
        self.process.communicate()
        self.download_finished.emit(self.process.returncode, self.check)


def __handleUrlGenerate(types, repo_url, mirror_url, repo_branch=None, mirror_branch=None, is_add=False):
    if types == 'url':
        file = os.path.join("temp", repo_url.split('/')[-1])
        url_cfg = f'curl -o {file} -L '
        if cfg.chinaStatus.value:
            return url_cfg + mirror_url
        elif cfg.proxyStatus.value:
            url_cfg = f'curl -x http://127.0.0.1:7890 -o {file} -L '
        return url_cfg + repo_url
    elif types == 'git':
        git_cfg = 'git config --global core.longpaths true && git clone --progress '
        if not is_add:
            if cfg.chinaStatus.value:
                return git_cfg + mirror_branch + mirror_url
            elif cfg.proxyStatus.value:
                git_cfg = 'git config --global core.longpaths true && git -c http.proxy=http://127.0.0.1:7890 -c https.proxy=http://127.0.0.1:7890 clone --progress '
            return git_cfg + repo_branch + repo_url
        else:
            if cfg.chinaStatus.value:
                return ''
            elif cfg.proxyStatus.value:
                git_cfg = 'git config --global core.longpaths true && git -c http.proxy=http://127.0.0.1:7890 -c https.proxy=http://127.0.0.1:7890 clone --progress '
            return ' && ' + git_cfg + repo_branch + repo_url


def handleDownloadGenerate(name):
    if name == 'audio':
        types = 'git'
        file_path = 'src\\audio'
        command = __handleUrlGenerate(types, cfg.DOWNLOAD_COMMANDS_AUDIO, cfg.DOWNLOAD_COMMANDS_AUDIO_MIRROR,
                                      '--branch audio ', '--branch audio ')
    elif name == 'git':
        types = 'url'
        file_path = os.path.join("temp", cfg.DOWNLOAD_COMMANDS_GIT.split('/')[-1])
        command = __handleUrlGenerate(types, cfg.DOWNLOAD_COMMANDS_GIT, cfg.DOWNLOAD_COMMANDS_GIT_MIRROR)
    elif name == 'java':
        types = 'url'
        file_path = os.path.join("temp", cfg.DOWNLOAD_COMMANDS_JAVA.split('/')[-1])
        command = __handleUrlGenerate(types, cfg.DOWNLOAD_COMMANDS_JAVA, cfg.DOWNLOAD_COMMANDS_JAVA_MIRROR)
    elif name == 'mongodb_installer':
        types = 'url'
        file_path = os.path.join("temp", cfg.DOWNLOAD_COMMANDS_MONGODB_INSTALLER.split('/')[-1])
        command = __handleUrlGenerate(types, cfg.DOWNLOAD_COMMANDS_MONGODB_INSTALLER, cfg.DOWNLOAD_COMMANDS_MONGODB_INSTALLER_MIRROR)
    elif name == 'mongodb_portable':
        types = 'git'
        file_path = 'tool\\mongodb'
        command = __handleUrlGenerate(types, cfg.DOWNLOAD_COMMANDS_MONGODB_PORTABLE, cfg.DOWNLOAD_COMMANDS_MONGODB_PORTABLE_MIRROR,
                                      '--branch mongodb ', '--branch mongodb ')
        print(command)
    elif name == 'lunarcore':
        types = 'git'
        file_path = 'server\\LunarCore'
        command = __handleUrlGenerate(types, cfg.DOWNLOAD_COMMANDS_LUNARCORE, cfg.DOWNLOAD_COMMANDS_LUNARCORE_MIRROR,
                                      '', '--branch development ')
    elif name == 'lunarcoreres':
        types = 'git'
        file_path = 'server\\LunarCore\\resources'
        command_1 = __handleUrlGenerate(types, cfg.DOWNLOAD_COMMANDS_LUNARCORE_RES_1,
                                        cfg.DOWNLOAD_COMMANDS_LUNARCORE_RES_MIRROR, '', '--branch lunarcoreres ')
        command_2 = __handleUrlGenerate(types, cfg.DOWNLOAD_COMMANDS_LUNARCORE_RES_2, '', '', '', True)
        command = command_1 + command_2
    elif name == 'fiddler':
        types = 'git'
        file_path = 'tool\\Fiddler'
        command = __handleUrlGenerate(types, cfg.DOWNLOAD_COMMANDS_FIDDLER, cfg.DOWNLOAD_COMMANDS_FIDDLER_MIRROR,
                                      '--branch fiddler ', '--branch fiddler ')
    return types, command, file_path
