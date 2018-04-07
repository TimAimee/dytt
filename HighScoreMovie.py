# -*-coding:utf-8-*-
# 中文注释要上面这行
import time
import os
import urllib2

from bs4 import BeautifulSoup

# 过滤标签，过滤分数
filter_tag = ''
filter_score = 7


# 保存路径
movie_url_dir = "E:\HighScoreMovie\\"
# 网页主页
url_host = 'http://www.dytt8.net'
# url_host = 'http://www.baidu.com'
# 电影传输协议
protrocl = 'ftp'


def getSoupFormUrl(url):
    """
    获取soup网页对象 \n
    :param url: 主机的地址\n
    :return: soup对象\n
    """
    # 加载网页的对象
    try:
        resp = urllib2.urlopen(url)
    except Exception:
        return None
    # 获取网页的对象
    html = resp.read()
    # BeautifulSoup
    soup = BeautifulSoup(html, "html.parser", from_encoding="gbk")
    return soup


def getAllHerfContent(url):
    """
    获取所有超链接的内容 \n
    :param url: 主机的地址\n
    :return: 所有超链接的内容\n
    """
    nameList = []
    soup = getSoupFormUrl(url)
    if soup == None:
        return nameList
    # 获取网页中所有的超链接
    nameList = soup.findAll("a")
    return nameList


def getHighScoreMovieList(url):
    """
    获取所有高分电影的超链接 \n
    :param url: 主机的地址\n
    :return: 所有高分电影的超链接\n
    """
    # 获取网页中所有的超链接
    nameList = getAllHerfContent(url)
    arr = []
    for movie_main_herf in nameList:
        # 获取超链接的内容
        if filter(movie_main_herf):
            herf = getReallyUrl(movie_main_herf, url)
            isExist = isHaveItem(arr, herf)
            if not isExist:
                arr.append(herf)
    return arr


def filter(movie_main_herf):

    no_game = "单机游戏"
    no_comic_animation = "动漫"
    no_main_american = "主打美剧"
    no_tv_play = "剧集"
    no_tv_play_china = "电视剧"
    no_tv_play_month = "月火剧"
    no_tv_play_king = "金土剧"
    no_tv_play_water = "水木剧"
    no_tv_play_weekden = "周末剧"
    no_tv_play_moring = "晨间剧"
    no_tv_play_dayday = "日日剧"
    no_herf_zongyi = "zongyi"
    no_herf_dongman = "dongman"

    """
    过滤高分电影的超链接 \n
    :param url: 主机的地址\n
    :return: 所有高分电影的超链接\n
    """
    # 获取网页中所有的超链接
    flag = False
    # 网页进行过滤
    unicode_partHtml = movie_main_herf.get('href')
    utf_8_partHtml = ""
    try:
        utf_8_partHtml = unicode_partHtml.encode("utf8")
    except Exception:
        print
    if no_herf_zongyi in utf_8_partHtml or no_herf_dongman in utf_8_partHtml:
        return flag

    # 内容进行过滤
    unicode_text = movie_main_herf.text
    utf_8_text = unicode_text.encode("utf8")
    if utf_8_text == '':
        return flag
    if no_game in utf_8_text or no_tv_play in utf_8_text or no_main_american in utf_8_text or no_comic_animation in utf_8_text or no_tv_play_china in utf_8_text or no_tv_play_month in utf_8_text or no_tv_play_king in utf_8_text or no_tv_play_water in utf_8_text or no_tv_play_weekden in utf_8_text or no_tv_play_moring in utf_8_text or no_tv_play_dayday in utf_8_text:
        return flag

    # 自行标签过滤
    if filter_tag != '':
        if filter_tag in utf_8_text:
            flag = True
        else:
            flag = False
    else:
        flag = True
    return flag


def isHaveItem(arr, url):
    """
    判断电影是否重复 \n
    :param arr: 超链接的数组\n
    :param url: 当前链接\n
    :return: 是否重复\n
    """
    flag = False
    for item in arr:
        if item == url:
            flag = True
            break
    return flag


