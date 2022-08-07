from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from pprint import pprint
import os
import sys
import datetime
from pathlib import Path
from kivy.logger import Logger
import traceback
import threading

#  所有基于模块的使用到__file__属性的代码，在源码运行时表示的是当前脚本的绝对路径，但是用pyinstaller打包后就是当前模块的模块名（即文件名xxx.py）
#  因此需要用以下代码来获取exe的绝对路径
if getattr(sys, "frozen", False):  # bundle mode with PyInstaller
    os.environ["WICO_ROOT"] = sys._MEIPASS
else:
    os.environ["WICO_ROOT"] = str(Path(__file__).parent)

KV_DIR = f"{os.environ['WICO_ROOT']}"
sys.path.append(KV_DIR)
Logger.info("MainScreen_KV_DIR:"+KV_DIR)




'''
Kv 语言特有的三个关键字：
app：总是指您的应用程序的实例。
root：指当前规则中的基本小部件/模板,root只代表其上层被<>包裹住的类
self：始终引用当前小部件
'''



class MainScreen(Screen):
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        '''Called when switching tabs.
        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''
        #print(instance_tab.name)
        if instance_tab.name=="inputed_ng_info":
            t1=threading.Thread(target=instance_tab.update())
            t1.start()
            

from EnterNgIfo import EnterNgIfo
from Manual_input import Manual_input
from OutPutInfo import OutPutInfo
from MDDataTable import Nginfo_tables
from Others import Others

class DemoApp(MDApp):

    def build(self):
        self.EnterNgIfo=EnterNgIfo()
        self.Manual_input=Manual_input()
        self.OutPutInfo=OutPutInfo()
        self.Nginfo_tables=Nginfo_tables()
        self.Others=Others()
        
        scn=Screen()
        a=MainScreen()
        a.ids.tab.add_widget(self.EnterNgIfo)
        a.ids.tab.add_widget(self.Manual_input)
        a.ids.tab.add_widget(self.OutPutInfo)
        a.ids.tab.add_widget(self.Nginfo_tables)
        a.ids.tab.add_widget(self.Others)
        scn.add_widget(a)
        return scn

    
if __name__ == '__main__':
    #如果KV定义了一个Root Widget，它将附加到 App 的root 属性并用作应用程序的根部件，这个根部件附加完成后，再执行__init__中的代码。
    Builder.load_file( f"{os.environ['WICO_ROOT']}/mainscreen.kv" )
    DemoApp().run()
        
