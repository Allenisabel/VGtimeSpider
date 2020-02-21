import requests
import re
import pandas as pd

kv = {'user-agent':'Mozilla/5.0'}
list = []
for i in range(1,12000):
    code = str(i)
    url = "https://www.vgtime.com/game/" + code +".jhtml"
    r = requests.get(url,headers=kv)
    html = r.text
    game1 = re.findall('更多有关.*?的评测',html)
    kfs1 = re.findall(r'游戏时光,.*?,vgtime',html)
    fxs1 = re.findall(r'vgtime,.*?,发售',html)
    fssj1 = re.findall('tid="0">最早发售&nbsp;.*?</span>',html)
    if game1:
        if kfs1:
            if fxs1:
                if fssj1:
                    game = game1[0].split('更多有关')[1].split('的评测')[0]
                    kfs = kfs1[0].split('游戏时光,')[1].split(',vgtime')[0]
                    fxs = fxs1[0].split('vgtime,')[1].split(',发售')[0]
                    fssj = fssj1[0].split('tid="0">最早发售&nbsp;')[1].split('</span>')[0]
                    list.append([game,kfs,fxs,fssj])
                    print(i)

title = ['游戏名','开发商','发行商','发售时间']
test = pd.DataFrame(columns=title,data=list)
test.to_csv('文件地址.csv',encoding='utf-8')
#测试下修改

