#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Duplicate Codes of Shape Codes
#

import sys
import re

# 读取需要测试的星妈
sc_file = open(sys.argv[1], mode='r', encoding='utf-8')
sc_txt = sc_file.read()

# 需要测试的汉字表
table_dict = {}
#table_dict["BIG5(1984)"]    = "tables-encoding/Big5-1984.txt"
table_dict["GB2312"]        = "tables-encoding/GB2312.txt"
#table_dict["GB18030(2000)"] = "tables-encoding/GB18030-2000.txt"
#table_dict["通用规范汉字"]  = "tables-charlist/通用规范汉字表.txt"

def longest_str_in_list(longest_list):
   common_result = []
   longest = len(max(longest_list, key=len))
   for each in longest_list:
       if(longest == len(each)):
           #common_result is list to store longest string in list
           common_result.append(each)
   return common_result

all_code = []
# 遍历已启用的汉字字表
for i in table_dict.values():
    zi_file = open(i, mode='r', encoding='utf-8')
    zi_txt = zi_file.readlines()
    # 
    for j in zi_txt:
        zi = j.strip()
        zi_encode = re.findall(zi + '\t.*', sc_txt)
        try:
            longest_code = []
            for k in zi_encode:
                longest_code.append(re.search('[a-z]+', k).group())
            for x in longest_str_in_list(longest_code):
                all_code.append(x)
        except ValueError:
            #print("缺字: " + zi)
            pass
    uniq_counter = []
    uniq_code = set(all_code)
    for k in uniq_code:
        uniq_num = all_code.count(k)
        if uniq_num > 1:
            uniq_counter.append(uniq_num)
    print(sys.argv[1].replace(".txt", "") + ": " + str(len(uniq_counter)))
