from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from search import *
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.screenmanager import Screen
import pprint
from kivy.logger import Logger


class Nginfo_tables(MDFloatLayout, MDTabsBase):
    def __init__(self, **kwargs):
        #一定要注意这里要加super，才能把现有的新初始化方法覆盖掉继承来的旧初始化方法
        super().__init__(**kwargs)
        self.title="已录入NG信息"
        self.name="inputed_ng_info"

        info=query_nginfo()
        for i,j in enumerate(info):
            info[i]=list(j)
            for x,y in enumerate(j):
                y="[size=25]"+str(y)
                info[i][x]=y
        self.data_tables = MDDataTable(
            use_pagination=False,
            check=True,
            column_data=[
                ("[size=25]车型", dp(18)),
                ("[size=25]座椅型号", dp(20)),
                ("[size=25]WICO番号", dp(21)),
                ("[size=25]TS番号", dp(27)),
                ("[size=25]零件名称", dp(30)),
                ("[size=25]不良信息", dp(25)),
                ("[size=25]维修方法", dp(25)),
                ("[size=25]批次号", dp(18)),
                ("[size=25]生产日期", dp(18)),
            ],
            row_data=info
            )
        self.data_tables.bind(on_row_press=self.on_row_press)
        self.data_tables.bind(on_check_press=self.on_check_press)
        self.add_widget(self.data_tables) 


    #更新表格中的数据
    def update(self):
        info=query_nginfo()
        for i,j in enumerate(info):
            info[i]=list(j)
            for x,y in enumerate(j):
                y="[size=25]"+str(y)
                info[i][x]=y
        self.data_tables.update_row_data(instance_data_table=self.data_tables,data=info)
 
    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''
        print(instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''

class DemoApp(MDApp):

    def build(self):
        scn=Screen()
        scn.add_widget(Nginfo_tables())
        return scn



if __name__=="__main__":
    #Builder.load_file( '' )
    DemoApp().run()
