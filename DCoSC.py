#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Duplicate Codes of Shape Codes
#

import multiprocessing
import os
import re
import sqlite3
import sys

from collections import Counter
from prettytable import PrettyTable


# 定义输出表格的样式
table = PrettyTable()
table.field_names = ["形码名称", "字表名称", "重码数量"]
table.align["形码名称"] = "l"
table.align["字表名称"] = "l"
table.align["重码数量"] = "l"
# 创建存放形码码表的 SQLite
conn_sc = sqlite3.connect(':memory:')
csc = conn_sc.cursor()
csc.execute('PRAGMA synchronous = OFF')
csc.execute('PRAGMA journal_mode = OFF')
csc.execute('CREATE TABLE csc_table (char TEXT, encode TEXT)')
csc.execute("CREATE INDEX idx_char ON csc_table(char)")
# 打开需要计算的形码码表 (参数 1)
# 码表文件需使用 unix 格式、utf-8 编码，内容组织形式为:
#     汉字\t编码       (例: 的	rqyy)
#     汉字\t编码\t频率 (例: 的	rqyy	1479)
#     汉字\t频率\t编码 (例: 的	1479	rqyy)
sc_file = sys.argv[1]
sc_name = os.path.basename(sc_file).replace('.txt', '')
sc_txt = open(sc_file, mode='r', encoding='utf-8')
# 读取形码码表文件并写进 SQLite 中
for i in sc_txt.readlines():
    i = i.strip()
    try:
        char = re.search('^.', i).group()
        encode = re.search('[a-z]+', i).group()
    except AttributeError:
        pass
    ins_data = [(char, encode)]
    csc.executemany('INSERT INTO csc_table VALUES (?, ?)', ins_data)
    conn_sc.commit()


# 需要统计的字表 (取消注释以启用)
char_table = {}
char_table["通规字表(总)"]  = "tables-charlist/通用规范汉字表.txt"
char_table["通规字表(1)"]   = "tables-charlist/通用规范汉字表-1.txt"
char_table["通规字表(2)"]   = "tables-charlist/通用规范汉字表-2.txt"
char_table["通规字表(3)"]   = "tables-charlist/通用规范汉字表-3.txt"
char_table["国标字表(总)"]  = "tables-charlist/国字标准字体表.txt"
char_table["国标字表(甲)"]  = "tables-charlist/国字标准字体表-甲.txt"
char_table["国标字表(乙)"]  = "tables-charlist/国字标准字体表-乙.txt"
    # 字符集
char_table["GB2312"]        = "tables-encoding/GB2312.txt"
char_table["BIG5(1984)"]    = "tables-encoding/BIG5-1984.txt"
char_table["GBK"]           = "tables-encoding/GBK.txt"
char_table["GB18030(2000)"] = "tables-encoding/GB18030-2000.txt"
char_table["GB18030(2005)"] = "tables-encoding/GB18030-2005.txt"
#char_table["GB18030(2022)"] = "tables-encoding/GB18030-2022.txt"
    # CJK 区段
char_table["CJK(部首补充)"] = "tables-unicode/CJK-汉字部首补充.txt"
char_table["CJK(康熙部首)"] = "tables-unicode/CJK-康熙部首.txt"
char_table["CJK(符号标点)"] = "tables-unicode/CJK-符号标点.txt"
char_table["CJK(笔画)"]     = "tables-unicode/CJK-笔画.txt"
char_table["CJK(扩A)"]      = "tables-unicode/CJK-扩展区-a.txt"
char_table["CJK(基本区)"]   = "tables-unicode/CJK-基本区.txt"
char_table["CJK(兼表)"]     = "tables-unicode/CJK-兼容表意文字.txt"
char_table["CJK(扩B)"]      = "tables-unicode/CJK-扩展区-b.txt"
char_table["CJK(扩C)"]      = "tables-unicode/CJK-扩展区-c.txt"
char_table["CJK(扩D)"]      = "tables-unicode/CJK-扩展区-d.txt"
char_table["CJK(扩E)"]      = "tables-unicode/CJK-扩展区-e.txt"
char_table["CJK(扩F)"]      = "tables-unicode/CJK-扩展区-f.txt"
char_table["CJK(兼表补充)"] = "tables-unicode/CJK-兼容表意文字补充区.txt"
char_table["CJK(扩G)"]      = "tables-unicode/CJK-扩展区-g.txt"
char_table["CJK(扩H)"]      = "tables-unicode/CJK-扩展区-h.txt"
#char_table["CJK(All)"]      = "tables-unicode/CJK-all.txt"


# 通过 Value 查 Index
def get_index_by_value(dic, value):
    #for k, v in dic.items():
    #    if v == value:
    #        return k
    return "".join([k for k, v in dic.items() if v == value])


# 返回列表里长度最长的字符串
def longest_str_in_list(encode_list):
    encode = len(max(encode_list, key=len))
    #longest = []
    #for i in encode_list:
    #    if len(i) == encode:
    #        longest.append(i)
    #return longest
    return [i for i in encode_list if len(i) == encode]


# 计算重复编码的数量
def count_str_repetitions(encode_list, sc_name, table_name):
    #duplicates = []
    #for i in set(encode_list):
    #    uniq_num = encode_list.count(i)
    #    if uniq_num > 1:
    #        duplicates.append(uniq_num)
    #table.add_row([sc_name, table_name, len(duplicates)])
    duplicates = [count for encode, count in Counter(encode_list).items() if count > 1]
    table.add_row([sc_name, table_name, len(duplicates)])


# 遍历已启用的字表
def traversal_char_table(i):
    # 获取当前字表的名称
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
    char_txt = open(i, mode='r', encoding='utf-8')
    for j in char_txt.readlines():
        # 得到单字
        char = j.strip()
        # 通过单字过滤出编码
        csc.execute('SELECT encode FROM csc_table WHERE char = ?', (char))
        rows = csc.fetchall()
        char_encode = [str(row).replace("('", "").replace("',)", "") for row in rows]
        # 只保存单字长度最长的编码
        try:
            # 方案 1
            [all_encode.append(m) for m in longest_str_in_list(set(char_encode))]
            # 方案 2
            #for m in longest_str_in_list(char_encode):
            #    cac.executemany('INSERT INTO cac_table VALUES (?)', ([m],))
            #conn_allcode.commit()
        except ValueError:
            #print(f"{table_name} -> {char}")
            pass
    # 计算重复编码的组数
        # 方案 1
    count_str_repetitions(all_encode, sc_name, table_name)
        # 方案 2
    #cac.execute('SELECT allcode, COUNT(*) as count FROM cac_table GROUP BY allcode HAVING count > 1')
    #table.add_row([sc_name, table_name, len(cac.fetchall())])


def main():
    # 单进程
    for i in char_table.values():
        traversal_char_table(i)
    print(table)
    # 多进程
    #pool = multiprocessing.Pool()
    #for i in char_table.values():
    #    pool.apply_async(traversal_char_table, args=(i,))
    #pool.close()
    #pool.join()


if __name__ == "__main__":
    main()
