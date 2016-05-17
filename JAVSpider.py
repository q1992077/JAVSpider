from bs4 import BeautifulSoup
from selenium import webdriver
import socket
import bt2mag
import time

numberList = []
errorNumberList = []
magnetList = []
driver = webdriver.Firefox()
socket.setdefaulttimeout(200)
time.sleep(20)
fo = open('linyounai.txt','wb+')
for index in range(1,2):
    strCurrentPage = "/currentPage/" + str(index)
    strUrl = "https://avmo.pw/cn/star/89n" + strCurrentPage
    print strUrl
    # response = urllib2.urlopen(strUrl)
    # html = response.read()
    try:
        driver.get(strUrl)
    except socket.timeout:
        print "time out"
    try:
        soup = BeautifulSoup(driver.page_source, "html.parser")
    except Exception as err:
        print "error ------------------------------------------- " + strUrl
    result = soup.find_all(name="date")
    time.sleep(2)
    for indexForDate in range(0,len(result)):
        if indexForDate%2 == 0:
            strResult = result[indexForDate]
            iStart = str(strResult).find('<date>',0) + 6
            iEnd = str(strResult).find('</date>',0)
            strResult = str(strResult)[iStart:iEnd]
            numberList.append(strResult)
    for number in numberList:
        magnet = bt2mag.FindMagnet(number,driver,1)
        if(len(magnet) <= 0):
            errorNumberList.append(number)
        else:
            if(len(magnet) > 5):
                magnetList.append(magnet)
    numberList = []
reStartList = errorNumberList
errorNumberList = []
for error in reStartList:
    magnet = bt2mag.FindMagnet(error,driver,2)
    if(len(magnet) <= 0):
        errorNumberList.append(error)
    else:
        if(len(magnet) > 5):
            magnetList.append(magnet)

for magnetOne in magnetList:
    fo.write(magnetOne + "\n")

for error in errorNumberList:
    print error

fo.close()
driver.close()