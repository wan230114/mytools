# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  wan230114@qq.com
# @Date:   2018-11-15 21:33:02
# @Last Modified by:   JUN
# @Last Modified time: 2018-11-16 17:48:02

# 思路，
# 1 文件目录
# 1 文件名字变化，包括文件新增，文件名删除和修改，重命名功能可以通过MD5变化判断，但计算MD5太慢，因而看时间
# 2 文件内容变化
# os.path.getatime(path)  返回最近访问时间（浮点型秒数）
# os.path.getmtime(path)  返回最近文件修改时间
# os.path.getctime(path)  返回文件 path 创建时间
# os.path.getsize(path)   返回文件大小，如果文件不存在就返回错误


import os
import sys
import time
import hashlib


class jiankong:

    def __init__(self, mypath, mytime):
        self.mypath = mypath
        self.stime = int(mytime)
        self.D = {}
        self.D1 = {}  # 存储旧数据
        # 开始执行
        self.fo = open("./moniMENU.log", "w")
        try:
            self.fmain()
        except KeyboardInterrupt:
            self.__del__()

    def fmain(self):
        self.fprint('当前监控的目录路径是: %s/' % self.mypath)
        # 初始化第一次读取
        self.getlist()
        self.D1 = self.D
        while True:
            self.getlist()
            if self.D != self.D1:
                self.fprint(
                    '\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                self.fprint('检测到文件或目录发生变化')
                # print(self.D1)
                # print(self.D)
                self.compared(self.D1, self.D)
                #os.system('python /ifs/TJPROJ3/Plant/chenjun/mytools/sendmail.py 1170101471@qq.com "Changed!!! see!"')
                self.D1 = self.D
            time.sleep(self.stime)

    def getlist(self):
        obj_all = os.walk(self.mypath)
        self.D = dict()
        for path, Ldict, Lfile in obj_all:
            Dfile = dict()
            for file in Lfile:
                filetime = os.path.getmtime(path + '/' + file)
                Dfile[file] = filetime
            self.D[path] = list([Ldict, Dfile])

    def compared(self, D1, D2):
        '''输出变化的文件或目录'''
        s1, s2 = set(D1), set(D2)
        if s1 - s2:
            self.fprint('删除文件夹: \n%s' % '\n'.join(s1 - s2))
        if s2 - s1:
            self.fprint('新增文件夹: \n%s' % '\n'.join(s2 - s1))
        Scon = s1 & s2  # 看交集
        for d1 in Scon:
            if D1[d1] == D2[d1]:
                continue
            else:
                Dfile1 = D1[d1][1]
                Dfile2 = D2[d1][1]
                s1, s2 = set(Dfile1), set(Dfile2)
                ss1 = {x for x in (s1 - s2) if '.swap' not in x}
                ss2 = {x for x in (s2 - s1) if '.swap' not in x}
                if ss1:  # 【】有点难开发，因为需要把前面一开始输出的时间和提示信息也考虑进去，晚点研究吧。。。
                    self.fprint('删除文件: \n%s/%s' % (d1, '\n'.join(ss1)))
                if ss2:
                    self.fprint('新增文件: \n%s/%s' % (d1, '\n'.join(ss2)))
                Scon = s1 & s2  # 看交集
                for f1 in Scon:
                    if Dfile1[f1] == Dfile2[f1]:
                        continue
                    else:
                        self.fprint('文件被更新: \n%s/%s' % (d1, f1))
                        time_old = time.strftime(
                            "%Y-%m-%d %H:%M:%S", time.localtime(Dfile1[f1]))
                        time_new = time.strftime(
                            "%Y-%m-%d %H:%M:%S", time.localtime(Dfile2[f1]))
                        self.fprint('上次更新时间： %s\n本次更新时间：%s' %
                                    (time_old, time_new))
    # def getmd5(self,filepath):
    #     objmd5 = hashlib.md5()
    #     with open(filepath,'rb') as fi:
    #         data=fi.read()  # 若有大文件需求，此处可以进一步更改，直接读取会很消耗内存
    #         self.fprint(data)
    #         objmd5.update(data)
    #     return objmd5.hexdigest()

    def fprint(self, s):
        print(s)
        self.fo.write(s + '\n')
        self.fo.flush()

    def __del__(self):
        self.fo.close()
        # print('析构函数已调用')
        # sys.exit()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv = ['', './tmp', '5']
    mypath = sys.argv[1]
    mytime = sys.argv[2]
    jiankong(mypath, mytime)
