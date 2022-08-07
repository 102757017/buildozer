#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3
import datetime
import os
import sys
import pprint
import mysql.connector as mariadb
import traceback
from pathlib import Path
from kivy.logger import Logger


if getattr(sys, "frozen", False):  # bundle mode with PyInstaller
    os.environ["WICO_ROOT"] = sys._MEIPASS
else:
    os.environ["WICO_ROOT"] = str(Path(__file__).parent)

KV_DIR = f"{os.environ['WICO_ROOT']}"



def sync_ngrecord(sqlite_conn,mariadb_conn):
    sqlite_cursor = sqlite_conn.cursor()
    sqlcmd='''
    SELECT
    *
    FROM
    ngrecord
    WHERE Sync = "{}"
    '''.format(0)
    sqlite_cursor.execute(sqlcmd)
    values = sqlite_cursor.fetchall()
    

    if len(values)>0:
        mariadb_cursor = mariadb_conn.cursor()
        for value in values:
            #把元组修改为list
            value=list(value)
            #同步标识置1
            value[-1]=1
            value=tuple(value)
            
            #提交数据到服务器
            sqlcmd="INSERT INTO ngrecord VALUES {}".format(value)
            sqlcmd=sqlcmd.replace("None","NULL")
            mariadb_cursor.execute(sqlcmd)

            #修改本地数据库的同步标识
            sqlcmd="REPLACE INTO ngrecord VALUES {}".format(value)
            sqlcmd=sqlcmd.replace("None","NULL")
            #print(sqlcmd)
            sqlite_cursor.execute(sqlcmd)


        sqlite_conn.commit()    
        mariadb_conn.commit()

        mariadb_cursor.close()
    sqlite_cursor.close()

        
def sync_volume(sqlite_conn,mariadb_conn):
    sqlite_cursor = sqlite_conn.cursor()
    sqlcmd='''
    SELECT
    *
    FROM
    volume
    WHERE Sync = "{}"
    '''.format(0)
    sqlite_cursor.execute(sqlcmd)
    values = sqlite_cursor.fetchall()
    

    if len(values)>0:
        mariadb_cursor = mariadb_conn.cursor()
        for value in values:
            #把元组修改为list
            value=list(value)
            #同步标识置1
            value[-1]=1
            value=tuple(value)
            
            #提交数据到服务器
            sqlcmd="REPLACE INTO volume VALUES {}".format(value)
            sqlcmd=sqlcmd.replace("None","NULL")
            mariadb_cursor.execute(sqlcmd)

            #修改本地数据库的同步标识
            sqlcmd="REPLACE INTO volume VALUES {}".format(value)
            sqlcmd=sqlcmd.replace("None","NULL")
            #print(sqlcmd)
            sqlite_cursor.execute(sqlcmd)
        
        sqlite_conn.commit()    
        mariadb_conn.commit()

        mariadb_cursor.close()
    sqlite_cursor.close()


def sync_partlist(sqlite_conn,mariadb_conn):
    mariadb_cursor = mariadb_conn.cursor()
    sqlcmd='''
    SELECT
    *
    FROM
    partlist
    WHERE Sync = "{}"
    '''.format(0)
    mariadb_cursor.execute(sqlcmd)
    values = mariadb_cursor.fetchall()
    

    if len(values)>0:
        sqlite_cursor = sqlite_conn.cursor()
        for value in values:
            #把元组修改为list
            value=list(value)
            #同步标识置1
            value[-1]=1
            value=tuple(value)
            
            #更新本地数据库
            sqlcmd="REPLACE INTO partlist VALUES {}".format(value)
            sqlcmd=sqlcmd.replace("None","NULL")
            sqlite_cursor.execute(sqlcmd)

            #修改服务器数据库的同步标识
            sqlcmd="REPLACE INTO partlist VALUES {}".format(value)
            sqlcmd=sqlcmd.replace("None","NULL")
            #print(sqlcmd)
            mariadb_cursor.execute(sqlcmd)
        
        sqlite_conn.commit()    
        mariadb_conn.commit()
        
        sqlite_cursor.close()
    mariadb_cursor.close()


