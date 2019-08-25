# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-09 12:05:31
# @Last Modified by:   JUN
# @Last Modified time: 2019-02-20 10:25:00
from socket import *
import os
import sys
import time
import traceback


def mkdir(mkpath):
    isExists = os.path.exists(mkpath)
    if not isExists:
        os.makedirs(mkpath)


def do_parent(s):
    while True:
        try:
            # print("\nWaiting for connect....")
            connfd, addr = s.accept()
            setdefaulttimeout(5)  #
            print("Connect from", addr)
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            msg = ''
            try:
                # msg, addr = s.recvfrom(1024)
                msg = connfd.recv(1024)
                msg = msg.decode()
            except timeout:
                print('已过5秒，未收到客户端信息')

            if msg == 'getlog':
                print('收到请求:' + msg)
                with open('sharedir/log', 'rb') as fi:
                    text = fi.read()
                connfd.send(text)
                print('发送成功')
            elif msg.startswith('[sendlog]'):
                mkdir('sharedir')
                with open('sharedir/log', 'w') as fo:
                    fo.write(msg.lstrip('[sendlog]'))
                print('写入成功')
                connfd.send('over'.encode())
                print('已发送确认信息:over')
            else:
                print('收到非指定信息：')
                print(msg.strip())
                text = 'Email: 1170101471@qq.com'
                connfd.send(text.encode())
                print('已发送：' + text)
            connfd.close()
            print('Connect closed\n')
            # time.sleep(10)
        except:
            print('额，遇到点问题，已重新开始\n错误信息是：')
            traceback.print_exc()
            print('')

# 创建套接字，创建链接，创建父子进程　功能函数调用


def main():
    # server address
    ADDR = ('0.0.0.0', 8080)

    # # 创建套接字　
    # s = socket(AF_INET, SOCK_DGRAM)
    # s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # 创建tcp套接字
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(ADDR)
    # 设置监听
    s.listen(5)

    do_parent(s)

    # # 创建父子进程，分别处理请求和发送管理员消息
    # pid = os.fork()

    # if pid < 0:
    #     sys.exit("创建进程失败")
    # elif pid == 0:
    #     # 执行子进程功能
    #     do_child(s, ADDR)
    # else:
    #     # 执行父进程功能
    #     do_parent(s, ADDR)

if __name__ == "__main__":
    main()
