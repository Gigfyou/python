import socket
import subprocess
import threading

def get_ip(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except socket.error:
        print(f"找不到链接 {link} 的IP地址")

def ping_ip(ip):
    try:
        ping_process = subprocess.Popen(['ping', '-c', '4', ip], stdout=subprocess.PIPE)
        output, _ = ping_process.communicate()
        output = output.decode('utf-8')
        lines = output.split('\n')
        for line in lines:
            if 'avg' in line:
                ping_value = float(line.split('=')[1].split('/')[1])
                return ping_value
        return -1  # 若未找到平均值，则返回-1
    except subprocess.CalledProcessError:
        print(f"无法ping通IP地址 {ip}")
        return -1

links_file = "links.txt"

try:
    with open(links_file, "r", encoding="utf-8") as f:
        links = f.read().splitlines()
except FileNotFoundError:
    print("未找到链接文件 links.txt")
    exit(1)

results = []
results_below_zero = []
lock = threading.Lock()

def process_link(link):
    hostname = link.split('/')[2]
    ip = get_ip(hostname)
    if ip:
        ping_value = ping_ip(ip)
        if ping_value > 0:
            with lock:
                results.append({"link": link, "ip": ip, "ping_value": ping_value})
        else:
            with lock:
                results_below_zero.append(link)

threads = []

for link in links:
    thread = threading.Thread(target=process_link, args=(link,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

sorted_results = sorted(results, key=lambda x: x["ping_value"])

with open("有效网址.txt", "w", encoding="utf-8") as f:
    for result in sorted_results:
        link = result["link"]
        ip = result["ip"]
        ping_value = result["ping_value"]
        f.write(f"   {link}  | ping值: {ping_value:.2f}ms\n")

with open("无效网址.txt", "w", encoding="utf-8") as f:
    for link in results_below_zero:
        f.write(f"网址：{link}\n")

print("有效网址已写入文件：有效网址.txt")
print("无效网址已写入文件：无效网址.txt")