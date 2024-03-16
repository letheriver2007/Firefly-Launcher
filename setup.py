import os
import sys
import json
import shutil
import zipfile
import subprocess
import urllib.request

if not os.path.exists('main.py'):
    print('正在配置环境...')

    yes = ['yes','Yes','YES','y','Y']
    no = ['no','No','NO','n','N']
    china = input('是否使用国内镜像?(' + "\033[32m" + 'y' + "\033[0m" + '/n)')
    if china in yes or china == '':
        chinaStatus = True
        proxyStatus = False
    else:
        chinaStatus = False
        proxy = input('是否使用代理端口?(' + "\033[32m" + 'y' + "\033[0m" + '/n)')
        if proxy in yes or proxy == '':
            proxyStatus = True
        else:
            proxyStatus = False

    print('配置完成!')


    print('开始检测更新...')

    try:
        with open('config/setup.json', 'r') as file:
            ver = json.load(file)
            APP_VERSION = ver['APP_VERSION']
        with open('config/server.json', 'r') as file:
            port = json.load(file)
            PROXY_PORT = port['PROXY_PORT']
    except:
        print('配置文件损坏,使用默认版本:v1.0.0')
        APP_VERSION = 'v1.0.0'
        if proxyStatus:
            PROXY_PORT = input('配置文件损坏,请输入代理端口:')
    print(f'当前版本：{APP_VERSION}')

    if chinaStatus:
        url = 'https://api.github.com/repos/letheriver2007/Firefly-Launcher/releases/latest'
        proxy_support = urllib.request.ProxyHandler()
    elif proxyStatus:
        url = 'https://api.github.com/repos/letheriver2007/Firefly-Launcher/releases/latest'
        proxy_support = urllib.request.ProxyHandler({'http': f'http://127.0.0.1:{PROXY_PORT}', 'https': f'https://127.0.0.1:{PROXY_PORT}'})
        print(f'已使用代理端口:{PROXY_PORT}')
    else:
        url = 'https://api.github.com/repos/letheriver2007/Firefly-Launcher/releases/latest'
        proxy_support = urllib.request.ProxyHandler()
    opener = urllib.request.build_opener(proxy_support)
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    skipnum = 0
    while True:
        try:
            with urllib.request.urlopen(url) as response:
                if response.getcode() == 200:
                    data = response.read()
                    release_info = json.loads(data)
                    latest_tag = release_info['tag_name']
                    break
                else:
                    latest_tag = None
        except Exception as e:
            latest_tag = None
            skipnum += 1
            again = input(f'检测更新失败({skipnum}次):{e}, 是否重试? (' + "\033[32m" + 'y' + "\033[0m" + '/n)')
            if again in no:
                input("请按 Enter 键关闭窗口...")
                sys.exit()
            if skipnum > 3 and input('失败次数过多,是否跳过? (y/' + "\033[32m" + 'n' + "\033[0m" + ')') in yes:
                latest_tag = 'v' + input('请手动输入最新版本号(X.X.X):')
                break

    print(f'最新版本：{latest_tag}')

    if latest_tag and latest_tag >= APP_VERSION:
        update = input(f'检测到新版本：{latest_tag}, 是否更新? (' + "\033[32m" + 'y' + "\033[0m" + '/n)')
        if update in yes or update == '':
            if chinaStatus == True:
                command = f'curl -o Firefly-Launcher.zip -L https://gitee.com/letheriver2007/Firefly-Launcher/releases/download/{latest_tag}/Firefly-Launcher.zip'
            else:
                if proxyStatus == True:
                    command = f'curl -x http://127.0.0.1:{PROXY_PORT} -o Firefly-Launcher.zip -L https://github.com/letheriver2007/Firefly-Launcher/releases/download/{latest_tag}/Firefly-Launcher.zip'
                else:
                    command = f'curl -o Firefly-Launcher.zip -L https://github.com/letheriver2007/Firefly-Launcher/releases/download/{latest_tag}/Firefly-Launcher.zip'
            
            while True:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
                for line in process.stdout:
                    print(line.rstrip('\n'))
                process.communicate()
                if process.returncode == 0:
                    break
                else:
                    again = input(f'下载失败, 是否重试? (' + "\033[32m" + 'y' + "\033[0m" + '/n)')
                    if again in no:
                        input("请按 Enter 键关闭窗口...")
                        sys.exit()

            print("下载完成!")


            print("正在删除旧版本...")

            current_dir = os.getcwd()
            for root, dirs, files in os.walk(current_dir, topdown=False):
                for name in files:
                    file_path = os.path.join(root, name)
                    if name not in ['auto.json', 'server.json', 'Setup.exe', 'Firefly-Launcher.zip']:
                        os.remove(file_path)
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    if name not in ['Firefly-Launcher', 'config']:
                        shutil.rmtree(dir_path)
            
            print("删除旧版本完成!")


            print("正在解压新版本...")

            zip_file_path = os.path.join(current_dir, 'Firefly-Launcher.zip')
            extract_folder = current_dir
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                for file in file_list:
                    target_file = os.path.join(extract_folder, file)
                    if os.path.exists(target_file):
                        print(f"{file}已存在,跳过解压!")
                        continue
                    zip_ref.extract(file, extract_folder)
            os.remove(zip_file_path)

            print("解压完成!")


            print("正在更新文件...")

            source_dir = os.path.join(current_dir, 'Firefly-Launcher')
            subprocess.run(f'xcopy /s /y /q "{source_dir}\*" "{current_dir}"', shell=True)
            shutil.rmtree(source_dir)

            print("更新文件完成!")


            run = input('更新完成,是否运行启动器?(' + "\033[32m" + 'y' + "\033[0m" + '/n)')
            if run in yes or run == '':
                subprocess.run(f'start ./Firefly-Launcher.exe', shell=True)
            else:
                input("请按 Enter 键关闭窗口...")
    else:
        run = input('当前是最新版本,是否运行启动器?(' + "\033[32m" + 'y' + "\033[0m" + '/n)')
        if run in yes or run == '':
            subprocess.run(f'start ./Firefly-Launcher.exe', shell=True)
        else:
            input("请按 Enter 键关闭窗口...")
            sys.exit()
else:
    print('当前为Dev版本,暂无法使用本程序!')
    input("请按 Enter 键关闭窗口...")
    sys.exit()