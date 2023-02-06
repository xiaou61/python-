#-*- coding: utf-8 -*-


import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
import json
#from multiprocessing import Pool#多进程池
import time
import math

def get_response(limit,offset,dtime,musicid):
    #参数
    para = {
        'limit':limit, #总数限制
        'offset':offset, #页数
        'before':dtime #每页最后一条评论的时间，携带该参数可绕过1000条限制
    }
    
    #歌曲api地址
    musicurl = "http://music.163.com/api/v1/resource/comments/R_SO_4_"+musicid+"?"+urlencode(para)
    # musicurl = "https://jiangjiangjiang-api.vercel.app/comment/music?id="+musicid+"&"+urlencode(para)
   
    #头结构
    headers = {
        #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'NMTID=00O2_bWHuAAxmGmJ0r6gziH_of9RFIAAAGBYfSoiw',
        #'Cookie':'vjuids=-13ac1c39b.1620457fd8f.0.074295280a4d9; vjlast=1520491298.1520491298.30; _ntes_nnid=3b6a8927fa622b80507863f45a3ace05,1520491298273; _ntes_nuid=3b6a8927fa622b80507863f45a3ace05; vinfo_n_f_l_n3=054cb7c136982ebc.1.0.1520491298299.0.1520491319539; __utma=94650624.1983697143.1521098920.1521794858.1522041716.3; __utmz=94650624.1521794858.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; JSESSIONID-WYYY=FYtmJTTpVwmbihVrUad6u76CKxuzXZnfYyPZfK9bi%5CarU936rIdoIiVU50pfQ6JwjGgBvSyZO0%2FR%2BcoboKdPuMztgHCJwzyIgx1ON4v%2BJ2mOvARluNGpRo6lmhA%5CfcfCd3EwdS88sPgxpiiXN%5C6HZZEMQdNRSaHJlcN%5CXY657Faklqdh%3A1522053962445; _iuqxldmzr_=32',
        #'Host':'music.163.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    }
    #代理IP
    proxies= {
        'http:':'http://121.232.146.184',
        'http:':'http://120.42.46.226:6666',
        'http:':'118.190.146.252:80',
        'http:':'101.34.55.147:8001',
        'https:':'https://144.255.48.197'
    }
    try:
        response = requests.post(musicurl,headers=headers,proxies=proxies)
        
        if response.status_code == 200:
           #return response.content
           return response.json()
    except RequestException:
        print("访问出错")

#解析返回页
def parse_return(html,page,songname):
    #data = json.loads(html)#将返回的值格式化为json
    data = html
    
    filename = songname + ".txt"
    with open(filename,"a",encoding="utf-8") as f:
        if data.get('hotComments'):
            hotcomm = data['hotComments']
            f.write("-------------------------------------------------------------------这是热门评论-------------------------------------------------------------------------\n")
            for hotitem in hotcomm:
                hotdata = {
                    '用户名': hotitem['user']['nickname'],
                    #'用户头像': hotitem['user']['avatarUrl'],
                    '评论': hotitem['content'],
                    '赞':hotitem['likedCount']
                }
                f.write(json.dumps(hotdata,ensure_ascii=False))
                f.write("\n")
        # else:
        #     print('--------------------------------------------------')
        if data.get('comments'):
            f.write("-------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            comm = data['comments']
            for item in comm:
                data = {
                    '用户名': item['user']['nickname'],
                    #'用户头像': item['user']['avatarUrl'],
                    '评论': item['content'].replace('\r', ' '),
                    '赞': item['likedCount']
                }
                f.write(json.dumps(data,ensure_ascii=False))
                f.write("\n")
                pagetime=item['time']
                #print(pagetime)
            f.write('----------------------------------------------------------------------第{}页--------------------------------------------------------------------------\n'.format(page))
            return pagetime

def main():
    # 歌曲id
    musicid = "496370620"  # That's Us
    #歌曲名
    songname = "断线"

    pagetime = 0 #初始时间为0
    #time_str = "2022-03-18 10:54:00" #到该时间
    #time_stamp = time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S'))
    page = 1 #第一页
    gethtml = get_response(100,0,pagetime,musicid)
    #parse_return(gethtml,page)
    pagetime = parse_return(gethtml,page,songname)
    # 评论总数
    total = gethtml['total']
    # 总页数
    pages = math.ceil(total / 100)
    print("评论总数:{}\n".format(total))
    print("每页100条，评论页数:{}\n".format(pages))
    #想要抓取的页数
    
    pages = 10
    print("开始抓取...")
    time.sleep(2)
    print("已抓取1页！") 


    page = 2 #从第二页开始
    while page <= pages:
        print("已抓取{}页！".format(page))
        gethtml = get_response(100,0,pagetime,musicid)
        pagetime = parse_return(gethtml,page,songname)
        
        page += 1
    #with open("dict.txt","a") as f:
     #   print(f.write(output))
    print("完成ok!")

if __name__ == '__main__':
    # groups = [x*20 for x in range(0,20)]
    # pool = Pool()
    # pool.map(main,groups)
    main()