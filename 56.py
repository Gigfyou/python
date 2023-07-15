from lxml.html import etree
from PIL import Image
import requests
import os
import threading
import re
import concurrent.futures
import time

path = './tutu2'

if not os.path.exists(path):
    os.makedirs(path)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

url_list = []
area = input('请输入类别：')
if '美女' in area:
    area = '4kmeinv'
elif '风景' in area:
    area = '4kfengjing'
# 省略其他判断条件...

page = int(input('请输入页数：'))

lock = threading.Lock()

def download_image(url):
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    
    html_text = re.sub(r'\s*xmlns="[^"]+"', '', r.text)
    html = etree.HTML(html_text)

    url = html.xpath('//a[@id="img"]/img/@src')
    rr = requests.get('http://pic.netbian.com' + url[0], headers=headers)
    name = html.xpath('//a[@id="img"]/img/@title')
    rr.encoding = rr.apparent_encoding

    lock.acquire()

    with open(f"./tutu2/{name[0]}.png", 'wb') as fw:
        fw.write(rr.content)
    img = Image.open(f"./tutu2/{name[0]}.png")
    img = img.resize((4000, 2000), Image.LANCZOS)
    img.save(f"./tutu2/{name[0]}.png", quality=95)
    print(f"{name[0]} 保存完成！")

    lock.release()

def download_all_images(url_list):
    num_threads = min(len(url_list), 10)  # 自动调整线程数量
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for url in url_list:
            executor.submit(download_image, url)
            # 发送网络请求间添加延时，限制速度
            time.sleep(3)  # 设置延时时间，单位为秒

for i in range(0, page + 1):
    if i == 1:
        url = f'http://pic.netbian.com/{area}/index.html'
    else:
        url = f'http://pic.netbian.com/{area}/index_{i}.html'

    res = requests.get(url=url, headers=headers)
    res.encoding = res.apparent_encoding
    
    html_text = re.sub(r'\s*xmlns="[^"]+"', '', res.text)
    html = etree.HTML(html_text)

    content = html.xpath('//ul[@class="clearfix"]/li')
    for item in content:
        tu_url = item.xpath('./a/@href')
        tupian_url = 'http://pic.netbian.com' + ''.join(tu_url)
        url_list.append(tupian_url)

download_all_images(url_list)

print("保存完成！")
