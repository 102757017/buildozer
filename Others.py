from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from pprint import pprint
from search import *
import os
import sys
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.utils import parseaddr, formataddr
from email.header import Header
from email.mime.application import MIMEApplication
from pathlib import Path
from kivy.logger import Logger

#  所有基于模块的使用到__file__属性的代码，在源码运行时表示的是当前脚本的绝对路径，但是用pyinstaller打包后就是当前模块的模块名（即文件名xxx.py）
#  因此需要用以下代码来获取exe的绝对路径
if getattr(sys, "frozen", False):  # bundle mode with PyInstaller
    os.environ["WICO_ROOT"] = sys._MEIPASS
else:
    os.environ["WICO_ROOT"] = str(Path(__file__).parent)

KV_DIR = f"{os.environ['WICO_ROOT']}"
sys.path.append(KV_DIR)
Logger.info("Others_KV_DIR:"+KV_DIR)


'''
Kv 语言特有的三个关键字：
app：总是指您的应用程序的实例。
root：指当前规则中的基本小部件/模板,root只代表其上层被<>包裹住的类
self：始终引用当前小部件
'''



class Others(MDFloatLayout, MDTabsBase):
    def send_mail(self, *args):
        self.ids.submit_advice.disabled=True
        text=self.ids.advice.text
        #传入'plain'表示纯文本
        content = MIMEText(text, 'plain', 'utf-8')

        msg = MIMEMultipart()
        msg.attach(content)
        

        # 输入Email地址和口令:
        from_addr = "wico2022@163.com"
        password = "EASEXKCOHRCGENFK"
        # 输入收件人地址:
        to_addr ="hewei@imasenwh.com"
        # 输入SMTP服务器地址:
        smtp_server = "smtp.yeah.net"
        smtp_server = "smtp.163.com"


        def _format_addr(s):
            name, addr = parseaddr(s)
            return formataddr((Header(name, 'utf-8').encode(), addr))

        msg['From'] = _format_addr('驻在员 <%s>' % from_addr)
        msg['To'] = _format_addr('何威 <%s>' % to_addr)
        msg['Subject'] = Header('驻在员反馈的改善建议', 'utf-8').encode()

        # SMTP协议默认端口是25
        server = smtplib.SMTP(smtp_server, 25) 
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        self.ids.content.text=""
        self.ids.submit_advice.disabled=False
        

    def send_database(self, *args):
        self.ids.submit_database.disabled=True
        text=self.ids.advice.text
        database=open('db.db','rb').read()
        #传入'plain'表示纯文本
        content = MIMEText(text, 'plain', 'utf-8')

        msg = MIMEMultipart()
        msg.attach(content)
        
        if database !=None:
             # 构建并添加db
            db = MIMEApplication(database)
            db.add_header('Content-Disposition', 'attachment', filename="db.db")   
            msg.attach(db)

        # 输入Email地址和口令:
        from_addr = "wico2022@163.com"
        password = "EASEXKCOHRCGENFK"
        # 输入收件人地址:
        to_addr ="sdf63fg@yeah.net"
        # 输入SMTP服务器地址:
        smtp_server = "smtp.yeah.net"
        smtp_server = "smtp.163.com"


        def _format_addr(s):
            name, addr = parseaddr(s)
            return formataddr((Header(name, 'utf-8').encode(), addr))

        msg['From'] = _format_addr('驻在员 <%s>' % from_addr)
        msg['To'] = _format_addr('何威 <%s>' % to_addr)
        msg['Subject'] = Header('客户不良信息数据库', 'utf-8').encode()

        # SMTP协议默认端口是25
        server = smtplib.SMTP(smtp_server, 25) 
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        self.ids.content.text=""
        self.ids.submit_database.disabled=False



class DemoApp(MDApp):

    def build(self):
        scn=Screen()
        scn.add_widget(Others(title="其它"))
        return scn

    
if __name__ == '__main__':
    #如果KV定义了一个Root Widget，它将附加到 App 的root 属性并用作应用程序的根部件，这个根部件附加完成后，再执行__init__中的代码。
    Builder.load_file( f"{os.environ['WICO_ROOT']}/others.kv" )
    DemoApp().run()
