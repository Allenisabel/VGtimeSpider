import requests
import re
import pandas as pd

kv = {'user-agent':'Mozilla/5.0'}
list = []
for i in range(10050,10060):
    code = str(i)
    url = "https://www.vgtime.com/game/" + code +".jhtml"
    r = requests.get(url,headers=kv)
    html = r.text
    game1 = re.findall(r'更多有关.*?的评测',html)
    gameEnglish1 = re.findall(r'</title>\n<meta content=".*?,.*?,',html)
    kfs1 = re.findall(r'游戏时光,.*?,vgtime',html)
    fxs1 = re.findall(r'vgtime,.*?,发售',html)
    zzfs1 = re.findall('tid="0">最早发售&nbsp;.*?</span>',html)
    zwfs1 = re.findall('tid="0">中文发售&nbsp;.*?</span>',html)
    zzfsdeb1 = re.findall(r'<span>\d{4}-\d{2}-\d{2}</span>',html)
    print (i)
    if game1:
        if kfs1:
            if fxs1:
                if zzfs1:
                    if zwfs1:
                        game = game1[0].split('更多有关')[1].split('的评测')[0]
                        gameEnlish = gameEnglish1[0].split(',')[1]
                        kfs = kfs1[0].split('游戏时光,')[1].split(',vgtime')[0]
                        fxs = fxs1[0].split('vgtime,')[1].split(',发售')[0]
                        zzfs = zzfs1[0].split('tid="0">最早发售&nbsp;')[1].split('</span>')[0]
                        zwfs = zwfs1[0].split('tid="0">中文发售&nbsp;')[1].split('</span>')[0]
                        list.append([code,url,game,gameEnlish,kfs,fxs,zzfs,zwfs])
                        print("成功：",i)
                    else:
                        game = game1[0].split('更多有关')[1].split('的评测')[0]
                        gameEnlish = gameEnglish1[0].split(',')[1]
                        kfs = kfs1[0].split('游戏时光,')[1].split(',vgtime')[0]
                        fxs = fxs1[0].split('vgtime,')[1].split(',发售')[0]
                        zzfs = zzfs1[0].split('tid="0">最早发售&nbsp;')[1].split('</span>')[0]
                        list.append([code,url,game,gameEnlish,kfs,fxs,zzfs,'/'])
                        print("成功：",i)
                else:
                    if zzfsdeb1:
                        if len(zzfsdeb1) > 1:
                            game = game1[0].split('更多有关')[1].split('的评测')[0]
                            gameEnlish = gameEnglish1[0].split(',')[1]
                            kfs = kfs1[0].split('游戏时光,')[1].split(',vgtime')[0]
                            fxs = fxs1[0].split('vgtime,')[1].split(',发售')[0]
                            zzfsdeb = zzfsdeb1[0].split('<span>')[1].split('</span>')[0]
                            zwfsdeb = zzfsdeb1[1].split('<span>')[1].split('</span>')[0]
                            list.append([code,url,game,gameEnlish,kfs,fxs,zzfsdeb,zwfsdeb])
                            print("成功：",i)
                        else:
                            game = game1[0].split('更多有关')[1].split('的评测')[0]
                            gameEnlish = gameEnglish1[0].split(',')[1]
                            kfs = kfs1[0].split('游戏时光,')[1].split(',vgtime')[0]
                            fxs = fxs1[0].split('vgtime,')[1].split(',发售')[0]
                            zzfsdeb = zzfsdeb1[0].split('<span>')[1].split('</span>')[0]
                            list.append([code,url,game,gameEnlish,kfs,fxs,zzfsdeb,'/'])
                            print("成功：",i)
                    else:
                        game = game1[0].split('更多有关')[1].split('的评测')[0]
                        gameEnlish = gameEnglish1[0].split(',')[1]
                        kfs = kfs1[0].split('游戏时光,')[1].split(',vgtime')[0]
                        fxs = fxs1[0].split('vgtime,')[1].split(',发售')[0]
                        list.append([code,url,game,gameEnlish,kfs,fxs,'/','/'])
                        print("成功：",i)
                       
title = ['code','url','游戏名','英文名','开发商','发行商','最早发售','中文发售']
test = pd.DataFrame(columns=title,data=list)
test.to_csv('Vgtime.csv',encoding='utf-8')


