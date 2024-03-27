import os
import random
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QButtonGroup, QStyleOptionViewItem
from PySide6.QtCore import Qt, QSize, QModelIndex, QRect, QTimer
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QFont, QColor
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (TogglePushButton, PrimaryPushButton, setCustomStyleSheet, FlowLayout,
                            InfoBar, InfoBarPosition, HorizontalFlipView, FlipImageDelegate)
from app.model.config import cfg


class CustomFlipItemDelegate(FlipImageDelegate):
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        super().paint(painter, option, index)
        self.setBorderRadius(35)
        painter.save()

        rect = option.rect
        rect = QRect(rect.x(), rect.y(), rect.width(), rect.height())
        painter.setPen(Qt.white)
        painter.setFont(QFont(cfg.APP_FONT, 35))
        painter.drawText(rect.adjusted(0, -20, 0, 0), Qt.AlignCenter, cfg.APP_NAME)
        painter.setFont(QFont(cfg.APP_FONT, 20))
        painter.drawText(rect.adjusted(0, 90, 0, 0), Qt.AlignCenter, cfg.APP_VERSION)

        painter.restore()


class Home(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)

        self.__initWidgets()

    def __initWidgets(self):
        self.flipView = HorizontalFlipView()
        self.flipView.addImages(["./src/image/bg_home_1.png", "./src/image/bg_home_2.png", "./src/image/bg_home_3.png"])
        self.flipView.setItemSize(QSize(1160, 350))
        self.flipView.setFixedSize(QSize(1160, 350))
        self.flipView.setCurrentIndex(random.randint(0, 2))
        self.flipView.setItemDelegate(CustomFlipItemDelegate(self.flipView))


        self.button_group = QButtonGroup()
        for name in cfg.SERVER_NAMES:
            name_addspace = '   '+ name
            button_server = TogglePushButton(FIF.TAG, name_addspace, self)
            button_server.setObjectName(name)
            button_server.setFixedSize(270, 70)
            button_server.setIconSize(QSize(18, 18))
            button_server.setFont(QFont(f'{cfg.APP_FONT}', 12))
            setCustomStyleSheet(button_server, 'PushButton{border-radius: 12px}', 'PushButton{border-radius: 12px}')
            self.button_group.addButton(button_server)

        self.button_launch = PrimaryPushButton(FIF.PLAY_SOLID, ' 一键启动')
        self.button_launch.setFixedSize(200, 65)
        self.button_launch.setIconSize(QSize(20, 20))
        self.button_launch.setFont(QFont(f'{cfg.APP_FONT}', 18))
        setCustomStyleSheet(self.button_launch, 'PushButton{border-radius: 12px}', 'PushButton{border-radius: 12px}')


        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.image_layout = QVBoxLayout()
        self.image_layout.addWidget(self.flipView)
        self.image_layout.setAlignment(Qt.AlignHCenter)
        
        self.button_layout = FlowLayout()
        self.button_layout.setVerticalSpacing(30)
        self.button_layout.setHorizontalSpacing(30)
        for button in self.button_group.buttons():
            self.button_layout.addWidget(button)

        self.button_h_layout = QHBoxLayout()
        self.button_h_layout.addSpacing(15)
        self.button_h_layout.addLayout(self.button_layout)
        self.button_h_layout.addSpacing(300)

        self.button_launch_layout = QHBoxLayout()
        self.button_launch_layout.setAlignment(Qt.AlignRight)
        self.button_launch_layout.addWidget(self.button_launch)
        self.button_launch_layout.setContentsMargins(0, 0, 25, 0)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 30, 10, 10)
        layout.addLayout(self.image_layout)
        layout.addSpacing(25)
        layout.addLayout(self.button_h_layout)
        layout.addSpacing(30)
        layout.addLayout(self.button_launch_layout)
        layout.addStretch(1)

    def __connectSignalToSlot(self):
        self.scrollTimer = QTimer(self)
        self.scrollTimer.timeout.connect(lambda: self.flipView.setCurrentIndex(random.randint(0, 2)))
        self.scrollTimer.start(5000)
        self.button_launch.clicked.connect(self.handleServerLaunch)

    def handleServerLaunch(self):
        if self.button_group.checkedButton():
            name = self.button_group.checkedButton().objectName()
            if os.path.exists(f'./server/{name}'):
                command = cfg.SERVER_COMMANDS.get(name, '')
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
                    title=f'找不到服务端{name}，请重新下载！',
                    content='',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
