import threading,sys,os
try:
    import requests
except ImportError:
    os.system("pip install requests")
    print("安装完后报错请重新运行")
    import requests
arg=[""]
def do():
    for _ in range(int(arg[1])):
        r=requests.get(
            f"https://lv.dingtalk.com/interaction/createLike?uuid={arg[3]}&count=100").content
        if r==b"success":print(f"成功")

if len(sys.argv)==1:
    print("钉钉刷赞 @aquamarine5")
    print("最后点赞数 = 单次刷赞次数 * 刷赞频率 * 100 ")
    t=input("单次刷赞次数: ")
    c=input("刷赞频率: ")
    uuid=input("钉钉直播LiveUUID (自查或询问) : ")
    arg=["",t,c,uuid]
else: arg=sys.argv
for i in range(int(arg[2])):
    threading.Thread(target=do).start()


