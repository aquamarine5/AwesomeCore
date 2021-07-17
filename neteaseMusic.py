import time
import urllib.parse
from base64 import b64encode
from typing import Dict, List, Union

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

# github.com/AwesomeCore/progress.py
from progress import Progresser

header = {"Content-Type": "application/x-www-form-urlencoded",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67"}
csrf_token = "238dcc46feb4e141800919ef1608b351"
encSecKey = "a0eb942126f004306a718aaf9fdbd8050c6aee4683d5fddc7f2946f27dc0d51164396be851a00f927d3449cf61f240442273dc46cfac1e6c160c8c85b78ff56034198914eb0a23ecbcadb493dc354c27d026a874dcb982f41e0077635b5c3fc9337e7fee2e0b30e84052d95e9fdc8ded40a00da010b947d9a6925fb6611a08c8"
URL_SONG_DETAIL = "http://music.163.com/weapi/song/detail"
URL_SONG_DATA = "http://music.163.com/weapi/song/enhance/player/url"
URL_SONG_DATA_V1 = "http://music.163.com/weapi/song/enhance/player/url/v1"
URL_ARTIST_DETAIL = "http://music.163.com/artist?id=%s"
URL_ALBUM_DETAIL = "http://music.163.com/album?id=%s"
URL_PLAYLIST_DETAIL = "https://music.163.com/playlist?id=%s"
URL_USER_RECORD = "http://music.163.com/weapi/v1/play/record"
URL_USER_HOME = "https://music.163.com/user/home?id=%s"
URL_USER_SIGN = f"https://music.163.com/weapi/point/dailyTask?csrf_token={csrf_token}"
URL_USER_LOGIN = "https://music.163.com/weapi/login/qrcode/client/login?csrf_token="
URL_USER_UNIKEY = "https://music.163.com/weapi/login/qrcode/unikey?csrf_token="
URL_USER_QRCODE = "http://music.163.com/login?codekey=%s"
URL_USER_GET = "https://music.163.com/weapi/w/nuser/account/get?csrf_token=%s"
SELF_USER_ID = 5014945121
FILE_PATH = "NeteaseMusic.txt"


class NeteaseMusicConfig:
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
                raise ValueError("请先登录")
            v = d[i.index(self.id)]
            v["lastSignDate"] = date
            self.lastSignDate = date

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
                b = eval(m)
                i = [j["id"] for j in b]
                if self.id in i:
                    print("用户已记录，无需登录")
                    return
                f.seek(0)
                f.truncate()
                b.append(self.toDict())
                f.write(str(b))

    @staticmethod
    def createWithDict(d: List[Dict[str, str]]):
        return NeteaseMusicConfig(d["isDefault"], d["nickName"], d["id"], d["MUSIC_U"], d["__csrf"], d["NMTID"])

    @classmethod
    def get_all_config(cls):
        with open(FILE_PATH) as f:
            d = eval(f.read())
            return [cls.createWithDict(i) for i in d]

    @classmethod
    def get_config(cls, id: int):
        d = cls.get_all_config()
        i = [j.id for j in d]
        if id not in i:
            raise ValueError("请先登录")
        return d[i.index(id)]

    @staticmethod
    def isLogin(id: int) -> bool:
        with open(FILE_PATH) as f:
            d = eval(f.read())
            i = [j["id"] for j in d]
            return id in i


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
                 "offset": 0, "csrf_token": csrf_token})
        return NeteaseMusicMain.neteaseMusicPost(URL_SONG_DETAIL, c) if isPost else NeteaseMusicMain.neteaseMusicEncrypt(c)

    @staticmethod
    def get_music_url(id: int, isPost: bool = True) -> Union[str, dict]:
        c = str({"ids": f"[{id}]", "br": 128000, "csrf_token": csrf_token})
        return NeteaseMusicMain.neteaseMusicPost(URL_SONG_DATA, c) if isPost else NeteaseMusicMain.neteaseMusicEncrypt(c)

    @staticmethod
    def get_music_url_v1(id: int, isPost: bool = True) -> Union[str, dict]:
        c = str({"ids": f"[{id}]", "level": "standard", "encodeType": "mp3"})
        return NeteaseMusicMain.neteaseMusicPost(URL_SONG_DATA_V1, c) if isPost else NeteaseMusicMain.neteaseMusicEncrypt(c)

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

    def download_hotsong(self):
        m = self.bsoup.find(
            "div", attrs={"id": "song-list-pre-cache"}).find_all('li')
        p = Progresser(len(m))
        for i in m:
            p.print_slider_complex_animation_next()
            NeteaseMusicSong(int(i.find('a')['href'].split('=')[1])).download(
                f"D:/a/{i.find('a').string}.mp3")


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


