import re
import requests
from time import sleep

num = 9
url = "https://www.shijuan1.com/a/sjyy6/list_609_" + str(num) + ".html"
domain = "https://www.shijuan1.com"
resp = requests.get(url)
resp.encoding = resp.apparent_encoding

obj = re.compile(r"<td width='52%' height='23'><a href=\"(?P<href>.*?)"
                 r"\" class=\"title\" target='_blank'>.*?<td width='10%'>人教版</td>", re.S)

obj2 = re.compile(r'<li><a href="(?P<download>.*?)" target="_blank"')

result = obj.finditer(resp.text)

# 定义一个爬虫进行子页面的爬取
child_href_list = []
for it in result:
    ul = it.group('href')
    child_href = domain + it.group('href')
    child_href_list.append(child_href)
    print(child_href_list)
# 提取子页面
for href in child_href_list:
    child_resp = requests.get(href)
    child_resp.encoding = child_resp.apparent_encoding
    result2 = obj2.search(child_resp.text, re.S)
    downloadadress = domain + result2.group('download')
    print(downloadadress)
    # 获取试卷
    img_resp = requests.get(downloadadress)
    img_picture_bite = img_resp.content  # 这里拿到的是字节
    img_name = downloadadress.split("/")[-1]  # 拿到url的最后一个/以后的内容
    with open(img_name, mode="wb") as f:
        f.write(img_picture_bite)  # 将字节写入到文件中
    print("over!", img_name)
    sleep(1)  # 为了防止服务器不把这个ip拉黑。模拟人工访问
