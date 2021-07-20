
import time
import urllib.parse
from base64 import b64encode
from sys import argv
from typing import Any, Dict, List, Union
from hashlib import md5

# NeteaseMusicUser.login() need create QR Code
import qrcode
# Must install this package to send the web requests
import requests
# Must install this package to compiled the web page
from bs4 import BeautifulSoup
# Must install this package to encrypt the message
from Crypto.Cipher import AES
# NeteaseMusicSong.download_with_metadata() need write the metadata(ID3)
from mutagen import id3

# github.com/AwesomeCore/commandCompiler.py
from commandCompiler import EasyCommandCompiler
# github.com/AwesomeCore/progress.py
from progress import Progresser

header = {"Content-Type": "application/x-www-form-urlencoded",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67"}
encSecKey = "a0eb942126f004306a718aaf9fdbd8050c6aee4683d5fddc7f2946f27dc0d51164396be851a00f927d3449cf61f240442273dc46cfac1e6c160c8c85b78ff56034198914eb0a23ecbcadb493dc354c27d026a874dcb982f41e0077635b5c3fc9337e7fee2e0b30e84052d95e9fdc8ded40a00da010b947d9a6925fb6611a08c8"
URL_SONG_DETAIL = "http://music.163.com/weapi/song/detail"
URL_SONG_DATA = "http://music.163.com/weapi/song/enhance/player/url"
URL_SONG_DATA_V1 = "http://music.163.com/weapi/song/enhance/player/url/v1"
URL_ARTIST_DETAIL = "http://music.163.com/artist?id=%s"
URL_ALBUM_DETAIL = "http://music.163.com/album?id=%s"
URL_PLAYLIST_DETAIL = "https://music.163.com/playlist?id=%s"
URL_USER_RECORD = "http://music.163.com/weapi/v1/play/record"
URL_USER_HOME = "https://music.163.com/user/home?id=%s"
URL_USER_SIGN = "https://music.163.com/weapi/point/dailyTask?csrf_token=%s"
URL_USER_LOGIN = "https://music.163.com/weapi/login/qrcode/client/login?csrf_token="
URL_USER_CELLPHONE = "https://interface.music.163.com/weapi/login/cellphone"
URL_USER_UNIKEY = "https://music.163.com/weapi/login/qrcode/unikey?csrf_token="
URL_USER_QRCODE = "http://music.163.com/login?codekey=%s"
URL_USER_GET = "https://music.163.com/weapi/w/nuser/account/get?csrf_token=%s"
FILE_PATH = "NeteaseMusic.txt"

NeteaseMusicBuffer: Dict[str, Any] = {}


class NeteaseMusicMain:
    @staticmethod
    def neteaseMusicEncrypt(content: str) -> str:
        def AES_encrypt(key: str, message: str) -> bytes:
            def a16(text):
                padding = 16 - len(text) % 16
                text = text.decode('utf-8')
                text += padding * chr(padding)
                return text.encode('utf-8')
            a = AES.new(key, AES.MODE_CBC, iv=b'0102030405060708')
            return b64encode(a.encrypt(a16(message)))
        asrsea0 = content
        asrsea3 = "0CoJUm6Qyw8W8jud"
        a_c = "GvuqQ2m9sizBbmo4"
        p = AES_encrypt(asrsea3.encode('utf-8'), asrsea0.encode('utf-8'))
        params = AES_encrypt(a_c.encode('utf-8'), p).decode('utf-8')
        return params

    @staticmethod
    def neteaseMusicEncrypt_cc(content: str):
        print(NeteaseMusicMain.neteaseMusicEncrypt(content))

    @classmethod
    def neteaseMusicPost(cls, url: str, content: str, cookies=None) -> dict:
        m = cls.neteaseMusicEncrypt(content)
        h = header.copy()
        if cookies != None:
            h["Cookie"] = cookies
        v = requests.post(
            url, cls.join(m), headers=h).json()
        return v

    @staticmethod
    def join(params: str, encsecKey: str = encSecKey) -> str:
        return f"params={urllib.parse.quote(params)}&encSecKey={urllib.parse.quote(encsecKey)}"


class NeteaseMusicConfig:
    class NotLoginError(BaseException):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)

        def __str__(self) -> str:
            return f"请先登录 使用account-login命令登录"

    class ConfigNotFoundError(BaseException):
        def __init__(self, id: int, *args: object) -> None:
            self.id = id
            super().__init__(*args)

        def __str__(self) -> str:
            return f"找不到id为{self.id}的用户"

    def __init__(self, isDefault: bool, nickName, id, MusicU, csrf, nmtid, lastSignDate=-1) -> None:
        self.isDefault = isDefault
        self.isDefaultN = 1 if isDefault else 0
        self.lastSignDate = lastSignDate
        self.nickName = nickName
        self.id = id
        self.MusicU = MusicU
        self.csrf = csrf
        self.nmtid = nmtid

    def __str__(self) -> str:
        return str(self.toDict())

    def updateLastSignDate(self, date: int):
        with open(FILE_PATH, "a+") as f:
            f.seek(0)
            d = eval(f.read())
            i = [j["id"] for j in d]
            if self.id not in i:
                raise self.NotLoginError()
            v = d[i.index(self.id)]
            v["lastSignDate"] = date
            self.lastSignDate = date
            f.seek(0)
            f.truncate()
            f.write(str(d))

    def toDict(self) -> dict:
        return {"isDefault": self.isDefaultN,
                "id": self.id,
                "nickName": self.nickName,
                "lastSignDate": self.lastSignDate,
                "MUSIC_U": self.MusicU,
                "NMTID": self.nmtid,
                "__csrf": self.csrf}

    def toCookie(self) -> str:
        return f"MUSIC_U={self.MusicU}; NMTID={self.nmtid}; __csrf={self.csrf}"

    def toHeader(self) -> dict:
        h = header.copy()
        h["Cookie"] = self.toCookie()
        return h

    def login(self):
        with open(FILE_PATH, "a+") as f:
            f.seek(0)
            m = f.read()
            if m == "":
                f.write(str([self.toDict()]))
            else:
                b: list = eval(m)
                i = [j["id"] for j in b]
                if self.id in i:
                    print("用户已记录，无需登录")
                    return
                f.seek(0)
                f.truncate()
                if self.isDefault:
                    b.insert(0, self.toDict())
                else:
                    b.append(self.toDict())
                f.write(str(b))

    @staticmethod
    def login_cc(id: int, csrf: str, musicU: str):
        r = NeteaseMusicMain.neteaseMusicPost(URL_USER_GET % csrf, str(
            {"csrf_token": csrf}), cookies=f"MUSIC_U={musicU}; __csrf={csrf}")
        if r["account"] == None and r["profile"] == None:
            raise ValueError("账户错误")
        name = r["profile"]["nickname"]
        NeteaseMusicConfig(NeteaseMusicConfig.get_all_config() == [],
                           name, id, musicU, csrf, '').login()

    @staticmethod
    def get_default_config():
        if "config" not in NeteaseMusicBuffer:
            with open(FILE_PATH, "a+") as f:
                f.seek(0)
                r = f.read()
                if r == "" or r == "[]":
                    raise NeteaseMusicConfig.NotLoginError()
                m: list = eval(r)
                if len(m) == 0:
                    return NeteaseMusicConfig.NotLoginError()
                c = NeteaseMusicConfig.createWithDict(m[0])
                NeteaseMusicBuffer["config"] = c
                return c
        else:
            return NeteaseMusicBuffer["config"]

    @classmethod
    def get_default_config_cc(cls):
        try:
            c = cls.get_default_config()
            print(f"当前登录：{c.nickName}({c.id}) cookie: {c.toCookie()}")
        except NeteaseMusicConfig.NotLoginError:
            print("没有登录默认账号")

    @staticmethod
    def createWithDict(d: List[Dict[str, str]]):
        return NeteaseMusicConfig(d["isDefault"], d["nickName"], d["id"], d["MUSIC_U"], d["__csrf"], d["NMTID"], d["lastSignDate"])

    @classmethod
    def get_all_config(cls):
        with open(FILE_PATH, "a+") as f:
            f.seek(0)
            r = f.read()
            if r == "" or r == "[]":
                return []
            d = eval(r)
            return [cls.createWithDict(i) for i in d]

    @classmethod
    def get_all_config_cc(cls):
        r = cls.get_all_config()
        print("存储的所有账户：")
        if r == []:
            print("没有任何账户")
        for i in range(len(r)):
            c = r[i]
            print(i+1, "●" if c.isDefault else "○",
                  f"{c.nickName}({c.id}) cookie:", c.toCookie())

    @staticmethod
    def change_default_config(id: int):
        with open(FILE_PATH, "a+") as f:
            f.seek(0)
            e: list = eval(f.read())
            i = [j["id"] for j in e]
            if len(e) == 0:
                raise NeteaseMusicConfig.ConfigNotFoundError(id)
            e[0]["isDefault"] = 0
            if id not in i:
                raise NeteaseMusicConfig.ConfigNotFoundError(id)
            c = e[i.index(id)]
            e.remove(c)
            c["isDefault"] = 1
            e.insert(0, c)
            f.seek(0)
            f.truncate()
            f.write(str(e))
            print(f"成功设置 {id} 为新默认用户")

    @staticmethod
    def delete_config(id: int):
        with open(FILE_PATH, "a+") as f:
            f.seek(0)
            r = f.read()
            if r == "" or r == "[]":
                raise NeteaseMusicConfig.ConfigNotFoundError(id)
            e: list = eval(r)
            i = [j["id"] for j in e]
            if id not in i:
                raise NeteaseMusicConfig.ConfigNotFoundError(id)
            d = i.index(id)
            c = e[d]
            if c["isDefault"] == 1:
                e[d+1]["isDefault"] = 1
            e.remove(c)
            f.seek(0)
            f.truncate()
            f.write(str(e))
            print(f"成功删除id为 {id} 的用户")

    @classmethod
    def get_config(cls, id: int):
        d = cls.get_all_config()
        i = [j.id for j in d]
        if id not in i:
            raise cls.NotLoginError()
        return d[i.index(id)]

    @staticmethod
    def isLogin(id: int) -> bool:
        with open(FILE_PATH, "a+") as f:
            f.seek(0)
            r = f.read()
            if r == "" or r == "[]":
                return False
            d = eval(r)
            i = [j["id"] for j in d]
            return id in i


