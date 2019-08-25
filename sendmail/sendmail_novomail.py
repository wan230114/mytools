# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-10-21 20:00:14
# @Last Modified by:   JUN
# @Last Modified time: 2019-07-20 02:21:23

# 用于发送邮件文本和附件

import os
import sys
import smtplib
import re
import base64
import socket
import time
#from prettytable import PrettyTable
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# python3开发，考虑兼容解决python2里面的编码问题
if sys.version[0] == '2':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

def jg():
    if os.system('cd /ifs/TJPROJ3/'):
        s = 'nj'
    else:
        s = 'tj'
    return s


class Send:
    """send帮助文档:
    功能：
        发送文字或者附件于指定收件人邮箱

    send命令：
        python sendmail.py mailaddress [-c text1 text2 ...] [-f file1 file2 ...]
    参数说明：
        mailaddress   (必选)发送的收件人邮箱，多个收件人用英文逗号隔开
        -c text1 text2 ... (可选)邮件发送的正文的备注内容。
        -f file1 file2 ... (可选)邮件发送的附件。
    查看帮助文档：
        python sendmail.py [--help]

    快捷设置：
        alias send="python /ifs/TJPROJ3/Plant/chenjun/mytools/sendmail.py "
        alias send="python /NJPROJ2/Plant/chenjun/mytools/sendmail.py "

    注意事项：
        1.[-c text1 text2 ...]：发送文本时text1、text2、...之间默认用\\n连接，也可手动输入\\n。
        注意，涉及特殊字符时(如空格)尽量使用转义字符或将其用引号引起来。
        2.请将收件人: wan230114@126.com 加入白名单，否则可能被拦截导致无法正常接收
        3.发送邮件因为对接网络可能会有一定失败率，目前程序默认在失败时重新发送100次，每次间隔6秒

    命令示例：
        # 1)发送邮件给test@qq.com，发送内容“Ara1流程结束  \\n速速生成报告！”（空格需要引号引起来，或用\\转义）
        send test@qq.com -c "Ara1流程结束  \\n速速生成报告！"
        send test@qq.com -c Ara1流程结束\\ \\ \\n速速生成报告！
        # 2)发送邮件给test@qq.com，发送内容“项目生成报告完毕\\n请查收附件”，并同时发送附件1，附件2，附件3
        send test@qq.com -c 项目生成报告完毕 请查收附件 -f file1 file2 file3
        """

    def __init__(self, Largv):
        self.recv = ''  # 收件人
        self.text = ''  # 发送内容
        self.Lfile = []  # 发送附件名列表
        self.P_c = 0
        self.P_f = 0
        self.P_time = 100  # 发送失败重试的次数
        self.P_time2 = 0
        self.P_sleeptime = 6  # 发送失败重试的间隔时间（秒）

        self.__fargvs__(Largv)

    def __fargvs__(self, Largv):
        def HELPargv():
            print('您输入的参数是: ')
            print(tuple(Largv[1:]))
            # print('您输入的参数是: ' + ' '.join(Largv))
            print(self.__doc__)
            sys.exit()

        if len(Largv) == 1:
            print(self.__doc__)
            sys.exit()
        elif len(Largv) >= 2:
            if Largv[1] == '--help':
                print(self.__doc__)
                sys.exit()
            jg_argv = re.findall('.+@.+\..+', Largv[1])
            if not jg_argv:
                print("Error: 发送未完成，请输入正确的收件人邮箱地址")
                HELPargv()
            self.recv = Largv[1]
            if len(Largv) == 2:
                self.text += '无'
        text_add = ''
        iC, iF = 0, 0
        if {'-c', '-f'} <= set(Largv):
            iC = Largv.index('-c')
            iF = Largv.index('-f')
            self.P_c, self.P_f = 1, 1
        elif '-c' in Largv:
            iC = Largv.index('-c')
            iF = len(Largv)
            self.P_c = 1
        elif '-f' in Largv:
            iC = len(Largv)
            iF = Largv.index('-f')
            self.P_f = 1
        else:
            print('输入参数有误')
            HELPargv()
        if self.P_c == 1:
            if iF < iC:
                L_add = Largv[iC + 1:]
            else:
                L_add = Largv[iC + 1:iF]
            if not L_add:
                print('输入参数有误')
                HELPargv()
            text_add = '\n'.join(L_add)
            self.text += text_add
        if self.P_f == 1:
            if iF > iC:
                self.Lfile = Largv[iF + 1:]
            else:
                self.Lfile = Largv[iF + 1:iC]
            if not self.Lfile:
                print('输入参数有误')
                HELPargv()
            # 处理文件列表，看是否都存在
            Ltmp = []
            for fname in self.Lfile:
                try:
                    open(fname).close()
                    Ltmp.append(fname)
                except:
                    print('WARNING : 文件 %s 未找到，已跳过该附件发送' % fname)
                    continue
            self.Lfile = Ltmp

    def send(self):
        mailserver = "14.17.57.217"  # 邮箱服务器地址
        username_send = 'chenjun4663@novogene.com'  # 邮箱用户名
        password = 'Chenjun2049'  # 邮箱密码：需要使用授权码
        try:
            print("正在发送邮件给%s" % self.recv)

            # 1) 创建要发送的邮件正文及附件对象
            # related 使用邮件内嵌资源，可以把附件中的图片等附件嵌入到正文中
            msg = MIMEMultipart('related')

            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # -功能搁置，暂时无用。
            # 创建一个用于发送文本的MIMEText对象  # msg = MIMEText(self.text, 'plain', 'utf-8')  # 这是邮件内容
            # 将图片加入文本中
            # # 加入文本
            # msg_text = MIMEText(
            #     '<h1 style="text-algin:center">恭喜您查收到该邮件</h1>\
            #      <span style="color:red">详情如下：</span><br>\
            #      <img src="cid:myzg">',
            #     'html', 'utf-8')
            # msg.attach(msg_text)
            # msg_image = MIMEImage(open(mailfile, 'rb').read())  # 创建MIMEImage对象，读取图片作为imgdata的数据参数
            # msg_image.add_header('Content-ID', 'myzg')  # 指定图片文件的Content-ID
            # # 添加图片附件
            # msg.attach(msg_image)
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

            # 2) 将附件添加到邮件中
            for mailfile in self.Lfile:
                attach = MIMEText(open(mailfile, 'rb').read(), 'base64', 'utf-8')
                attach['Content-type'] = 'application/octet-stream'  # 指定当前文件格式类型
                # 处理发送的附件名的中文乱码情况
                mailfile = mailfile.split('/')[-1]
                new_filename = '=?utf-8?b?' + base64.b64encode(mailfile.encode()).decode() + '?='
                attach['Content-Disposition'] = 'attachment;filename="%s"' % new_filename
                # 把附件添加到msg中
                msg.attach(attach)

            # 添加邮件正文的内容（MIMEText第一个将成为正文，而再添加其他则会成为附件）
            # msg.attach(MIMEText(self.text, 'plain', 'utf-8'))
            msg.attach(MIMEText(self.text, 'html', 'utf-8'))

            # 3) 发送邮件
            # 设置必要请求头信息
            jq = jg()
            if jq == 'nj':
                msg['Subject'] = '【南京下机数据删除确认】'   # '这是邮件主题'
            elif jq == 'tj':
                msg['Subject'] = '【天津下机数据删除确认】'   # '这是邮件主题'
            msg['From'] = username_send  # 发件人
            msg['To'] = self.recv  # 收件人；[]里的三个是固定写法
            # 连接邮箱服务器，smtp的端口号是25。QQ邮箱的服务器和端口号smtp=smtplib.SMTP_SSL('smtp.qq.com',port=465)
            smtp = smtplib.SMTP(mailserver, timeout=10)
            # smtp = smtplib.SMTP(mailserver, port=25, timeout=10)
            smtp.login(username_send, password)  # 登录邮箱
            # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
            smtp.sendmail(username_send, self.recv.split(','), msg.as_string())
            smtp.quit()  # 发送完毕后退出smtp

            print('发送成功，通知邮件已发送至%s' % self.recv)
            print("邮件内容： ")
            print('[正文:]\n%s' % self.text)
            #Column1 = u"邮件内容： "
            #objContent = PrettyTable([Column1])
            #objContent.align[Column1] = u"l"
            #objContent.add_row([u'[正文:]\n%s' % self.text])
            if self.Lfile:
                print('\n[附件:]\n%s' % '\n'.join([x.split('/')[-1] for x in self.Lfile]))
                #objContent.add_row([u'\n[附件:]\n%s' % '\n'.join(
                #    [x.split('/')[-1] for x in self.Lfile])])
            elif self.P_f == 1:
                print('\n[附件:]\n%s' % '无')
                #objContent.add_row([u'\n[附件:]\n%s' % '无'])
            #print(objContent)
            print('\n')
        except socket.gaierror:
            print('Error: 发送未完成，请检查网络连接状况')
            time.sleep(self.P_sleeptime)
            self.P_time -= 1
            self.P_time2 += 1
            if self.P_time > 0:
                print('（重新发送中! 第%s次尝试）' % self.P_time2)
                self.send()

    def __add2image__(self, msg, path):
        """定义添加图片附件的函数: path 图片路径   imgid对应附件id，可以根据id嵌入正文"""
        msg_image = MIMEImage(open(path, 'rb').read())  # 创建MIMEImage对象，读取图片作为imgdata的数据参数
        msg_image.add_header('Content-ID', 'myzg')  # 指定图片文件的Content-ID
        # 加入文本
        msg_text = MIMEText(
            '<h1 style="text-algin:center">恭喜您查收到该邮件</h1><span style="color:red">详情如下：</span><br><img src="cid:myzg">', 'html', 'utf-8')
        msg.attach(msg_text)
        # 添加图片附件
        msg.attach(self.__add2image__('sendmail.png', 'myzg'))
        return msg


