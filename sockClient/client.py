#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：client.py

import socket               # 导入 socket 模块

from tkinter import *
import socket               # 导入 socket 模块
import asyncio
import time
import sys
from struct import *
import json, types,string
import threading

def circle(canvas, x, y, r, color=None):
    id = canvas.create_oval(x-r, y-r, x+r, y+r, fill = color)
    return id



class Cpixel:
    def __init__(self, m, n):
        self.x = m
        self.y = n

class Cpoint:
    def __init__(self, m, n):
        self.x = m
        self.y = n


class Cqizi:
    def __init__(self, point = None, color = "red", str = "", alive = 1):
        self.point = point
        self.str = str
        self.color = color
        self.focus = 0
        self.focus_color = "yellow"
        self.alive = alive
    def set_point(self, point):
        self.point = point
    def set_focus(self):
        self.focus = 1
    def clear_focus(self):
        self.focus = 0
    def dead(self):
        self.alive = 0
    def is_alive(self):
        return self.alive

    #start为棋盘开始的像素点， gap为棋盘相邻交叉点距离
    def paint(self, master, start, gap):
        r = gap*3/8
        circle(master, start.x + self.point.x * gap, start.y + self.point.y * gap, r, self.color)
        if self.focus == 1:
            circle(master, start.x + self.point.x * gap, start.y + self.point.y * gap, gap*9/16, self.focus_color)
        master.create_text(start.x + self.point.x * gap, start.y + self.point.y * gap, text=self.str)



class Cqipan:
    #start_piexl为棋盘开始的像素点， gap为棋盘相邻交叉点距离
    def __init__(self, start_piexl, gap, master, sock, color):
        self.m_over = 0
        self.m_master = master
        self.m_current_player = 'red'
        self.m_choose_qizi = None
        self.m_start_piexl = start_piexl
        self.m_gap = gap
        self.sock = sock
        self.m_color = color
        self.m_yline_count = 9
        self.m_xline_count = 10
        self.qizilist = []
        self.pointlist = []
