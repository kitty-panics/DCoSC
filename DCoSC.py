#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Duplicate Codes of Shape Codes
#

import re
import sys
from collections import Counter

# 读取需要计算的形码码表 (sc = shape codes)
# 码表文件需使用 unix 格式、utf-8 编码
# 内容组织形式为: 汉字\t编码       (的	rqyy)
#                 汉字\t编码\t频率 (的	rqyy	21479)
# 形码的码表文件 (参数 1)
sc_file = sys.argv[1]
# 形码的名字
sc_name = sc_file.replace(".txt", "")
# 读取形码码表文件
read_file = open(sc_file, mode='r', encoding='utf-8')
sc_txt = read_file.read()


# 需要计算的字表 (取消注释以启用)
char_table = {}
char_table["BIG5(1984)"]    = "tables-encoding/Big5-1984.txt"
char_table["GB2312"]        = "tables-encoding/GB2312.txt"
#char_table["GB18030(00)"] = "tables-encoding/GB18030-2000.txt"
#char_table["GB18030(05)"] = "tables-encoding/GB18030-2005.txt
#char_table["GB18030(20)"] = "tables-encoding/GB18030-2020.txt
char_table["通规字表"]  = "tables-charlist/通用规范汉字表.txt"
char_table["国标字表"]  = "tables-charlist/国字标准字体表.txt"


# 通过 Value 查 Index
def get_index_by_value(dic, value):
    for k, v in dic.items():
        if v == value:
            return k


# 返回列表里长度最长的字符串
def longest_str_in_list(encode_list):
   longest = []
   encode = len(max(encode_list, key=len))
   for i in encode_list:
       if len(i) == encode:
           longest.append(i)
   return longest


# 计算重复编码的数量
def count_str_repetitions(encode_list, sc_name, table_name):
    uniq_counter = []
    #uniq_code = set(encode_list)
    #for k in uniq_code:
    #    uniq_num = all_encode.count(k)
    #    if uniq_num > 1:
    #        uniq_counter.append(uniq_num)
    #print(sc_name + " - " + table_name + ": " + str(len(uniq_counter)))
    counter = Counter(encode_list)
    duplicates = {item: count for item, count in counter.items() if count > 1}
    for item, count in duplicates.items():
        if count > 1:
            uniq_counter.append(count)
    print(sc_name + " -> " + table_name + ":\t" + str(len(uniq_counter)))


# 遍历已启用的字表
for i in char_table.values():
    # 字表名称
    table_name = get_index_by_value(char_table, i)
    # 用于存放当前字表的所有编码
    all_encode = []
    # 遍历当前的字表
    zi_file = open(i, mode='r', encoding='utf-8')
    zi_txt = zi_file.readlines()
    for j in zi_txt:
        # 得到单个汉字
        zi = j.strip()
        # 通过汉字获取过滤出编码
        zi_encode = re.findall(zi + '\t.*', sc_txt)
        try:
            # 获取长度最长的编码
            longest_encode = []
            for k in zi_encode:
                longest_encode.append(re.search('[a-z]+', k).group())
            for m in longest_str_in_list(longest_encode):
                all_encode.append(m)
        except ValueError:
            #print("缺字: " + zi)
            pass
    # 计算重复编码的组数
    count_str_repetitions(all_encode, sc_name, table_name)