if __name__ == "__main__":
    Largv = sys.argv
    # Largv = ["", "chenjun4663@novogene.com,1170101471@qq.com", '-c',
    #          """hi,all:<br>&nbsp;&nbsp;以下项目涉及的下机文库即将上云并在本地删除。<br>&nbsp;&nbsp;若需要本地保留，请相关项目负责人两日内回复，我们将在下周二统一提交删除<br><br>下机信息路径:&nbsp;/NJPROJ2/Plant/chenjun/Admin/04.mapXiaji/auto/01.mapfile/lst.merge.tiqu<br>项目大小:&nbsp;1.606T<br>扫盘大小:&nbsp;3.333T<br>文库数量:&nbsp;368<br><table border="1" cellspacing="0" cellpadding="6" style="word-break: break-all;"><tr><th>#文库数量</th><th>大小(b/k/m/g/t)</th><th>大小(b)</th><th>信息负责人</th><th>运营</th><th>项目编号</th><th>项目名称</th></tr><tr><td>112</td><td>148.142G</td><td>159066417902</td><td>孙天琳</td><td>杨阳</td><td>X101SC19041163-Z01</td><td>上海市农业科学院130个白菜WGS-seq群体进化分析技术服务（委托）合同</td></tr><tr><td>58</td><td>104.056G</td><td>111729796354</td><td>周梦妍</td><td>王德芬</td><td>P101SC18010857-01</td><td>东北农业大学1个植物基因组图谱构建及分析技术服务（委托）合同</td></tr><tr><td>41</td><td>798.642G</td><td>857534901766</td><td>张莹钧</td><td>杨阳</td><td>X101SC19041655-Z01</td><td>茶叶所38个茶叶WGS-seq群体进化分析技术服务（委托）合同</td></tr><tr><td>40</td><td>363.144G</td><td>389923325376</td><td>高丹</td><td>薛宁宁</td><td>P101SC18041890-01</td><td>嵩草基因组与群体遗传学研究</td></tr><tr><td>39</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td></tr><tr><td>15</td><td>3.641G</td><td>3909615765</td><td>李祥孔</td><td>黄瑞君</td><td>P101SC17050491-01</td><td>武汉植物园150个海菜花RAD-seq群体进化分析技术服务（委托）合同</td></tr><tr><td>13</td><td>12.957G</td><td>13912516083</td><td>刘伟</td><td>杨阳</td><td>P101SC18091448-01</td><td>云南大学250个植物RAD-seq变异检测分析技术合作合同</td></tr></table>"""]
    # Largv = ["", "wan230114@126.com,1170101471@qq.com",
    #             "-c", "hahaha", "ang~\nxx项目已跑完，请速速查看",
    #             "-f", "./sendmail.png", "sendmail中文1.png"]
    # Largv = ["", "--help"]
    send = Send(Largv)
    send.send()

    ##########################################################################
    # 放置此处以后待探索云服务API：
    # https://dm.aliyuncs.com/?Action=SingleSendMail
    # &AccountName=time@shijianzhushou.xyz
    # &ReplyToAddress=true
    # &AddressType=1
    # &ToAddress=1170101471@qq.com
    # &Subject=Hello New World
    # &HtmlBody=Hello MyFriend
    ##########################################################################
    # https://dm.aliyuncs.com/?Action=BatchSendMail
    # &AccountName=test@shijianzhushou.xyz
    # &AddressType=1
    # &TemplateName=test1
    # &ReceiversName=test2
    # &TagName=test3
    ##########################################################################
    # 名称    类型  是否必须    描述
    # Action    String  必须  操作接口名，系统规定参数，取值：BatchSendMail。
    # AccountName   String  必须  管理控制台中配置的发信地址。
    # AddressType   Number  必须  取值范围 0~1: 0 为随机账号；1 为发信地址。
    # TemplateName  String  必须  预先创建且通过审核的模板名称。
    # ReceiversName String  必须  预先创建且上传了收件人的收件人列表名称。
    # TagName   String  可选  邮件标签名称
    # ClickTrace    String  可选  取值范围 0~1: 1 为打开数据跟踪功能; 0 为关闭数据跟踪功能。该参数默认值为 0。
    ##########################################################################
