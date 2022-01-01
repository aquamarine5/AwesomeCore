import hashlib
import random
import urllib
from json import loads
from sys import argv
# seealso: PEP-484
from typing import *

# pip install requests
import requests
# pip install googletrans
# https://github.com/ssut/py-googletrans
from googletrans import Translator
from googletrans.constants import LANGUAGES
# pip install playsound
from playsound import playsound


class ArgsNotCorrectException(BaseException):
    def __init__(self, message: str) -> None:
        self.message: str = message

    def __str__(self) -> str:
        return f"输入参数数量不正确，应为: {self.message}个"


def _checkArgsCountCorrect(arg: List[str], num: int) -> bool:
    if len(arg) != num+2:
        raise ArgsNotCorrectException(num)


class translation():
    def __init__(self, arg: List[str]) -> None:
        # 为百度翻译apikey，因为机器人兼容问题写在文件里
        apikey='["22017485","oNfU2HyP4Zf41uGkbu4yjOIQ","2zrW5eo8PQnN6BpwV8MkhpXRLAOCC6Km","20200820000547489","c8tMufVsKLEPRmdhxCKJ","R6OG1LZUR4Ri10QzhGNzJVYk1oWFZZU2pjRWIwNHhOSUpPbDUzeEphc29sbVJmRVFBQUFBJCQAAAAAAAAAAAEAAADE8KcAandzaGkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACgJPV8oCT1fRF"]'
        self._checkArgsCorrect(arg)
        trsBaiduDict = {
            "韩语": "kor",
            "韩国": "kor",
            "葡萄牙语": "pt",
            "葡萄牙": "pt",
            "希腊语": "el",
            "希腊": "el",
            "保加利亚语": "bul",
            "保加利亚": "bul",
            "文言文": "wyw",
            "粤语": "yue",
            "阿拉伯语": "ara",
            "阿拉伯": "ara",
            "德语": "de",
            "荷兰语": "nl",
            "荷兰": "nl",
            "英语": "en",
            "English": "en",
            "英文": "en",
            "日语": "jp",
            "日本": "jp",
            "俄语": "ru",
            "波兰语": "pl",
            "中文": "zh"
        }
        if (arg[2] == "粤语") | (arg[2] == "文言文") | (arg[2] == "文言文中文") | (arg[2] == "粤语中文") | (
                arg[3] == "b"):  # 翻译（百度）
            app=eval(apikey)
            appid = app[3]
            secretKey = app[4]
            fromLang = 'auto'
            info = " ".join(arg[4:])
            toLang = trsBaiduDict[arg[2]]
            if arg[2] == "文言文中文":
                fromLang = "wyw"
                toLang = "zh"
            elif arg[2] == "粤语中文":
                fromLang = "yue"
                toLang = "zh"
            else:
                if arg[2] not in trsBaiduDict:
                    self.text = "错误的语言，尝试 help 百度翻译"
                    self.textWrite = True
                    return
            # api.fanyi.baidu.com 官方要求的实例
            salt = random.randint(32768, 65536)
            sign = appid + str(info) + str(salt) + secretKey
            sign = hashlib.md5(sign.encode()).hexdigest()
            myurl = f"http://api.fanyi.baidu.com/api/trans/vip/translate?appid={appid}&q={urllib.parse.quote(info)}&from={fromLang}&to={toLang}&salt={salt}&sign={sign}"
            self.text = loads(requests.get(myurl).text.encode(
                "utf-8").decode("unicode_escape"))["trans_result"][0]["dst"]
        #######################################################
        elif (arg[3] == "Google") | (arg[3] == "g") | (arg[3] == "1"):  # 翻译（谷歌）
            # FIXME:用dict查找或许更易于理解
            if arg[2] == "中文":
                dest = "zh-cn"
            elif arg[2] == "简体中文":
                dest = "zh-cn"
            elif arg[2] == "繁体中文":
                dest = "zh-tw"
            elif arg[2] == "日语":
                dest = "ja"
            elif (arg[2] == "英语") | (arg[2] == "英文"):
                dest = "en"
            elif arg[2] == "德语":
                dest = "de"
            elif arg[2] == "加泰罗尼亚语":
                dest = "ca"
            elif arg[2] == "塔吉克语":
                dest = "tg"
            elif arg[2] == "孟加拉语":
                dest = "bn"
            elif arg[2] == "法语":
                dest = "fr"
            elif (arg[2] == "犹太语") | (arg[2] == "依地语"):
                dest = "yi"
            elif arg[2] == "芬兰语":
                dest = "fi"
            elif arg[2] == "葡萄牙语":
                dest = "pt"
            elif (arg[2] == "保加利亚") | (arg[2] == "保加利亚语"):
                dest = "bg"
            elif arg[2] == "祖鲁语":
                dest = "zu"
            elif (arg[2] == "朝鲜语") | (arg[2] == "韩国语") | (arg[2] == "韩语"):
                dest = "ko"
            elif arg[2] == "库尔德语":
                dest = "ku"
            elif arg[2] == "南非语":
                dest = "af"
            elif arg[2] == "希腊语":
                dest = "el"
            elif arg[2] == "西班牙语":
                dest = "es"
            elif (arg[2] == "象形") | (arg[2] == "阿姆哈拉文"):
                dest = "am"
            elif (arg[2] == "阿拉伯语") | (arg[2] == "阿拉伯"):
                dest = "ar"
            else:
                if arg[2] not in LANGUAGES:
                    self.text = "错误的语言，如需翻译文言文等中文变体请使用: \n 翻译 [需要翻译文本] 文言文\n文言文转中文请使用: 翻译 [需要翻译文本] 文言文中文" \
                                "\n空格请用+代替谢谢"
                    return
                else:
                    dest = arg[3]
            trsor = Translator(service_urls=["translate.google.cn"])
            inp = " ".join(arg[4:])
            try:
                self.text = trsor.translate(inp, dest=dest).text
            except AttributeError:
                self.text = "谷歌翻译服务器的土豆可能发芽了"

    def _checkArgsCorrect(self, arg: List[str]):
        if len(arg) <= 4:
            raise ArgsNotCorrectException("大于4")
        if arg[3] not in ["g", "b"]:
            raise ValueError("第三项（翻译引擎）只能为g（谷歌）或b（百度）")

    def get_result(self) -> str:
        return self.text
