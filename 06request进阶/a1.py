import requests

# 会话
session = requests.session();
# 登录
data = {
    "loginName": "17713088356",
    "password": "yuhongge0"
}
url = "https://passport.17k.com/ck/user/login"
session.post(url, data=data)
# print(resp.cookies)这里可以看到是有cookies的
# 拿到数据
# 刚才那个session中是有cookies的
resp = session.get("https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919")
print(resp.json())
