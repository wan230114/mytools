from socket import *
import sys
import os
import time


def mkdir(mkpath):
    isExists = os.path.exists(mkpath)
    if not isExists:
        os.makedirs(mkpath)


def do_recv(s):
    # s.sendto(msg.encode(), addr)
    s.send('getlog'.encode())
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # for i in range(10):
    # msg, addr = s.recvfrom(1024)
    msg = s.recv(1024)
    print('Received content.')
    # print(msg.decode().strip())

    with open('sharedir/log', 'wb') as fo:
        fo.write(msg)
    print('Written to file: sharedir/log\n')
    # else:
    #     print('读取服务器失败！')


def do_send(s):
    msg = open('sharedir/log').read()
    # msg = ''.join([str(x) for x in range(2000)])
    # msg = '''/TJNAS01/PAG/Plant/ 磁盘空间不足5T，剩余3.31836T\n/TJPROJ1/DENOVO/    磁盘空间不足5T，剩余2.08591T\n/ifs/TJPROJ3/Plant/ 磁盘空间不足5T，剩余1.21085T'''
    s.send(('[sendlog]' + msg).encode())
    # s.send((msg).encode())
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # print(msg)
    msg = s.recv(1024)
    if msg.decode() == 'over':
        print('Write to the server Success.\n')
    else:
        print('Write to server failed !!! \n\n')
        print(msg)


# 创建套接字，创建父子进程，登录


def main():
    # sys.argv = ['', '144.34.199.131', '8080', 'send']
    # sys.argv = ['', '144.34.179.130', '8080', 'send']
    sys.argv = ['', '144.34.179.130', '8080', 'recv']
    # sys.argv = ['', '127.0.0.1', '8080', 'send']
    # sys.argv = ['', '127.0.0.1', '8080', 'recv']
    if len(sys.argv) < 3:
        print("argv is error")
        return

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST, PORT)

    # s = socket(AF_INET, SOCK_DGRAM)

    # 创建套接字 tcp 默认参数即可
    s = socket()
    setdefaulttimeout(5)  # 设置超时时间
    time = 10
    mkdir('sharedir')
    for i in range(time):
        try:
            s.connect(ADDR)
            break
        except (ConnectionRefusedError, timeout):
            print('Warning: An error has occurred on the server. Please contact the server administrator.')
            with open('sharedir/log', 'wb') as fo:
                fo.write('Warning: An error has occurred on the server. Please contact the server administrator.'.encode('utf-8'))
            raise

    if sys.argv[3] == 'send':
        do_send(s)
    elif sys.argv[3] == 'recv':
        do_recv(s)

    s.close()

if __name__ == "__main__":
    main()
