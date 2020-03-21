import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

#定义headers和list
kv = {'user-agent':'Mozilla/5.0'}
list = []

#开始循环
for i in range(10050,10100):
    print (i)
    
    #定义游戏名,英文名,关注数,缩略图url,开发商,发行商,最早发售,中文发售,平台列表,游戏基因列表,官网链接,官方截图
    gameName = "/"
    gameEnlishName = "/"
    followNum = "/"
    imgDataUrl = "/"
    developerName = "/"
    publisherName = "/"
    earliestReleaseTime = "/"
    chineseReleaseTime = "/"
    platformList = []
    geneList = []
    lanuageList = []
    link = "/"
    imgOfficialUrlList = []
    editorWords = "/"
    aboutTheGame = "/"

    #定义code,url,html
    code = str(i)
    url = "https://www.vgtime.com/game/" + code +".jhtml"
    r = requests.get(url,headers=kv)
    html = r.text

    #使用BeautifulSoup解析
    soup = BeautifulSoup(html,'html.parser')

    #1找出game_box main的div块
    soupGameBoxMain = soup.find('div',attrs = {'class':'game_box main'})
    #游戏名、英文名
    try:
        soupGameBoxMain = str(soupGameBoxMain)
        gameName1 = re.findall(r'.jhtml">.*?</a></h2>',soupGameBoxMain)
        gameEnglishName1 = re.findall(r'<p>.*?</p>',soupGameBoxMain)
        gameName = gameName1[0].split('.jhtml">')[1].split('</a></h2>')[0]
        gameEnlishName = gameEnglishName1[0].split('<p>')[1].split('</p>')[0]
    except:
        continue

    #2找出game_box right的div块
    soupGameBoxRight = soup.find('div',attrs = {'class':'game_box right'})

    #2.1找出game_share的div块
    soupGameShare = soup.find('div',attrs = {'class':'game_share'})
    #关注数
    try:
        soupGameShare = str(soupGameShare)
        followNum1 = re.findall(r'>关注数 .*?</span>',soupGameShare)
        followNum = followNum1[0].split('>关注数 ')[1].split('</span>')[0]
    except:
        continue
    
    #2.2找出game_info_box的div块
    soupGameInfoBox = soup.find('div',attrs = {'class':'game_info_box'})
    #缩略图url
    try:
        soupGameInfoBoxImg = soupGameInfoBox.find('img')
        imgDataUrl = soupGameInfoBoxImg.get('data-url')
    except:
        continue
    
    
    #2.2.1找出game_descri的div块
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
                developer = re.findall(r'开发商',descriBox)
                publisher = re.findall(r'发行商',descriBox)
                earliestRelease = re.findall(r'最早发售',descriBox)
                chineseRelease = re.findall(r'中文发售',descriBox)
                
                #平台
                if platformName:
                    platformList1 = re.findall(r'>.*?</span>',descriBox)
                    for i in range(len(platformList1)):
                        platform = platformList1[i].split('>')[1].split('<')[0]
                        platformList.append(platform)

                #基因
                if geneName:
                    geneList1 = re.findall(r'>.*?</span>',descriBox)
                    for i in range(len(geneList1)):
                        gene = geneList1[i].split('>')[1].split('<')[0]
                        geneList.append(gene)

                #语言
                if lanuageName:
                    lanuageList1 = re.findall(r'>.*?</span>',descriBox)
                    for i in range(len(lanuageList1)):
                        lanuage = lanuageList1[i].split('>')[1].split('<')[0]
                        lanuageList.append(lanuage)

                #游戏官网
                if linkName:
                    link1 = re.findall(r'href=".*?"',descriBox)
                    link = link1[0].split('"')[1]

                #开发商
                if developer:
                    try:
                        developer1 = re.findall(r'>.*?</span>',descriBox)
                        developerName = developer1[0].split('>')[1].split('<')[0]
                    except:
                        developer1 = re.findall(r'>.*?</a>',descriBox)
                        developerName = developer1[0].split('>')[1].split('<')[0]

                #发行商
                if publisher:
                    try:
                        publisher1 = re.findall(r'>.*?</span>',descriBox)
                        publisherName = publisher1[0].split('>')[1].split('<')[0]
                    except:
                        publisher1 = re.findall(r'>.*?</a>',descriBox)
                        publisherName = publisher1[0].split('>')[1].split('<')[0]


                #最早发售
                if earliestRelease:
                    try:
                        earliestReleaseTime1 = re.findall(r'最早发售 .*?</span>',descriBox)
                        earliestReleaseTime = earliestReleaseTime1[0].split('最早发售 ')[1].split('</span>')[0]
                    except:
                        earliestReleaseTime1 = re.findall(r'>.*?</span>',descriBox)
                        earliestReleaseTime = earliestReleaseTime1[0].split('>')[1].split('<')[0]

                #中文发售
                if chineseRelease:
                    try:
                        chineseReleaseTime1 = re.findall(r'中文发售 .*?</span>',descriBox)
                        chineseReleaseTime = chineseReleaseTime1[0].split('中文发售 ')[1].split('</span>')[0]
                    except:
                        chineseReleaseTime1 = re.findall(r'>.*?</span>',descriBox)
                        chineseReleaseTime = chineseReleaseTime1[0].split('>')[1].split('<')[0]
                        
            except:
                continue
    except:
        continue

    '''
    #获取官方截图
    try:
        #3.1.2找出game_focus_lbox的div块
        soupGameFocusLbox = soup.find('div',attrs = {'class':'game_focus_lbox'})
        #3.1.2.1找出ul块
        soupGameFocusLboxUl = soupGameFocusLbox.find('ul')
        #官方截图
        for li in soupGameFocusLboxUl.children:
            liImg = li.find('img')
            liImg = str(liImg)
            imgOfficialUrl1 = re.findall(r'data-source=".*?" onerror',liImg)
            try:
                imgOfficialUrl = imgOfficialUrl1[0].split('data-source="')[1].split('" onerror')[0]
                imgOfficialUrlList.append(imgOfficialUrl)
            except:
                continue
    except:
        continue
    '''
    
    #获取编辑的话、关于游戏
    try:
        #3找出game_box main的div块
        soupGameBoxMainList = soup.find_all('div',attrs = {'class':'game_box main'})
        soupGameBoxMain2 = soupGameBoxMainList[1]
        #3.x找出section块
        for section in soupGameBoxMain2.children:
            try:
                section = str(section)
                editor = re.findall(r'编辑的话',section)
                forgame = re.findall(r'关于游戏',section)
                #编辑的话
                if editor:
                    editorWords1 = re.findall(r'tion">.*?</p>',section)
                    editorWords = editorWords1[0].split('tion">')[1].split('</p>')[0]
                #关于游戏
                if forgame:
                    aboutTheGame1 = re.findall(r'tion">.*?</p>',section)
                    aboutTheGame = aboutTheGame1[0].split('tion">')[1].split('</p>')[0]
            except:
                continue
    except:
        continue
    

    list.append([code,url,gameName,gameEnlishName,followNum,imgDataUrl,developerName,publisherName,earliestReleaseTime,chineseReleaseTime,platformList,geneList,lanuageList,link,imgOfficialUrlList,editorWords,aboutTheGame])


#打印到csv文件
title = ['code','url','游戏名','英文名','关注数','缩略图url','开发商','发行商','最早发售','中文发售','游戏平台','游戏基因','语言','游戏官网','官方截图','编辑的话','关于游戏']
test = pd.DataFrame(columns=title,data=list)
test.to_csv('Vgtime.csv',encoding='utf-8')


