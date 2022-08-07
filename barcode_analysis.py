# -*- coding: UTF-8 -*-
import re          #导入正则表达式库
from search import get_Regulars
import pprint


#imasen_barcode,1TBA([1-9A-E])1([1-9A-C])([1-9A-HJ-NP-X])([0-9A-F]{3})([0-9A-Z])([WT])
#imasen_label,([0-9]{2})([A-L])([0-3][0-9])([A-C]) ([0-9]{3})
#mitsuba_qrcode,NR([0-9])([A-L])([0-9]{2})([0-9]{4})
#sanyo_qrcod,23-4729910-2.+?:([0-9]{2})([0-9]{2})([0-9]{2})


def imasen_barcode(result):
    print('This is imasen_barcode')
    d_year={"1":"2015","2":"2016","3":"2017","4":"2018","5":"2019","6":"2020","7":"2021","8":"2022","9":"2023","A":"2024","B":"2025","C":"2026","D":"2027","E":"2028"}
    d_month={"1":"01","2":"02","3":"03","4":"04","5":"05","6":"06","7":"07","8":"08","9":"09","A":"10","B":"11","C":"12"}
    d_day={"1":"1","2":"2","3":"3","4":"4","5":"5","6":"6","7":"7","8":"8","9":"9","A":"10","B":"11","C":"12","D":"13","E":"14","F":"15","G":"16","H":"17","J":"18","K":"19","L":"20","M":"21","N":"22","P":"23","Q":"24","R":"25","S":"26","T":"27","U":"28","V":"29","W":"30","X":"31"}
    d_line={"3":"58103","7":"58107","8":"58108","G":"58116","H":"58117","J":"58119","K":"58120","L":"58118"}
    d_country={"W":"中国","T":"泰国"}
    year,month,day,line="","","",""
    try:
        year=d_year[result[0][0]]
        month=d_month[result[0][1]]
        day=d_day[result[0][2]]
    except BaseException as e:
        print('年月日代码有误')
    seq=int(result[0][3], 16)
    try:
        line=d_line[result[0][4]]
    except BaseException as e:
        print('生产线代码{}不在数据库中，请联络程序开发人员更新APP'.format(e))

    try:
        country=d_country[result[0][5]]    
    except BaseException as e:
        print('国别代码{}不在数据库中，请联络程序开发人员更新APP'.format(e))
    
    date=year+"-"+month+"-"+day
    print("{}工厂{}生产线  {}生产的第{}个产品".format(country,line,date,seq))
    return date,line
    
def imasen_lable(result):
    #([0-9]{2})([A-L])([0-3][0-9])([A-C]) ([0-9]{3})
    d_month={"A":"01","B":"02","C":"03","D":"04","E":"05","F":"06","G":"07","H":"08","I":"09","J":"10","K":"11","L":"12"}
    year,month,day="","",""

    year="20"+result[0][0]
    month=d_month[result[0][1]]
    day=result[0][2]
    seq=result[0][4]
    date=year+"-"+month+"-"+day
    print("{}生产的第{}个产品".format(date,seq))
    return date


    
    
    

    
def mitsuba_qrcode(result):
    print('This is mitsuba_qrcode')
    year,month,day,line="","","",""
    d_year={"1":"2021","2":"2022","3":"2023","4":"2024","5":"2025","6":"2026","7":"2027","8":"2028","9":"2029"}
    d_month={"A":"1","B":"2","C":"3","D":"4","E":"5","F":"6","G":"7","H":"8","I":"9","J":"10","K":"11","L":"12"}
    try:
        year=d_year[result[0][0]]
        month=d_month[result[0][1]]
        day=result[0][2]
    except BaseException as e:
        print('年月日代码有误')
    date=year+"-"+month+"-"+day
    seq=result[0][3]
    print("{}生产的第{}个产品".format(date,seq))
    return date,line

    
def sanyo_qrcode(result):
    #23-4729910-2.+?:([0-9]{2})([0-9]{2})([0-9]{2})
    year,month,day,line="","","",""
    print('This is sanyo_qrcod')
    year,month,day,line="","","",""
    year="20"+result[0][2]
    month=result[0][1]
    day=result[0][0]
    date=year+"-"+month+"-"+day
    print("{}生产的产品".format(date))
    return date,line

    
def default():
    print('根据正则表达式的长度匹配不到已知的规则，不知道是那种类型的条码，无法解析生产日期')




def analysis_code(t):
    found=0
    Regular=get_Regulars()
    for x in Regular:
        part_number=x[0]
        #正则表达式
        re_rule=x[1]
        result = re.findall(re_rule, t)
        if len(result)==1:
            found=1
            #根据正则表达式的长度匹配条码规则，判断是那种类型的条码，进入不同的解析函数
            if len(re_rule)==70:
                date,line=imasen_barcode(result)
                
            if len(re_rule)==36:
                date,line=mitsuba_qrcode(result)
                
            if len(re_rule)==46:
                date,line=sanyo_qrcode(result)
            break
    if found==0:
        print("无法匹配已知的条码模板，输入的条码有误")
        part_number,line,date="","",""

    return part_number,line,date



def analysis_part_lable(lable,Regular):
    result = re.findall(Regular, lable)
    if Regular=="([0-9]{2})([A-L])([0-3][0-9])([A-C]) ([0-9]{3})":
        date=imasen_lable(result)
        line=""
    
    #根据正则表达式的长度匹配条码规则，判断是那种类型的条码，进入不同的解析函数
    if len(Regular)==64:
        date,line=imasen_barcode(result)
        
    if len(Regular)==36:
        date,line=mitsuba_qrcode(result)
        
    if len(Regular)==46:
        date,line=sanyo_qrcode(result)
    
    return line,date







if __name__ == '__main__':
    #t="IMAFT WITHOUT HES MOTORLV NO.:LVSMT111912-A03IMASEN NO.:Z23-4729910-2MOTOR NO.:250222 B302 02311"
    t="13M0817K064GW"
    part_number,line,date=analysis_code(t)
    print(part_number,line,date)

    line,date=analysis_part_lable("13M0817K064GW","13M0([1-9A-E])1([1-9A-C])([1-9A-X])([0-9A-F]{3})([0-9A-Z])([WT])")
    print(line,date)


