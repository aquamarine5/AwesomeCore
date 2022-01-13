# AwesomeCore
[![GitHub repo size](https://img.shields.io/github/repo-size/awesomehhhhh/AwesomeCore)](https://github.com/awesomehhhhh/AwesomeCore)
[![Code lines](https://img.shields.io/tokei/lines/github/awesomehhhhh/AwesomeCore)](https://github.com/awesomehhhhh/AwesomeCore)
[![Commit Activity](https://img.shields.io/github/commit-activity/m/awesomehhhhh/AwesomeCore)]()
[![Last commit](https://img.shields.io/github/last-commit/awesomehhhhh/AwesomeCore)]()
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/awesomehhhhh/AwesomeCore.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/awesomehhhhh/AwesomeCore/context:python)  
AwesomeCore是一些小工具集，有作者平时或偶尔会用到的工具。其中的某些工具可能不会维护。  
## NeteaseMusic
- 支持通过网易云的加密算法（AES，最后有params和encSecKey）进行POST （`NeteaseMusicMain.neteaseMusicEncrypt()`）
- 下载音乐（128kbps）（`NeteaseMusicSong(id).download()`）以及可选的附带元数据版本（`NeteaseMusicSong(id).download_with_metadata()`）
- 下载专辑或歌单的全部音乐（`NeteaseMusicWebLoader(id).download_all()`）
- 扫码登录获取cookies（`NeteaseMusicUser.login()`）
- **分析每周/全部所听歌曲（每首歌听了多少次，一共听了多久，这周多少时间在听歌）（`NeteaseMusicUser().analyse()` & `NeteaseMusicUser().alltime()`）**
- 签到（`NeteaseMusicUser().sign()`）
## Progress
- 主要为`Progress.Progresser`类，使用`Progress.Progresser(length)`指定进度条长度
- 通常使用`Progresser().print_slider_complex_animation_next()`来实现动态进度条
- `Progresser().print_slider_complex_animation()`可以自定义进度条样式
- TODO：修复ETA
## translation_v1 & v2
### v1
- 仅用于`Webapi.__init__() -> "trs"`中，不推荐使用
### v2
- `translation.translate()`可以翻译，`engine`可选'g'（google）和'b'（baidu）
- `translation.translationLanguage`是翻译语种
- `translation.translate_crazy()`是翻译生草机，推荐配合谷歌翻译引擎食用
## CommandCompiler
- 可用`commandCompiler.CommandCompiler()`新建
- 如```
CommandCompiler({
    0:{
      "a":CommandFunction(a,CommandArgument())},
    1:{
      "b":CommandFunction(b,CommandArgument([int]))}})```
- `commandCompiler.EasyCommandCompiler()`可以更快编写，替代了`CommandFunction`和`CommandArgument`
## Webapi
- 详见[awesomehhhhh/AwesomeBot](github.com/awesomehhhhh/AwesomeBot)
## Leet-code
- 难是真难
- Reference: [力扣](leetcode-cn.com)
