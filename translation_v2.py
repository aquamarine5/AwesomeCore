import hashlib
from progress import Progresser
import random
import sys
import urllib
from time import sleep
from json import loads
from typing import *

import requests
from googletrans import Translator
from googletrans.constants import LANGUAGES
dicGoogle = {
            "中文": "zh-cn", "简体中文": "zh-cn", "繁体中文": "zh-tw", "日语": "ja", "英语": "en",
            "英文": "en", "德语": "de", "加泰罗尼亚语": "ca", "塔吉克语": "tg", "孟加拉语": "bn", "法语": "fr",
            "犹太语": "yi", "依地语": "yi", "芬兰语": "fi", "葡萄牙语": "pt", "保加利亚": "bg", "保加利亚语": "bg",
            "祖鲁语": "zu", "朝鲜语": "ko", "韩国语": "ko", "韩语": "ko", "库尔德语": "ku", "南非语": "af", "西班牙语": "es",
            "象形": "am", "阿姆哈拉文": "am", "阿拉伯语": "ar"}
dicBaidu = {
    "韩语": "kor", "韩国": "kor", "葡萄牙语": "pt", "葡萄牙": "pt", "希腊语": "el", "希腊": "el", "保加利亚语": "bul",
    "保加利亚": "bul", "文言文": "wyw", "粤语": "yue", "阿拉伯语": "ara", "阿拉伯": "ara", "德语": "de", "荷兰语": "nl",
    "荷兰": "nl", "英语": "en", "English": "en", "英文": "en", "日语": "jp", "日本": "jp", "俄语": "ru", "波兰语": "pl", "中文": "zh"}


class translationLanguage():
    def __init__(self, language: str, engine: str = "b",withoutError:bool=False) -> None:
        self.engine = engine
        self.inlang = language
        if language not in ["文言文中文", "粤语中文"]:
            self.lang = self.toLangKey(language, engine,withoutError)

    def __str__(self) -> str:
        return self.lang

    def checkEngineIsCorrect(self, usingEngine: str):
        if usingEngine != self.engine:
            raise ValueError("引擎不同")
        else:
            pass

    @staticmethod
    def toLangKey(language: str, engine: str,withoutError:bool=False):
        if engine not in ['g', 'b']:
            raise ValueError("引擎必须是b（百度）或g（谷歌）")
        if engine == "g":
            if language not in dicGoogle:
                if language not in LANGUAGES:
                    if withoutError:
                        print("暂时不支持此语言，如需要查看全部支持的语言请发送AwesomeBot:trsHelp")
                    raise ValueError('错误语言')
                else:
                    lang = language
            else:
                lang = dicGoogle[language]
        elif engine == "b":
            if language not in dicBaidu:
                if withoutError:
                    print("暂时不支持此语言，如需要查看全部支持的语言请发送AwesomeBot:trsHelp")
                raise ValueError("错误语言")
            else:
                lang = dicBaidu[language]
        return lang


class translation():
    @staticmethod
    def translate(toLang: translationLanguage, content: str, engine: str):
        if engine == "b":
            return translation.translate_baidu(toLang, content)
        elif engine == "g":
            return translation.translate_google(toLang, content)
        else:
            raise ValueError('错误引擎')

    @staticmethod
    def translate_baidu(toLang: translationLanguage, content: str):
        toLang.checkEngineIsCorrect('b')
        apikey = '["22017485","oNfU2HyP4Zf41uGkbu4yjOIQ","2zrW5eo8PQnN6BpwV8MkhpXRLAOCC6Km","20200820000547489","c8tMufVsKLEPRmdhxCKJ","R6OG1LZUR4Ri10QzhGNzJVYk1oWFZZU2pjRWIwNHhOSUpPbDUzeEphc29sbVJmRVFBQUFBJCQAAAAAAAAAAAEAAADE8KcAandzaGkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACgJPV8oCT1fRF"]'
        app = eval(apikey)
        appid = app[3]
        secretKey = app[4]
        fromLang = 'auto'
        info = content
        if toLang.inlang == "文言文中文":
            fromLang = "wyw"
            toLang = "zh"
        elif toLang.inlang == "粤语中文":
            fromLang = "yue"
            toLang = "zh"
        # api.fanyi.baidu.com 官方要求的实例
        salt = random.randint(32768, 65536)
        sign = appid + str(info) + str(salt) + secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = f"http://api.fanyi.baidu.com/api/trans/vip/translate?appid={appid}&q={urllib.parse.quote(info)}&from={fromLang}&to={toLang}&salt={salt}&sign={sign}"
        r=loads(requests.get(myurl).text.encode(
            "utf-8").decode("unicode_escape"))
        return r["trans_result"][0]["dst"]

    @staticmethod
    def translate_google(toLang: translationLanguage, content: str):
        toLang.checkEngineIsCorrect('g')
        trsor = Translator(service_urls=["translate.google.cn"])
        try:
            text = trsor.translate(content, dest=toLang.lang).text
        except AttributeError:
            text = "谷歌翻译服务器的土豆可能发芽了"
        return text

    def _checkArgsCorrect(self, arg: List[str]):
        if len(arg) <= 4:
            raise ValueError("参数数量应该大于4")
        if arg[3] not in ["g", "b"]:
            raise ValueError("第三项（翻译引擎）只能为g（谷歌）或b（百度）")


def translate(engine: str, targetLang: translationLanguage, text: str) -> str:
    return translation.translate(targetLang, text, engine)


def translate_crazy(engine: str, targetLang: translationLanguage, textLang: translationLanguage, text: str, num: int, show_slider: bool = True) -> str:
    #print("输入的翻译内容: ", text, "\n")
    bufferResult = text
    lastResult = text
    p: Progresser = Progresser(num*2)
    if show_slider:
        p.pslider_complex_animation(0)
    for i in range(num):
        bufferResult = translate(engine, targetLang, bufferResult)
        if engine == "b":
            sleep(1)
        if show_slider:
            p.print_slider_complex_animation_next()
        bufferResult = translate(engine, textLang, bufferResult)
        if bufferResult == lastResult:
            #print("翻译结果相同，取消循环翻译")
            break
        lastResult = bufferResult
        #print(i+1, bufferResult)
        if show_slider:
            p.print_slider_complex_animation_next()

    if show_slider:
        p.pslider_complex(p.length)
    return bufferResult

if __name__=="__main__":
    rune=sys.argv
    if rune[1].startswith("translate_"):
        try:
            trs=translationLanguage(rune[2])
        except ValueError:
            pass
        finally:
            print(translate(rune[1][-1],trs," ".join(rune[3:])))
    elif rune[1]=="translateCrazyGlass":
        print(translate_crazy("g",translationLanguage("中文","g"),translationLanguage("英语","g")," ".join(rune[3:]),10,show_slider=False))
