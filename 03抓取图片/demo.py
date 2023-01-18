#1.拿到主页面的源代码。提取子页面。找到herf的值
#2.通过herf拿到子页面的内容。从子页面中找到图片的下载地址。
#3.下载图片
import time

import requests
from bs4 import BeautifulSoup
url="https://www.umei.cc/bizhitupian/weimeibizhi/"
resp=requests.get(url)
resp.encoding=resp.apparent_encoding


#把源代码交给bs
main_page=BeautifulSoup(resp.text,"html.parser")
alist=main_page.find("div",class_="item_list infinite_scroll").find_all("a")

for a in alist:
    href="https://www.umei.cc"+(a.get('href'))#直接通过get就可以拿到属性的值
    #拿到子页面的源代码
    child_page_resp=requests.get(href)
    child_page_resp.encoding=child_page_resp.apparent_encoding
    child_page_text=child_page_resp.text

    #从子页面拿到图片下载途径

    child_page=BeautifulSoup(child_page_text,"html.parser")
    div=child_page.find("div",class_="big-pic")
    img=div.find("img")
    src=img.get("src")
    print(src)

    #下载图片
    img_resp=requests.get(src)
    img_picture_bite=img_resp.content#这里拿到的是字节
    img_name=src.split("/")[-1]#拿到url的最后一个/以后的内容
    with open(img_name,mode="wb") as f:
        f.write(img_picture_bite)#将字节写入到文件中
    print("over!",img_name)
    time.sleep(1)#为了防止服务器不把这个ip拉黑。模拟人工访问

print("all over")