import json
import urllib.request
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import LineEdit, PasswordLineEdit, PrimaryPushButton, FluentIcon
from app.model.config import get_json
from app.model.setting_card import SettingCard


def handleApply(uid):
    base_url = 'https://' + get_json('./config/config.json', 'SERVER_URL') + get_json('./config/config.json',
                                                                                      'ROUTE_APPLY')
    params = {
        'uid': uid
    }
    url = base_url + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method='GET')

    try:
        with urllib.request.urlopen(req) as response:
            response_data = response.read()
            response_json = json.loads(response_data)
            if response_json['retcode'] == 200:
                return 'success', response_json['message']
            else:
                return 'error', response_json['message']

    except urllib.error.HTTPError as http_err:
        print(f'网络请求失败, {http_err}')
        return 'error', http_err

    except urllib.error.URLError as req_err:
        print(f'请求格式错误, {req_err}')
        return 'error', req_err

    except Exception as err:
        print(f'未知错误, {err}')
        return 'error', err


def handleVerify(uid, code, key):
    base_url = 'https://' + get_json('./config/config.json', 'SERVER_URL') + get_json('./config/config.json',
                                                                                      'ROUTE_VERIFY')
    params = {
        'uid': uid,
        'code': code,
        'password': key
    }
    url = base_url + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method='GET')

    try:
        with urllib.request.urlopen(req) as response:
            response_data = response.read()
            response_json = json.loads(response_data)
            if response_json['retcode'] == 200:
                return 'success', response_json['message']
            else:
                return 'error', response_json['message']

    except urllib.error.HTTPError as http_err:
        print(f'网络请求失败, {http_err}')
        return 'error', http_err

    except urllib.error.URLError as req_err:
        print(f'请求格式错误, {req_err}')
        return 'error', req_err

    except Exception as err:
        print(f'未知错误, {err}')
        return 'error', err


def handleCommandSend(uid, key, command):
    base_url = 'https://' + get_json('./config/config.json', 'SERVER_URL') + get_json('./config/config.json',
                                                                                      'ROUTE_REMOTE')
    params = {
        'uid': uid,
        'key': key,
        'command': command
    }
    url = base_url + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method='GET')

    try:
        with urllib.request.urlopen(req) as response:
            response_data = response.read()
            response_json = json.loads(response_data)
            if response_json['retcode'] == 200:
                return 'success', response_json['message']
            else:
                return 'error', response_json['message']

    except urllib.error.HTTPError as http_err:
        print(f'网络请求失败, {http_err}')
        return 'error', http_err

    except urllib.error.URLError as req_err:
        print(f'请求格式错误, {req_err}')
        return 'error', req_err

    except Exception as err:
        print(f'未知错误, {err}')
        return 'error', err


class PrimaryPushSettingCard_URL(SettingCard):
    clicked_seturl = Signal()

    def __init__(self, title, content, icon=FluentIcon.WIFI):
        super().__init__(icon, title, content)
        self.lineedit_seturl = LineEdit(self)
        self.lineedit_seturl.setPlaceholderText(self.tr("服务端地址"))
        self.lineedit_seturl.setFixedWidth(150)
        self.button_seturl = PrimaryPushButton(self.tr('设置'), self)
        self.hBoxLayout.addWidget(self.lineedit_seturl, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_seturl, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_seturl.clicked.connect(self.clicked_seturl)


class PrimaryPushSettingCard_API(SettingCard):
    clicked_setapi = Signal()

    def __init__(self, title, content, icon=FluentIcon.LABEL):
        super().__init__(icon, title, content)
        self.button_seturl = PrimaryPushButton(self.tr('打开文件'), self)
        self.hBoxLayout.addWidget(self.button_seturl, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_seturl.clicked.connect(self.clicked_setapi)


class PrimaryPushSettingCard_UID(SettingCard):
    clicked_setuid = Signal()

    def __init__(self, title, content, icon=FluentIcon.QUICK_NOTE):
        super().__init__(icon, title, content)
        self.lineedit_setuid = LineEdit(self)
        self.lineedit_setuid.setPlaceholderText("UID")
        self.lineedit_setuid.setFixedWidth(150)
        self.lineedit_setuid.setValidator(QIntValidator(self))
        self.button_setuid = PrimaryPushButton(self.tr('设置'), self)
        self.hBoxLayout.addWidget(self.lineedit_setuid, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_setuid, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_setuid.clicked.connect(self.clicked_setuid)


class PrimaryPushSettingCard_Verify(SettingCard):
    clicked_apply = Signal()
    clicked_verify = Signal()

    def __init__(self, title, content, icon=FluentIcon.FINGERPRINT):
        super().__init__(icon, title, content)
        self.button_apply = PrimaryPushButton(self.tr('发送'), self)
        self.lineedit_code = LineEdit(self)
        self.lineedit_code.setPlaceholderText(self.tr("验证码"))
        self.lineedit_code.setFixedWidth(100)
        self.lineedit_code.setValidator(QIntValidator(self))
        self.lineedit_key = PasswordLineEdit(self)
        self.lineedit_key.setPlaceholderText(self.tr("密码"))
        self.lineedit_key.setFixedWidth(150)
        self.button_verify = PrimaryPushButton(self.tr('设置'), self)
        self.hBoxLayout.addWidget(self.lineedit_code, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_apply, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.hBoxLayout.addWidget(self.lineedit_key, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_verify, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_apply.clicked.connect(self.clicked_apply)
        self.button_verify.clicked.connect(self.clicked_verify)