def getReallyUrl(link, url):
    """
    判断电影是否重复 \n
    :param link: 链接的对象\n
    :param url: 主机的地址\n
    :return: 真实的电影地址\n
    """
    unicode_partHtml = link.get('href')
    utf_8_partHtml = url
    try:
        utf_8_partHtml = unicode_partHtml.encode("utf8")
    except Exception:
        print "------------>Error getReallyUrl encode=", utf_8_partHtml
        return utf_8_partHtml
    if not utf_8_partHtml.startswith("http"):
        utf_8_partHtml = url + utf_8_partHtml
    return utf_8_partHtml


def getDownloadFtp(nameList):
    """
    获取电影的ftp下载链接 \n
    :param nameList: 网页中所有的超链接\n
    :return: 电影的ftp下载链接\n
    """
    for link in nameList:
        # 获取超链接的内容
        unicode_text = link.text
        unicode_partHtml = link.get('href')
        try:
            utf_8_partHtml = unicode_partHtml.encode("utf8")
        except Exception:
            print "------------>Error getDownloadFtp encode =", utf_8_partHtml
            return ""
        if protrocl in utf_8_partHtml:
            return utf_8_partHtml


def saveFtpUrl(herf):
    """
    打印ftp的url \n
    :param herf: 主机网址\n
    """
    ftpUrlList = []
    movie_list = getHighScoreMovieList(herf)
    for high_score_main_herf in movie_list:
        score = getIMDbScore(high_score_main_herf)
        download_url = getAllHerfContent(high_score_main_herf)
        ftpUrl = getDownloadFtp(download_url)
        if isinstance(ftpUrl, str) and score >= filter_score:
            ftpUrlList.append(str(score))
            ftpUrlList.append(ftpUrl)
            ftpUrlList.append("")
            print score, ftpUrl
    print "一共", len(ftpUrlList) / 3, "部电影"
    if len(ftpUrlList) != 0:
        saveTofile(ftpUrlList)
    else:
        print "无内容"


def getIMDbScore(url):
    """
    获取电影的评分 \n
    :param herf: 电影的主链接\n
    :return: 电影的评分\n
    """
    score = 0.0
    soup = getSoupFormUrl(url)
    if soup == None:
        return score
    IMDbScore = "";
    findIMDbScoreSpan = soup.find_all('span', attrs={'style': 'FONT-SIZE: 12px'})
    for tag in findIMDbScoreSpan:
        htmToStr = tag.encode("utf8")
        start = htmToStr.find("评分")
        end = htmToStr.find("from")
        partContent = htmToStr[start + len("评分"):end]
        IMDbScore = blankValue(partContent).replace("/10", "")
        try:
            score = float(IMDbScore)
        except ValueError:
            print "------------>Error: 格式转换错误:",IMDbScore[0:10],url
    return score;


def blankValue(value):
    return value.replace(' 　', '').replace('　', '').replace('  ', '').replace(' ', '').replace(' ', '')


def saveTofile(ftpUrlList):
    """
     保存ftp的链接
     :param ftpUrlList: ftp的链接数组\n
     :return: 时间\n
     """
    if not os.path.exists(movie_url_dir):
        os.mkdir(movie_url_dir)
    filePath = movie_url_dir
    if filter_tag != "":
        filePath = filePath + "_";
    filePath = filePath + str(filter_score) + "分以上_" + getDateTime() + ".txt"
    print "saveTofile=", filePath
    fileObject = open(filePath.decode('utf-8'), 'w')
    for itemFtp in ftpUrlList:
        fileObject.write(itemFtp)
        fileObject.write('\n')
    fileObject.close()


def getDateTime():
    """
    获得当前时间时间戳
    :return: 时间\n
    """
    now = int(time.time())
    timeStruct = time.localtime(now)
    strTime = time.strftime("%Y_%m_%d_%H_%M_%S", timeStruct)
    return strTime


# 获取高分电影的内容
saveFtpUrl(url_host)
