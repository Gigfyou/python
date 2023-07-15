import requests
from bs4 import BeautifulSoup
import time

class Position():
    def __init__(self, position_name, position_require):
        self.position_name = position_name
        self.position_require = position_require

    def __str__(self):
        return f'{self.position_name}\t{self.position_require}\n'

class Aiqiyi():
    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47"
        }

    def get_html(self, url):
        response = requests.get(url, headers=self.headers)
        return response.text

    def get_positions(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        positions = []
        position_items = soup.select('.qy-mod-li')
        for item in position_items:
            position_name = item.select_one('.qy-mod-link-wrap').text.strip()
            position_require = item.select_one('.title-wrap').text.strip()
            position = Position(position_name, position_require)
            positions.append(position)
        return positions

    def get_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        link_items = soup.find('div', class_='qy-list-wrap').find_all('a')
        for item in link_items:
            link = item.get('href')
            links.append(f'https:{link}')
        return links

if __name__ == '__main__':
    a = Aiqiyi()
    url = 'https://list.iqiyi.com/www/1/-------------11-1-1-iqiyi--.html'
    
    page = 1
    count = 0
    while count < 4:
        positions_html = a.get_html(url)
        positions = a.get_positions(positions_html)
        with open('练习.txt', 'a+', encoding='utf-8') as f:
            for position in positions:
                f.write(str(position))
            print('职位信息已保存')
        
        links_html = a.get_html(url)
        links = a.get_links(links_html)
        with open('地址.txt', 'a+', encoding='utf-8') as f:
            for link in links:
                f.write(link + '\n')
            print('网址已保存')

        count += 1
        page += 1
        url = url.replace(f'-{page-1}-', f'-{page}-')
        time.sleep(2)  # 增加延时，避免过快请求被封禁