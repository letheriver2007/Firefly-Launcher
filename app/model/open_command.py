import json
import ssl
import urllib.request

def ping(uid):
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
                return True
            else:
                print("获取token失败:", response_json['message'])
                return None
    except urllib.error.URLError as e:
        print("与服务器通信时出现错误:", e)
        return None

def send_code(uid):
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
                return response_json['token']
            else:
                print("获取token失败:", response_json['message'])
                return None
    except urllib.error.URLError as e:
        print("与服务器通信时出现错误:", e)
        return None

def verify_token(temp_token, code):
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
                return True
            else:
                print("验证token失败:", response_json['message'])
                return None
    except urllib.error.URLError as e:
        print("与服务器通信时出现错误:", e)
        return None

def send_command(command):
    request_data = {
        'action': 'command',
        'token': token,
        'data': {
            'command': command,
        }
    }
    request_data_json = json.dumps(request_data).encode('utf-8')
    
    req = urllib.request.Request(url, data=request_data_json, method='POST')

    try:
        with urllib.request.urlopen(req, context=context) as response:
            response_data = response.read()
            response_json = json.loads(response_data)
            if response_json['retcode'] == 200:
                return response_json['data']
    except urllib.error.URLError as e:
        print("与服务器通信时出现错误:", e)


context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
url = 'https://127.0.0.1:443/opencommand/api'

ping_status = ping()
if ping_status == None:
    print("无法连接到服务器")
    return

uid = input("请输入UID:")
token = send_code(uid)
if token == None:
    print("获取临时token失败")
    return

code = input("请输入游戏内验证码:")
verify = verify_token(code)
if verify == None:
    print("验证code失败")
    return
print(f"验证成功,token为:{token}")

command = input("请输入指令:")
command_return = send_command(command)
print(f"指令执行结果:{command_return}")
# 我反正加好了，等LC和插件修咯~~~