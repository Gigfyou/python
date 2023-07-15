#导入爬虫需要的包
import requests
from bs4 import BeautifulSoup
#requests与BeautifulSoup用来解析网页的
import time
#设置访问网页时间，防止自己IP访问多了被限制拒绝访问
import re
class Position():
 
    def __init__(self,position_name,position_require,):#构建对象属性
        self.position_name=position_name
        self.position_require=position_require
 
    def __str__(self):
        return '%s%s/n'%(self.position_name,self.position_require)#重载方法将输入变量改成字符串形式
 
class Aiqiyi():
    def iqiyi(self,url):
        head= {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47"
        }  #模拟的服务器头
        html = requests.get(url,headers=head)
        #headers=hard 让脚本以浏览器的方式去访问，有一些网址禁止以python的反爬机制，这就是其中一个
        soup = BeautifulSoup(html.content, 'lxml', from_encoding='utf-8')  # BeautifulSoup打看网页
        soupl = soup.select(".qy-list-wrap")  # 查找标签，用css选择器，选择自己需要数据 进行选择页面第一次内容（标签要找到唯一的，找id好，如果没有考虑其他标签如class）
        results = []  # 创建一个列表用来存储数据
        for e in soupl:
            biao = e.select('.qy-mod-li')  # 进行二次筛选
            for h in biao:
                p=Position(h.select_one('.qy-mod-link-wrap').get_text(strip=True),
                       h.select_one('.title-wrap').get_text(strip=True))#调用类转换（继续三次筛选选择自己需要内容）
                results.append(p)
        return results  # 返回内容
 
    def address(self,url):
        #保存网址
        head = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47"
        }  # 模拟的服务器头
        html = requests.get(url, headers=head)
        soup = BeautifulSoup(html.content, 'lxml', from_encoding='utf-8')  # BeautifulSoup打看网页
        alist = soup.find('div', class_='qy-list-wrap').find_all("a")  # 查找div块模块下的  a标签
        ls=[]
        for i in alist:
            ls.append(i.get('href'))
 
        return ls
 
 
 
if __name__ == '__main__':
    time.sleep(2)
    #设置2秒访问一次
    a=Aiqiyi()
    url = "https://list.iqiyi.com/www/1/-------------11-1-1-iqiyi--.html"
    with open(file='视频.txt ', mode='a+') as f:  # e:/练习.txt 为我电脑新建的文件，a+为给内容进行添加，但不进行覆盖原内容。
         for item in a.iqiyi(url):
             line = f'{item.position_name}\t{item.position_require}\n'
             f.write(line)  # 采用方法
             print("下载完成")
    with open(file='视频2.txt ', mode='a+') as f:  # e:/练习.txt 为我电脑新建的文件，a+为给内容进行添加，但不进行覆盖原内容。
        for item in a.address(url):
            line=f'https:{item}\n'
            f.write(line)  # 采用方法
            print("下载完成")