# coding=utf-8
"""
@author:  xueyun
@license: Apache Licence 
@contact: znmei12@gmail.com
@site: http://www.cloudgrassland.com
@file: chineseNumToArabic.py
@time: 2015/12/21 9:27
"""

# 阿拉伯数字0-9与中文数字的对照表
CHN_NUM_CHAR = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
# 中文中的节点单位 每四位一个节
CHN_UNIT_SECTION = ["", "万", "亿", "万亿"]
# 每个节内各位数字的权
CHN_UNIT_CHAR = ["", "十", "百", "千"]


class ChnNameValue:
    def __init__(self, name, value, sec_unit):
        self.name = name
        self.value = value
        self.sec_unit = sec_unit


CHN_VALUE_PAIR = []
CHN_VALUE_PAIR.append(ChnNameValue("十", 10, False))
CHN_VALUE_PAIR.append(ChnNameValue("百", 100, False))
CHN_VALUE_PAIR.append(ChnNameValue("千", 1000, False))
CHN_VALUE_PAIR.append(ChnNameValue("万", 10000, True))
CHN_VALUE_PAIR.append(ChnNameValue("亿", 100000000, True))
CHN_VALUE_PAIR.append(ChnNameValue("万亿", 10000000000000, True))


def chinese_to_value(chnstr):
    for i in range(0, CHN_NUM_CHAR.__len__()):
        if chnstr == CHN_NUM_CHAR[i]:
            return i

    return -1


def chinese_to_unit(chnstr):
    for i in range(0, CHN_VALUE_PAIR.__len__()):
        if chnstr == CHN_VALUE_PAIR[i].name:
            return (CHN_VALUE_PAIR[i].value, CHN_VALUE_PAIR[i].sec_unit)
    return 1,


def chinese_to_arabic(chnstring):
    rtn = 0
    section = 0
    number = 0
    sec_unit = False
    pos = 0
    while pos < len(chnstring):
        num = chinese_to_value(chnstring[pos:(pos + 1)])
        if num >= 0:
            number = num
            pos += 1
            if pos >= len(chnstring):
                section += number
                rtn += section
                break
        else:
            if (chnstring[pos:(pos + 2)] == "万亿"):
                unit, sec_unit = chinese_to_unit(chnstring[pos:(pos + 2)])
                pos += 2
            else:
                a = chnstring[pos:(pos + 1)]
                print(a)
                unit, sec_unit = chinese_to_unit(chnstring[pos:(pos + 1)])
                pos += 1
            if sec_unit:
                section = (section + number) * unit
                rtn += section
                section = 0
            else:
                section += number* unit
            number = 0

            if (pos >= len(chnstring)):
                rtn += section
                break
    return rtn


if __name__ == "__main__":
    print(chinese_to_arabic("三十万亿二千零一十三亿零一百五十万零二百三十六"))