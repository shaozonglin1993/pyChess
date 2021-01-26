
from tkinter import *
import socket               # 导入 socket 模块
import asyncio
import time
import sys
import threading
import json, types,string
from struct import *
from ctypes import *

'''
#加载库文件
lib = CDLL('./hello.so')
func = lib.test
func.restype = c_int
print(func(3,100))
'''
g_qipan = [None]*50
g_count = 0

'''
class Ctest(Structure):
    _fields_ = [('n0', c_byte),
                ('n1', c_byte),
                ('n2', c_byte),
                ('x', c_int), ('y', c_int),
                 ]
func = lib.test1
func.restype = c_int

b = bytes('好', 'utf8')

print(b)
print(func(byref(Ctest(n0 = b[0],n1 = b[1],n2 = b[2],x=100, y=200))))

'''

def circle(canvas, x, y, r, color=None):
    id = canvas.create_oval(x-r, y-r, x+r, y+r, fill = color)
    return id


class 	Cpixel:
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
        self.last_color = "gray"
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


    #判断两点是否在一条直线上
    def on_same_line(self, point1, point2):
        if (point1.x == point2.x and point1.y != point2.y) or (point1.y == point2.y and point1.x != point2.x):
            return 1
        else:
            return 0
    #遍历棋子列表，查看是否有棋子位于两点之间的线上
    def no_qizi_on_line(self, point1, point2):
        if self.on_same_line(point1, point2) == 0:
            return 0
        for item in self.qizilist:
            #如果是Y方向直线
            if item.is_alive() and item.point.x == point1.x and item.point.x == point2.x and item.point.y != point1.y and item.point.y != point2.y:
                if (item.point.y > point1.y and item.point.y > point2.y) or (item.point.y < point1.y and item.point.y < point2.y):
                    continue
                else:
                    return 0
            #如果是X方向直线
            if item.is_alive() and item.point.y == point1.y and item.point.y == point2.y and item.point.x != point1.x and item.point.x != point2.x:
                if (item.point.x > point1.x and item.point.x > point2.x) or (item.point.x < point1.x and item.point.x < point2.x):
                    continue
                else:
                    return 0
        return 1
    #判断两点是否为日子形
    def on_rizi_line(self, point1, point2):
        # X坐标差1，y坐标差2
        if (abs(point1.x - point2.x) == 1 and abs(point1.y-point2.y) == 2):
            return 1
        # X坐标差2，y坐标差1
        if (abs(point1.x - point2.x) == 2 and abs(point1.y - point2.y) == 1):
            return 1
        return 0;
    #遍历棋子列表，查看是否有棋子位于日子别腿点
    def no_qizi_on_rizi(self, point1, point2):
        if self.on_rizi_line(point1, point2) == 0:
            return 0
        #马可以走8个方向，每个方向对应一个别子坐标
        dic = {(1,-2):Cpoint(point1.x, point1.y-1),
               (2,-1):Cpoint(point1.x+1, point1.y),
               (2,1): Cpoint(point1.x + 1, point1.y),
               (1,2): Cpoint(point1.x, point1.y+1),
               (-1,2):Cpoint(point1.x, point1.y+1),
               (-2,1):Cpoint(point1.x - 1, point1.y),
               (-2,-1):Cpoint(point1.x - 1, point1.y),
               (-1,-2):Cpoint(point1.x, point1.y-1)
               }
        x_difference = point2.x - point1.x
        y_difference = point2.y - point1.y
        key = (x_difference, y_difference)
        bie_point =  dic[key]
        for item in self.qizilist:
            #如果是Y方向直线
            if item.point.x == bie_point.x and item.point.y == bie_point.y:
                print("get bie point")
                return 0
        print("no bie point")
        return 1

    #判断两点是否为田字形
    def on_tianzi_line(self, point1, point2):
        # X坐标差2，y坐标差2
        if (abs(point1.x - point2.x) == 2 and abs(point1.y-point2.y) == 2):
            return 1

        return 0;
    #遍历棋子列表，查看是否有棋子位于田字路径上
    def no_qizi_on_tianzi(self, point1, point2):
        if self.on_tianzi_line(point1, point2) == 0:
            return 0
        #马可以走4个方向，每个个方向对应一个别子坐标
        dic = {(2,2):Cpoint(point1.x+1, point1.y+1),
               (-2,2):Cpoint(point1.x-1, point1.y+1),
               (2,-2): Cpoint(point1.x + 1, point1.y-1),
               (-2,-2): Cpoint(point1.x-1, point1.y-1)
               }
        x_difference = point2.x - point1.x
        y_difference = point2.y - point1.y
        key = (x_difference, y_difference)
        bie_point =  dic[key]
        for item in self.qizilist:
            #如果是Y方向直线
            if item.point.x == bie_point.x and item.point.y == bie_point.y:
                print("get bie point")
                return 0
        print("no bie point")
        return 1


    # 判断两点是否为口字形 且point2 必须不能出宫
    def on_kouzi_line(self, point1, point2):

        if self.m_current_player == 'red':
            if point2.x < 3 or point2.x > 5 or point2.y < 0 or point2.y > 2:
                return 0
        if self.m_current_player == 'green':
            if point2.x < 3 or point2.x > 5 or point2.y > 9 or point2.y < 7:
                return 0
        # X坐标差1，y坐标差1
        if (abs(point1.x - point2.x) == 1 and abs(point1.y - point2.y) == 1):
            return 1

        return 0

    # 判断两点是否为一字形 且point2 必须不能出宫
    def on_yizi_line(self, point1, point2):

        if self.m_current_player == 'red':
            if point2.x < 3 or point2.x > 5 or point2.y < 0 or point2.y > 2:
                return 0
        if self.m_current_player == 'green':
            if point2.x < 3 or point2.x > 5 or point2.y > 9 or point2.y < 7:
                return 0
        # X坐标差1，y坐标差1
        if (abs(point1.x - point2.x) == 1 and point1.y == point2.y) or (point1.x == point2.x and abs(point1.y - point2.y) == 1):
            return 1

        return 0

    # 判断两点是否为一字形 且point2 只能向前
    def on_bingzi_line(self, point1, point2):
        if self.m_current_player == 'red':
            if point2.y < point1.y or (point1.y < 5 and point1.x != point2.x):
                return 0
        if self.m_current_player == 'green':
            if point2.y > point1.y or (point1.y >=  5 and point1.x != point2.x):
                return 0
        # X坐标差1，y坐标差1
        if (abs(point1.x - point2.x) == 1 and point1.y == point2.y) or (point1.x == point2.x and abs(point1.y - point2.y) == 1):
            return 1

    def one_qizi_on_line(self, point1, point2):
        qizi_count = 0
        if self.on_same_line(point1, point2) == 0:
            return 0
        for item in self.qizilist:
            # 如果是Y方向直线
            if item.is_alive() and item.point.x == point1.x and item.point.x == point2.x and item.point.y != point1.y and item.point.y != point2.y:
                if (item.point.y > point1.y and item.point.y > point2.y) or (
                        item.point.y < point1.y and item.point.y < point2.y):
                    continue
                else:
                    qizi_count = qizi_count+1
            # 如果是X方向直线
            if item.is_alive() and item.point.y == point1.y and item.point.y == point2.y and item.point.x != point1.x and item.point.x != point2.x:
                if (item.point.x > point1.x and item.point.x > point2.x) or (
                        item.point.x < point1.x and item.point.x < point2.x):
                    continue
                else:
                    qizi_count = qizi_count + 1
        if qizi_count == 1:
            return 1

        return 0

    def qizi_on_point(self, point):
        for item in self.qizilist:
            if item.is_alive():
                if item.point.x == point.x and item.point.y == point.y:
                    return item
        return None

    def go(self, qizi, point):
        #point是否位于棋盘线交叉点，是则返回交叉点，否则返回NONE
        focus_point = point
        if focus_point == None:
            return 0

        if qizi.str == "車":
            #車走直线，所以判断两点是否在同一条直线
            if self.on_same_line(qizi.point, focus_point):
                #車行走的路径中不能有其他棋子
                if self.no_qizi_on_line(qizi.point, focus_point):
                    chizi = self.qizi_on_point(focus_point)
                    if chizi != None:
                        if qizi.color != chizi.color:
                            chizi.dead()
                        else:
                            return 0
                    qizi.set_point(focus_point)
                    return 1
            return 0

        if qizi.str == "马":
            #马走日子，且不能有别马子
            if self.on_rizi_line(qizi.point, focus_point):
                #马走日子不能有别子
                if self.no_qizi_on_rizi(qizi.point, focus_point):
                    chizi = self.qizi_on_point(focus_point)
                    if chizi != None:
                        if qizi.color != chizi.color:
                            chizi.dead()
                        else:
                            return 0
                    qizi.set_point(focus_point)
                    return 1

        if qizi.str == "象" or qizi.str == "相":
            #象走田字，且不能路径上不能有其它子
            if self.on_tianzi_line(qizi.point, focus_point):
                if self.no_qizi_on_tianzi(qizi.point, focus_point):
                    chizi = self.qizi_on_point(focus_point)
                    if chizi != None:
                        if qizi.color != chizi.color:
                            chizi.dead()
                        else:
                            return 0
                    qizi.set_point(focus_point)
                    return 1
        if qizi.str == "士":
            #士走口字
            if self.on_kouzi_line(qizi.point, focus_point):
                chizi = self.qizi_on_point(focus_point)
                if chizi != None:
                    if qizi.color != chizi.color:
                        chizi.dead()
                    else:
                        return 0
                qizi.set_point(focus_point)
                return 1

        if qizi.str == "将" or qizi.str == "帅":
            #将走一字
            if self.on_yizi_line(qizi.point, focus_point):
                chizi = self.qizi_on_point(focus_point)
                if chizi != None:
                    if qizi.color != chizi.color:
                        chizi.dead()
                    else:
                        return 0
                qizi.set_point(focus_point)
                return 1

        if qizi.str == "兵" or qizi.str == "卒":
            #兵走一字 只向前
            if self.on_bingzi_line(qizi.point, focus_point):
                chizi = self.qizi_on_point(focus_point)
                if chizi != None:
                    if qizi.color != chizi.color:
                        chizi.dead()
                    else:
                        return 0
                qizi.set_point(focus_point)
                return 1

        if qizi.str == "炮":
            #炮走直线，所以判断两点是否在同一条直线,且路径上必须只能有一个棋子
            if self.on_same_line(qizi.point, focus_point):
                #車行走的路径中不能有其他棋子
                chizi = self.qizi_on_point(focus_point)
                if chizi != None:
                    if self.one_qizi_on_line(qizi.point, focus_point):
                        if qizi.color != chizi.color:
                            chizi.dead()
                            qizi.set_point(focus_point)
                            return 1
                else:
                    if self.no_qizi_on_line(qizi.point, focus_point):
                        qizi.set_point(focus_point)
                        return 1
            return 0

        return 0

    def check_win(self):
        red = 0;
        green = 0;
        for item in self.qizilist:
            if item.str == "帅" and item.is_alive():
                red = 1
            if item.str == "将" and item.is_alive():
                green = 1
        if red == 0:
            self.m_master.create_text(self.m_start_piexl.x + self.m_gap*4, self.m_start_piexl.y + self.m_gap*10, text="绿方赢")
            self.m_over = 1
        if green == 0:
            self.m_master.create_text(self.m_start_piexl.x + self.m_gap * 4, self.m_start_piexl.y + self.m_gap * 10, text="红方赢")
            self.m_over = 1


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
                item.paint(self.m_master, start, gap)

    def send_qizi_info(self):
        test_count = 0
        for item in self.qizilist:
            msg = [{'name':item.str, 'color':item.color, 'x':item.point.x, 'y':item.point.y, 'focus':item.focus, 'alive':item.alive}]
            jmsg = json.dumps(msg)
            jmsg_len  = len(jmsg)
            pack_msg = pack("l", jmsg_len)
            self.sock.send(pack_msg)
            self.sock.send(bytes(jmsg, 'utf-8'))
            print("send:", item.str, " x:", item.point.x, " y:", item.point.y)


    def get_point(self, event, piexl = 0, witch = 'red'):
        if self.m_over == 1  or self.m_current_player != witch:
            return None
        x, y = event.x, event.y
        if piexl == 0:
            #获取点对应的棋盘交叉点
            focus_point = self.pixel_to_point(Cpixel(x, y))
        else:
            focus_point = Cpoint(x, y)

        if focus_point != None:
            #查找改点是否落在棋子上
            qizi = self.qizi_on_point(focus_point)
            #如果还没有选定棋子
            if self.m_choose_qizi == None:
                if qizi != None and qizi.color == self.m_current_player:
                    self.m_choose_qizi = qizi
                    self.m_choose_qizi.set_focus()
                    self.paint()
            #如果已经选定过棋子
            else:
                #本次新点击的棋子也属于本方，则切换焦点到新棋子上
                if qizi != None and qizi.color == self.m_current_player:
                    self.m_choose_qizi.clear_focus()
                    self.m_choose_qizi = qizi
                    self.m_choose_qizi.set_focus()
                    self.paint()
                #走棋
                else:
                    ret = self.go(self.m_choose_qizi, focus_point)
                    if ret == 1:
                        self.m_choose_qizi.clear_focus()
                        self.m_choose_qizi = None
                        self.paint()
                        self.player_switch()
        self.check_win()
        self.send_qizi_info()
        print(x, y)

    def player_switch(self):
        if self.m_current_player == 'red':
            self.m_current_player = 'green'
        else:
            self.m_current_player = 'red'