########################################


def weather_report(arg: List[str]) -> str:
    _checkArgsCountCorrect(arg, 2)
    # api from baidu.com
    url = f"http://weathernew.pae.baidu.com/weathernew/pc?query={arg[2]}{arg[3]}天气&srcid=4982&city_name={arg[2]}&province_name={arg[3]}"
    t: str = requests.get(url).text
    result = loads(t.split("</script>")[0].split("window.tplData = ")[1][:-1])
    temperature = result["weather"]["temperature"]
    weather = result["weather"]["weather"]
    pm25 = f'{result["ps_pm25"]["level"]} {result["ps_pm25"]["ps_pm25"]}'
    return f"{arg[2]}{arg[3]}天气是: {weather}，{temperature}，空气质量为{pm25}"
########################################


def help(argKey: str) -> str:
    helpDict = {"translate": "请用xxx.py translate [要翻译的语种] [翻译引擎，g为谷歌，b为百度] [要翻译的内容 允许空格]",
                "weather": "请用xxx.py weather [省] [市]",
                "tts": "请用xxx.py tts [内容 允许空格]",
                "#": "请用xxx.py help translate获取翻译帮助，xxx.py help weather获取天气帮助，xxx.py help tts获取语音转文字帮助"}
    if argKey not in helpDict:
        raise ValueError("没有这项功能的帮助文档")
    return helpDict[argKey]
########################################


def tts(arg: List[str]):
    # api from fanyi.baidu.com
    with open("./tts.mp3", "wb+") as f:
        f.write(requests.get(
            f"https://fanyi.baidu.com/gettts?lan=zh&text={urllib.parse.quote(' '.join(arg[2:]))}&spd=5&source=web").content)
    playsound("./tts.mp3")
########################################

if __name__ == "__main__":
    arg: List[str] = argv
    if len(arg) != 1:
        argKey = argv[1]
        result: str = ""
        if argKey == "weather":
            result = weather_report(arg)
        elif argKey == "translate":
            result = translation(arg).get_result()
        elif argKey == "help":
            result = help(argKey)
        elif argKey == "tts":
            tts(arg)
        else:
            raise ValueError("函数标识只能是: weather或translate或tts")
        print(result)
    else:
        print(help("#"))
