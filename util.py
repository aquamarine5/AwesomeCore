import time

import requests

# github.com/AwesomeCore -> progress.py
from progress import Progresser


def progresser_download(url: str, downloadPath: str, streamBytes: int = 1024, isParentPath: bool = True, header: dict = None, slider_length: int = 40, isGetRequestsHead: bool = True):
    def bytes_format(byte: int) -> str:
        kb = round(byte/1024, 2)
        if kb <= 1024:
            return f"{kb}Kb"
        mb = round(kb/1024, 2)
        if mb <= 1024:
            return f"{mb}Mb"
        else:
            return f"{round(mb/1024,2)}Gb"
    if isGetRequestsHead:
        headerResponce = requests.head(url, headers=header)
        if isParentPath:
            if "content-disposition" in headerResponce.headers:
                fileName = headerResponce.headers["content-disposition"].split("filename=")[
                    1].replace('"', "")
            else:
                fileName = url.split("?")[0].split("/")[-1:][0]
            filePath = f"{downloadPath}/{fileName}"
        else:
            filePath = downloadPath
    else:
        filePath = downloadPath
    responce = requests.get(url, stream=True, headers=header)
    responceLength = int(responce.headers["content-length"])
    print(f"文件大小： {bytes_format(responceLength)}")
    print(responce.status_code)
    downloadSize: int = 0
    progresser = Progresser(responceLength)
    if responce.status_code == 200:
        with open(filePath, "wb") as f:
            iterTime = time.time()
            showDownloadCount: int = 0
            downloadSpeedList: float = 0
            for data in responce.iter_content(streamBytes):
                f.write(data)
                downloadSize += len(data)
                nowTime = time.time()
                downloadTime = nowTime-iterTime
                iterTime = nowTime
                showDownloadCount += 1
                downloadSpeedList += downloadTime
                if downloadTime == 0:
                    continue
                if downloadSpeedList < 1:
                    continue
                downloadSpeed = (
                    streamBytes*showDownloadCount)//downloadSpeedList
                showDownloadCount = 0
                downloadSpeedList = 0
                print(
                    f"{progresser.get_slider_complex(downloadSize,slider_length=slider_length)} {bytes_format(downloadSpeed)}/s", end="\r")
            #print(f"{progresser.get_slider_complex(progresser.length,slider_length=40)} {bytes_format(downloadSpeed)}/s")
