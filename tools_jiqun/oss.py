# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  1170101471@qq.com
# @Date:   2018-10-21 20:00:14
# @Last Modified by:   JUN
# @Last Modified time: 2019-06-18 19:41:53

import os
import sys
import getpass


shelp = '''集群任务互传工具ossutil:
使用说明: 
    python oss.py  fu   file1  path/
    python oss.py  fd   path/  path2/
    python oss.py  lsu [file1]
    python oss.py  lsd [file1]
    python oss.py  rmu [file1]
    python oss.py  rmd [file1]
    命令助记：命令中f含义是file，u含义是上传，d含义是下载

设置.bashrc快捷命令:
    天津:  alias oss="python /ifs/TJPROJ3/Plant/chenjun/mytools/tools_jiqun/oss.py"
    南京:  alias oss="python /NJPROJ2/Plant/chenjun/mytools/tools_jiqun/oss.py"

原理：
    互通云有4个云存储，分别为：天津u、天津d、南京u、南京d。(u:up, d:down)
     1、在天津集群运行 fu 将本地文件上传至 天津u, 随后被自动同步至 南京d, 运行lsu确认上传完成，
	    再去南京集群运行lsd查看确认文件传输完成，运行 fd 即可下载
     2、在南京集群运行 fu 将本地文件上传至 南京u, 随后被自动同步至 天津d, 运行lsu确认上传完成，
	    再去天津集群运行lsd查看确认文件传输完成，运行 fd 即可下载

示例: 南京u-->天津d
    1) 上传：将文件(夹)上传至南京u ，南京u会自动同步到 天津d
            南京客户端: oss fu file(或dir/) dict1/
    2) 查看：查看南京u、天津d（两者应该相同，否则请等待后台传输完毕(数据量大有延时)）
            南京客户端: oss lsu
            天津客户端: oss lsd
    3) 下载：从天津d下载
        1.下载所有文件到当前文件夹
            天津客户端: oss fd
        2.下载指定文件(夹)到当前文件夹
            天津客户端: oss fd dict1/ ./
    4) 删除：清理云端数据（转移完毕去上传端 南京u 删除数据）
        1.删除所有的上传数据
            南京客户端: oss rmu
        2.删除指定文件(夹)
            南京客户端: oss rmu dict1/
      （一般来说`oss rmd`不会用到，原则是在上传端去删除，这样删除操作才会同步至另一个中心，若在下载端rmd则会需要在上传端去再删除1次）'''


def jgq():
    if os.system('ls /ifs/TJPROJ3/Plant/chenjun/mytools &>/dev/null'):
        return '-n'
    else:
        return '-t'


def jq(Largv):
    print("Input args:", *Largv[1:])
    if ('--help' in Largv) or ('-h' in Largv):
        print(shelp)
        sys.exit()
    try:
        # q = Largv[1]  # t天津，n南京
        mode = Largv[1]
        try:
            file1 = Largv[2]
            try:
                file2 = Largv[3]
            except IndexError:
                file2 = ''
        except IndexError:
            file1 = ''
            file2 = ''
        q = jgq()
        if q == '-t':
            Dargv = {'softpath': '/ifs/TJPROJ3/Plant/chenjun/mytools/other',
                     'osspath': 'tj',
                     'op_e': 'oss-cn-beijing-internal.aliyuncs.com'}
        elif q == '-n':
            Dargv = {'softpath': '/NJPROJ2/Plant/chenjun/mytools/other',
                     'osspath': 'nj',
                     'op_e': 'oss-cn-hangzhou-internal.aliyuncs.com'}
        Dargv.update({'file1': file1, 'file2': file2, 'whoami': getpass.getuser()})

        def RUNs(s, mod=1):
            if mod:
                print('CMD runing: %s' % s)
                os.system(s)
            else:
                foname = 'do_oss.sh'
                s_input = input(
                    'CMD: %s\n是否直接运行？如果否，则将命令写入文件%s\n输入选择(回车-->Y，任意字符-->N)：' % (s, foname))
                while os.path.exists(foname):
                    s_input2 = input('检测到输入文件%s已存在，请重新输入脚本名(直接回车将进行覆盖)：' % foname)
                    if s_input2:
                        foname = s_input2
                    else:
                        break
                if not s_input:
                    RUNs(s)
                else:
                    with open(foname, 'w') as fo:
                        fo.write('%s\n' % s)

        if mode == 'fu':
            # 天津上传
            s = '%(softpath)s/ossutil cp -r %(file1)s oss://novo-%(osspath)s-upload/novo-plant/%(whoami)s/%(file2)s -e %(op_e)s -i LTAIqS6yZi9YY9IQ -k gthbZClPZPQSa8S6b53m5X62edTiyH' % Dargv
            RUNs(s, 0)
        elif mode == 'fd':
            # 天津下载
            if not Dargv['file2']:
                print('检测到没有输入下载目录，已纠正为当前目录“./”')
                Dargv['file2'] = './'
            s = '%(softpath)s/ossutil cp -r oss://novo-%(osspath)s-down/novo-plant/%(whoami)s/%(file1)s %(file2)s -e %(op_e)s -i LTAIqS6yZi9YY9IQ -k gthbZClPZPQSa8S6b53m5X62edTiyH' % Dargv
            print(s)
            RUNs(s, 0)
        elif mode == 'lsu':
            # 天津查看天津上传的
            s = '%(softpath)s/ossutil ls oss://novo-%(osspath)s-upload/novo-plant/%(whoami)s/%(file1)s -e %(op_e)s -i LTAIqS6yZi9YY9IQ -k gthbZClPZPQSa8S6b53m5X62edTiyH' % Dargv
            RUNs(s)
        elif mode == 'lsd':
            # 天津查看南京上传的
            s = '%(softpath)s/ossutil ls oss://novo-%(osspath)s-down/novo-plant/%(whoami)s/%(file1)s -e %(op_e)s -i LTAIqS6yZi9YY9IQ -k gthbZClPZPQSa8S6b53m5X62edTiyH' % Dargv
            RUNs(s)
        elif mode == 'rmu':
            # 天津删除天津上传的
            s = '%(softpath)s/ossutil rm -r oss://novo-%(osspath)s-upload/novo-plant/%(whoami)s/%(file1)s -e %(op_e)s -i LTAIqS6yZi9YY9IQ -k gthbZClPZPQSa8S6b53m5X62edTiyH' % Dargv
            RUNs(s)
        elif mode == 'rmd':
            # 天津删除南京上传的
            s = '%(softpath)s/ossutil rm -r oss://novo-%(osspath)s-down/novo-plant/%(whoami)s/%(file1)s -e %(op_e)s -i LTAIqS6yZi9YY9IQ -k gthbZClPZPQSa8S6b53m5X62edTiyH' % Dargv
            RUNs(s)
    except IndexError:
        print(shelp)


def main():
    jq(sys.argv)


if __name__ == "__main__":
    main()
