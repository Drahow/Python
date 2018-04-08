#!/usr/bin/env python
#-*- coding: utf-8 -*-

import argparse
import os
import sqlite3
import re
import itertools

#创建解析对象
parser = argparse.ArgumentParser()

#添加命令行
#根据pos和lock选择边模
#parser.add_argument('-p','--position',type = int, choices = range(0,1000),dest = 'position', help ='BM position')
parser.add_argument('-p','--position',type = int ,dest = 'position', help = 'BM Position')
parser.add_argument('-l','--lock',type = int, dest = 'lock',help='BM lock status')
parser.add_argument('-m','--maxnum',type = int, dest = 'maxnum', help = 'BM maxnum number')
parser.add_argument('-n','--num',type = int ,dest = 'number',help = 'BM number')
parser.add_argument('-i','--id',type = int,dest = 'id', help = 'BM ID')
parser.add_argument('-s','--sort',type = int,dest = 'sort',help = 'BM sort status', default = 1)
#parser.add_argument('-X','--Xposition',type = float, choices = range(-100000,100000),dest = 'Xposition', help = 'BM X Position')
parser.add_argument('-X','--Xposition',type = float, dest = 'Xposition',help = 'X Positon')
#parser.add_argument('-Y','--Yposition',type = float, choices = range(-100000,100000),dest = 'Yposition',help = 'BM Y Position')
parser.add_argument('-Y','--Yposition',type = float, dest = 'Yposition',help = 'Y Position')
#parser.add_argument('-Z','--Zposition',type = float, choices = range(-100000,100000),dest = 'Zposition',help = 'BM Z Position')
parser.add_argument('-Z','-Zposition',type = float, dest = 'Zposition', help = 'Z Position')
#parser.add_argument('-C','--Cposition',type = float, choices = range(-180,180),dest = 'Cposition',help = 'BM C Position')
parser.add_argument('-C','--Cposition',type = float, dest ='Cposition', help = 'C Position')

#查询or删除or修改or插入
parser.add_argument('use',type = str,help = 'sel or selall or del or update or insert')
#数据库名称
parser.add_argument('-name',type = str,help = 'database name',default = 'shutter.sqlite')
#解析命令行
args = parser.parse_args()
sql_name = args.name
print(sql_name)
sql_oname = re.findall('(.*?)\..*',sql_name)
print(sql_oname)

#数据库操作
def sql_operation(use,kw):
#def sql_operation(use,pos,sort,lock,maxnum,num,id,x,y,z,a):
#    print(kw)
    operater = operation()
    [pos, sort, lock, maxnum, num, id, x, y, z, a] = kw
#    conn = sqlite3.connect(args.name)
#    cursor = conn.cursor()
    if use == 'sel':
        operater.sql_select(pos,sort)
    elif use == 'del':
        operater.sql_delete(pos,sort)
    elif use == 'update':
        operater.sql_update(kw)
    elif use == 'insert':
        operater.sql_insert(pos,maxnum,num,id,lock,sort,x,y,z,a)
    elif use == 'selall':
        operater.sql_selectall()

#    cursor.close()
#    conn.commit()
#    conn.close()

