#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Duplicate Codes of Shape Codes
#

import re
import sys
import sqlite3

from collections import Counter

# 读取需要计算的形码码表 (sc = shape codes)
# 码表文件需使用 unix 格式、utf-8 编码
# 内容组织形式为: 汉字\t编码       (例: 的	rqyy)
#                 汉字\t编码\t频率 (例: 的	rqyy	1479)
#                 汉字\t频率\t编码 (例: 的	1479	rqyy)
# 形码的码表文件 (参数 1)
sc_file = sys.argv[1]
# 形码的名字
sc_name = sc_file.replace(".txt", "")
# 打开形码码表文件
sc_txt = open(sc_file, mode='r', encoding='utf-8')

conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute('CREATE TABLE mytable (zi TEXT, code TEXT)')
c.execute("CREATE INDEX idx_zi ON mytable(zi)")
for i in sc_txt.readlines():
    i = i.strip()
    try:
        zi = re.search('^.', i).group()
        code = re.search('[a-z]+', i).group()
    except AttributeError:
        pass
    data = [(zi, code)]
    c.executemany('INSERT INTO mytable VALUES (?, ?)', data)
    conn.commit()


# 需要计算的字表 (取消注释以启用)
char_table = {}
char_table["国标字表"]   = "tables-charlist/国字标准字体表.txt" # 台湾
char_table["常用字表"]   = "tables-charlist/常用字字形表.txt"   # 香港
char_table["通规字表"]   = "tables-charlist/通用规范汉字表.txt" # 大陆
char_table["BIG5-1984"]  = "tables-encoding/Big5-1984.txt"
char_table["GB2312"]     = "tables-encoding/GB2312.txt"
char_table["GB18030-00"] = "tables-encoding/GB18030-2000.txt"
#char_table["GB18030-05"] = "tables-encoding/GB18030-2005.txt"
char_table["GBK"]        = "tables-encoding/GBK.txt"
#char_table["CJK-All"]    = "tables-encoding/All.txt.txt"


# 通过 Value 查 Index
def get_index_by_value(dic, value):
    #for k, v in dic.items():
    #    if v == value:
    #        return k
    return "".join([k for k, v in dic.items() if v == value])


# 返回列表里长度最长的字符串
def longest_str_in_list(encode_list):
    #encode = len(max(encode_list, key=len))
    #longest = []
    #for i in encode_list:
    #    if len(i) == encode:
    #        longest.append(i)
    #return longest
    encode = len(max(encode_list, key=len))
    return [i for i in encode_list if len(i) == encode]


# 计算重复编码的数量
def count_str_repetitions(encode_list, sc_name, table_name):
    #uniq_counter = []
    #uniq_code = set(encode_list)
    #for k in uniq_code:
    #    uniq_num = all_encode.count(k)
    #    if uniq_num > 1:
    #        uniq_counter.append(uniq_num)
    #print(sc_name + " - " + table_name + ":\t" + str(len(uniq_counter)))
    duplicates = [count for encode, count in Counter(encode_list).items() if count > 1]
    print(sc_name + " -> " + table_name + ":\t" + str(len(duplicates)))


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
        c.execute('SELECT code FROM mytable WHERE zi = ?', (zi))
        rows = c.fetchall()
        zi_encode = [str(row).replace("('", "").replace("',)", "") for row in rows]
        # 获取长度最长的编码并给 all_encode
        [all_encode.append(m) for m in longest_str_in_list(zi_encode)]
    # 计算重复编码的组数
    count_str_repetitions(all_encode, sc_name, table_name)
