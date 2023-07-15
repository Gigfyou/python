import requests
from bs4 import BeautifulSoup
import csv

url = 'https://list.iqiyi.com/www/1/-------------{}-1-1-iqiyi--.html'

def get_movie_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_list = soup.find_all('li', class_='qy-mod-li')

    results = []
    for movie in movie_list:
        title = movie.find('a', class_='link-txt').text.strip()
        
        try:
            img_url = movie.find('img', class_='i71-img')['src']
        except:
            img_url = ''
        
        # 使用 try-except 捕获异常
        try:
            rating = movie.find('span', class_='label-score').text.strip()
        except:
            rating = ''
        
        description = movie.find('p', class_='sub').text.strip()

        movie_info = {
            'title': title,
            'img_url': img_url,
            'rating': rating,
            'description': description
        }
        results.append(movie_info)

    return results

def save_data_to_csv(data):
    with open('movies.csv', 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['title', 'img_url', 'rating', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    movie_data = []
    for i in range(1, 2):
        page_url = url.format(i)
        data = get_movie_info(page_url)
        movie_data.extend(data)

    for movie in movie_data:
        print(f"片名：{movie['title']}")
        print(f"图片链接：{movie['img_url']}")
        print(f"评分：{movie['rating']}")
        print(f"描述：{movie['description']}")
        print("-----")

    save_data_to_csv(movie_data)

if __name__ == '__main__':
    main()