from bs4 import BeautifulSoup
from selenium import webdriver
import urllib2
import bt2mag
import time

numberList = []
driver = webdriver.PhantomJS()
for index in range(1,7):
    strUrl = "http://www.javmoo.xyz/cn/star/6qd/currentPage/"+str(index)
    print strUrl
    response = urllib2.urlopen(strUrl)
    html = response.read()
    soup = BeautifulSoup(html,"html.parser")
    result = soup.find_all(name="date")
    time.sleep(3)
    for indexForDate in range(0,len(result)):
        if indexForDate%2 == 0:
            strResult = result[indexForDate]
            iStart = str(strResult).find('<date>',0)+6
            iEnd = str(strResult).find('</date>',0)
            strResult = str(strResult)[iStart:iEnd]
            numberList.append(strResult)
    for number in numberList:
        if(bt2mag.FindMagnet(number,driver) == False):
            print "didn't find                       " + str(number)
driver.close()