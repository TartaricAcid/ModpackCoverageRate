#!/usr/bin/python3
# @Author TartaricAcid
# @Title 特殊模组检索下载
######################################

print("download Script Loading")

import operator
import re
import time
import json
import urllib.request

# 读取 log 文件，做到增量更新
modpack_download_log = open("modpack_download.log", "r", encoding='UTF-8')
download_log = open("download.log", "r", encoding='UTF-8')

modpack_coverage_rate_file = open(
    "modpack_coverage_rate.md", 'w', encoding='UTF-8')
modpack_coverage_rate_file.writelines(
    "### " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n\n")
modpack_coverage_rate_file.close()

# 创建映射表，记录更新情况
modpack_log_list = list()     # 用来记录整合包 mod
log_list = list()     # 用来记录 weblate 的 mod
no_mod_list = list()    # 用了记录对比中没有的 mod


def make_list(log_file, log_list):
    for line in log_file.readlines():
        if line != None and line[0] != "#" and "=" in line:
            line_list = line.split("=", 1)        # 依据等号切分语言文件条目
            log_list.append(line_list[0])


make_list(modpack_download_log, modpack_log_list)
make_list(download_log, log_list)

for modpack_name in modpack_log_list:
    with open("tmp/" + modpack_name, "r") as f:
        data = json.load(f)

    for manifest in data["files"]:
        url = "https://minecraft.curseforge.com/mc-mods/" + \
            str(manifest["projectID"])
        try:
            real_url = urllib.request.urlopen(url).geturl()
        except:
            print("no mod found")
            continue
        mod_url_name = re.findall(
            r"https://minecraft.curseforge.com/projects/(.*)", real_url)

        # 设定一个变量，用来返回检验结果
        is_have = False
        for mod_list_name in log_list:

            if operator.eq(mod_list_name, mod_url_name[0]):
                is_have = True
                break

        if not is_have:
            no_mod_list.append(mod_url_name[0])

    total = len(data["files"])
    no_mod_num = len(no_mod_list)
    percentage = round(((total - no_mod_num) / total * 100), 2)

    modpack_coverage_rate_file = open(
        "modpack_coverage_rate.md", 'w', encoding='UTF-8')
    modpack_coverage_rate_file.write(
        "### " + modpack_name + " 整合包下载情况：" + str(percentage) + "%\t\t\n")

    k = 1
    for i in no_mod_list:
        modpack_coverage_rate_file.write(str(k) + "|" + i + "\n")
        k = k + 1

    modpack_coverage_rate_file.write("\n\n")
print("download Script Stop Load")
