import os
import random
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QButtonGroup, QStyleOptionViewItem
from PySide6.QtCore import Qt, QSize, QModelIndex, QRect, QTimer
from PySide6.QtGui import QPainter, QFont
from qfluentwidgets import (TogglePushButton, PrimaryPushButton, setCustomStyleSheet, InfoBarPosition,
                            InfoBarIcon, InfoBar, FlowLayout,HorizontalFlipView, FlipImageDelegate, FluentIcon)
from app.model.config import cfg, Info


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
        self.parent = parent

        self.__initWidgets()

    def __initWidgets(self):
        self.flipView = HorizontalFlipView()
        self.flipView.addImages(["./src/image/bg_home_1.png", "./src/image/bg_home_2.png", "./src/image/bg_home_3.png"])
        self.flipView.setItemSize(QSize(1160, 350))
        self.flipView.setFixedSize(QSize(1160, 350))
        self.flipView.setCurrentIndex(random.randint(0, 2))
        self.flipView.setItemDelegate(CustomFlipItemDelegate(self.flipView))

        self.button_group = QButtonGroup()
        for name, details in cfg.SERVER.items():
            icon = FluentIcon.TAG
            if 'ICON' in details and details['ICON']:
                icon = getattr(FluentIcon, details['ICON'], FluentIcon.TAG)

            button_server = TogglePushButton(icon, '   ' + name, self)
            button_server.setObjectName(name)
            button_server.setFixedSize(270, 70)
            button_server.setIconSize(QSize(18, 18))
            button_server.setFont(QFont(f'{cfg.APP_FONT}', 12))
            setCustomStyleSheet(button_server, 'PushButton{border-radius: 12px}', 'PushButton{border-radius: 12px}')

            self.button_group.addButton(button_server)

        self.button_launch = PrimaryPushButton(FluentIcon.PLAY_SOLID, self.tr(' 一键启动'))
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

        self.play_layout = QHBoxLayout()
        self.play_layout.addSpacing(15)
        self.play_layout.addLayout(self.button_layout)
        self.play_layout.addSpacing(300)

        self.button_launch_layout = QHBoxLayout()
        self.button_launch_layout.setAlignment(Qt.AlignRight)
        self.button_launch_layout.addWidget(self.button_launch)
        self.button_launch_layout.setContentsMargins(0, 0, 25, 0)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 30, 10, 10)
        self.main_layout.addLayout(self.image_layout)
        self.main_layout.addSpacing(25)
        self.main_layout.addLayout(self.play_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.button_launch_layout)
        self.main_layout.addSpacing(25)

    def __connectSignalToSlot(self):
        self.scrollTimer = QTimer(self)
        self.scrollTimer.timeout.connect(lambda: self.flipView.setCurrentIndex(random.randint(0, 2)))
        self.scrollTimer.start(5000)
        self.button_launch.clicked.connect(self.handleServerLaunch)

    def handleServerLaunch(self):
        server = self.button_group.checkedButton()
        if server:
            name = server.objectName()
            if os.path.exists(f'./server/{name}'):
                command = cfg.SERVER[name]['COMMAND']
                subprocess.run(command, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                Info(self, 'S', 1000, self.tr('服务端已启动!'))
            else:
                server_error = InfoBar(
                    icon=InfoBarIcon.ERROR,
                    title=self.tr('找不到服务端') + name + '!',
                    content='',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )

                server_page = {'LunarCore': 3}
                if name in server_page:
                    page_index = server_page[name]
                    server_error_button = PrimaryPushButton(self.tr('前往下载'))
                    server_error_button.clicked.connect(lambda: self.parent.stackedWidget.setCurrentIndex(page_index))
                    server_error.addWidget(server_error_button)
                    server_error.show()
                else:
                    server_error.show()
