import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

mailserver = "smtp.126.com"  #邮箱服务器地址
username_send = 'wan230114@126.com'  #邮箱用户名
password = 'cj1234567'   #邮箱密码：需要使用授权码
username_recv = '1170101471@qq.com'  #收件人，多个收件人用逗号隔开
mail = MIMEMultipart()
# file = r'E:\\testpy\\python-mpp\\day8\\练习\\sendmail.py'
# att = MIMEText(open(file,encoding='utf-8').read())  #这个只可以发送py或者txt附件，复杂一点的就会报错
file=r'mpp.xls'
file=r'mpp中文.xls'
att = MIMEText(open(file, 'rb').read(),"base64", "utf-8")  #这个可以发送复杂的附件，比如附件为表格
att["Content-Type"] = 'application/octet-stream'

#这行是把附件的格式进行一些处理，不知道为啥要这么写，但是如果不写接收到的附件已经不是表格样式了
new_file='=?utf-8?b?' + base64.b64encode(file.encode()).decode() + '?='
new_file='test'

att["Content-Disposition"] = 'attachment; filename="%s"'%new_file
mail.attach(att)
mail.attach(MIMEText('这是一封带有附件的邮件正文内容，假装很长'))#邮件正文的内容
mail['Subject'] = '这是邮件主题'
mail['From'] = username_send  #发件人
mail['To'] = username_recv  #收件人；[]里的三个是固定写法，别问为什么，我只是代码的搬运工
smtp = smtplib.SMTP(mailserver,port=25) # 连接邮箱服务器，smtp的端口号是25
# smtp=smtplib.SMTP_SSL('smtp.qq.com',port=465) #QQ邮箱的服务器和端口号
smtp.login(username_send,password)  #登录邮箱
smtp.sendmail(username_send,username_recv,mail.as_string())# 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
smtp.quit() # 发送完毕后退出smtp
print ('success')