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
    
    return None

def check_url(url):
    status = get_url_status(url)
    return status

def process_result(result):
    processed_result = result + " (已二次处理)"
    return processed_result

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

processed_results = []
for result in results:
    if result is not None:
        processed_result = process_result(result)
        processed_results.append(processed_result)

with open(output_file_path, "w") as file:
    for processed_result in processed_results:
        file.write(processed_result + "\n")

print("结果已保存在 {} 中。".format(output_file_path))
print("经过二次处理后的结果如下:")

with open(output_file_path, "r") as file:
    processed_results = file.read().splitlines()

for processed_result in processed_results:
    print(processed_result)