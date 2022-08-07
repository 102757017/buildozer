### 一、解决中文乱码问题

Kivy和KivyMD原生不支持中文，采用的默认字体是英文字体，直接运行起来就会显示方框。

Kivy中可以通过设置LabelBase修改字体，但是每一个控件都要在代码中增加font_style的定义，非常不方便。而KivyMD的控件就没有提供定义LabelBase改字体的功能。

而且，即使在本机开发环境中修改了字体设置，在打包生成apk文件安装后，在手机上运行时仍然是乱码。

下面是使用buildozer打包时，彻底解决中文乱码问题的方法。

**第一步，修改kivy字体设置**

下载中文字体保存到main.py 所在的文件夹中，在main.py中设置字体

kv语言设置方式:

```
Label:
    size_hint: None, None
    font_name:"DroidSansFallback.ttf"
    text: "中文"
```

py文件设置方式

```
Label(text='中文',font_name="DroidSansFallback.ttf")
```



**第二步，修改kivyMD的字体设置**

clone kivyMD的库，首先将新增的msyh.ttc字体文件复制到kivymd/fonts/目录下，然后修改font_definitions.py.

```
fonts = [
     {
         "name": "Roboto",
         "fn_regular": fonts_path + "DroidSansFallback.ttf",
         "fn_bold": fonts_path + "DroidSansFallback.ttf",
         "fn_italic": fonts_path + "DroidSansFallback.ttf",
         "fn_bolditalic": fonts_path + "DroidSansFallback.ttf",
     },
     {
         "name": "RobotoThin",
         "fn_regular": fonts_path + "DroidSansFallback.ttf",
         "fn_italic": fonts_path + "DroidSansFallback.ttf",
     },
     {
         "name": "RobotoLight",
         "fn_regular": fonts_path + "DroidSansFallback.ttf",
         "fn_italic": fonts_path + "DroidSansFallback.ttf",
     },
     {
         "name": "RobotoMedium",
         "fn_regular": fonts_path + "DroidSansFallback.ttf",
         "fn_italic": fonts_path + "DroidSansFallback.ttf",
     },
     {
         "name": "RobotoBlack",
         "fn_regular": fonts_path + "DroidSansFallback.ttf",
         "fn_italic": fonts_path + "DroidSansFallback.ttf",
     },
     {
         "name": "Icons",
         "fn_regular": fonts_path + "materialdesignicons-webfont.ttf",
     },
 ]
```

这里，同样不修改Boboto的字体类型名称，这样不用修改其它诸多py文件。我是都改为了msyh.ttc，你也可以按需增加light、Black等字体。

修改完成后push到github

在buildozer.spec中设置依赖包为修改后的KivyMD库

```
requirements = 
    git+https://github.com/102757017/KivyMD.git@master,
```









### 二、buildozer.spec的设置问题

buildozer.spec的设置很重要，往往决定了打包apk过程能否顺利，以及apk安装到手机后能否正常运行。以下几个设置需要关注。

**一是依赖模块要全**

比如我的程序的依赖模块如下

```
requirements = 
    python3==3.8.5,
    #kivy[base] @ https://github.com/102757017/kivy/archive/master.zip,
    kivy,
    git+https://github.com/102757017/KivyMD.git@master,
    sdl2_ttf==2.0.15,
    pillow,
    android,
    #opencv-python,
    xcamera,
    pyzbar
```

KivyMD默认版本过低，必须用github上的。

requirements中的包仅支持无需编译就可以安装的包（whl或者py文件的），上方的kivy自定义分支，由于需要编译后才能安装，因此使用buildozer打包时会虽然可以生成apk，但是运行时会报错。

android是请求安卓权限必须的（特别是在安卓10和11上）。





**二是安卓权限要定义，并在程序运行中动态请求**

安卓10以后，对权限的管理大为改变，我初期调试时多次因为权限设置问题通不过。

buildozer.spec中要进行定义：

```
 android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET,WAKE_LOCK
 android.wakelock = True
```

然后代码中要进行相应申请：

```
 from kivy.utils import platform
 if platform == "android":
     from android.permissions import request_permissions, Permission
     request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.INTERNET])    
     from android.storage import primary_external_storage_path
     appwd=primary_external_storage_path()+'/Download/yourapp'
```



### 三、解决自定义模块路径问题

buildozer打包成apk时，会出现找不到当前目前下的模块的问题，import自定义模块时找不到文件

