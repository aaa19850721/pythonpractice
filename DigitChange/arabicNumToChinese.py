# coding=utf-8

"""
@author:  xueyun
@license: Apache Licence
@contact: znmei12@gmail.com
@site: http://www.cloudgrassland.com
@file: arabicNumToChinese.py
@time: 2015/12/18 9:35
"""


# 阿拉伯数字0-9与中文数字的对照表
CHN_NUM_CHAR = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
# 中文中的节点单位 每四位一个节
CHN_UNIT_SECTION = ["", "万", "亿", "万亿"]
# 每个节内各位数字的权
CHN_UNIT_CHAR = ["", "十", "百", "千"]


def arabic_to_chinese(num):
    # 记录节的位置
    unitpos = 0
    strins = []
    chnstr = []
    # 某节是否需要补零的标识
    is_need_zero = False
    # 每次循环，节以从小到大的方向向前推进
    while num > 0:
        section = num % 10000
        if is_need_zero:
            chnstr.insert(0, [CHN_NUM_CHAR[0]])
        # 将这个节转换为中文
        strins = section_to_chinese(section)

        strins.append(CHN_UNIT_SECTION[unitpos] if section != 0 else CHN_UNIT_SECTION[0])

        chnstr.insert(0, strins)
        # 通过此节千位是否为0，得到下一节是否需要在末尾补0
        is_need_zero = (section < 1000) and (section > 0)
        num = int(num / 10000)
        unitpos += 1
        tempstr = []
        for i in range(0, chnstr.__len__()):
            temp = "".join(chnstr[i])
            tempstr.append(temp)
        result = "".join(tempstr)

    return result


def section_to_chinese(section):
    chnstr = []
    strins = ""
    unitpos = 0
    zero = True
    while section > 0:
        v = int(section % 10)
        if v == 0:
            if not zero:
                zero = True
                print(chnstr)
                chnstr.insert(0, CHN_NUM_CHAR[v])
                print(chnstr)
        else:
            zero = False
            strins = CHN_NUM_CHAR[v]
            strins += CHN_UNIT_CHAR[unitpos]
            chnstr.insert(0, strins)
        unitpos += 1
        section = int(section / 10)

    return chnstr


if __name__ == "__main__":
    print(arabic_to_chinese(3201301500236))