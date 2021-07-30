import math
import os
import subprocess
import time
from sys import argv
from typing import Any, Dict, List, Optional, Tuple
from util import progresser_download

import requests

# github.com/AwesomeCore -> commandCompiler.py
from commandCompiler import EasyCommandCompiler
# github.com/AwesomeCore -> config.py
from config import BaseConfig, BaseConfigUser
# github.com/AwesomeCore -> ffmpeg.py
from ffmpeg import FFMpegCommandCollection, FFMpegController
# github.com/AwesomeCore -> progress.py
from progress import ValuedProgresser

URL_VIDEO_VIEW = "http://api.bilibili.com/x/web-interface/view?bvid=%s"
URL_VIDEO_PLAYURL = "https://api.bilibili.com/x/player/playurl?cid=%s&otype=json&type=&quality=16&qn=16&fnver=0&fnval=16&bvid=%s"
URL_USER_HISTORY = "https://api.bilibili.com/x/web-interface/history/cursor?view_at=%s"


class BilibiliConfigUser(BaseConfigUser):
    def __init__(self, id: int, isDefault: bool, nickName: str, sessdata: str) -> None:
        self.id = id
        self.sessdata = sessdata
        self.nickName = nickName
        super().__init__(id, isDefault=isDefault,
                         **{"SESSDATA": sessdata, "nickName": nickName})

    def toCookie(self) -> str:
        return f"SESSDATA={self.sessdata}"

    def toUser(self) -> str:
        return f"{self.nickName}({self.id}) SESSDATA:{self.sessdata}"

    @classmethod
    def createWithDict(cls, dt: Dict[str, Any]):
        return cls(dt["id"], dt["isDefault"], dt["nickName"], dt["SESSDATA"])


class BilibiliConfigBase(BaseConfig):
    def __init__(self) -> None:
        super().__init__("Bilibili.json", BilibiliConfigUser)

    def login(self, data: BilibiliConfigUser):
        return super().login(data)

    def login_cc(self, id: int, sessdata: str):
        u = BilibiliConfigUser(
            id, self.get_all_config() == [], "", sessdata)
        self.login(u)
        print(f"登录成功 ,", u.toUser())

    def get_config(self, id: int) -> BilibiliConfigUser:
        return super().get_config(id)

    def get_all_config(self) -> List[BilibiliConfigUser]:
        return super().get_all_config()

    def get_default_config(self) -> BilibiliConfigUser:
        return super().get_default_config()


BilibiliConfig: BilibiliConfigBase = BilibiliConfigBase()


