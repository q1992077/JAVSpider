from selenium import webdriver
from bs4 import BeautifulSoup
import time

def getMagnet(rowArray, list, driver):
    for passOne in list:
        bPass = False
        for row in rowArray:
            if (str(row).find(str(passOne)) >= 0):
                bPass = True
                break
        if (bPass):
            iStart = str(row).find('href=', 0) + 6
            iEnd = str(row).find('title', 0) - 2
            strResult = str(row)[iStart:iEnd]
            time.sleep(3)
            driver.get(strResult)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            magnet = soup.textarea
            if (str(magnet).find('None') < 0):
                print magnet.string
            else:
                print "error~!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                print rowArray
                print row
                print strResult
                print magnet
                bPass = False
            break

    return bPass

def FindMagnet(strNumber, driver):
    strUrl = "http://www.bt2mag.com/search/" + strNumber
    listHightQuality = ['.1080p', '.720p', '[1080p]', '[720p]', '-1080p','-720p','[FHD]', '-FHD', '[Thz.la]']
    listOrdinaryQuality = [strNumber + '.mp4', str(strNumber).lower() + '.mp4',strNumber + '.avi',str(strNumber).lower() + '.avi','@SIS001@',strNumber,str(strNumber).lower()]
    time.sleep(3)
    driver.get(strUrl)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    rowArray = soup.find_all(name='a',attrs={'class':''})
    bPass = False

    bPass = getMagnet(rowArray, listHightQuality, driver)
    if (bPass == False):
        bPass = getMagnet(rowArray, listOrdinaryQuality, driver)

    return bPass