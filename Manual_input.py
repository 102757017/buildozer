from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from pprint import pprint
import time
from search import *
import os
import sys
from functools import partial
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField
from barcode_analysis import analysis_part_lable
import re
from synch import sync_all
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
Logger.info("Manual_input_KV_DIR:"+KV_DIR)


'''
Kv 语言特有的三个关键字：
app：总是指您的应用程序的实例。
root：指当前规则中的基本小部件/模板,root只代表其上层被<>包裹住的类
self：始终引用当前小部件
'''

class UPPER_TEXT(MDTextField):
    #将输入转换为大写字符
    def insert_text(self, substring, from_undo=False):
        s = substring.upper()
        return super(UPPER_TEXT, self).insert_text(s, from_undo=from_undo)


class Manual_input(MDFloatLayout, MDTabsBase):
    def show_model1(self):
        bs_menu_1 = MDListBottomSheet()
        scroll = ScrollView()
        #CarModel=["2FW","2HY","2VH","2VP","2WB","2YC","2YN","2YS","2YT","3BS"]
        CarModel=get_CarModel()
        for item in CarModel:
            bs_menu_1.add_item(item,callback=lambda x, y=item: self.select_model1(y))                
        bs_menu_1.open()
    def select_model1(self, *args):
        self.ids.CarModel1.text=args[0]
        self.ids.SeatModel.text=""
        self.ids.PartType.text=""
        self.ids.WicoPartNumber.text=""
        self.ids.TsPartNumber.text=""
        self.ids.PartName.text=""
        self.ids.lot.text=""
        self.ids.NgInfo.text=""
        self.ids.RepairMethod1.text=""

    def show_SeatModel(self):
        bs_menu_1 = MDListBottomSheet()
        scroll = ScrollView()
        CarModel=self.ids.CarModel1.text
        SeatModel=get_SeatModel(CarModel)
        #SeatModel=["手动-前排-左席座椅","手动-前排-右席座椅"]
        for item in SeatModel:
            bs_menu_1.add_item(item,callback=lambda x, y=item: self.select_SeatModel(y))                
        bs_menu_1.open()
    def select_SeatModel(self, *args):
        self.ids.SeatModel.text=args[0]
        self.ids.PartType.text=""
        self.ids.WicoPartNumber.text=""
        self.ids.TsPartNumber.text=""
        self.ids.PartName.text=""
        self.ids.lot.text=""
        self.ids.NgInfo.text=""
        self.ids.RepairMethod1.text=""


    def show_product_type(self):
        bs_menu_1 = MDListBottomSheet()
        scroll = ScrollView()
        CarModel=self.ids.CarModel1.text
        SeatModel=self.ids.SeatModel.text
        PartType=get_PartType(CarModel,SeatModel)
        for item in PartType:
            bs_menu_1.add_item(item,callback=lambda x, y=item: self.select_product_type(y))                
        bs_menu_1.open()
    def select_product_type(self, *args):
        self.ids.PartType.text=args[0]
        self.ids.WicoPartNumber.text=""
        self.ids.TsPartNumber.text=""
        self.ids.PartName.text=""
        self.ids.lot.text=""
        self.ids.NgInfo.text=""
        self.ids.RepairMethod1.text=""


    def show_WicoPartNumber(self):
        bs_menu_1 = MDListBottomSheet()
        scroll = ScrollView()
        CarModel=self.ids.CarModel1.text
        SeatModel=self.ids.SeatModel.text
        PartType=self.ids.PartType.text
        WicoPartNumber,TsPartNumber,PartName,Supplier,Regular,Production_Line,PartPicUrl=get_PartNumberName(CarModel,SeatModel,PartType)
        for index, item in enumerate(WicoPartNumber):
            bs_menu_1.add_item(item,callback=partial(self.select_WicoPartNumber,item,TsPartNumber[index],PartName[index],Supplier[index],Regular[index],Production_Line[index],PartPicUrl[index]))
        bs_menu_1.open()
    def select_WicoPartNumber(self, *args):
        self.ids.WicoPartNumber.text=args[0]
        self.ids.TsPartNumber.text=args[1]
        self.ids.PartName.text=args[2]
        self.ids.lot.text=""
        self.ids.NgInfo.text=""
        self.ids.RepairMethod1.text=""
        self.Supplier=args[3]
        self.Regular=args[4]
        self.Production_Line=args[5]
        self.PartPicUrl=args[6]
        self.ids.part_image.source=self.PartPicUrl
        
        

    def show_TsPartNumber(self):
        bs_menu_1 = MDListBottomSheet()
        scroll = ScrollView()
        CarModel=self.ids.CarModel1.text
        SeatModel=self.ids.SeatModel.text
        PartType=self.ids.PartType.text
        WicoPartNumber,TsPartNumber,PartName,Supplier,Regular,Production_Line,PartPicUrl=get_PartNumberName(CarModel,SeatModel,PartType)
        for index, item in enumerate(TsPartNumber):
            bs_menu_1.add_item(item,callback=partial(self.select_TsPartNumber,WicoPartNumber[index],item,PartName[index],Supplier[index],Regular[index],Production_Line[index],PartPicUrl[index]))
        bs_menu_1.open()
    def select_TsPartNumber(self, *args):
        self.ids.WicoPartNumber.text=args[0]
        self.ids.TsPartNumber.text=args[1]
        self.ids.PartName.text=args[2]
        self.ids.lot.text=""
        self.ids.NgInfo.text=""
        self.ids.RepairMethod1.text=""
        self.Supplier=args[3]
        self.Regular=args[4]
        self.Production_Line=args[5]
        self.PartPicUrl=args[6]
        self.ids.part_image.source=self.PartPicUrl


    def show_PartName(self):
        bs_menu_1 = MDListBottomSheet()
        scroll = ScrollView()
        CarModel=self.ids.CarModel1.text
        SeatModel=self.ids.SeatModel.text
        PartType=self.ids.PartType.text
        WicoPartNumber,TsPartNumber,PartName,Supplier,Regular,Production_Line,PartPicUrl=get_PartNumberName(CarModel,SeatModel,PartType)
        for index, item in enumerate(PartName):
            bs_menu_1.add_item(item,callback=partial(self.select_PartName,WicoPartNumber[index],TsPartNumber[index],item,Supplier[index],Regular[index],Production_Line[index],PartPicUrl[index]))
        bs_menu_1.open()
    def select_PartName(self, *args):
        self.ids.WicoPartNumber.text=args[0]
        self.ids.TsPartNumber.text=args[1]
        self.ids.PartName.text=args[2]
        self.ids.lot.text=""
        self.ids.NgInfo.text=""
        self.ids.RepairMethod1.text=""
        self.Supplier=args[3]
        self.Regular=args[4]
        self.Production_Line=args[5]
        self.PartPicUrl=args[6]
        self.ids.part_image.source=self.PartPicUrl
        

    def show_ng_information1(self):
        bs_menu_1 = MDListBottomSheet()
        PartType=self.ids.PartType.text
        NgInfo=get_NgInfo(PartType)
        #NgInfo=["异音","震动"]
        for item in NgInfo:
            bs_menu_1.add_item(item,callback=lambda x, y=item: self.select_ng_information1(y))
        bs_menu_1.open()
    def select_ng_information1(self, *args):
        self.ids.NgInfo.text=args[0]
        self.ids.RepairMethod1.text=""
        
    def show_repair_method1(self):
        bs_menu_1 = MDListBottomSheet()
        PartType=self.ids.PartType.text
        NgInfo=self.ids.NgInfo.text
        RepairMethod=get_RepairMethod(PartType,NgInfo)
        #RepairMethod=["涂油","换电机"]
        for item in RepairMethod:
            bs_menu_1.add_item(item,callback=lambda x, y=item: self.select_repair_method1(y))
        bs_menu_1.open()
    def select_repair_method1(self, *args):
        self.ids.RepairMethod1.text=args[0]


    
    def upload(self):
        #返修方法，产品番号是否填写
        if self.ids.RepairMethod1.text !="" and self.ids.NgInfo.text !="" and self.ids.WicoPartNumber.text !="":
            # 格式化成2016-03-20 11:45:39形式
            NgTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            CarModel=self.ids.CarModel1.text
            SeatModel=self.ids.SeatModel.text
            WicoPartNumber=self.ids.WicoPartNumber.text
            TsPartNumber=self.ids.TsPartNumber.text
            PartName=self.ids.PartName.text
            PartType=self.ids.PartType.text
            Supplier=self.Supplier
            NgInfo=self.ids.NgInfo.text
            RepairMethod=self.ids.RepairMethod1.text
            Production_Line=self.Production_Line
            Lot=self.ids.lot.text
            ManufactureDate=""
            #批次号是否填写，是否有条码规则
            if self.ids.lot.text !="" and self.Regular !="":
                #查询番号&条码是否重复
                if search_barcode(WicoPartNumber,Lot)==False:

                    #条码与条码规则是否匹配
                    result = re.findall(self.Regular, Lot)
                    if len(result)==1:
                        #根据标签/条码提取（生产线号）、生产日期
                        line,lable_date=analysis_part_lable(lable,Regular)
                        if line =="":
                            ManufactureDate=lable_date
                        else:
                            Production_Line=line
                            ManufactureDate=lable_date
                        #提交表单
                        uploade_ngrecord(NgTime,
                                        CarModel,
                                        SeatModel,
                                        WicoPartNumber,
                                        TsPartNumber,
                                        PartName,
                                        PartType,
                                        Supplier,
                                        NgInfo,
                                        RepairMethod,
                                        Lot,
                                        ManufactureDate,
                                        Production_Line,
                                        0)
                        #toast("数据在本地保存完成")
                        f=sync_all()
                        if f==True:
                            toast("数据已上传到服务器")
                        else:
                            toast("数据上传到服务器失败，稍后重新启动app将再次尝试上传")

                        self.ids.RepairMethod1.text =""
                        self.ids.NgInfo.text =""
                        self.ids.lot.text =""
                    else:
                        toast("输入的批次号与本产品批次号格式不符,请重新输入批次号")
                else:
                    toast("此批次号的产品此前已经上传过不良信息了，请勿重复上传")               
            else:
                #提交表单
                uploade_ngrecord(NgTime,
                                CarModel,
                                SeatModel,
                                WicoPartNumber,
                                TsPartNumber,
                                PartName,
                                PartType,
                                Supplier,
                                NgInfo,
                                RepairMethod,
                                Lot,
                                ManufactureDate,
                                Production_Line,
                                0)
                #toast("数据在本地保存完成")
                f=sync_all()
                if f==True:
                    toast("数据已上传到服务器")
                else:
                    toast("数据上传到服务器失败，稍后重新启动app将再次尝试上传")
                self.ids.RepairMethod1.text =""
                self.ids.NgInfo.text =""
                self.ids.lot.text =""
        else:
            toast("请将表单填写完整后再上传")



class DemoApp(MDApp):

    def build(self):
        scn=Screen()
        scn.add_widget(Manual_input())
        return scn

    
if __name__ == '__main__':
    #如果KV定义了一个Root Widget，它将附加到 App 的root 属性并用作应用程序的根部件，这个根部件附加完成后，再执行__init__中的代码。
    Builder.load_file( f"{os.environ['WICO_ROOT']}/manual_input.kv" )
    DemoApp().run()
