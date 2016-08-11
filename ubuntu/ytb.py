#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import subprocess

def main(action_params):
    video_url = action_params[6:]
    play_video(video_url)

def show_notify(title=None):
    subprocess.Popen(["/usr/bin/notify-send", "-t", "10000", "-a", "totem", "-i", "totem", title if title else "正在加载视频,请稍等..."])

def play_video(url):
    show_notify()
    subprocess.Popen(["/usr/local/bin/you-get", "-p", "/usr/bin/mpv", url])
    
if __name__ == '__main__':
    main(sys.argv[1])