def sync_seatlist(sqlite_conn,mariadb_conn):
    mariadb_cursor = mariadb_conn.cursor()
    sqlcmd='''
    SELECT
    *
    FROM
    seatlist
    WHERE Sync = "{}"
    '''.format(0)
    mariadb_cursor.execute(sqlcmd)
    values = mariadb_cursor.fetchall()
    

    if len(values)>0:
        sqlite_cursor = sqlite_conn.cursor()
        for value in values:
            #把元组修改为list
            value=list(value)
            #同步标识置1
            value[-1]=1
            value=tuple(value)
            
            #更新本地数据库
            sqlcmd="REPLACE INTO seatlist VALUES {}".format(value)
            sqlcmd=sqlcmd.replace("None","NULL")
            sqlite_cursor.execute(sqlcmd)

            #修改服务器数据库的同步标识
            sqlcmd="REPLACE INTO seatlist VALUES {}".format(value)
            sqlcmd=sqlcmd.replace("None","NULL")
            #print(sqlcmd)
            mariadb_cursor.execute(sqlcmd)
        
        sqlite_conn.commit()    
        mariadb_conn.commit()
        
        sqlite_cursor.close()
    mariadb_cursor.close()


def sync_ngtype(sqlite_conn,mariadb_conn):
    mariadb_cursor = mariadb_conn.cursor()
    sqlcmd='''
    SELECT
    *
    FROM
    ngtype
    WHERE Sync = "{}"
    '''.format(0)
    mariadb_cursor.execute(sqlcmd)
    values = mariadb_cursor.fetchall()
    

    if len(values)>0:
        sqlite_cursor = sqlite_conn.cursor()
        for value in values:
            #把元组修改为list
            value=list(value)
            #同步标识置1
            value[-1]=1
            value=tuple(value)
            
            #更新本地数据库
            sqlcmd="REPLACE INTO ngtype VALUES {}".format(value)
            sqlcmd=sqlcmd.replace("None","NULL")
            sqlite_cursor.execute(sqlcmd)

            #修改服务器数据库的同步标识
            sqlcmd="REPLACE INTO ngtype VALUES {}".format(value)
            sqlcmd=sqlcmd.replace("None","NULL")
            #print(sqlcmd)
            mariadb_cursor.execute(sqlcmd)
        
        sqlite_conn.commit()    
        mariadb_conn.commit()
        
        sqlite_cursor.close()
    mariadb_cursor.close()

def sync_all():
    # 连接到SQLite数据库
    # 数据库文件是test.db
    # 如果文件不存在，会自动在当前目录创建:
    sqlite_conn = sqlite3.connect(f"{os.environ['WICO_ROOT']}/db.db")
    
    try: 
        mariadb_conn = mariadb.connect( 
        user="hewei", 
        password="wico2022", 
        host="sunnyho.f3322.net", 
        port=3306, 
        database="pyytest" )
        t1=datetime.datetime.now()
        sync_ngrecord(sqlite_conn,mariadb_conn)
        #print("NG品记录已同步完成")
        t2=datetime.datetime.now()
        sync_volume(sqlite_conn,mariadb_conn)
        #print("客户产量已同步完成")
        t3=datetime.datetime.now()
        sync_partlist(sqlite_conn,mariadb_conn)
        #print("产品清单已同步完成")
        t4=datetime.datetime.now()
        sync_seatlist(sqlite_conn,mariadb_conn)
        #print("座椅-部品信息已同步完成")
        t5=datetime.datetime.now()
        sync_ngtype(sqlite_conn,mariadb_conn)
        #print("不良类型及维修方法已同步完成")
        t6=datetime.datetime.now()
        Logger.info("ngrecord:{},volume:{},partlist:{},seatlist:{},ngtype:{}".format(t2-t1,t3-t2,t4-t3,t5-t4,t6-t5))
        return True
    except Exception:
        print(traceback.format_exc())
        return False

    

if __name__=="__main__":
    a=sync_all()
    print(a)
