import os
import sys
import subprocess
from PySide6.QtGui import QIcon, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QApplication
from PySide6.QtCore import Qt, Signal, QTranslator
from qframelesswindow import FramelessWindow, StandardTitleBar
from qfluentwidgets import (Pivot, qrouter, ScrollArea, PrimaryPushSettingCard, Theme,
                            TitleLabel, BodyLabel, PrimaryPushButton, FluentIcon, setTheme,
                            ExpandGroupSettingCard, ComboBox, PrimaryToolButton, FluentTranslator)
from app.model.style_sheet import StyleSheet
from app.model.setting_card import SettingCard, SettingCardGroup
from app.model.config import open_file, Info, cfg
from devkit.convert import handleResConvert


class Main(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        setTheme(Theme.LIGHT)
        self.setTitleBar(StandardTitleBar(self))

        self.resize(1208, 688)
        self.setWindowTitle('FireFly Devkit (Lethe)')
        self.setWindowIcon(QIcon('./src/image/icon.ico'))

        self.DevkitInterface = Devkit("Devkit Interface", self)

        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 25, 0, 0)
        self.mainLayout.addWidget(self.DevkitInterface)
        self.setLayout(self.mainLayout)

        self.titleBar.raise_()


class ExpandGroupSettingCard_Convert(ExpandGroupSettingCard):
    convert_clear = Signal()
    convert_open = Signal()
    convert = Signal()

    def __init__(self, title, content, icon=FluentIcon.SYNC):
        super().__init__(icon, title, content)

        self.__initWidget()

    def __initWidget(self):
        self.label_convert = BodyLabel(self.tr('资源格式转换'))
        self.combobox_handbook = ComboBox()
        self.button_refresh = PrimaryToolButton(FluentIcon.ROTATE, self)
        self.button_convert = PrimaryPushButton(self.tr('转换'), self)

        self.label_open = BodyLabel(self.tr('打开输出文件夹'))
        self.button_open = PrimaryPushButton(self.tr('打开'), self)

        self.label_delete = BodyLabel(self.tr('删除输出文件'))
        self.button_delete = PrimaryPushButton(self.tr('删除'), self)

        self.__initInfo()
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initInfo(self):
        self.handleHandbookLoad()

    def __initLayout(self):
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.viewLayout.setSpacing(0)

        self.convert_widget = QWidget()
        self.convert_widget.setFixedHeight(60)
        self.convert_layout = QHBoxLayout(self.convert_widget)
        self.convert_layout.setContentsMargins(48, 12, 48, 12)
        self.convert_layout.addWidget(self.label_convert)
        self.convert_layout.addStretch(1)
        self.convert_layout.addWidget(self.combobox_handbook)
        self.convert_layout.addWidget(self.button_refresh)
        self.convert_layout.addSpacing(10)
        self.convert_layout.addWidget(self.button_convert)

        self.open_widget = QWidget()
        self.open_widget.setFixedHeight(60)
        self.open_layout = QHBoxLayout(self.open_widget)
        self.open_layout.setContentsMargins(48, 12, 48, 12)
        self.open_layout.addWidget(self.label_open)
        self.open_layout.addStretch(1)
        self.open_layout.addWidget(self.button_open)

        self.delete_widget = QWidget()
        self.delete_widget.setFixedHeight(60)
        self.delete_layout = QHBoxLayout(self.delete_widget)
        self.delete_layout.setContentsMargins(48, 12, 48, 12)
        self.delete_layout.addWidget(self.label_delete)
        self.delete_layout.addStretch(1)
        self.delete_layout.addWidget(self.button_delete)

        self.addGroupWidget(self.convert_widget)
        self.addGroupWidget(self.open_widget)
        self.addGroupWidget(self.delete_widget)

    def __connectSignalToSlot(self):
        self.button_refresh.clicked.connect(self.__initInfo)

        self.button_convert.clicked.connect(self.convert)
        self.button_open.clicked.connect(self.convert_open)
        self.button_delete.clicked.connect(self.convert_clear)

    def handleHandbookLoad(self):
        self.combobox_handbook.clear()
        filenames_no_ext = [os.path.splitext(filename)[0] for filename in os.listdir('.\\devkit\\handbook')]
        self.combobox_handbook.addItems(filenames_no_ext)


