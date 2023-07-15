filtered_urls = []

with open("地址.txt", "r") as file:
    urls = file.readlines()

    # 删除包含"/lib/"的网址并去除重复项
    unique_urls = set()
    for url in urls:
        if "/lib/" not in url:
            unique_urls.add(url.strip())

    filtered_urls = list(unique_urls)

with open("filtered_urls.txt", "w") as output_file:
    for url in filtered_urls:
        output_file.write(url + "\n")