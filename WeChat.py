import json
import os
import random
from time import sleep, time, strftime
from typing import Tuple, Union

import requests
from PIL import Image, ImageDraw, ImageFont
from progress import Progresser


class WeChatDialogConfigBase:
    def __init__(self) -> None:
        self.height = 193
        self.splitLineThickness = 2
        self.splitLineLeft = 208
        self.width = 1080
        self.splitLineRight = self.width-self.splitLineLeft
        self.faceUp = 31
        self.faceLeft = 43
        self.faceLength = 130
        self.nameLeft = 34+self.faceLength+self.faceLeft
        self.nameUp = 32
        self.detailUp = 100
        self.detailLeft = self.nameLeft
        self.timeLeft = self.width-120
        self.timeUp = 47
        self.headHeight = 259


class WeChatConfigMaster:
    def __init__(self) -> None:
        self.friendDialog = WeChatDialogConfigBase()


class BilibiliFace:
    def __init__(self) -> None:
        self.bilibiliUserContentDatabase: dict = {}
        self.readIndex: int = 0

    def randomGetUserContent(self) -> Tuple[str, int]:
        while True:
            if self.bilibiliUserContentDatabase == {}:
                if os.path.exists("./bilibiliUserContentDatabase.json"):
                    with open("./bilibiliUserContentDatabase.json") as f:
                        self.bilibiliUserContentDatabase = json.loads(f.read())
                        self.length = len(self.bilibiliUserContentDatabase)
            if self.readIndex < self.length:
                k = list(self.bilibiliUserContentDatabase.keys())[
                    self.readIndex]
                r = (self.bilibiliUserContentDatabase[k], k)
                self.readIndex += 1
                return r
            sleep(0.05)
            r = random.randint(1, 666666666)
            url = f"http://api.bilibili.com/x/space/acc/info?mid={r}"
            o = json.loads(requests.get(url, verify=False).text)
            if o["code"] == (-404):
                continue
            elif o["code"] == (-412):
                with open("./bilibiliUserContentDatabase.json", "w+") as f:
                    f.write(json.dumps(self.bilibiliUserContentDatabase))
                raise ValueError(o)
            elif o["data"]["face"] == "http://i0.hdslb.com/bfs/face/member/noface.jpg":
                continue
            else:
                n: str = o["data"]["name"]
                if n.startswith("bili") or n.endswith("bili"):
                    continue
                if not os.path.exists(".\Face"):
                    os.mkdir(".\Face")
                with open(f".\Face\{r}.jpg", "wb+") as f:
                    f.write(requests.get(o["data"]["face"]).content)
                    self.bilibiliUserContentDatabase[r] = n
                    return (n, r)


class WeChatFriendDialogMaker:
    def __init__(self, length: int = 8) -> None:
        self.config = WeChatConfigMaster().friendDialog
        config = self.config
        self.image = Image.new("RGB", (config.width, config.headHeight+config.height *
                                       length), (255, 255, 255))
        topImage = Image.open(".\Top.jpg")
        self.image.paste(topImage, (0, 0))
        self.font42 = ImageFont.truetype(
            ".\SourceHanSansSC-VF.otf", 42)
        self.font42.set_variation_by_name('Medium')
        self.font33 = ImageFont.truetype(
            ".\SourceHanSansSC-VF.otf", 33)
        self.font33.set_variation_by_name('Regular')
        self.p: Progresser = Progresser(length)
        self.b = BilibiliFace()
        self.tm = strftime("%H:%M")
        for i in range(length):
            self.instanceDialogue(i)
        self.image.show()
        self.image.save("./Result.jpg")

    def instanceDialogue(self, index: int):
        config = self.config
        try:
            c = self.b.randomGetUserContent()
            name = c[0]
            id = c[1]
        except ValueError as err:
            self.image.show()
            self.image.save("./Result.jpg")
            print(
                f"\033[0;31m如出现-412请求被拦截可稍等重新运行脚本，出错前已存储之前加载完毕的数据于：{os.path.abspath('.//Face')}\\bilibiliUserContentDatabase.json\033[0m")
            raise err
        offset = config.headHeight + config.height*index
        faceImage = Image.open(f".\Face\{id}.jpg").resize(
            (config.faceLength, config.faceLength), Image.ANTIALIAS)
        self.image.paste(faceImage, (config.faceLeft, offset+config.faceUp))
        draw = ImageDraw.Draw(self.image)
        draw.text((config.nameLeft, config.nameUp+offset),
                  name, fill=(10, 10, 10), font=self.font42)
        draw.text((config.detailLeft, config.detailUp+offset),
                  "[链接] 汇总|全国青少年机器人(三级)真题...", fill=(160, 160, 160), font=self.font33)
        draw.text((config.timeLeft, config.timeUp+offset),
                  text=self.tm, fill=(160, 160, 160), font=self.font33)
        draw.line([(config.splitLineLeft, (config.height-2)+offset),
                   (config.width, (config.height-2)+offset)],
                  fill=(239, 239, 239), width=config.splitLineThickness)
        self.p.print_slider_complex_animation_next()


WeChatFriendDialogMaker()