class ExpandGroupSettingCard_Translate(ExpandGroupSettingCard):
    translate_dump = Signal()
    translate_open = Signal()
    translate_publish = Signal()

    def __init__(self, title, content, icon=FluentIcon.SYNC):
        super().__init__(icon, title, content)

        self.__initWidget()

    def __initWidget(self):
        self.label_dump = BodyLabel(self.tr('导出源文本'))
        self.button_dump = PrimaryPushButton(self.tr('导出'), self)

        self.label_translate = BodyLabel(self.tr('打开输出文件夹'))
        self.button_translate = PrimaryPushButton(self.tr('打开'), self)

        self.combobox_publish = ComboBox()
        self.button_refresh = PrimaryToolButton(FluentIcon.ROTATE, self)
        self.label_publish = BodyLabel(self.tr('发布翻译文件'))
        self.button_publish = PrimaryPushButton(self.tr('发布'), self)

        self.__initInfo()
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initInfo(self):
        self.handlePublishLoad()

    def __initLayout(self):
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.viewLayout.setSpacing(0)

        self.dump_widget = QWidget()
        self.dump_widget.setFixedHeight(60)
        self.dump_layout = QHBoxLayout(self.dump_widget)
        self.dump_layout.setContentsMargins(48, 12, 48, 12)
        self.dump_layout.addWidget(self.label_dump)
        self.dump_layout.addStretch(1)
        self.dump_layout.addWidget(self.button_dump)

        self.translate_widget = QWidget()
        self.translate_widget.setFixedHeight(60)
        self.translate_layout = QHBoxLayout(self.translate_widget)
        self.translate_layout.setContentsMargins(48, 12, 48, 12)
        self.translate_layout.addWidget(self.label_translate)
        self.translate_layout.addStretch(1)
        self.translate_layout.addWidget(self.button_translate)

        self.publish_widget = QWidget()
        self.publish_widget.setFixedHeight(60)
        self.publish_layout = QHBoxLayout(self.publish_widget)
        self.publish_layout.setContentsMargins(48, 12, 48, 12)
        self.publish_layout.addWidget(self.label_publish)
        self.publish_layout.addStretch(1)
        self.publish_layout.addWidget(self.combobox_publish)
        self.publish_layout.addWidget(self.button_refresh)
        self.publish_layout.addSpacing(10)
        self.publish_layout.addWidget(self.button_publish)

        self.addGroupWidget(self.dump_widget)
        self.addGroupWidget(self.translate_widget)
        self.addGroupWidget(self.publish_widget)

    def __connectSignalToSlot(self):
        self.button_refresh.clicked.connect(self.__initInfo)

        self.button_dump.clicked.connect(self.translate_dump)
        self.button_translate.clicked.connect(self.translate_open)
        self.button_publish.clicked.connect(self.translate_publish)

    def handlePublishLoad(self):
        self.combobox_publish.clear()
        ts_filenames = [filename for filename in os.listdir('.\\devkit\\translate\\') if filename.endswith('.ts')]
        filenames_no_ext = [os.path.splitext(filename)[0] for filename in ts_filenames]
        self.combobox_publish.addItems(filenames_no_ext)


