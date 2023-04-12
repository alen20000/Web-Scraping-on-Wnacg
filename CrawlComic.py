'''
Wnacg爬蟲
'''

import requests
import os 
from bs4 import BeautifulSoup


# r定位路徑，防止被轉義
path = r'C:\Users\Cliff\Desktop\Craw from Wnacg'  
  # 漫畫頁數

def GetTitle_CreatFolder():

    re = requests.get(Main_Page)
    soup = BeautifulSoup(re.text,'html.parser')
    global title_word
    title_word = soup.find(id="bodywrap", class_="userwrap") # Get the title of manga
    title_word = title_word.h2.text
    print ('Name of Manga is', title_word)
    global path_of_manga
    path_of_manga = path + '\\' + title_word
    if not os.path.isdir(path_of_manga): #判斷路徑目標資料夾是否存在
        os.makedirs(path_of_manga)       #不存在則建立



def EnterTheCover(): #進入第一頁圖片頁

    re = requests.get(Main_Page)
    soup = BeautifulSoup(re.text,'html.parser')
    ExtractSoup = soup.find(class_="pic_box tb")
    ExtractURL = ExtractSoup.a['href']
    global PageURL
    PageURL = 'https://www.wnacg.org' + ExtractURL

def ExtactPic():#提取圖片網址

    re= requests.get(PageURL)
    soup = BeautifulSoup(re.text, 'html.parser')
    ExtractSoup = soup.span.a.img['src']
    global ImgURL
    ImgURL = 'http:' + ExtractSoup
    print('提取網址圖片,網址為',ImgURL)

def SaveImage(): #儲存圖片
    global PageCounter
    global countID
    global PageURL
    GetImage = requests.get(ImgURL)
    Image = GetImage.content # 將提取資料轉成二進位制
    ImageName = countID + '.png'
    Imagesave = open(path_of_manga + '\\'+ImageName,'wb')
    Imagesave.write(Image)
    Imagesave.close()
    print('Finished page',PageCounter)
    PageCounter += 1
    countID = '{:04d}'.format(PageCounter)

def NextPage(): #進入下一頁圖片頁
    global PageURL
    re = requests.get(PageURL)
    soup = BeautifulSoup(re.text,'html.parser')
    ExtractSoup = soup.find("a", class_ = "btntuzao", text = "下一頁")
    PageURL = 'https://www.wnacg.org' + ExtractSoup['href']
    print('下一頁網址:',PageURL)


def totalpage(): #計算總共幾頁
    re = requests.get(Main_Page)
    soup = BeautifulSoup(re.text,'html.parser')

Main_Page = input('請輸入爬蟲網址:') # 主頁
totalpage = int(input('請輸入爬取頁數:'))

PageCounter = 1 
countID = '{:04d}'.format(PageCounter)

GetTitle_CreatFolder() #創建
EnterTheCover()#進入第一張圖片頁面
ExtactPic()#提取圖片
SaveImage()#儲存圖片

for i in range(1,totalpage):
    NextPage()
    ExtactPic()#提取圖片
    SaveImage()#儲存圖片
    
