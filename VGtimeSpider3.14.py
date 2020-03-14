import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

#定义headers和list
kv = {'user-agent':'Mozilla/5.0'}
list = []

#开始循环
for i in range(1,12000):
    print (i)
    
    #定义游戏名,英文名,开发商,发行商,最早发售,中文发售，平台列表，游戏基因列表，官网链接
    game = "/"
    gameEnlish = "/"
    kfs = "/"
    fxs = "/"
    zzfs = "/"
    zwfs = "/"
    platformList = []
    geneList = []
    lanuageList = []
    link = "/"

    #定义code,url,html
    code = str(i)
    url = "https://www.vgtime.com/game/" + code +".jhtml"
    r = requests.get(url,headers=kv)
    html = r.text

    #使用BeautifulSoup解析
    soup = BeautifulSoup(html,'html.parser')
    #找出game_descri的div块
    soupGameDescri = soup.find('div',attrs = {'class':'game_descri'})
    #循环遍历game_descri的div子块
    try:
        for descriBox in soupGameDescri.children:
            try:
                descriBox = str(descriBox)
                platformName = re.findall(r'平台',descriBox)
                geneName = re.findall(r'游戏基因',descriBox)
                lanuageName = re.findall(r'语言',descriBox)
                linkName = re.findall(r'游戏官网',descriBox)
                
                #如果该块是平台
                if platformName:
                    platformList1 = re.findall(r'>.*?</span>',descriBox)
                    for i in range(len(platformList1)):
                        platform = platformList1[i].split('>')[1].split('<')[0]
                        platformList.append(platform)

                #如果该块是基因
                if geneName:
                    geneList1 = re.findall(r'>.*?</span>',descriBox)
                    for i in range(len(geneList1)):
                        gene = geneList1[i].split('>')[1].split('<')[0]
                        geneList.append(gene)

                #如果该块是语言
                if lanuageName:
                    lanuageList1 = re.findall(r'>.*?</span>',descriBox)
                    for i in range(len(lanuageList1)):
                        lanuage = lanuageList1[i].split('>')[1].split('<')[0]
                        lanuageList.append(lanuage)

                #如果该块是游戏官网
                if linkName:
                    link1 = re.findall(r'href=".*?"',descriBox)
                    link = link1[0].split('"')[1]
            except:
                continue
    except:
        continue

    #正则表达式取数
    game1 = re.findall(r'更多有关.*?的评测',html)
    gameEnglish1 = re.findall(r'<p>.*?</p>',html)
    kfs1 = re.findall(r'游戏时光,.*?,vgtime',html)
    fxs1 = re.findall(r'vgtime,.*?,发售',html)
    zzfs1 = re.findall(r'tid="0">最早发售&nbsp;.*?</span>',html)
    zwfs1 = re.findall(r'tid="0">中文发售&nbsp;.*?</span>',html)
    #zzfs2 = re.findall(r'<p>最早发售</p>\n*<span>\d{4}-\d{2}-\d{2}</span>',html)
    #zwfs2 = re.findall(r'<p>中文发售</p>\n<span>\d{4}-\d{2}-\d{2}</span>',html)
    fssj2 = re.findall(r'<span>\d{4}-\d{2}-\d{2}</span>',html)

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
        zzfs = zzfs1[0].split('tid="0">最早发售&nbsp;')[1].split('</span>')[0]
    if zwfs1:
        zwfs = zwfs1[0].split('tid="0">中文发售&nbsp;')[1].split('</span>')[0]

    #页面形式2：https://www.vgtime.com/game/10050.jhtml这样的
    #使用正则表达式取出所有<span>中的时间字符串，如果列表长度大于1，则有两个发售时间，否则只有一个
    if fssj2:
        if len(fssj2) > 1:
            zzfs = fssj2[0].split('<span>')[1].split('</span>')[0]
            zwfs = fssj2[1].split('<span>')[1].split('</span>')[0] 
        else:
            zzfs = fssj2[0].split('<span>')[1].split('</span>')[0]

    '''
    if zzfs2:
        zzfs = zzfs2[0].split('<span>')[1].split('</span>')[0]
    if zwfs2:
        zwfs = zwfs2[0].split('<span>')[1].split('</span>')[0]
    '''

    list.append([code,url,game,gameEnlish,kfs,fxs,zzfs,zwfs,platformList,geneList,lanuageList,link])
    

#打印到csv文件
title = ['code','url','游戏名','英文名','开发商','发行商','最早发售','中文发售','游戏平台','游戏基因','语言','游戏官网']
test = pd.DataFrame(columns=title,data=list)
test.to_csv('Vgtime.csv',encoding='utf-8')


