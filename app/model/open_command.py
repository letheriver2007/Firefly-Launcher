import json
import ssl
import urllib.request

def ping():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    url = 'https://127.0.0.1:443/opencommand/api'
    request_data = {
        'action': 'ping',
        }
    request_data_json = json.dumps(request_data).encode('utf-8')
    
    req = urllib.request.Request(url, data=request_data_json, method='POST')

    try:
        with urllib.request.urlopen(req, context=context) as response:
            response_data = response.read()
            response_json = json.loads(response_data)
            if response_json['retcode'] == 200:
                message = response_json['message']
                return 'success', message
            else:
                message = response_json['message']
                return 'error', message
    except urllib.error.URLError as e:
        return 'error', e

def send_code(uid):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    url = 'https://127.0.0.1:443/opencommand/api'
    request_data = {
        'action': 'sendCode',
        'data': uid,
        }
           
    request_data_json = json.dumps(request_data).encode('utf-8')
    
    req = urllib.request.Request(url, data=request_data_json, method='POST')

    try:
        with urllib.request.urlopen(req, context=context) as response:
            response_data = response.read()
            response_json = json.loads(response_data)
            if response_json['retcode'] == 200:
                token = response_json['token']
                return 'success', token
            else:
                message = response_json['message']
                return 'error', message
    except urllib.error.URLError as e:
        return 'error', e

def verify_token(temp_token, code):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    url = 'https://127.0.0.1:443/opencommand/api'
    request_data = {
        'action': 'verify',
        'token': temp_token,
        'data': code,
        }
    request_data_json = json.dumps(request_data).encode('utf-8')
    
    req = urllib.request.Request(url, data=request_data_json, method='POST')

    try:
        with urllib.request.urlopen(req, context=context) as response:
            response_data = response.read()
            response_json = json.loads(response_data)
            if response_json['retcode'] == 200:
                return 'success'
            else:
                message = response_json['message']
                return 'error', message
    except urllib.error.URLError as e:
        return 'error', e

def send_command(token, command):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    url = 'https://127.0.0.1:443/opencommand/api'
    request_data = {
        'action': 'command',
        'token': token,
        'data': command,
    }
    request_data_json = json.dumps(request_data).encode('utf-8')
    
    req = urllib.request.Request(url, data=request_data_json, method='POST')

    try:
        with urllib.request.urlopen(req, context=context) as response:
            response_data = response.read()
            response_json = json.loads(response_data)
            if response_json['retcode'] == 200:
                data = response_json['data']
                return 'success', data
            else:
                message = response_json['message']
                return 'error', message
    except urllib.error.URLError as e:
        return 'error', e