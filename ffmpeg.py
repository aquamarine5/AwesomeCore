from config import BaseConfig
from commandCompiler import EasyCommandCollection
import json,os
class FFMpegController:
    def __init__(self,path:str) -> None:
        self.path=path
    @staticmethod
    def get_ffmpeg():
        return FFMpegController(FFMpegConfig.read())
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
    def bind_ffmpeg(path:str):
        if os.path.exists(path) and os.path.exists(path+"/ffmpeg.exe"):
            FFMpegConfig.add(path)
        else:
            raise ValueError("目录不正确")
    @staticmethod
    def download():
        pass

class FFMpegCommandCollection(EasyCommandCollection):
    def __init__(self) -> None:
        super().__init__({
            0:{
                "ffmpeg-install":(FFMpegController.check_is_installed_cc,[]),
                "ffmpeg-download":(FFMpegController.download,[])
            },
            1:{
                "ffmpeg-bind":(FFMpegController.bind_ffmpeg,[str])
            }
        })
class FFMpegConfig:
    file_path="FFMpegConfig.json"
    @classmethod
    def add(cls,path:str):
        with open(cls.file_path,"a") as f:
            f.seek(0)
            f.truncate()
            f.write(json.dumps({"path":path}))
    @classmethod
    def read(cls)->str:
        with open(cls.file_path,"r") as f:
            return json.loads(f.read())["path"]
    @classmethod
    def isDefined(cls)->bool:
        with open(cls.file_path,"a+") as f:
            return f.read()=="" or f.read()=="{}"
