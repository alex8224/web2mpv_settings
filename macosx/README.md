Mac OSX EI Captain 设置方法
===================

1. 将web2mpv.scpt 用AppleSciptEditor打开，修改其中脚本的路径并导出为应用程序 
2. 使用 Info.plist 替换 web2mpv.app/Contents/Info.plist
3. web2mpv.app可能需要打开一下，否则系统可能中找不到注册的 url handler

BUG
===

1. mpv 播放完成或者中途按 Q 退出， mpv进程不会退出，需要按 Command + q 退出


