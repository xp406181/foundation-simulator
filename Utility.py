import urllib.request
import urllib
import re
import json
import time


def DownloadHtml(url, defaultName):
    response = urllib.request.urlopen(url)
    htmlText = response.read()
    htmlText = htmlText.decode()

    print("下载完成,url:{0}".format(url))

    searchObj = re.search(r"<title>(.*)?</title>", htmlText)
    if searchObj:
        fileName = searchObj.group(1) + ".txt"
    else:
        fileName = defaultName

    with open(fileName, "w") as f:
        f.write(htmlText)
        print("写入完成,fileName:{0}".format(fileName))
        return
    print("写入失败,fileName:{0}".format(fileName))


def DownloadFoundationHtml(foundationCode):
    url = "http://fund.10jqka.com.cn/{0}/historynet.html#historynet".format(
        foundationCode)
    DownloadHtml(url, str(foundationCode))


def SaveHistoryNetValue(fileName):
    with open(fileName, "r") as f:
        text = f.read(-1)
        searchObj = re.search(r"JsonData = (.*)?;", text)
        if searchObj:
            historyData = searchObj.group(1)
            fileName = "JsonData" + fileName
            with open(fileName, "w") as df:
                df.write(historyData)
                print("JsonData保存完毕,fileName:{0}".format(fileName))
                return
    print("JsonData保存失败,fileName:{0}".format(fileName))


def GetDateDiff(date1, date2):
    tuple1 = time.strptime(date1, "%Y-%m-%d")
    t1 = time.mktime(tuple1)

    tuple2 = time.strptime(date2, "%Y-%m-%d")
    t2 = time.mktime(tuple2)

    seconds = abs(t2 - t1)
    m, _ = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    # print(d, h, m, s)
    return int(d)


def GetSellCharge(day):
    if day < 7:
        return 0.015
    elif day < 365:
        return 0.005
    elif day < 730:
        return 0.0025
    else:
        return 0.0


def GetBuyCharge(money):
    if money < 1000000:
        return 0.0015
    elif money < 5000000:
        return 0.0012
    elif money < 10000000:
        return 0.0003
    else:
        return 0.0


def GetChargeRatio(bc, sc):
    return (1 - sc)/(1 + bc)


if __name__ == "__main__":
    # CompareDate("2016-02-1", "2016-3-1")
    pass
