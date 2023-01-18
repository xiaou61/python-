#1.定位
#2.提取到子页面的链接地址
#3.请求子页面，拿到我们的下载地址
import re

import requests
domain="https://www.dytt89.com/"
resp=requests.get(domain,verify=False)#varify=False意思是去掉安全验证
resp.encoding='gb2312'

obj1=re.compile(r"2022必看热片.*?<ul>(?P<ul>.*?)</ul>",re.S)
obj2=re.compile(r"<a href='(?P<href>.*?)'",re.S)
obj3=re.compile(r'◎片　　名　(?P<movie>.*?)<br />.*?'
                r'<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="'
                r'(?P<download>.*?)">',re.S)

result1=obj1.search(resp.text)

child_href_list=[]#存储子页面列表
ul=result1.group('ul')

result2=obj2.finditer(ul)
for itt in result2:
    #拼接子页面：域名+子页面地址
    child_href=domain+itt.group('href').strip('/')#strip移除字符串头尾指定的字符
    child_href_list.append(child_href)
#提取子页面

for href in child_href_list:
    child_resp=requests.get(href,verify=False)
    child_resp.encoding=child_resp.apparent_encoding
    result3=obj3.search(child_resp.text)
    print(result3.group('movie'))
    print(result3.group('download'))