class Devkit(ScrollArea):
    Nav = Pivot

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setObjectName(text)
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)

        self.pivot = self.Nav(self)
        self.stackedWidget = QStackedWidget(self)

        self.ResourceInterface = SettingCardGroup(self.scrollWidget)
        self.HandbookCard = PrimaryPushSettingCard(
            self.tr('打开'),
            FluentIcon.LABEL,
            self.tr('LC Handbook修改'),
            self.tr('根据格式修改Handbook资源')
        )
        self.ConvertCard = ExpandGroupSettingCard_Convert(
            self.tr('资源格式转换'),
            self.tr('将LC Handbook转换为Firefly-Launcher格式'),
        )
        self.TranslateInterface = SettingCardGroup(self.scrollWidget)
        self.dumpCodeTextCard = PrimaryPushSettingCard(
            self.tr('获取'),
            FluentIcon.CLOUD_DOWNLOAD,
            self.tr('获取源文本'),
            self.tr('获取代码中未翻译的文本')
        )
        self.translateCard = ExpandGroupSettingCard_Translate(
            self.tr('翻译工作'),
            self.tr('建议使用QT Linguist工具进行翻译')
        )

        self.__initWidget()

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(20, 0, 20, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        self.scrollWidget.setObjectName('scrollWidget')
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.ResourceInterface.addSettingCard(self.HandbookCard)
        self.ResourceInterface.addSettingCard(self.ConvertCard)
        self.TranslateInterface.addSettingCard(self.translateCard)

        self.addSubInterface(self.ResourceInterface, 'ResourceInterface', self.tr('资源'), icon=FluentIcon.PIE_SINGLE)
        self.addSubInterface(self.TranslateInterface, 'TranslateInterface', self.tr('翻译'), icon=FluentIcon.LANGUAGE)

        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setSpacing(15)
        self.vBoxLayout.setContentsMargins(0, 10, 10, 0)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.ResourceInterface)
        self.pivot.setCurrentItem(self.ResourceInterface.objectName())
        qrouter.setDefaultRouteKey(self.stackedWidget, self.ResourceInterface.objectName())

    def __connectSignalToSlot(self):
        self.HandbookCard.clicked.connect(lambda: open_file(self, '.\\devkit\\handbook\\'))

        self.ConvertCard.convert_clear.connect(lambda: self.handleConvert('clear'))
        self.ConvertCard.convert_open.connect(lambda: open_file(self, '.\\devkit\\output\\'))
        self.ConvertCard.convert.connect(lambda: self.handleConvert('convert'))

        self.translateCard.translate_dump.connect(lambda: self.handleTranslate('dump'))
        self.translateCard.translate_open.connect(lambda: open_file(self, '.\\devkit\\translate\\'))
        self.translateCard.translate_publish.connect(lambda: self.handleTranslate('publish'))

    def addSubInterface(self, widget: QLabel, objectName, text, icon=None):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            icon=icon,
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())
        qrouter.push(self.stackedWidget, widget.objectName())

    def handleConvert(self, mode):
        if mode == 'convert':
            FILENAME = self.ConvertCard.combobox_handbook.currentText()
            handleResConvert(FILENAME)
            Info(self, 'S', 1000, self.tr('转换成功!'))

        elif mode == 'clear':
            if os.path.exists('.\\devkit\\output'):
                os.system('del /s /q .\\devkit\\output && rmdir /s /q .\\devkit\\output')
            Info(self, 'S', 1000, self.tr('清空成功!'))

    def handleTranslate(self, mode):
        if mode == 'dump':
            command = (
                'start cmd /c "'
                '.\\devkit\\linguist\\lupdate.exe '
                '.\\firefly-devkit.py '
                '.\\app\\environment_interface.py '
                '.\\app\\home_interface.py '
                '.\\app\\launcher_interface.py '
                '.\\app\\lunarcore_command.py '
                '.\\app\\lunarcore_edit.py '
                '.\\app\\lunarcore_interface.py '
                '.\\app\\main_interface.py '
                '.\\app\\proxy_interface.py '
                '.\\app\\setting_interface.py '
                '.\\app\\model\\check_update.py '
                '.\\app\\model\\setting_card.py '
                '.\\app\\model\\login_card.py '
                '.\\app\\model\\download_process.py '
                '-ts .\\devkit\\translate\\en_US.ts && '
                'pause"'
            )
            subprocess.run(command, shell=True)

            Info(self, 'S', 1000, self.tr('获取成功!'))

        elif mode == 'publish':
            current_file = self.translateCard.combobox_publish.currentText()
            command = (
                'start cmd /c "'
                '.\\devkit\\linguist\\lrelease.exe '
                f'.\\devkit\\translate\\{current_file}.ts && '
                'pause"'
            )
            subprocess.run(command, shell=True)

            Info(self, 'S', 1000, self.tr('发布成功!'))


if __name__ == '__main__':
    if cfg.get(cfg.dpiScale) != "Auto":
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    locale = cfg.get(cfg.language).value
    translator = FluentTranslator(locale)
    localTranslator = QTranslator()
    localTranslator.load(f"src\\translate\\{locale.name()}.qm")

    app.installTranslator(translator)
    app.installTranslator(localTranslator)

    window = Main()
    window.show()
    sys.exit(app.exec())
