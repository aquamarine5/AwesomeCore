import math,time
import requests
from sys import argv
from commandCompiler import EasyCommandCompiler
URL_VIDEO_VIEW="http://api.bilibili.com/x/web-interface/view?bvid=%s"
URL_USER_HISTORY="https://api.bilibili.com/x/web-interface/history/cursor?view_at=%s"
class BilibiliConfig:
    @staticmethod
    def self_token():
        return {"SESSDATA":""}
class BilibiliUser:
    def __init__(self,uid:int) -> None:
        self.uid=uid
    def analyse(self):
        w=requests.Session()
        w.cookies.set("SESSDATA","/",domain="bilibili.com")
        print(w.cookies)
        def post_view_requests(view:int):
            return w.get(URL_USER_HISTORY%view).json()
        
class BilibiliVideo:
    def __init__(self, bvid: str) -> None:
        self.content:dict=requests.get(URL_VIDEO_VIEW%bvid).json()["data"]
        self.av:int=self.content["aid"]
        self.bvid=bvid
        self.cid:int=self.content["cid"]
        self.cover:str=self.content["pic"]
        self.desc:str=self.content["desc"]
        self.title:str=self.content["title"]
        self.owner=BilibiliUser(self.content["owner"]["mid"])
    @staticmethod
    def bv2av(bvid: str) -> int:
        keys = {
            '1': '13', '2': '12', '3': '46', '4': '31', '5': '43', '6': '18', '7': '40', '8': '28', '9': '5',
            'A': '54', 'B': '20', 'C': '15', 'D': '8', 'E': '39', 'F': '57', 'G': '45', 'H': '36', 'J': '38', 'K': '51',
            'L': '42', 'M': '49', 'N': '52', 'P': '53', 'Q': '7', 'R': '4', 'S': '9', 'T': '50', 'U': '10', 'V': '44',
            'W': '34', 'X': '6', 'Y': '25', 'Z': '1',
            'a': '26', 'b': '29', 'c': '56', 'd': '3', 'e': '24', 'f': '0', 'g': '47', 'h': '27', 'i': '22', 'j': '41',
            'k': '16', 'm': '11', 'n': '37', 'o': '2','p': '35', 'q': '21', 'r': '17', 's': '33', 't': '30', 'u': '48',
            'v': '23', 'w': '55', 'x': '32', 'y': '14','z': '19'}
        b=[]
        p=[6,2,4,8,5,9,3,7,1,0]
        for _,v in enumerate(bvid[2:]):
            b.append(int(keys[v]))
        b2=[int(b[i]*math.pow(58,p[i])) for i in range(10)]
        s=0
        for i in b2:
            s+=i
        s-=100618342136696320
        return s^177451812
    
    @staticmethod
    def bv2av_cc(bvid:str):
        print(BilibiliVideo.bv2av(bvid))
BilibiliUser(1).analyse()
cc=EasyCommandCompiler({
    1:{
        "bv2av":(BilibiliVideo.bv2av_cc,[str])
    }
})
cc.compiled(argv)