class NeteaseMusicSong:
    def __init__(self, id: int) -> None:
        self.id = id
        self.isVip = self.url == None
        v = self.get_music_detail(id)
        if v["code"] == -460:
            v = None
            print("获取详情失败")
            return
        else:
            if v["songs"] == []:
                raise ValueError("找不到歌曲")
        self.infos = v["songs"]
        self.info = v["songs"][0]
        self.name = self.info["name"]
        self.picUrl = self.info["album"]["picUrl"]
        self.album = NeteaseMusicAlbum(self.info["album"]["id"])
        self.artists = [NeteaseMusicSinger(i["id"])
                        for i in self.info["artists"]]
        self.artistsName = "/".join([i["name"] for i in self.info["artists"]])

    @property
    def url(self) -> str:
        return NeteaseMusicSong.get_music_url(self.id)["data"][0]["url"]

    @property
    def music_webplayer(self):
        return NeteaseMusicSong.get_music_url_v1(self.id)

    @property
    def music_iframe(self) -> str:
        return NeteaseMusicSong.get_music_url(self.id)

    @property
    def detail(self) -> str:
        return NeteaseMusicSong.get_music_detail(self.id)
    #######################################

    @staticmethod
    def get_music_detail(id: int, isPost: bool = True) -> Union[str, dict]:
        c = str({"id": id, "ids": f'["{id}"]', "limit": 10000,
                 "offset": 0, "csrf_token": NeteaseMusicConfig.get_default_config().csrf})
        return NeteaseMusicMain.neteaseMusicPost(URL_SONG_DETAIL, c) if isPost else NeteaseMusicMain.neteaseMusicEncrypt(c)

    @staticmethod
    def get_music_url(id: int, isPost: bool = True) -> Union[str, dict]:
        c = str({"ids": f"[{id}]", "br": 128000,
                 "csrf_token": NeteaseMusicConfig.get_default_config().csrf})
        return NeteaseMusicMain.neteaseMusicPost(URL_SONG_DATA, c) if isPost else NeteaseMusicMain.neteaseMusicEncrypt(c)

    @staticmethod
    def get_music_url_v1(id: int, isPost: bool = True) -> Union[str, dict]:
        c = str({"ids": f"[{id}]", "level": "standard", "encodeType": "mp3"})
        return NeteaseMusicMain.neteaseMusicPost(URL_SONG_DATA_V1, c) if isPost else NeteaseMusicMain.neteaseMusicEncrypt(c)

    @staticmethod
    def download_cc(id, path="./Download.mp3"):
        NeteaseMusicSong(id).download(path)

    @staticmethod
    def download_metadata_cc(id, path="./Download.mp3"):
        NeteaseMusicSong(id).download_with_metadata(path)

    def download(self, path):
        if self.isVip:
            print(f"\n{self.id}({self.id})不能下载")
            return
        with open(path, "wb+") as f:
            f.write(requests.get(self.url).content)

    def download_with_metadata(self, path, includeImage: bool = True):
        if self.isVip:
            print(f"\n{self.id}({self.id})不能下载")
            return
        with open(path, "wb+") as f:
            f.write(requests.get(self.url).content)
        f = id3.ID3(path)
        f.update_to_v24()
        f["TPE1"] = id3.TPE1(encoding=3, text=self.artistsName)
        f["WOAR"] = id3.WOAR(
            encoding=3, url=f"https://music.163.com/song?id={self.id}")
        f["TALB"] = id3.TALB(encoding=3, text=self.info["album"]["name"])
        f["TIT2"] = id3.TIT2(encoding=3, text=self.name)
        if includeImage:
            print(1)
            f["APIC"] = id3.APIC(encoding=3, mime="image/jpeg", type=3, desc=u"cover",
                                 data=requests.get(f"{self.picUrl}?param=256y256").content)
        f.save()