def net_rec(i, sock):
    while True:
        data = sock.recv(2)
        print(len(data))
        if not data:
            continue
        g_qipan[i].get_point(Cpoint(data[0], data[1]), piexl = 1, witch = 'green')


def task_func(c, addr, i):
    global g_qipan

    print('in task_func')
    print('连接地址：', addr)
    c.send(bytes('欢迎链接！', encoding='utf-8'))

    frame = Tk()
    canvas_width = 800
    canvas_height = 600
    master = Canvas(frame,
                      width=canvas_width,
                      height=canvas_height)

    master.pack()

    start_pixel = Cpixel(150, 30)
    g_qipan[i] = Cqipan(start_pixel, 50, master, c, 'red')

    g_qipan[i].paint()

    master.bind("<Button-1>", g_qipan[i].get_point)

    thread = threading.Thread(target=net_rec, args=(i, c, ))
    thread.start()

    frame.mainloop()

    return 'the result'


s = socket.socket()  # 创建 socket 对象
host = socket.gethostname()  # 获取本地主机名
port = 12345  # 设置端口
s.bind((host, port))  # 绑定端口
print(host)

s.listen(5)  # 等待客户端连接

print("waitting for connection...")
while True:
    c, addr = s.accept()  # 建立客户端连接。
	
    thread = threading.Thread(target=task_func, args=(c, addr,g_count, ))
    thread.start()
    g_count += 1













