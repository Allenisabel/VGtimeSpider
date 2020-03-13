import requests
import re
import pandas as pd

#定义headers和list
kv = {'user-agent':'Mozilla/5.0'}
list = []

#开始循环
for i in range(1,12000):
    #定义code,url,html
    code = str(i)
    url = "https://www.vgtime.com/game/" + code +".jhtml"
    r = requests.get(url,headers=kv)
    html = r.text
    #正则表达式取数
    game1 = re.findall(r'更多有关.*?的评测',html)
    gameEnglish1 = re.findall(r'<p>.*?</p>',html)
    kfs1 = re.findall(r'游戏时光,.*?,vgtime',html)
    fxs1 = re.findall(r'vgtime,.*?,发售',html)
    zzfs1 = re.findall('tid="0">最早发售&nbsp;.*?</span>',html)
    zwfs1 = re.findall('tid="0">中文发售&nbsp;.*?</span>',html)
    zzfsdeb1 = re.findall(r'<span>\d{4}-\d{2}-\d{2}</span>',html)
    print (i)
    if game1:
        game = game1[0].split('更多有关')[1].split('的评测')[0]
        if gameEnglish1:
            gameEnlish = gameEnglish1[0].split('<p>')[1].split('</p>')[0]
            if kfs1:
                kfs = kfs1[0].split('游戏时光,')[1].split(',vgtime')[0]
                if fxs1:
                    fxs = fxs1[0].split('vgtime,')[1].split(',发售')[0]
                    #根据发售时间的两个页面拆分
                    #页面形式1：https://www.vgtime.com/game/10053.jhtml这样的
                    if zzfs1:
                        if zwfs1:
                            zzfs = zzfs1[0].split('tid="0">最早发售&nbsp;')[1].split('</span>')[0]
                            zwfs = zwfs1[0].split('tid="0">中文发售&nbsp;')[1].split('</span>')[0]
                            list.append([code,url,game,gameEnlish,kfs,fxs,zzfs,zwfs])
                            print("成功：",i)
                        else:
                            zzfs = zzfs1[0].split('tid="0">最早发售&nbsp;')[1].split('</span>')[0]
                            list.append([code,url,game,gameEnlish,kfs,fxs,zzfs,'/'])
                            print("成功：",i)
                    #页面形式2：https://www.vgtime.com/game/10050.jhtml这样的
                    else:
                        #使用正则表达式取出所有<span>中的时间字符串，如果列表长度大于1，则有两个发售时间，否则只有一个
                        if zzfsdeb1:
                            if len(zzfsdeb1) > 1:
                                zzfsdeb = zzfsdeb1[0].split('<span>')[1].split('</span>')[0]
                                zwfsdeb = zzfsdeb1[1].split('<span>')[1].split('</span>')[0]
                                list.append([code,url,game,gameEnlish,kfs,fxs,zzfsdeb,zwfsdeb])
                                print("成功：",i)
                            else:
                                zzfsdeb = zzfsdeb1[0].split('<span>')[1].split('</span>')[0]
                                list.append([code,url,game,gameEnlish,kfs,fxs,zzfsdeb,'/'])
                                print("成功：",i)
                        #如果页面上没有发售时间，则两个值都为空
                        else:
                            list.append([code,url,game,gameEnlish,kfs,fxs,'/','/'])
                            print("成功：",i)

#打印到csv文件
title = ['code','url','游戏名','英文名','开发商','发行商','最早发售','中文发售']
test = pd.DataFrame(columns=title,data=list)
test.to_csv('/Users/zhengbowen/郑博文（个人）/Python自学文件/Vgtime.csv',encoding='utf-8')


