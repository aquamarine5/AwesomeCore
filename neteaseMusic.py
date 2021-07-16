import qrcode
import time
import urllib.parse
from base64 import b64encode
from typing import List, Union
from mutagen import id3

import requests
from bs4 import BeautifulSoup
from Crypto.Cipher import AES

from progress import Progresser
musicS = "MUSIC_U=65890480ad5869dce7725569e5573a120dbfb9a24bc49efa4eff36367b0e60fa33a649814e309366; NMTID=00OCs3pI_PYI7DWB0I7o2z-6FxHN_UAAAF6rwE_dg; __csrf=238dcc46feb4e141800919ef1608b351"
# musicU = "WM_TID=qyIQ5eA%2Bec1FVUAEUFI5syMueJq8BbKz; mail_psc_fingerprint=00df36902df270546613057e4c4cc3b0; nts_mail_user=bd171806@163.com:-1:1; _ntes_nuid=3bd1cc25b439160508f867d6a06a3432; _ntes_nnid=3bd1cc25b439160508f867d6a06a3432,1600257913229; NMTID=00Ojx2JxZQbPv-cVkmXgZAplNcaylIAAAF16oKWYw; vinfo_n_f_l_n3=679f67c0d72b8abb.1.29.1568973237766.1609407754525.1615640498287; P_INFO=sjwncepu@163.com|1615980993|0|mail163|00&99|CN&1615976495&mail163#bej&null#10#0#0|137525&0|mail163|sjwncepu@163.com; UM_distinctid=17892671a9b48a-0a66823f554318-5c3f1e49-1fa400-17892671a9ca4a; WEVNSM=1.0.0; __remember_me=true; ntes_kaola_ad=1; lang=zh; WNMCID=basoty.1622644417830.01.0; MUSIC_U=65890480ad5869dce7725569e5573a122b1291d054acbedb9197be7e98266da533a649814e309366; __csrf=cf36174f8c24f1d5d2c847dd28f11028; _iuqxldmzr_=32; WM_NI=%2FeAjD3Gs4IFgXa3VU%2BcsPPc6aAIefqPqq58g%2BCuV1ma%2B6MuEEkoLtVWA7Z%2BgWKJ6STmuoFAR4Toce7%2Fz3HwQDFgRtPhNiWVw7FagXxGrJo2iFr8KK4n%2B1c2e%2BQDzRp5gYXM%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea8ca4fac96fbdab662bab08eb7d55f839a9b85f439a19a8e84fb6e9a8d87b6b62af0fea7c3b92aedbb8f8bc73985adfcaac56d9cbffdb7d821a1ada0b1e23ea39f8786e57b94afbfd6bb6de99dbbb7b467a3f5faaef84f87b5a1adf75e959ff9bbaa6d959586d7d260afaba1a7c45af88ca184e83deda6fda9f65b889aa9b3f75cac92a7b8d57df59aaf88db7485ae8690b16386aef8acca40aef5ff84b16fe98f8c9bd17cf7b997b9d037e2a3; JSESSIONID-WYYY=STek%2Bb9Z2XYHiH72%2BnROxJdkP2B0EljkrKMQDD174%2FUtJ%2FSIGiAyztIRGt5Nnf1jC%2BnDRos%2Bl3GTkIhxe1pYRRPQajj9gwDI54Vsxn1vJc1fSMYDg0TVqHt2BET%2Bxk%2BAbxcH7YeZfzwJd8mAe40%2BB8ls%2FYxmXEM7%5CJGu1Hdmu6ET6pbP%3A1625716635768"
header = {"Content-Type": "application/x-www-form-urlencoded",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67",
          "Cookie": musicS}
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
    def __init__(self, nickName, id, MusicU, csrf, nmtid) -> None:
        self.nickName = nickName
        self.id = id
        self.MusicU = MusicU
        self.csrf = csrf
        self.nmtid = nmtid

    def __str__(self) -> str:
        return str(self.toDict())

    def toDict(self) -> dict:
        return {"id": self.id, "nickname": self.nickName, "lastSignDate": -1, "MUSIC_U": self.MusicU, "NMTID": self.nmtid, "__csrf": self.csrf}

    def login(self):
        with open(FILE_PATH, "a+") as f:
            f.seek(0)
            m = f.read()
            if m == "":
                f.write(str([self.toDict()]))
            else:
                f.truncate()
                f.write(eval(m).append(self.toDict()))

    @staticmethod
    def get_all_config():
        with open("NeteaseMusic.txt") as f:
            f.read()


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
    def neteaseMusicPost(cls, url: str, content: str, containHeader=True) -> dict:
        m = cls.neteaseMusicEncrypt(content)
        v = requests.post(
            url, cls.join(m), headers=header if containHeader else None).json()
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
        self.id = id
        self.isMyself = id == SELF_USER_ID
        r = BeautifulSoup(requests.get(URL_USER_HOME %
                                       id, headers=header).text, features="html.parser")
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
            time.sleep(1)
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
            q = NeteaseMusicMain.neteaseMusicEncrypt(cc)
            time.sleep(1)
            re = w.post(URL_USER_LOGIN, NeteaseMusicMain.join(q),
                        headers={"Content-Type": "application/x-www-form-urlencoded"}).json()
            name = re["nickname"]
            if re["code"] == 803:
                break
        print(w.cookies)
        s = w.post(URL_USER_GET % w.cookies.get("__csrf"), NeteaseMusicMain.join(
            NeteaseMusicMain.neteaseMusicEncrypt(""))).json()
        id = s["profile"]["userId"]
        co = {"id": id, "nickname": name, "lastSignDate": -1, "MUSIC_U": w.cookies.get(
            "MUSIC_C"), "NMTID": w.cookies.get("NMTID"), "__csrf": w.cookies.get("__csrf")}

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
        return NeteaseMusicMain.neteaseMusicPost(URL_USER_RECORD, c) if isPost else NeteaseMusicMain.neteaseMusicEncrypt(c)
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


'''
a = NeteaseMusicUser(SELF_USER_ID)
a.sign()
a = a.record
a.analyse_week()
a.analyse_all()
a.alltime_week()
a.alltime_all()'''
NeteaseMusicUser.login()
# NeteaseMusicSong(1480344409).download_with_metadata("D:/aaa.mp3")
# NeteaseMusicPlaylist(6765943151).download_all("D:/a")
# a.alltime_all()
# NeteaseMusicAlbum(82321807).download_all("D:/a")
