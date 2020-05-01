import requests
from bs4 import BeautifulSoup
import urllib.request
import os,sys
from tqdm import tqdm

#By default resolution of the image will be the maximum available; If you need to download the lowest resolutions available

def GetURLs():      #This is to get level one urls from the main wallpaper web page
    plain_text = open("wallpapers.html", encoding="utf8")
    soup = BeautifulSoup(plain_text, "html.parser")
    m = soup.select("a[class=link-block]")
    f=open("lvl_1_urls.txt", "w")
    for i in m:
        f.write(i.get("href")+"\n")
    f.close()
    plain_text.close()

def down_pics():
    #GetURLs()
###At this point we have level 1 links in the text file names "lvl_1_urls.txt"
###We need to download the web pages manually. OR you can download it from my project folder

###In the below section, we make sure that we do not get any kind of errors [Especially. 403 Forbidden error]
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

###List containing images link[part of link] with best resolution available and least resolution available
    best_res_list=[]
    least_res_list=[]

###Obtaining the current path of your directory in which this particular python file is present
    CUR_PATH = os.path.abspath(os.curdir)

###We have all our html files inside html folder
    hts = os.listdir(CUR_PATH+"\\html")
    os.chdir(CUR_PATH+"\html")
    loop = tqdm(total=len(hts), position=0, leave=False)
    for html in hts:        ###goes through every html files
        loop.set_description("Downloading...".format(html))
        PATH=CUR_PATH+"\\images\\"+html.split(".")[0]
        if not os.path.exists(PATH):
            os.makedirs(PATH)
        ind = 0
        htm = open(html, "r")
        souup = BeautifulSoup(htm, 'html.parser')
        x = souup.select("div[class=size] select")
        names_ = souup.select("h3[class=title]")
        names=[]
        for n in names_:
            names.append(n.getText().replace("\"", "").replace("?", ""))
        for y in x:
            list_values = []
            list_pixels=[]
            res_pix=[]
            z = y.select("option")
            for zz in z:
                val = zz.get("value")
                if val:
                    if val.isdigit():
                        list_values.append(int(val))
                        list_pixels.append(int(zz.getText().split("*")[0])*int(zz.getText().split("*")[1]))
                        res_pix.append(zz.getText())
            maxx=list_values[list_pixels.index(max(list_pixels))]
            minn=list_values[list_pixels.index(min(list_pixels))]
            best_res_pix = res_pix[list_pixels.index(max(list_pixels))].replace(" * ", "x")
            best_res_list.append(maxx)
            least_res_list.append(minn)
            IMG_NAME = names[ind]+ " "+ best_res_pix +".jpg"
            src = "https://rog.asus.com/wallpapers-list.aspx?action=download&id=" + str(maxx)
            if IMG_NAME not in os.listdir(PATH):
                urllib.request.urlretrieve(src, PATH + "\\"+IMG_NAME)
                print(PATH + "\\"+IMG_NAME)
            ind=ind+1
        loop.update(1)

down_pics()
