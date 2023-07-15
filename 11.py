import requests
import threading
from requests.exceptions import RequestException

def get_url_status(url, max_retries=3):
    retries = 0
    
    while retries < max_retries:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == requests.codes.ok:
                return "网址：{} 正常".format(url)
            else:
                return "网址：{} 返回状态码：{}".format(url, response.status_code)
        except RequestException:
            retries += 1
    
    return "网址：{} 请求超时，已达到最大重试次数。".format(url)

def check_url(url):
    status = get_url_status(url)
    return status

file_path = "urls.txt"
output_file_path = "results.txt"

with open(file_path, "r") as file:
    urls = file.read().splitlines()

threads = []
results = []

for url in urls:
    thread = threading.Thread(target=lambda: results.append(check_url(url)))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

with open(output_file_path, "w") as file:
    for result in results:
        file.write(result + "\n")

print("结果已保存在 {} 中。".format(output_file_path))