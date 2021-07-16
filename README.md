# AwesomeCore
## NeteaseMusic
- 支持通过网易云的加密算法（AES，最后有params和encSecKey）进行POST （`NeteaseMusicMain.neteaseMusicEncrypt()`）
- 下载音乐（128kbps）（`NeteaseMusicSong(id).download()`）以及可选的附带元数据版本（`NeteaseMusicSong(id).downlaod_with_metadata()`）
- 下载专辑或歌单的全部音乐（`NeteaseMusicWebLoader(id).download_all()`）
- 扫码登录获取cookies（`NeteaseMusicUser.login()`）
- 分析每周/全部所听歌曲（每首歌听了多少次，一共听了多久，这周多少时间在听歌）（`NeteaseMusicUser().analyse()` & `NeteaseMusicUser().alltime()`）
- 签到（`NeteaseMusicUser().sign()`）
## Progress
- 主要为`Progress.Progresser`类，使用`Progress.Progresser(length)`指定进度条长度
- 通常使用`Progresser().print_slider_complex_animation_next()`来实现动态进度条
- `Progresser().print_slider_complex_animation()`可以自定义进度条样式
- TODO：修复ETA
## Webapi
- 详见[awesomehhhhh/AwesomeBot](github.com/awesomehhhhh/AwesomeBot)
## Leet-code
- 难是真难
- Reference: [力扣](leetcode-cn.com)
## translation_v1 & v2
### v1
- 仅用于`Webapi.__init__() -> "trs"`中，不推荐使用
### v2
- `translation.translate()`可以翻译，`engine`可选'g'（google）和'b'（baidu）
- `translateion.translationLanguage`是翻译语种
- `translateion.translate_crazy()`是翻译生草机，推荐配合谷歌翻译引擎食用