class NeteaseMusicAlbum(NeteaseMusicWebLoader):
    def __init__(self,  id: int) -> None:
        super().__init__(URL_ALBUM_DETAIL, id)


class NeteaseMusicUser:
    def __init__(self, id: int) -> None:
        self.isLogin: bool = NeteaseMusicConfig.isLogin(id)
        self.config: NeteaseMusicConfig = NeteaseMusicConfig.get_config(id)
        print(self.config.toCookie())
        self.id = id
        self.isMyself = id == SELF_USER_ID
        r = BeautifulSoup(requests.get(URL_USER_HOME %
                                       id, headers={"cookie": self.config.toCookie()}).text, features="html.parser")
        self.allListen = int(
            r.find("div", id="rHeader").h4.string.split("歌")[1][:-1])
        f = r.find("div", class_="name f-cb").find("a", hidefocus="true")
        self.singer = NeteaseMusicSinger(
            int(f["href"].split("=")[1])) if f.has_attr("href") else None
        self.record = NeteaseMusicRecord(self)

    @staticmethod
    def login():
        c = '{"type":"1","csrf_token":""}'
        r = NeteaseMusicMain.neteaseMusicPost(URL_USER_UNIKEY, c)
        key = r["unikey"]
        print("key:", key)
        print("url:", URL_USER_QRCODE % key)
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
            print(q, "次数：", t)
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
            print(re, "次数：", t)
            if re["code"] == 803:
                break
            elif re["code"] == -460:
                print("登录次数过多")
                break
        print(w.cookies)
        print(URL_USER_GET % w.cookies.get("__csrf"))
        csrf = w.cookies.get("__csrf")
        s = w.post(URL_USER_GET % csrf, NeteaseMusicMain.join(
            NeteaseMusicMain.neteaseMusicEncrypt(str({"csrf_token": csrf})))).json()
        print(s)
        id = s["profile"]["userId"]
        name = s["profile"]["nickname"]
        co = {"id": id, "nickName": name, "lastSignDate": -1, "MUSIC_U": w.cookies.get(
            "MUSIC_U"), "NMTID": w.cookies.get("NMTID"), "__csrf": w.cookies.get("__csrf")}
        co["isDefault"] = True
        NeteaseMusicConfig.login(NeteaseMusicConfig.createWithDict(co))
        return NeteaseMusicUser(id)

    def sign(self):
        if not self.isMyself:
            return
        with open("NeteaseMusic.txt", "ab+") as f:
            t = time.strftime("%Y%m%d", time.localtime()).encode('utf-8')
            f.seek(-8, 2)
            if t == f.read(8):
                print("已经签到了")
                return
            else:
                f.seek(0)
                f.write(t)
        c = str({"type": 1})
        r = NeteaseMusicMain.neteaseMusicPost(URL_USER_SIGN, c)
        print("签到成功" if r["code"] == 200 else f"签到失败，详情：{r}")


class NeteaseMusicRecord:
    def __init__(self, id: NeteaseMusicUser) -> None:
        self.data = NeteaseMusicRecord.get_user_record(id.id)
        self.allListen = id.allListen
        self.hasPermission = self.data["code"] == 200
        self.allData = self.data["allData"] if self.hasPermission else None
        self.weekData = self.data["weekData"] if self.hasPermission else None

    @staticmethod
    def get_user_record(id: int, isPost: bool = True):
        c = str({"limit": "1000", "offset": "0", "total": "true",
                 "type": "-1", "uid": str(id), "csrf_token": csrf_token})
        return NeteaseMusicMain.neteaseMusicPost(URL_USER_RECORD, c, NeteaseMusicConfig.get_config(id).toCookie()) if isPost else NeteaseMusicMain.neteaseMusicEncrypt(c)
    #######################################

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
        return alt
    #######################################

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


a = NeteaseMusicUser.login()
# a.sign()
a = a.record
a.analyse_week()
a.analyse_all()
a.alltime_week()
a.alltime_all()
