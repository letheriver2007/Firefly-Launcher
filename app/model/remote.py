import json
import urllib.request
from app.model.config import get_json

def handleApply(uid):
    base_url = 'http://' + get_json('./config/config.json', 'SERVER_URL') + get_json('./config/config.json', 'ROUTE_APPLY')
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
    base_url = 'http://' + get_json('./config/config.json', 'SERVER_URL') + get_json('./config/config.json', 'ROUTE_VERIFY')
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
    base_url = 'http://' + get_json('./config/config.json', 'SERVER_URL') + get_json('./config/config.json', 'ROUTE_REMOTE')
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