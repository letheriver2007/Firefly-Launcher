import sys
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QLocale
from PySide6.QtWidgets import QApplication, QVBoxLayout
from qfluentwidgets import FluentTranslator, ScrollArea, setTheme, Theme
from app.component.style_sheet import StyleSheet
from app.command_interface import Command
from app.module.config import cfg


class Main_Command(ScrollArea):
    def __init__(self):
        super().__init__()
        self.initMainWindow()
        self.commandInterface = Command('Command Interface', self)
        setTheme(Theme.LIGHT)

        layout = QVBoxLayout()
        layout.addWidget(self.commandInterface)
        self.setLayout(layout)
    
    def initMainWindow(self):
        self.setWindowTitle(cfg.APP_NAME)
        self.setFixedSize(1230, 702)
        self.setWindowIcon(QIcon('./src/image/icon.ico'))

        # 居中显示
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
translator = FluentTranslator(QLocale(QLocale.Chinese, QLocale.China))
app.installTranslator(translator)

window = Main_Command()
window.show()
sys.exit(app.exec())