class operation(object):
#    def __init__(self,sql_name):
#        self.sql_name = sql_name

    def sql_select(self,pos,sort):
        conn = sqlite3.connect(sql_name)
        cursor = conn.cursor()
        condition = '<a>pos=%s and sort = %s</a>'%(pos,sort)
        cond = re.compile('<a>(.*?)</a>')
        cond = cond.findall(condition)
        print(cond)
        cursor.execute('select * from %s where %s'%(sql_oname[0],cond[0]))
        datas = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        for data in datas:
            print(data)

    def sql_delete(self,pos,sort):
        conn = sqlite3.connect(sql_name)
        cursor = conn.cursor()
        condition ='<a>pos=%s and sort=%s</a>'%(pos,sort)
        print(condition)
        cond = re.compile('<a>(.*?)</a>')
        cond = cond.findall(condition)
        cursor.execute('delete from %s where %s'%(sql_oname[0],cond[0]))
        print('delete from shutter where %s'%cond[0])
    #    info = cursor.fetchall()
    #    print(info)
        cursor.close()
        conn.commit()
        conn.close()

    def sql_insert(self,pos,maxnum,num,id,lock,sort,x,y,z,a):
        conn = sqlite3.connect(sql_name)
        cursor = conn.cursor()
        condition = '<a>(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)</a>'%(pos,maxnum,num,id,lock,sort,x,y,z,a)
        cond = re.compile('<a>(.*?)</a>')
        cond = cond.findall(condition)
        cursor.execute('insert into %s (pos,maxnum,num,id,lock,sort,x,y,z,a) values %s'%(sql_oname[0],cond[0]))
        cursor.close()
        conn.commit()
        conn.close()

    def sql_selectall(self):
        conn = sqlite3.connect(sql_name)
        cursor = conn.cursor()
        cursor.execute('select * from %s'%sql_oname[0])
        datas = cursor.fetchall()
        print(len(datas))
        for data in datas:
            print(data)
        cursor.close()
        conn.commit()
        conn.close()

    def sql_update(self,kw):
        [pos, sort, lock, maxnum, num, id, x, y, z, a] = kw
        dict = {'pos': pos,'sort': sort,'lock': lock,'maxnum': maxnum,'num': num,'id': id,'x': x,'y': y,'z': z,'a': a}
        for value in dict.values():
             print(value)
        conn = sqlite3.connect(sql_name)
        cursor = conn.cursor()
        condition = '<a>pos = %s and sort = %s</a>'%(pos,sort)
        cond = re.compile('<a>(.*?)</a>')
        cond = cond.findall(condition)
        operate_dict = {}
        while(1):
            new_pos = input('new_pos_input (''I'' represent ignore): ')
            if new_pos == ('I' or 'i'):
               print('new_pos is None')
            elif type(new_pos) is int or float:
               operate_dict.setdefault('pos', new_pos)  
               break
            new_sort = input('new_sort: ')
            if new_sort == 'I':
               pass
            elif type(new_sort) is int or float:
                operate_dict.setdefault('sort', new_sort)
                break
            new_lock = input('new_lock: ')
            if new_lock == 'I':
                pass
            else:
                operate_dict.setdefault('lock', new_lock)
                break
            new_maxnum = input('new_maxnum: ')
            if new_maxnum == 'I':
                pass
            else:
                operate_dict.setdefault('maxnum', new_maxnum)
                break
            new_num = input('new_num: ')
            if new_num == 'I':
                pass
            else:
                operate_dict.setdefault('num', new_num)
                break
            new_id = input('new_id: ')
            if new_id == 'I':
                pass
            else:
                operate_dict.setdefault('id', new_id)
                break
            new_x = input('new_x: ')
            if new_x == 'I':
                pass
            else:
                operate_dict.setdefault('x', new_x)
                break
            new_y = input('new_y: ')
            if new_y == 'I':
                pass
            else:
                operate_dict.setdefault('y', new_y)
                break
            new_z = input('new_z: ')
            if new_z == 'I':
                pass
            else:
                operate_dict.setdefault('z', new_z)
                break
            new_a = input('new_a: ')
            if new_a == 'I':
                pass
            else:
                operate_dict.setdefault('a', new_a)
                break
#        new_dict = {'new_pos': new_pos,'new_sort': new_sort,'new_lock': new_lock,'new_maxnum': new_maxnum,'new_num': new_num,'new_id': new_id,'new_x': new_x,'new_y': new_y,'new_z': new_z,'new_a': new_a}
        key_list,value_list = [],[]
        for key,value in operate_dict.items():
            key_list.append(key),value_list.append(value)
        print(cond)
        cursor.execute('update %s set %s = %s where %s'%(sql_oname[0],key,value,cond[0]))
        print('update %s set %s = %s where %s'%(sql_oname[0],key,value,cond[0]))
        datas = cursor.fetchall()
        print(datas)
        cursor.close()
        conn.commit()
        conn.close()



if __name__=='__main__':
    try:
#        sql_operation(args.use,args.position,args.sort,args.lock,args.maxnum,args.number,args.id,args.Xposition,args.Yposition,args.Zposition,args.Cposition)
        sql_operation(args.use,[args.position,args.sort,args.lock,args.maxnum,args.number,args.id,args.Xposition,args.Yposition,args.Zposition,args.Cposition])
        print('try working')
    except sqlite3.OperationalError as e:
        print('Error info: ',e)
        pos = input('position: ')
        maxnum = input('maxnumber: ')
        num = input('number: ')
        id = input('ID: ')
        lock = input('lock: ')
        sort = input('sort: ')
        x = input('x: ')
        y = input('y: ')
        z = input('z: ')
        a = input('a: ')
        sql_operation(args.use,[pos,sort,lock,maxnum,num,id,x,y,z,a])
        print('except working')
