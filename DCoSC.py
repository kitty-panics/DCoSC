#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Duplicate Codes of Shape Codes
#

import re
import sys
import sqlite3
import multiprocessing

from collections import Counter

# 在内存中创建 SQLite
conn_sc = sqlite3.connect(':memory:')
csc = conn_sc.cursor()
csc.execute('PRAGMA synchronous = OFF')
csc.execute('PRAGMA journal_mode = OFF')
csc.execute('CREATE TABLE csc_table (zi TEXT, code TEXT)')
csc.execute("CREATE INDEX idx_zi ON csc_table(zi)")
# 读取需要计算的形码码表 (sc = shape codes)
# 码表文件需使用 unix 格式、utf-8 编码
# 内容组织形式为: 汉字\t编码       (例: 的	rqyy)
#                 汉字\t编码\t频率 (例: 的	rqyy	1479)
#                 汉字\t频率\t编码 (例: 的	1479	rqyy)
# 形码的码表文件 (参数 1)
sc_file = sys.argv[1]
# 形码的名字
sc_name = sc_file.replace(".txt", "")
# 打开形码码表文件，并写进 SQLite 中
sc_txt = open(sc_file, mode='r', encoding='utf-8')
for i in sc_txt.readlines():
    i = i.strip()
    try:
        zi = re.search('^.', i).group()
        code = re.search('[a-z]+', i).group()
    except AttributeError:
        pass
    data = [(zi, code)]
    csc.executemany('INSERT INTO csc_table VALUES (?, ?)', data)
    conn_sc.commit()


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
def traversal_char_table(i):
    # 获取字表名称
    table_name = get_index_by_value(char_table, i)
    # 用于存放当前字表的所有编码
        # 方案 1
    all_encode = []
        # 方案 2
    #conn_allcode = sqlite3.connect(':memory:')
    #cac = conn_allcode.cursor()
    #cac.execute('PRAGMA synchronous = OFF')
    #cac.execute('PRAGMA journal_mode = OFF')
    #cac.execute('CREATE TABLE cac_table (allcode TEXT)')
    #cac.execute("CREATE INDEX idx_allcode ON cac_table(allcode)")
    # 遍历当前的字表
    zi_file = open(i, mode='r', encoding='utf-8')
    zi_txt = zi_file.readlines()
    for j in zi_txt:
        # 得到单字
        zi = j.strip()
        # 通过单字过滤出编码
        csc.execute('SELECT code FROM csc_table WHERE zi = ?', (zi))
        rows = csc.fetchall()
        zi_encode = [str(row).replace("('", "").replace("',)", "") for row in rows]
        # 只保存单字长度最长的编码
            # 方案 1
        [all_encode.append(m) for m in longest_str_in_list(zi_encode)]
            # 方案 2
        #for m in longest_str_in_list(zi_encode):
        #    cac.executemany('INSERT INTO cac_table VALUES (?)', ([m],))
        #conn_allcode.commit()
    # 计算重复编码的组数
        # 方案 1
    count_str_repetitions(all_encode, sc_name, table_name)
        # 方案 2
    #cac.execute('SELECT allcode, COUNT(*) as count FROM cac_table GROUP BY allcode HAVING count > 1')
    #print(sc_name + " -> " + table_name + ":\t" + str(len(cac.fetchall())))


def main():
    for i in char_table.values():
        # 单进程
        traversal_char_table(i)
        # 多进程
        #pool = multiprocessing.Pool()
        #for i in char_table.values():
        #    pool.apply_async(traversal_char_table, args=(i,))
        #pool.close()
        #pool.join()


if __name__ == "__main__":
    main()
