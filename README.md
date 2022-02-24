# AwesomeCore
[![GitHub repo size](https://img.shields.io/github/repo-size/awesomehhhhh/AwesomeCore)](https://github.com/awesomehhhhh/AwesomeCore)
[![Code lines](https://img.shields.io/tokei/lines/github/awesomehhhhh/AwesomeCore)](https://github.com/awesomehhhhh/AwesomeCore)
[![Commit Activity](https://img.shields.io/github/commit-activity/m/awesomehhhhh/AwesomeCore)]()
[![Last commit](https://img.shields.io/github/last-commit/awesomehhhhh/AwesomeCore)]()
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/awesomehhhhh/AwesomeCore.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/awesomehhhhh/AwesomeCore/context:python)  
![Alt](https://repobeats.axiom.co/api/embed/9707861484b64816d1d6f02d50e9a63965926ef0.svg "Repobeats analytics image")  
AwesomeCore是一些小工具集，有作者平时或偶尔会用到的工具，其中的某些工具可能不再维护。  
# 工具列表
- *带 &#42; 的工具在之后大概率以后将不会维护。*
## NeteaseMusic
<!--
- 支持通过网易云的加密算法（AES，最后有params和encSecKey）进行POST （`NeteaseMusicMain.neteaseMusicEncrypt()`）
- 下载音乐（128kbps）（`NeteaseMusicSong(id).download()`）以及可选的附带元数据版本（`NeteaseMusicSong(id).download_with_metadata()`）
- 下载专辑或歌单的全部音乐（`NeteaseMusicWebLoader(id).download_all()`）
- 扫码登录获取cookies（`NeteaseMusicUser.login()`）
- **分析每周/全部所听歌曲（每首歌听了多少次，一共听了多久，这周多少时间在听歌）（`NeteaseMusicUser().analyse()` & `NeteaseMusicUser().alltime()`）**
- 签到（`NeteaseMusicUser().sign()`）-->
- 已单独拆分至[aquamarine5/NeteaseMusicUtil](https://github.com/aquamarine5/NeteaseMusicUtil)
## Progress
- 主要为`Progress.Progresser`类，使用`Progress.Progresser(length)`指定进度条长度
- 通常使用`Progresser().print_slider_complex_animation_next()`来实现动态进度条
- `Progresser().print_slider_complex_animation()`可以自定义进度条样式
- TODO：修复ETA
## Bilibili
- 下载bilibili视频，可指定分集数、清晰度
- bv号转av号
- 分析最近看的b站视频总时长
- 随机获取用户头像
## dingtalk_likes_creater
- 钉钉直播课堂全自动刷赞机，即使禁用了点赞也是可以用这个工具刷赞的啦
- 使用方法：dingtalk_likes_creater.py `<count>` `<threads>` `<liveUUID>`
- `count`参数为每个线程执行的发送的点赞请求数，发送一个点赞请求客户端会收到100赞
- `threads`为执行点赞请求的线程数，每个线程都执行`count`次点赞请求，故最后总点赞量 = `count * threads * 100`
- `liveUUID`为直播的UUID，推荐[Fiddler](https://www.telerik.com/fiddler)爬取
## genshin_gacha_standard
- 将使用[sunfkny/genshin-gacha-export](https://github.com/sunfkny/genshin-gacha-export)导出的抽卡数据转换为[paimon.moe](https://paimon.moe)可以识别的`Paimon.moe Wish History Export`格式
## Wechat
- 使用`PIL`生成微信首页的界面，支持输入聊天人的头像、名称、对话内容、时间
## Translation (v1&#42; & v2)
### v1 *&#42;*
- 仅用于`Webapi.__init__() -> "trs"`中，不推荐使用，请使用v2版本。
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
## Config
- 简易的用户数据存储类
## FFmpeg
- 下载、绑定、调用FFMpeg
## Leet-code *&#42;*
- 难是真难 Reference: [力扣](leetcode-cn.com)
## Webapi *&#42;*
- 详见[awesomehhhhh/AwesomeBot](github.com/awesomehhhhh/AwesomeBot)