这是因为buildozer使用到了pyinstaller，会生成临时目录_MEIPASS，打包进去的kv文件都被展开到临时目录下。这就要在main.py中进行修改：

所有基于模块的使用到____file____属性的代码，在源码运行时表示的是当前脚本的绝对路径，但是用pyinstaller打包后就是当前模块的模块名（即文件名xxx.py）

因此需要用以下代码来获取脚本的绝对路径

```
import sys
import os
if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
print("工作路径",bundle_dir)
sys.path.append(bundle_dir)
from kivy_garden.zbarcam.zbarcam import ZBarCam
```

修改完后运行pyinstaller.exe xxxx.spec，成功。



### 四、打包成apk

由于打包需要的依赖项目有很多资源在国内的网络条件下难以下载，因此在github actions中进行编译，以下是工作流文件

```
# This is a basic workflow to help you get started with Actions

name: kivydemo编译apk

# Controls when the action will run. Triggers the workflow on push or pull request
# events but only for the main branch
on:
  #手动触发工作流程运行
  workflow_dispatch:

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "build"
  build-and-deploy:
    name: Build for Android
    # The type of runner that the job will run on
    runs-on: ubuntu-latest

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
      - name: Checkout
        uses: actions/checkout@v2    
    
      - name: Build with Buildozer
        uses: ArtemSBulgakov/buildozer-action@v1
        id: buildozer
        with:
          workdir: zbarcam-develop
          buildozer_version: stable
         
      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: package
          path: ${{ steps.buildozer.outputs.filename }}
```



## 

### 五、安卓调试问题

安装软件包

```
adb devices
adb install -r /Users/streetpoet/Desktop/MytvPauselive.apk
```



如果程序闪退，则进行adb调试查看错误信息，直接运行adb logcat，会显示大量老旧和无关调试信息，造成定位我们程序Bug的难度增加。

这里，可以先清空log文件。再开始记录

```
adb logcat -c
adb logcat > my_log.txt
```

然后通过搜索‘Python for android ended’这句话，快速找到出错点。

比如下面的log文件就显示出，程序崩溃是因为没有加载docutils模块。

```
10-06 23:20:08.445  4181  6396 I python  :    File "/home/xxx/Documents/kivy_exp/.buildozer/android/platform/build-armeabi-v7a/build/python-installs/yourapp/kivy/uix/rst.py", line 81, in <module>                                          
 10-06 23:20:08.445  4181  6396 I python  :  ModuleNotFoundError: No module named 'docutils'    
 10-06 23:20:08.445  4181  6396 I python  : Python for android ended.            
```



from kivy.logger import Logger
Logger.info('title: This is a info message.')



run-as org.kivymd.wico

cd files/app/.kivy/logs

ls

cat XXX.txt



### 五、在安卓上使用webview的问题

网上关于此问题最好的示代代码如下：

https://insideconspiracy.blogspot.com/2020/03/inline-webview-within-your-kivy-app.html

一键配置脚本
将上面的过程写入一个 bash 脚本，可以轻松的实现一键配置代理：

#!/bin/bash
host_ip=$(cat /etc/resolv.conf |grep "nameserver" |cut -f 2 -d " ")
export ALL_PROXY="http://$host_ip:10809"

脚本通过 cat /etc/resolv.conf 来获取 DNS 服务器，也就是 Windows 的 IP，再将其中的 IP 部分截取出来，加上代理客户端的端口（我的是 7890，可以根据自己实际情况修改），使用 export 写入环境变量中。






sudo apt install default-jre -y

sudo apt install default-jdk -y





错误信息：
正克隆到‘python-for-android’...
fatal：无法访问‘https://github.com/kivy/python-for-android.git/  之类错误

which buildozer  #找到buildozer路径

cat /usr/local/bin/buildozer  #查看入口点load_entry_point('buildozer==1.0.1.dev0

cd /usr/local/lib/python2.7/dist-packages #python2.7目录里找到buildozer-1.0.1.dev0-py2.7.egg/文件夹

cd /usr/local/lib/python2.7/dist-packages/buildozer-1.0.1.dev0-py2.7.egg/buildozer/targets #就这里

vim android.py     

\#找到TargetAndroid(Target)类，p4a_fork = 'kivy' 改成p4a_fork = 'mirrors'      

\#找到github.com替换gitee.com





- 进入您的应用程序目录并运行：

  ```
  buildozer init
  # edit the buildozer.spec, then
  buildozer android debug deploy run
  ```