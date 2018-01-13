#!/usr/bin/python3
# @Author TartaricAcid
# @Title 批量整合模组下载工具
######################################

print("download Script Loading")

import urllib.request
import urllib.parse
import re
import time

download_log = open("modpack_download.log", "w", encoding='UTF-8')
download_log.writelines(
    "# " + time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()) + "\n\n")
download_log.close()

version = ["1.12.2", "filter-game-version=" +
           urllib.parse.quote("2020709689:6756")]

# 开始遍历 curseforge 页面，暂定为第 1 页
for num in range(1, 2):
    # 限定版本，按照下载量排序
    url = "https://www.curseforge.com/minecraft/modpacks?" + \
        version[1] + "&filter-sort=downloads" + "&page=" + str(num)
    data = urllib.request.urlopen(url).read()
    data = data.decode("utf-8")

    # 正则抓取 mod id
    modpack_name = re.findall(
        r"href=\"/minecraft/modpacks/(.*)/download\?client=y\"", data)

    for i in modpack_name:
        # 找到 mod 下载页面
        url = "https://www.curseforge.com/minecraft/modpacks/" + \
            i + "/files/?" + version[1]
        data = urllib.request.urlopen(url).read()
        data = data.decode('utf-8')

        # 正则抓取文件id，文件名称
        project_file_id = re.findall(r"\"ProjectFileID\": (.*),", data)

        if not any(project_file_id):
            continue

        url = "https://www.curseforge.com/minecraft/modpacks/" + \
            i + "/download/" + project_file_id[0] + "/file"
        # 用 geturl 方法得到真正的下载地址
        real_url = urllib.request.urlopen(url).geturl()

        # 输出到屏幕
        print("###############################" + "\n"
              + "下载整合：" + i + "\n"
              + "下载地址：" + real_url + "\n"
              + "文件ID：" + project_file_id[0] + "\n"
              + "页数：" + str(num) + "\n"
              + "###############################")

        # 下载 mod
        urllib.request.urlretrieve(real_url, "./modpacks/" + i)
        print(i + " 模组更新完毕\n")
        # 写入日志中
        download_log = open("modpack_download.log", 'a', encoding='UTF-8')
        download_log.write(i + "=" + project_file_id[0] + "\n")
        download_log.close()

print("download Script Stop Load")
