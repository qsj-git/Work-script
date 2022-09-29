import re
import os


# 只要匹配就替换，全文
def all_alter(file, old_str, new_str):
    with open(file, "r", encoding='utf-8') as f1, open("{}.bak".format(file), "w", encoding="utf-8") as f2:
        for line in f1:
            f2.write(re.sub(old_str, new_str, line))
    # 删除原文件
    os.remove(file)
    # 将新文件重命名为原文件同名文件
    os.rename("{}.bak".format(file), file)


# 精确匹配，全文
def exact_match(file, old_str, new_str):
    new_list = []
    old_str = old_str + '\n'
    new_str = new_str + '\n'
    with open(file, 'r', encoding='utf-8') as f1:
        oldfile = f1.readlines()
        for i in oldfile:
            #print("i 是：{}, old_str is:{}".format(i, old_str))
            if old_str == i:  # is 比较的是两个变量的内存地址，==比较的是两个变量的内容是否相等
                new_list.append(new_str)
            else:
                new_list.append(i)
    with open("{}.bak".format(file), 'w', encoding='utf-8') as f2:
        for s in new_list:
            f2.write(s)
    os.remove(file)
    os.rename("{}.bak".format(file), file)
