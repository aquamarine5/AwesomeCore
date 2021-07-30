import json
import os
from typing import Optional
import zipfile

import requests

# github.com/AwesomeCore -> commandCompiler.py
from commandCompiler import EasyCommandCollection
# github.com/AwesomeCore -> util.py
from util import progresser_download


class FFMpegController:
    def __init__(self, path: str) -> None:
        self.path = path

    @staticmethod
    def get_ffmpeg():
        path = FFMpegConfig.read()
        if path==None:
            return
        if not os.path.exists(path):
            raise ValueError("FFMpeg.exe缺失，请重新绑定或下载")
        return FFMpegController(path)

    @staticmethod
    def check_is_installed():
        return FFMpegConfig.isDefined()

    @staticmethod
    def check_is_installed_cc():
        if FFMpegConfig.isDefined():
            print(f"已安装，地址：{FFMpegConfig.read()}")
        else:
            print("未安装或未绑定，使用ffmpeg-bind绑定或ffmpeg-download在线下载安装")

    @staticmethod
    def bind_ffmpeg(path: str):
        path=path.replace("??"," ")
        if os.path.exists(path) and path.endswith("ffmpeg.exe"):
            FFMpegConfig.add(path)
        else:
            raise ValueError("目录不正确")

    @staticmethod
    def download():
        netdiskApi = "https://pan.huang1111.cn/api/v3/share/download/AmMfB"
        downloadUrl = requests.put(netdiskApi).json()["data"]
        downloadPath = os.path.abspath("./ffmpeg.zip")
        progresser_download(downloadUrl, downloadPath, isParentPath=False)
        zip = zipfile.ZipFile(downloadPath.replace("\\", "/"))
        zip.extractall(os.path.abspath("."))
        del zip
        os.remove(downloadPath)
        if not os.path.exists(downloadPath):
            raise ValueError()
        FFMpegController.bind_ffmpeg(downloadPath.replace("ffmpeg.zip","ffmpeg.exe"))


class FFMpegCommandCollection(EasyCommandCollection):
    def __init__(self) -> None:
        super().__init__({
            0: {
                "ffmpeg-check": (FFMpegController.check_is_installed_cc, []),
                "ffmpeg-download": (FFMpegController.download, [])
            },
            1: {
                "ffmpeg-bind": (FFMpegController.bind_ffmpeg, [str])
            }
        }, '''
ffmpeg-check 检测是否安装ffmpeg
ffmpeg-download 在线安装ffmpeg
ffmpeg-bind <path:str> 绑定ffmpeg路径
''')


class FFMpegConfig:
    file_path = "FFMpegConfig.json"

    @classmethod
    def add(cls, path: str):
        with open(cls.file_path, "a") as f:
            f.seek(0)
            f.truncate()
            f.write(json.dumps({"path": path}))

    @classmethod
    def read(cls) -> Optional[str]:
        with open(cls.file_path, "r") as f:
            c=f.read()
            if c=="":
                return None
            else:
                return json.loads(c)["path"]

    @classmethod
    def isDefined(cls) -> bool:
        with open(cls.file_path, "a+") as f:
            f.seek(0)
            return f.read() != "" and f.read() != "{}"