#生成所有棋子，并初始化其坐标
        x = 0
        y = 0

        self.qizilist.append(Cqizi(Cpoint(x,y), "red",  "車"))
        x += 1
        self.qizilist.append(Cqizi(Cpoint(x,y), "red",  "马"))
        x += 1
        self.qizilist.append(Cqizi(Cpoint(x,y), "red",  "象"))
        x += 1
        self.qizilist.append(Cqizi(Cpoint(x,y), "red",  "士"))
        x += 1
        self.qizilist.append(Cqizi(Cpoint(x,y), "red",  "帅"))
        x += 1
        self.qizilist.append(Cqizi(Cpoint(x,y), "red",  "士"))
        x += 1
        self.qizilist.append(Cqizi(Cpoint(x,y), "red",  "象"))
        x += 1
        self.qizilist.append(Cqizi(Cpoint(x,y), "red",  "马"))
        x += 1
        self.qizilist.append(Cqizi(Cpoint(x,y), "red",  "車"))

        x = 0
        y = 3
        self.qizilist.append(Cqizi(Cpoint(x,y), "red",  "兵"))
        x += 2
        self.qizilist.append(Cqizi(Cpoint(x, y), "red", "兵"))
        x += 2
        self.qizilist.append(Cqizi(Cpoint(x, y), "red", "兵"))
        x += 2
        self.qizilist.append(Cqizi(Cpoint(x, y), "red", "兵"))
        x += 2
        self.qizilist.append(Cqizi(Cpoint(x, y), "red", "兵"))

        x = 1
        y = 2
        self.qizilist.append(Cqizi(Cpoint(x, y), "red", "炮"))
        x += 6
        self.qizilist.append(Cqizi(Cpoint(x, y), "red", "炮"))


        x = 0
        y = self.m_xline_count - 1

        self.qizilist.append(Cqizi(Cpoint(x,y), "green",  "車"))
        x += 1
        self.qizilist.append(Cqizi(Cpoint(x,y), "green",  "马"))
        x += 1
        self.qizilist.append(Cqizi(Cpoint(x,y), "green",  "相"))
        x += 1
        self.qizilist.append(Cqizi(Cpoint(x,y), "green",  "士"))
        x += 1
        self.qizilist.append(Cqizi(Cpoint(x,y), "green",  "将"))
        x += 1
        self.qizilist.append(Cqizi(Cpoint(x,y), "green",  "士"))
        x += 1
        self.qizilist.append(Cqizi(Cpoint(x,y), "green",  "相"))
        x += 1
        self.qizilist.append(Cqizi(Cpoint(x,y), "green",  "马"))
        x += 1
        self.qizilist.append(Cqizi(Cpoint(x,y), "green",  "車"))

        x = 0
        y = 6
        self.qizilist.append(Cqizi(Cpoint(x,y), "green",  "卒"))
        x += 2
        self.qizilist.append(Cqizi(Cpoint(x, y), "green", "卒"))
        x += 2
        self.qizilist.append(Cqizi(Cpoint(x, y), "green", "卒"))
        x += 2
        self.qizilist.append(Cqizi(Cpoint(x, y), "green", "卒"))
        x += 2
        self.qizilist.append(Cqizi(Cpoint(x, y), "green", "卒"))

        x = 1
        y = 7
        self.qizilist.append(Cqizi(Cpoint(x, y), "green", "炮"))
        x += 6
        self.qizilist.append(Cqizi(Cpoint(x, y), "green", "炮"))

    # 生成所有有效点
        x = 0
        y = 0
        for i in range(self.m_yline_count):
            for j in range(self.m_xline_count):
                self.pointlist.append(Cpoint(x+i, y+j))


    #像素点到棋盘焦点转换 pixel_start为棋盘开始像素点， pixel为要转换的像素点， gap为棋盘相邻两个交叉点距离
    def pixel_to_point(self, pixel):

        gap = self.m_gap
        x = self.m_start_piexl.x + gap * (self.m_yline_count-1)
        y = self.m_start_piexl.y + gap * (self.m_xline_count-1)
        end_piexl = Cpixel(x, y)

        r = gap*3/8

        if (pixel.x < (self.m_start_piexl.x - r) or pixel.x > (end_piexl.x + r) or pixel.y < (self.m_start_piexl.y - r) or pixel.y > (end_piexl.y + r)):
            return None

        pixel.x = pixel.x - self.m_start_piexl.x
        pixel.y = pixel.y - self.m_start_piexl.y

        for item in self.pointlist:
            if pixel.x <= (item.x*gap + r) and pixel.x >= (item.x*gap - r) and pixel.y <= (item.y*gap + r) and pixel.y > (item.y*gap - r):
                return item
        return None


    def paint(self):
        start = self.m_start_piexl
        gap = self.m_gap

        self.m_master.delete('all')
        for i in range(self.m_xline_count):
            self.m_master.create_line(start.x, (start.y + i*gap), (start.x + (self.m_yline_count-1)*gap), (start.y + i*gap), fill="#476042")

        for i in range(self.m_yline_count):
            self.m_master.create_line((start.x + i*gap), start.y, (start.x + i*gap), (start.y + (self.m_xline_count-1)*gap), fill="#476042")

        for item in self.qizilist:
            if item.is_alive():
                print("paint:", item.str, " x:", item.point.x, " y:", item.point.y)
                item.paint(self.m_master, start, gap)

    def get_point(self, event):
        point = self.pixel_to_point(Cpixel(event.x, event.y))
        if point != None:
            data = [point.x, point.y]
            self.sock.send(bytes(data))
            print(point.x, point.y)

    def player_switch(self):
        if self.m_current_player == 'red':
            self.m_current_player = 'green'
        else:
            self.m_current_player = 'red'

def net_recv(s, req_len):
    ret_data = b""
    rec_len = 0
    while True:
        data = s.recv(req_len)
        rec_len += len(data)
        ret_data += data
        if rec_len >= req_len:
            break
    return ret_data

def net_adapter(s, qipan):

    while True:
        for item in qipan.qizilist:
            data_len = unpack("l", net_recv(s, 8))
            print('data_len:', data_len)
            data = net_recv(s, data_len[0])
            qizi_info = json.loads(data.decode('utf-8'))

            item.str = qizi_info[0]['name']
            item.color = qizi_info[0]['color']
            item.alive = qizi_info[0]['alive']
            item.focus = qizi_info[0]['focus']
            print("name:", item.str, "aline:", item.alive)
            item.point.x = qizi_info[0]['x']
            item.point.y = qizi_info[0]['y']
        qipan.paint()



s = socket.socket()          # 创建 socket 对象
#host = socket.gethostname() # 获取本地主机名
host = "127.0.0.1"           # 获取本地主机名
port = 12345                 # 设置端口号

s.connect((host, port))
print (str(s.recv(1024),'utf-8'))


frame = Tk()
frame.title('client')
canvas_width = 800
canvas_height = 600
master = Canvas(frame,
                width=canvas_width,
                height=canvas_height)

master.pack()

start_pixel = Cpixel(150, 30)
qipan = Cqipan(start_pixel, 50, master, s, 'green')

qipan.paint()

master.bind("<Button-1>", qipan.get_point)

thread = threading.Thread(target=net_adapter, args=(s, qipan,))
thread.start()

frame.mainloop()

s.close()
