# Firefly Launcher
## 简介
本软件是一款基于 Pyside6 和 QFluentWidgets 的服务端启动器GUI , 旨在快捷地安装服务端所需环境、一键打开服务端 , 为PS之旅提供一个赏心悦目的操作界面 ~~而不是冰冷的CLI~~ 。

![image](https://github.com/letheriver2007/Firefly-Launcher/assets/77842352/b85f96a0-e185-48d2-b7eb-ae8aa2391bda)
## 计划
详情请见 [Project](https://github.com/letheriver2007/Firefly-Launcher/projects)
## 声明
### 警告
本仓库已开源 , 严禁二次打包发布 , 严禁倒卖 , 违者必究 ！！！
### 鸣谢
 - [PySide6-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/tree/PySide6)
## 使用
### 安装
#### 方法一(普通)
从本仓库的 [Release](https://github.com/letheriver2007/Firefly-Launcher/releases) 下载对应操作系统的稳定版本
#### 方法二(进阶)
从本仓库的 [Actions](https://github.com/letheriver2007/Firefly-Launcher/actions/) 下载对应操作系统的开发版本
#### 方法三(开发)
克隆本仓库，从源码构建GUI，目前运行build.bat可一键构建源码(无虚拟环境)
### 构建
解压文件或者构建，以下是构建完成后的文件目录

![image](https://github.com/letheriver2007/Firefly-Launcher/assets/77842352/2118e3a4-afa0-4683-9a1a-ca11084851a7)
### 字体
下载字体文件并安装，[字体文件](https://github.com/letheriver2007/Firefly-Launcher/releases/download/v1.2.0/zh-cn.ttf)
### 配置
#### 配置文件
打开软件->设置->配置->设置配置->打开文件 , 修改合适的代理端口、服务端名称和命令，默认文件见[config.json](https://github.com/letheriver2007/Firefly-Launcher/blob/main/config/config.json)
#### 代理设置
打开软件->设置->代理 , 根据需要调整代理设置
### 下载
#### 官方
前往下载页根据提示下载(仅支持Fiddler、Mitmdump、Lunarcore)

![image](https://github.com/letheriver2007/Firefly-Launcher/assets/77842352/8def8337-81b7-436c-9f65-1d939357201a)
#### 本地
根据需要可以自行下载文件后放入相应文件夹内
### 启动
#### 第一步
选择合适的服务端后点击一键启动
#### 第二步(可选)
对于部分需要额外启动代理软件的 , 如Fiddler、Mitmdump , 打开软件->设置->代理 , 选择相应软件后打开即可
#### 第三步(可选)
对于关闭服务端后存在未关闭代理设置的 , 打开软件->设置->代理->重置代理->重置 , 可一键关闭
