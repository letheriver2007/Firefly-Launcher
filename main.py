import os
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QLocale
from qfluentwidgets import FluentTranslator
from app.main_interface import Main
from src.module.config import cfg

app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
translator = FluentTranslator(QLocale(QLocale.Chinese, QLocale.China))
app.installTranslator(translator)   # 似乎必须分如上两行

window = Main()
window.show()
sys.exit(app.exec())