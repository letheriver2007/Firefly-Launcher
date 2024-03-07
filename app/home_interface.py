import os
import random
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QButtonGroup
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QFont
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import TogglePushButton, PrimaryPushButton, setCustomStyleSheet, InfoBar, InfoBarPosition
from app.module.config import cfg


class RoundedImageWithText(QWidget):
    def __init__(self, image_path: str, parent=None):
        super().__init__(parent=parent)
        self.image_path = image_path

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pixmap = QPixmap(self.image_path)
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 20, 20)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, self.width(), self.height(), pixmap)

        painter.setPen(Qt.white)
        painter.setFont(QFont(cfg.APP_FONT, 35))
        painter.drawText(self.rect().adjusted(0, -20, 0, 0), Qt.AlignHCenter | Qt.AlignVCenter, cfg.APP_NAME)
        painter.setFont(QFont(cfg.APP_FONT, 20))
        painter.drawText(self.rect().adjusted(0, 90, 0, 0), Qt.AlignHCenter | Qt.AlignVCenter, cfg.APP_VERSION)


class Home(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text.replace(' ', '-'))
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        image_widget = RoundedImageWithText("./src/image/bg_home_" + str(random.randint(1, 3)) + ".png")
        image_widget.setFixedSize(1160, 350)
        image_layout = QVBoxLayout()
        image_layout.addWidget(image_widget)
        image_layout.setAlignment(Qt.AlignHCenter)
        layout.addLayout(image_layout)
        
        button_layout = QGridLayout()
        row, col = 0, 0
        for name in cfg.SERVER_NAMES:
            name_addspace = '   '+ name
            button_server = TogglePushButton(FIF.TAG, name_addspace, self)
            button_server.setObjectName(name)
            button_server.setFixedSize(270, 70)
            button_server.setIconSize(QSize(18, 18))
            button_server.setFont(QFont(f'{cfg.APP_FONT}', 12))
            setCustomStyleSheet(button_server, 'PushButton{border-radius: 12px}', 'PushButton{border-radius: 12px}')
            button_layout.addWidget(button_server, row, col)
            button_layout.setHorizontalSpacing(20)    # 水平间距
            col += 1
            if col == 3:
                col = 0
                row += 1
        button_layout.setVerticalSpacing(20)    # 垂直间距
        button_layout.setAlignment(Qt.AlignLeft)
        layout.addLayout(button_layout)

        self.button_launch = PrimaryPushButton(FIF.PLAY_SOLID, ' 一键启动')
        self.button_launch.setFixedSize(200, 65)
        self.button_launch.setIconSize(QSize(20, 20))
        self.button_launch.setFont(QFont(f'{cfg.APP_FONT}', 18))
        setCustomStyleSheet(self.button_launch, 'PushButton{border-radius: 12px}', 'PushButton{border-radius: 12px}')

        button_launch_layout = QHBoxLayout()
        button_launch_layout.setAlignment(Qt.AlignRight)
        button_launch_layout.addWidget(self.button_launch)
        button_launch_layout.setContentsMargins(0, 0, 25, 0)
        layout.addLayout(button_launch_layout)

        self.button_launch.installEventFilter(self)
        self.button_launch.clicked.connect(self.launch_exe)

        self.button_group = QButtonGroup()
        for button in cfg.SERVER_NAMES:
            obj_name = button
            button = self.findChild(TogglePushButton, obj_name)
            self.button_group.addButton(button)
        self.button_group.buttonClicked.connect(self.button_clicked)

    def button_clicked(self, button):
        self.clicked_button = button.objectName()

    def launch_exe(self):
        if os.path.exists(f'./server/{self.clicked_button}'):
            command = cfg.SERVER_COMMANDS.get(self.clicked_button, '')
            subprocess.run(command, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            InfoBar.success(
                title='服务端已启动！',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
        else:
            InfoBar.error(
                title=f'找不到服务端{self.clicked_button}，请重新下载！',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
