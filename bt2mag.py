from bs4 import BeautifulSoup
import time
import socket
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')
socket.setdefaulttimeout(200)
def getMagnet(rowArray, strNumber, list, driver):
    # bBool = False
    for passOne in list:
        bPass = ""
        for row in rowArray:
            arrSize = row.find_all(name = 'div',attrs = {'class':'col-xs-12 size-date visible-xs-block' })
            size = arrSize[0].string
            iEnd = size.find('GB')
            fSize = float(size[5:iEnd])
            if ((fSize > 3.0) and (fSize < 10.0)):
                title =  row['title']
                strinfo = re.compile('-')
                _strNumber = strinfo.sub('_',strNumber)
                if (title.find('DVD') < 0 and title.find('@') < 0 and title.find('iso') < 0 and (title.find(strNumber) > 0 or title.find(_strNumber))):
                    # bBool = True
                    bPass = "pass"
                    break
            if (str(row['title']).find(str(passOne)) > 0):
                bPass = "pass"
                break
        # if (bBool):
        #     break
        if (len(bPass) > 1):
            strResult = row.get('href')
            time.sleep(2)
            try:
                driver.get(strResult)
            except socket.timeout:
                print "time out"
            try:
                soupForMagnet = BeautifulSoup(driver.page_source, "html.parser")
            except Exception as err:
                print "error ++++++++++++++++++++++++++++++ " + strResult
                return ""
            magnet = soupForMagnet.textarea
            if (str(magnet).find('None') < 0):
                return magnet.string
            else:
                print "error~!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                print rowArray
                print row
                print strResult
                print magnet
                bPass = ""
            break

    return bPass

def FindMagnet(strNumber, driver,iQuality):
    strUrl = "https://btio.pw/search/" + strNumber
    listHightQuality = ['.1080p', '.720p', '[1080p]', '[720p]', '-1080p','-720p','[FHD]', '-FHD', '[Thz.la]','[HD]','(720)','(1080)',strNumber + '-HD','-FULLHD' ,'_FHD','_HD']
    listOrdinaryQuality = [strNumber + '.mp4', str(strNumber).lower() + '.mp4',strNumber + '.avi',str(strNumber).lower() + '.avi','@SIS001@']
    time.sleep(2)
    try:
        driver.get(strUrl)
    except socket.timeout:
        print "time out"

    try:
        soupForSearch = BeautifulSoup(driver.page_source, "html.parser")
    except Exception as err:
        print "error ==================== " + strUrl
        return ""

    aArray = []
    dataListArray = soupForSearch.find_all(name='div',attrs={'class':'data-list'})
    if(len(dataListArray) <= 0):
        return "null"
    for dataList in dataListArray:
         rowArray = dataList.find_all(name = 'div',attrs = {'class':'row'})
         for row in rowArray:
             sizeArray = row.find_all(name = 'div',attrs = {'class':'col-sm-2 col-lg-1 hidden-xs text-right size'})
             for size in sizeArray:
                 strSize = size.string
                 if (str(strSize).find('GB') > 0):
                     aArr = row.find_all(name = 'a')
                     if(aArr.count > 0):
                         aArray.extend(aArr)
    if(int(iQuality) == 1):
        bPass = getMagnet(aArray, strNumber , listHightQuality, driver)
    elif(int(iQuality) == 2):
        bPass = getMagnet(aArray, strNumber , listOrdinaryQuality, driver)
    return bPass