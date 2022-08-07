[app]

# (str) Title of your application
title = WICO

# (str) Package name
package.name = WICO

# (str) Package domain (needed for android/ios packaging)
package.domain = org.kivymd

# (str) Source code where the main.py live
source.dir = .

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/assets/images/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/assets/images/logo.png


# (list) Source files to include (let empty to include all the files)
#source.include_exts = py, gif, png, jpg, jpeg, ttf, kv, json, txt, md

source.exclude_exts = xlsx, md


# (str) Application versioning (method 2)
version = 0.1


# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
#python的小版本对app有影响，如果用错了版本，虽然apk会生成成功，但是会闪崩。
#指定版本时需要明确完整版本号，例如python3==3.8.10,python3=3.8，python3>=3.8.10都是不行的
#这里只能放入纯python的模块，如果有依赖C的模块，要看recipe清单中有无支持(https://github.com/kivy/python-for-android/tree/develop/pythonforandroid/recipes)，
#将对应的项目拷贝到./p4a-recipes文件夹后再在requirements中添加依赖
requirements = python3, \
               kivy==2.1.0, \
               git+https://github.com/102757017/KivyMD.git@master, \
               pillow, \
               certifi, \
               pyzbar, \
               mysql_connector, \
               camera4kivy, \
               gestures4kivy

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = all

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0


#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios
# Alternately, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# Another platform dependency: ios-deploy
# Uncomment to use a custom checkout
#ios.ios_deploy_dir = ../ios_deploy
# Or specify URL and branch
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

# (bool) Whether or not to sign the code
ios.codesign.allowed = false

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) The development team to use for signing the debug version
#ios.codesign.development_team.debug = <hexstring>

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s

# (str) The development team to use for signing the release version
#ios.codesign.development_team.release = <hexstring>

# (str) URL pointing to .ipa file to be installed
# This option should be defined along with `display_image_url` and `full_size_image_url` options.
#ios.manifest.app_url =

# (str) URL pointing to an icon (57x57px) to be displayed during download
# This option should be defined along with `app_url` and `full_size_image_url` options.
#ios.manifest.display_image_url =

# (str) URL pointing to a large icon (512x512px) to be used by iTunes
# This option should be defined along with `app_url` and `display_image_url` options.
#ios.manifest.full_size_image_url =



#
# OSX Specific
#

#
# author = © Copyright Info

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 1.9.1


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0
