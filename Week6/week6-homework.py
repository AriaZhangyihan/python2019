import re
import os
import sys
#cmd python week6-homework.py filename
path = ""
filename = sys.argv[1]
fn=path+filename
name=os.path.splitext(filename)
fn_EN=path+name[0]+'_EN.txt' 
fn_ZH=path+name[0]+'_ZH.txt'
try:
    with open(fn, "r") as f:
        string=f.read()
        en = re.sub(u"([\u4e00-\u9fa5]|[\（\）\《\》\——\；\，\、\？\。\……\“\”\<\>\！\：\·\•])","",string)
        zh = re.sub(u"([\u0041-\u005a\u0061-\u007a]|[\.\'\"\‘\?\．])","",string)
    with open(fn_EN, 'w') as f_en:
        f0.write(en)
    with open(fn_ZH, 'w') as f_zh:
        f1.write(zh)
except IOError:
    print("Error")
else:
    print("Success")
    