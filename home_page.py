from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QButtonGroup, QPushButton
from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QIcon, QColor
from qfluentwidgets import TogglePushButton, PrimaryPushButton, Theme
from qfluentwidgets import FluentIcon as FIF
from config import cfg
import os

button_names = ["Grasscutter", "NahidaImpact", "Lunarcore", "Hutao-GS"]

class RoundedImageWidget(QWidget):
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


class Home(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)

        self.setObjectName(text.replace(' ', '-'))
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        image_layout = QVBoxLayout()
        image_widget = RoundedImageWidget("./src/image/bg_home.png")
        image_layout.addWidget(image_widget)
        image_widget.setFixedSize(1160, 350)
        image_layout.setAlignment(Qt.AlignHCenter)
        layout.addLayout(image_layout)
        

        button_layout = QGridLayout()

        row, col = 0, 0
        for name in button_names:
            name_addspace = '   '+ name
            button = TogglePushButton(FIF.TAG, name_addspace, self)
            button.setObjectName(name)
            button.setFixedSize(270, 70)
            button_layout.addWidget(button, row, col)
            button_layout.setHorizontalSpacing(20)    # 水平间距
            col += 1
            if col == 3:
                col = 0
                row += 1

        button_layout.setVerticalSpacing(20)    # 垂直间距
        button_layout.setAlignment(QtCore.Qt.AlignLeft)
        layout.addLayout(button_layout)

        # 按钮
        button_launch = QPushButton(QIcon("src/image/play_light.png"), '   一键启动')
        button_launch.setIconSize(QtCore.QSize(30, 30))
        button_launch.setFixedSize(230, 70)
        button_launch.setStyleSheet("background-color: #ffc0cb; color: white; font-size: 24px; border-radius: 15px;")
        
        # 按钮布局
        button_launch_layout = QHBoxLayout()
        button_launch_layout.setAlignment(Qt.AlignRight)
        button_launch_layout.addWidget(button_launch)
        button_launch_layout.setContentsMargins(0, 0, 25, 0)

        # 加入主布局
        layout.addLayout(button_launch_layout)

        button_launch.clicked.connect(self.launch_exe)

        self.button_group = QButtonGroup()
        for button in button_names:
            obj_name = button
            button = self.findChild(TogglePushButton, obj_name)
            self.button_group.addButton(button)
        self.button_group.buttonClicked.connect(self.handle_button_clicked)
        self.launch_button_num = 0

    def handle_button_clicked(self, button):
        for index, name in enumerate(button_names, start=1):
            if button.objectName() == name:
                self.launch_button_num = index

    def launch_exe(self):
        if self.launch_button_num in range(1, 7):
            if self.launch_button_num == 1:
                os.system('cd ./server/Grasscutter/ && start java.exe -jar grasscutter.jar')
            elif self.launch_button_num == 2:
                os.system('start ./server/NahidaImpact/NahidaImpact.Proxy/bin/Release/net8.0/NahidaImpact.Proxy.exe')
                os.system('start ./server/NahidaImpact/NahidaImpact.SDK/bin/Release/net8.0/NahidaImpact.SDK.exe')
                os.system('cd ./server/NahidaImpact/NahidaImpact.GameServer/bin/Release/net8.0/ && start NahidaImpact.GameServer.exe')
            elif self.launch_button_num == 3:
                os.system('cd ./server/LunarCore/ && start java.exe -jar LunarCore.jar')
            elif self.launch_button_num == 4:
                os.system('cd ./server/HuTao-GS-dev-435/ && start START-DEV.bat')
        else:
            print("请先选择要打开的服务端！")
