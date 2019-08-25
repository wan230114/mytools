import urllib.request
import re
import time


def getTime():
    """
    获取北京时间
    """
    def func():
        try:
            url = "http://time1903.beijing-time.org/time.asp"
            # 定义头信息变量
            headers = (
                "User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36")
            # 创建自定义的opener对象
            opener = urllib.request.build_opener()
            # 对opener对象添加属性--头信息addheaders
            opener.addheaders = [headers]
            # 用open()打开opener对象网页
            data = opener.open(url, timeout=1).read().decode()
            Ldata = re.findall('[0-9]+', data)
            Ldata = Ldata[1:4] + Ldata[5:]
            Ttime = time.strptime('-'.join(Ldata), '%Y-%m-%d-%H-%M-%S')
            stime = time.strftime("%Y-%m-%d %H:%M:%S", Ttime)
            return stime
        except Exception:
            return 0
    stime = func()
    if not stime:
        stime = func()
    if not stime:
        stime = time.strftime(" %Y-%m-%d %H:%M:%S ", time.localtime())
    print(stime)
    return stime


if __name__ == '__main__':
    getTime()
    # for i in range(10):
    #     t0 = time.time()
    #     getTime()
    #     print(time.time() - t0)
