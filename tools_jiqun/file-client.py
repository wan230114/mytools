# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-06-23 00:27:04
# @Last Modified by:   11701
# @Last Modified time: 2019-07-09 08:42:00

from socket import *
import sys
import time
import getpass
import json
import struct


def getsize(size):
    # D = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    D = {0: 'b', 1: 'K', 2: 'M'}
    for x in D:
        if int(size) < 1024**(x + 1):
            hsize = str('%.3f' % (int(size) / 1024**x)) + D[x]
            return hsize


def myrecv_size(s, len_s):
    '''处理tcp的粘包问题'''
    #print('01start', len_s)
    L = []
    all_size = 0
    while all_size < len_s:
        size = len_s - all_size
        #print('will-->', size)
        msg = s.recv(size)
        if not msg:
            # time.sleep(1)
            break
        all_size += len(msg)
        L.append(msg)
    #print('\n---------------\n', b''.join(L), '\n------------\n')
    if all_size == len_s:
        # print('geted', all_size, len_s)
        pass
    else:
        print('ERROgetlen', all_size, len_s)
        sys.exit(1)
    return b''.join(L)


def mysend(s, header_dic, msg):
    header_json = json.dumps(header_dic)
    header_bytes = header_json.encode('utf-8')
    header_size = len(header_bytes)
    # 2、先发送报头的长度
    s.send(struct.pack('i', header_size))
    # print(len(struct.pack('i', header_size)),
    #       struct.pack('i', header_size))
    # 3、发送报头
    s.send(header_bytes)
    # print(len(header_bytes), header_bytes)
    # 4、发送真实的数据
    s.send(msg)
    # print(len(msg))
    # print('------end-------')
    # print(msg.decode('utf-8'))


def do_recv(client, ADDR, url, foname=None):
    client.send(('[send-url]%s[%s]' % (url, getpass.getuser())).encode())
    print(time.strftime("%Y-%m-%d %H:%M:%S, Content Success",
                        time.localtime()))
    if not foname:
        foname = url.split('/')[-1]
    with open(foname, 'wb') as fo:
        print('正在排队...')
        msg = myrecv_size(client, 7)
        if msg == b'[start]':
            print('排队结束, 下载中...')
        else:
            print(msg)
            print('ConnectionError: [start]single not correct')
            sys.exit(1)
        # len_s_speed = 0
        # size = 1024
        t0 = time.time()
        ll = myrecv_size(client, 4)
        header_size = struct.unpack('i', ll)[0]
        header_json = myrecv_size(client, header_size).decode('utf-8')
        header_dic = json.loads(header_json)
        total_size = header_dic['total_size']
        print('\n[文件总大小:', total_size, getsize(total_size), ']')
        n = 0
        all_size = 0
        while True:
            # t00 = time.time()
            # msg, addr2 = s.recvfrom(size)
            # msg = s.recv(size)
            # if not msg:
            #     break
            # elif msg == (b'[Download Failed]'):
            #     # print(s.recv(size))
            #     break
            # else:
            #     fo.write(msg)
            #     # print('WARNING.连接故障...')
            # 1、接收报文头的长度
            # n += 1
            # if n == 2:
            #     break
            # print('\n------------')
            ll = myrecv_size(client, 4)
            if ll == b'[ok]':
                stime = time.time() - t0
                hsize = getsize(all_size)
                print('\n[下载总大小:', total_size, getsize(total_size), ']')
                print('\n下载完毕',
                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                      '\n耗时%.3fs' % (stime),
                      '平均速度: %.3f%s/s' %
                      (float(hsize[:-1]) / stime, hsize[-1]),
                      sep='\n')
                break
            elif ll == b'[FL]':
                print('下载失败，已下载 %s / %s' % (all_size, total_size))
                break
            header_size = struct.unpack('i', ll)[0]
            # 2、接收报文
            header_json = myrecv_size(client, header_size).decode('utf-8')
            # 3、解析报文
            header_dic = json.loads(header_json)
            # 4、获取真实数据的长度
            total_size = header_dic['size']
            all_size += total_size
            # print('03:', total_size, type(total_size))
            # 5、获取数据
            fo.write(myrecv_size(client, total_size))
            # sys.exit()
            if all_size // (50 * 1024**3) > n:
                print('\r已下载%s' % getsize(all_size), end='\n')
                n = all_size // (50 * 1024**3)
            else:
                print('已下载%s' % getsize(all_size), end='\r')
        # if msg.startswith(b'[end]1234567'):
        #     if int(msg[12:-1]) == n:
        #     else:
        #         print('Warning: 下载的文件字节数可能有问题')
        # else:
        #     print("下载失败.", msg.decode())
        # s.send(b'[end-ok]')
        # s_speed = "%.03fM/s" % (size / 1024**3 / (time.time() - t00))
        # print(s_speed+" "*(10 - len(s_speed)), end="\r")
        # print(msg.decode().strip())


# 创建套接字，创建父子进程，登录
def fmain(IP, port, url, foname=None):
    HOST = IP
    PORT = int(port)
    ADDR = (HOST, PORT)
    # 1) 创建套接字
    # tcp
    s = socket()  # tcp套接字创建,默认参数即可
    # udp
    # s = socket(AF_INET, SOCK_DGRAM)

    # 2) 连接客户端，仅tcp需要
    setdefaulttimeout(10)  # 设置超时时间
    time = 3
    for i in range(time):
        try:
            s.connect(ADDR)
            # msg = s.recv(1024).decode()
            # if msg:
            # print(msg + '正在使用, 排队中...')
            break
        except (ConnectionRefusedError, timeout):
            print('Warning: Connect Failed. An error has occurred on the server. Please contact the server administrator.')
            raise
    # 设置缓冲区
    s.setsockopt(SOL_SOCKET, SO_RCVBUF, 0)

    # 3) 传输数据
    do_recv(s, ADDR, url, foname)
    # s.close()


def main():
    # sys.argv = ['', '144.34.199.131', '8080', 'send']
    # sys.argv = ['', '144.34.179.130', '8080', 'recv']
    # sys.argv = ['', '127.0.0.1', '8080', 'recv']
    # fmain('118.89.194.65', '8080', sys.argv[1])
    try:
        foname = sys.argv[2]
    except Exception:
        foname = None
    fmain('144.34.179.247', '8080', sys.argv[1], foname)


if __name__ == "__main__":
    main()


'''
from socket import *
IP, port = '144.34.179.247', '8080'
PORT = int(port)
ADDR = (HOST, PORT)
HOST = IP
ADDR = (HOST, PORT)
s = socket()
s.connect(ADDR)
s.send('[send-url]http://144.34.179.247:8999/frpc.ini[chenjun]'.encode())

'''