class NeteaseMusicSinger:
    def __init__(self, id: int) -> None:
        self.url = URL_ARTIST_DETAIL % id
        self.bsoup = BeautifulSoup(requests.get(self.url,
                                                headers={
                                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64"}
                                                ).text, features="html.parser")

    def download_hotsong(self, path):
        m = self.bsoup.find(
            "div", attrs={"id": "song-list-pre-cache"}).find_all('li')
        p = Progresser(len(m))
        for i in m:
            p.print_slider_complex_animation_next()
            NeteaseMusicSong(int(i.find('a')['href'].split('=')[1])).download(
                f"{path}/{i.find('a').string}.mp3")

    @staticmethod
    def download_hotsong_cc(id: int, path: str = "."):
        NeteaseMusicSinger(id).download_hotsong(path)


class NeteaseMusicWebLoader:
    def __init__(self, baseUrl: str, id: int) -> None:
        self.data = BeautifulSoup(requests.get(
            baseUrl % id, headers=header).text, features="html.parser").find("div", id="song-list-pre-cache")

    def download_all(self, path: str):
        d = self.data.find_all("li")
        p = Progresser(len(d))
        for i in d:
            a = i.a
            name = a.string
            id = int(a["href"].split("=")[1])
            NeteaseMusicSong(id).download(path+f"/{name}.mp3")
            p.print_slider_complex_animation_next()


class NeteaseMusicPlaylist(NeteaseMusicWebLoader):
    def __init__(self,  id: int) -> None:
        super().__init__(URL_PLAYLIST_DETAIL, id)

    @staticmethod
    def download_all_cc(id: int, path: str = "."):
        return NeteaseMusicPlaylist(id).download_all(path)


class NeteaseMusicAlbum(NeteaseMusicWebLoader):
    def __init__(self,  id: int) -> None:
        super().__init__(URL_ALBUM_DETAIL, id)

    @staticmethod
    def download_all_cc(id: int, path: str = "."):
        return NeteaseMusicAlbum(id).download_all(path)


class NeteaseMusicUser:
    def __init__(self, id: int, config: NeteaseMusicConfig = None) -> None:
        self.isLogin: bool = NeteaseMusicConfig.isLogin(id)
        self.config: NeteaseMusicConfig = NeteaseMusicConfig.get_config(
            id) if config == None else config
        self.id = id
        r = BeautifulSoup(requests.get(URL_USER_HOME %
                                       id, headers={"cookie": self.config.toCookie()}).text, features="html.parser")
        if r.find("div", class_="n-for404") != None:
            print(f"404 id为{self.id}账户不存在")
            self.allListen = -1
            self.record = NeteaseMusicRecord(self)
            return
        self.allListen = int(
            r.find("div", id="rHeader").h4.string.split("歌")[1][:-1])
        f = r.find("div", class_="name f-cb").find("a", hidefocus="true")
        self.singer = NeteaseMusicSinger(
            int(f["href"].split("=")[1])) if f.has_attr("href") else None
        self.record = NeteaseMusicRecord(self)

    @staticmethod
    def createWithConfig(config: NeteaseMusicConfig):
        return NeteaseMusicUser(config.id, config)

    @staticmethod
    def login_message(phone: int, password: str):
        m = md5(str(password).encode("utf-8")).hexdigest()
        s = requests.Session()
        c = str({"password": m, "phone": str(phone),
                 "checkToken": "9ca17ae2e6ffcda170e2e6eed4d225aabd879ac1408eb48eb2c14f869e9ebaaa73899b9dd0cb59ba97bab5b52af0feaec3b92a888ea586d379b7be9cccd44e868b9bb6d15a9bafa783c854f589acd7f97cfb98ee9e"})
        r = s.post(URL_USER_CELLPHONE, NeteaseMusicMain.join(
            NeteaseMusicMain.neteaseMusicEncrypt(c)), headers=header)
        q = r.json()
        print(q)
        k = s.cookies
        if q["code"] != 400 and q["code"] != 250:
            NeteaseMusicConfig(NeteaseMusicConfig.get_all_config() == [],
                               "", -1, k.get("MUSIC_U"), k.get("__csrf"), k.get("NMTID")).login()

    @staticmethod
    def login():
        c = '{"type":"1","csrf_token":""}'
        r = NeteaseMusicMain.neteaseMusicPost(URL_USER_UNIKEY, c)
        key = r["unikey"]
        print("key:", key)
        print("url:", URL_USER_QRCODE % key)
        print("请用网易云音乐APP扫描二维码授权登录")
        cc = str({"csrf_token": "", "key": key, "type": "1"})
        q = qrcode.QRCode()
        q.add_data(URL_USER_QRCODE % key)
        im = q.make_image()
        im.show()
        t = 0
        while True:
            t += 1
            q = NeteaseMusicMain.neteaseMusicPost(URL_USER_LOGIN, cc)
            time.sleep(0.5)
            print("次数：", t, q)
            if q["code"] == 802:
                break
            elif q["code"] == 800:
                print("即将重试")
                time.sleep(1)
                NeteaseMusicUser.login()
                return
        w = requests.Session()
        while True:
            t += 1
            q = NeteaseMusicMain.neteaseMusicEncrypt(cc)
            time.sleep(0.5)
            re = w.post(URL_USER_LOGIN, NeteaseMusicMain.join(q),
                        headers={"Content-Type": "application/x-www-form-urlencoded"}).json()
            print("次数：", t, re)
            if re["code"] == 803:
                break
            elif re["code"] == -460:
                print("登录次数过多")
                break
        csrf = w.cookies.get("__csrf")
        s = w.post(URL_USER_GET % csrf, NeteaseMusicMain.join(
            NeteaseMusicMain.neteaseMusicEncrypt(str({"csrf_token": csrf}))), headers=header).json()
        id = s["profile"]["userId"]
        name = s["profile"]["nickname"]
        co = {"id": id, "nickName": name, "lastSignDate": -1, "MUSIC_U": w.cookies.get(
            "MUSIC_U"), "NMTID": w.cookies.get("NMTID"), "__csrf": csrf}
        co["isDefault"] = NeteaseMusicConfig.get_all_config() == []
        f = NeteaseMusicConfig.createWithDict(co)
        print(f"要登录的账号是：{f.nickName}({f.id}) cookie: {f.toCookie()}")
        f.login()
        print("登录成功")
        print("已设置为默认账户" if co["isDefault"] else "")
        return NeteaseMusicUser(id)

    @staticmethod
    def sign_cc():
        NeteaseMusicUser.createWithConfig(
            NeteaseMusicConfig.get_default_config()).sign()

    def sign(self):
        if not self.isLogin:
            raise NeteaseMusicConfig.NotLoginError()
        v = self.config

        t = time.strftime("%Y%m%d", time.localtime())
        if t == str(v.lastSignDate):
            print("已经签到了")
            return
        c = str({"type": 1, "csrf_token": self.config.csrf})
        r = NeteaseMusicMain.neteaseMusicPost(
            URL_USER_SIGN % self.config.csrf, c, self.config.toCookie())
        if r["code"] == 200:
            v.updateLastSignDate(t)
            print("签到成功")
        else:
            print(f"签到失败，详情：{r}")
            if r["code"] == -2:
                v.updateLastSignDate(t)


class NeteaseMusicRecord:
    def __init__(self, id: NeteaseMusicUser) -> None:
        self.id = id
        self.data = self.get_user_record(id.id)
        self.allListen = id.allListen
        self.hasPermission = self.data["code"] == 200
        self.allData = self.data["allData"] if self.hasPermission else None
        self.weekData = self.data["weekData"] if self.hasPermission else None

    def get_user_record(self, id: int, isPost: bool = True):
        c = str({"limit": "1000", "offset": "0", "total": "true",
                 "type": "-1", "uid": str(id), "csrf_token": NeteaseMusicConfig.get_default_config().csrf})
        return NeteaseMusicMain.neteaseMusicPost(URL_USER_RECORD, c, self.id.config.toCookie()) if isPost else NeteaseMusicMain.neteaseMusicEncrypt(c)
    #######################################

    @staticmethod
    def alltime_cc(i: str):
        self = NeteaseMusicUser.createWithConfig(
            NeteaseMusicConfig.get_default_config()).record
        if i == "all":
            self.alltime_all()
        elif i == "week":
            self.alltime_week()

    def alltime_week(self):
        if not self.hasPermission:
            raise ValueError("没有权限")
        print("一周共 168 个小时")
        print(f"这周{round(self.alltime(self.weekData,False)/604800,4)*100}%的时间都在听音乐")

    def alltime_all(self, isSlimp: bool = True):
        if not self.hasPermission:
            raise ValueError("没有权限")
        self.alltime(self.allData, isSlimp)

    def alltime(self, data: List[dict], isSlimp: bool = True):
        def slimp(now: int, target: int, average: int) -> int:
            t = target-100
            tt = t*0.7
            t1 = t*0.3
            tf = t-tt
            offset = tf/now
            a = 0
            for _ in range(now):
                a += average*now*offset
                now -= 1
            a += average*1*t1
            return int(a)

        def second_format(s: int) -> str:
            m = s//60
            ss = s % 60
            hh = m//60
            mm = m % 60

            def fill_to_2(i: int) -> str:
                s = str(i)
                return s if len(s) == 2 else "0"*(2-len(s))+s
            return f"{fill_to_2(hh)}:{fill_to_2(mm)}:{fill_to_2(ss)}"
        alt = 0
        t = 0
        for i in data:
            t += i["song"]["dt"]//1000
            alt += i["song"]["dt"]//1000*i["playCount"]
        if isSlimp and len(data) == 100:
            s = slimp(data[-1]["playCount"], self.allListen, t//len(data))
            a = s+alt
            print("一共听了：", second_format(alt), "+",
                  second_format(s), "=", second_format(a), "小时的音乐")
        else:
            print("一共听了：", second_format(alt), "小时的音乐")
            print(f"本周平均每天听 {second_format(alt//7)} 小时的音乐")
        return alt
    #######################################

    @staticmethod
    def analyse_complex():
        self = NeteaseMusicUser.createWithConfig(
            NeteaseMusicConfig.get_default_config()).record
        self.analyse_week()
        self.analyse_all()
        self.alltime_week()
        self.alltime_all()

    @staticmethod
    def analyse_cc(i: str):
        self = NeteaseMusicUser.createWithConfig(
            NeteaseMusicConfig.get_default_config()).record
        if i == "all":
            self.analyse_all()
        elif i == "week":
            self.analyse_week()

    def analyse_week(self):
        if not self.hasPermission:
            raise ValueError("没有权限")
        print("\n====================WEEK DATA ANALYSE:")
        self.analyse(self.weekData)

    def analyse_all(self):
        if not self.hasPermission:
            raise ValueError("没有权限")
        print("\n====================ALL DATA ANALYSE:")
        self.analyse(self.allData)

    def analyse(self, data: List[dict]):
        def second_format(s: int) -> str:
            m = s//60
            ss = s % 60
            hh = m//60
            mm = m % 60

            def fill_to_2(i: int) -> str:
                s = str(i)
                return s if len(s) == 2 else "0"*(2-len(s))+s
            return f"{fill_to_2(hh)}:{fill_to_2(mm)}:{fill_to_2(ss)}"
        songData = []
        tData = []
        for i in data:
            pc = i["playCount"]
            t = i["song"]["dt"]//1000
            tt = pc*t
            tData.append(tt)
            songData.append(i)
        ts = tData.copy()
        ts.sort()
        for i in range(10):
            time = ts[-(i+1)]
            index = tData.index(time)
            song = songData[index]
            print(
                f"{i+1}: {song['song']['name']} || T:{second_format(song['song']['dt']//1000)} || C:{song['playCount']} || A:{second_format(time)}")


cc = EasyCommandCompiler({
    0: {
        "login": (NeteaseMusicUser.login, []),
        "sign": (NeteaseMusicUser.sign_cc, []),
        "analyse": (NeteaseMusicRecord.analyse_complex, []),
        "account-login": (NeteaseMusicUser.login, []),
        "account-login-qrcode": (NeteaseMusicUser.login, []),
        "account-all": (NeteaseMusicConfig.get_all_config_cc, []),
        "account-default": (NeteaseMusicConfig.get_default_config_cc, [])
    },
    1: {
        "encrypt": (NeteaseMusicMain.neteaseMusicEncrypt_cc, [str]),
        "account-change": (NeteaseMusicConfig.change_default_config, [int]),
        "account-delete": (NeteaseMusicConfig.delete_config, [int]),
        "analyse": (NeteaseMusicRecord.analyse_cc, [str]),
        "alltime": (NeteaseMusicRecord.alltime_cc, [str]),
        "download": (NeteaseMusicSong.download_cc, [int]),
        "download-metadata": (NeteaseMusicSong.download_metadata_cc, [int]),
        "download-album": (NeteaseMusicAlbum.download_all_cc, [int]),
        "download-playlist": (NeteaseMusicPlaylist.download_all_cc, [int]),
        "downlaod-singer": (NeteaseMusicSinger.download_hotsong_cc, [int])
    },
    2: {
        "account-login-message": (NeteaseMusicUser.login_message, [int, str]),
        "download": (NeteaseMusicSong.download_cc, [int, str]),
        "download-metadata": (NeteaseMusicSong.download_metadata_cc, [int, str]),
        "download-album": (NeteaseMusicAlbum.download_all_cc, [int, str]),
        "download-playlist": (NeteaseMusicPlaylist.download_all_cc, [int, str]),
        "downlaod-singer": (NeteaseMusicSinger.download_hotsong_cc, [int, str])
    },
    3: {
        "account-add": (NeteaseMusicConfig.login_cc, [int, str, str])
    }
}, '''
使用方法：
在控制台输入
python neteaseMusic.py [后接函数名称] [参数,]
目前可用的函数以及函数名称：

sign - 签到
account-login - 使用二维码登录
account-login-qrcode - 使用二维码登录（推荐）
account-login-message <phone:int> <password:str> - 使用账号密码登录（不推荐）
account-add <id:int> <csrf:str> <musicu:str> - 添加账户
account-default - 显示当前默认账户
account-all - 显示当前全部账户
account-change <id:int> - 更改默认账户
account-delete <id:int> - 删除账户
analyse - 整体分析
analyse <all/week> - 分析全部/本周数据
alltime <all/week> - 分析全部/这周听歌时长
download <id:int> [path:str] - 下载音乐
download-metadata <id:int> [path:str] - 下载音乐附带作者、专辑等元数据
download-album <id:int> [path:str] - 下载专辑全部音乐
download-playlist <id:int> [path:str] - 下载播放列表的全部音乐
download-singer <id:int> [path:str] - 下载歌手前五十音乐''')
cc.compiled(argv)
