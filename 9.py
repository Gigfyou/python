import os

folder_path = "./tutu"  # 替换为要重命名的文件夹路径

files = os.listdir(folder_path)
files.sort()

count = 1
for file in files:
    if file.endswith(".png"):
        file_path = os.path.join(folder_path, file)
        new_file_name = str(count) + ".png"
        new_file_path = os.path.join(folder_path, new_file_name)
        os.rename(file_path, new_file_path)
        count += 1