class BilibiliVideo:
    def __init__(self, bvid: str) -> None:
        self.content: dict = requests.get(URL_VIDEO_VIEW % bvid).json()
        if self.content["code"] == 62002 or self.content["code"] == -404:
            self.time = 0
            return
        try:
            self.content = self.content["data"]
        except KeyError as e:
            print(self.content)
            print(bvid)
            raise e
        self.av: int = self.content["aid"]
        self.bvid = bvid
        self.cid: int = self.content["cid"]
        self.cover: str = self.content["pic"]
        self.desc: str = self.content["desc"]
        self.time: int = self.content["duration"]
        self.title: str = self.content["title"]
        self.owner = BilibiliUser(self.content["owner"]["mid"])

    @staticmethod
    def bv2av(bvid: str) -> int:
        keys = {
            '1': '13', '2': '12', '3': '46', '4': '31', '5': '43', '6': '18', '7': '40', '8': '28', '9': '5',
            'A': '54', 'B': '20', 'C': '15', 'D': '8', 'E': '39', 'F': '57', 'G': '45', 'H': '36', 'J': '38', 'K': '51',
            'L': '42', 'M': '49', 'N': '52', 'P': '53', 'Q': '7', 'R': '4', 'S': '9', 'T': '50', 'U': '10', 'V': '44',
            'W': '34', 'X': '6', 'Y': '25', 'Z': '1',
            'a': '26', 'b': '29', 'c': '56', 'd': '3', 'e': '24', 'f': '0', 'g': '47', 'h': '27', 'i': '22', 'j': '41',
            'k': '16', 'm': '11', 'n': '37', 'o': '2', 'p': '35', 'q': '21', 'r': '17', 's': '33', 't': '30', 'u': '48',
            'v': '23', 'w': '55', 'x': '32', 'y': '14', 'z': '19'}
        b = []
        p = [6, 2, 4, 8, 5, 9, 3, 7, 1, 0]
        for _, v in enumerate(bvid[2:]):
            b.append(int(keys[v]))
        b2 = [int(b[i]*math.pow(58, p[i])) for i in range(10)]
        s = 0
        for i in b2:
            s += i
        s -= 100618342136696320
        return s ^ 177451812

    @staticmethod
    def bv2av_cc(bvid: str):
        print(BilibiliVideo.bv2av(bvid))

    def download(self, path: str = ".", quality: int = 80):
        def get_ffmpeg_path() -> Optional[str]:
            if FFMpegController.check_is_installed():
                return FFMpegController.get_ffmpeg().path
            else:
                print("没有安装ffmpeg，可用ffmpeg-bind绑定或ffmpeg-download在线下载")
                return None

        def is_overwrite_file(path: str) -> bool:
            if os.path.exists(path):
                absPath = os.path.abspath(path)
                questionResult = input(f"{absPath} 已经存在，是否覆盖? [y/n] > ")
                if questionResult == "y":
                    os.remove(absPath)
                    return True
                elif questionResult == "n":
                    print("已终止")
                    return False
                else:
                    return is_overwrite_file(path)
            else:
                return True
        header = {
            "Referer": "http://player.bilibili.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55"
        }
        if (ffmpegPath := get_ffmpeg_path()) == None:
            return
        playc = requests.get(URL_VIDEO_PLAYURL % (self.cid, self.bvid)).json()
        playcd = playc["data"]
        if quality not in playcd["accept_quality"]:
            raise ValueError()
        if quality == 116:
            raise ValueError()
        basePath = f"{path}/{self.bvid}"
        qualityIndex = playcd["accept_quality"].index(quality)
        qualityDesc = playcd["accept_description"][qualityIndex]
        videoDash = playcd["dash"]["video"][qualityIndex]
        videoUrl: str = videoDash["baseUrl"]
        videoType = videoUrl.split("?")[0].split(".")[-1:][0]
        videoPath = f"{basePath}_video.{'mp4' if videoType=='m4s' else videoType}"
        audioDashList = {i["id"]-30200: i for i in playcd["dash"]["audio"]}
        if quality in audioDashList:
            audioDash = audioDashList[quality]
        else:
            audioDash = audioDashList[80]
        audioUrl: str = audioDash["baseUrl"]
        audioType = audioUrl.split("?")[0].split(".")[-1:][0]
        audioPath = f"{basePath}_audio.{'mp4' if audioType=='m4s' else audioType}"
        videoResultPath = f"{basePath}_video_mix.mp4"
        audioDecodePath = f'{basePath}_audio_decode.aac'
        progresser_download(videoUrl, videoPath,
                            isParentPath=False, header=header)
        progresser_download(audioUrl, audioPath,
                            isParentPath=False, header=header)

        if not is_overwrite_file(audioDecodePath):
            return

        if not is_overwrite_file(videoResultPath):
            return
        subprocess.run(f'"{ffmpegPath}" -i "{audioPath}" -c copy "{audioDecodePath}"',
                       shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8", cwd="\\".join(ffmpegPath.split("\\")[:-1]))
        subprocess.run(f'"{ffmpegPath}" -i "{videoPath}" -i "{audioDecodePath}" -c copy "{videoResultPath}"',
                       shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8", cwd="\\".join(ffmpegPath.split("\\")[:-1]))
        os.remove(audioDecodePath)
        os.remove(audioPath)
        os.remove(videoPath)
        print(
            f"{self.bvid}下载完成，质量：{qualityDesc}，地址：\n{os.path.abspath(videoResultPath)}")

    @staticmethod
    def download_cc(bvid: str, path: str = ".", quality: int = 80):
        BilibiliVideo(bvid).download(path, quality)


class BilibiliUser:
    def __init__(self, uid: int) -> None:
        self.uid = uid

    def analyse(self, days: int = 7):
        def second_format(s: int) -> str:
            m = s//60
            ss = s % 60
            hh = m//60
            mm = m % 60

            def fill_to_2(i: int) -> str:
                s = str(i)
                return s if len(s) == 2 else "0"*(2-len(s))+s
            return f"{fill_to_2(hh)}:{fill_to_2(mm)}:{fill_to_2(ss)}"
        w = requests.Session()
        w.cookies.set("SESSDATA", BilibiliConfig.get_default_config().sessdata,
                      domain="bilibili.com")
        print(w.cookies)
        nt: int = 0
        r: int = 0
        t = time.time()-60*60*24*days
        c = 0
        p = ValuedProgresser(slider_length=20, filled_str=">")

        def post_view_requests(view: int, c: int) -> Tuple[int, int, bool, int]:
            fd = w.get(URL_USER_HISTORY % view).json()["data"]
            nt = fd["cursor"]["view_at"]
            b: int = 0
            for i in fd["list"]:
                c += 1
                p.pslider_animation_next(c)
                tt = i["view_at"]
                if tt <= t:
                    return b, nt, True, c
                bvid = i["history"]["bvid"]
                if bvid == "":
                    continue
                b += BilibiliVideo(bvid).time \
                    if i["progress"] == - 1 else i["progress"]
            return b, nt, False, c
        while True:
            v = post_view_requests(nt, c)
            c = v[3]
            r += v[0]
            nt = v[1]
            if v[2]:
                break
        print(f"\n{days}天平均看{second_format(r//days)}小时的视频")
        print(f"一共看了{second_format(r)}小时的视频")

    @classmethod
    def analyse_cc(cls):
        BilibiliUser(BilibiliConfig.get_default_config().id).analyse()


cc = EasyCommandCompiler({
    0: {
        "analyse": (BilibiliUser.analyse_cc, [])
    },
    1: {
        "bv2av": (BilibiliVideo.bv2av_cc, [str]),
        "download": (BilibiliVideo.download_cc, [str])
    },
    2: {
        "login": (BilibiliConfig.login_cc, [int, str]),
        "download": (BilibiliVideo.download_cc, [str, str])
    },
    3: {
        "download": (BilibiliVideo.download_cc, [str, str, int])
    }
}, '''
使用方法：
在控制台输入
python bilibili.py [后接函数名称] [参数,...]
目前可用的函数以及函数名称：

analyse : 分析视频观看时长
login : 登录（暂不可用）
bv2av <bv:str> : bv号转av号
download <bv:str> [path:str] [quality:int] : 下载视频
''')
cc.add_collection(FFMpegCommandCollection())
cc.compiled(argv)
