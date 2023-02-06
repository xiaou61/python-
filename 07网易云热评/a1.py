# 1.找到未加密的参数   windos.arsea(参数,xxxx,xxx)
# 2.想办法把参数进行加密，参考网易的逻辑进行加密 params=>encText，encSecKey=>encSecKey
# 3.请求到网易，拿到评论信息
from Crypto.Cipher import AES
from base64 import b64encode
import json
url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="
# 请求方式是post
data = {
    "csrf_token": "",
    "cursor": "-1",
    "offset": "0",
    "orderType": "1",
    "pageNo": "1",
    "pageSize": "20",
    "rid": "R_SO_4_496370620",
    "threadId": "R_SO_4_496370620"
}
e="010001"
f="00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
g="0CoJUm6Qyw8W8jud"
#处理加密过程
#下面是加密的函数
#入口是这个d
i="hwafcLoZwSYTZ0xO";
#这里把i定死
def get_encSecKey():
    return "6bb616ed74dc86f70ef67ccaa83797d348ae31a515e5109fec18ed5831d0b6209a37bea849519d807ced57c8147b"
def get_params(data):#默认这个收到的是字符串
    first= enc_params(data,g)
    second= enc_params(first,i)
    return second#返回的就是params
def to_16(data):
    pad=16-len(data) %16
    data+=chr(pad)*pad
    return data
def enc_params(data,key):#加密过程
    iv="0102030405060708"
    data=to_16(data)
    aes= AES.new(key=key.encode("utf-8"),IV=iv.encode("utf-8"),mode=AES.MODE_CBC)#创造加密器
    bs=aes.encrypt(data.encode("utf-8"))#加密,加密的内容的长度必须是16的倍数
    return str(b64encode(bs))#转换成字符串返回
"""
 function a(a) {#a:随机产生16个字符串
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)#循环16次，
            e = Math.random() * b.length,#随机数
            e = Math.floor(e),#取整
            c += b.charAt(e);#取字符串中的某某位置
        return c
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) { d：数据 e：010001，f:很长    
    
        var h = {}#空对象
          , i = a(16);#i就是一个16位的随机值
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),#返回的就是params
        h.encSecKey = c(i, e, f),#得到的就是encSecKey#这里的e和f是固定的，但是i是随机的
        
        h
    }
"""
import requests
resp=requests.post(url,data={
    "params":get_params(json.dumps(data)),
    "encSecKey":get_encSecKey()
})
print(resp.text)
