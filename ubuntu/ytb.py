#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import sys
import tempfile
import subprocess
import you_get.common
from you_get.common import r1

SITES = {
    'bilibili'         : 'bilibili',
}

def main(action_params):
    video_url = action_params[6:]
    play_video(video_url)

def has_danmu(url):
    try:
        video_host = r1(r'https?://([^/]+)/', url)
        video_url = r1(r'https?://[^/]+(.*)', url)
        assert video_host and video_url
    except:
        return False

    if video_host.endswith('.com.cn'):
        video_host = video_host[:-3]
    domain = r1(r'(\.[^.]+\.[^.]+)$', video_host) or video_host
    assert domain, 'unsupported url: ' + url

    k = r1(r'([^.]+)', domain)
    print(k)
    if k in SITES:
        return True
    else:
        return False

def get_srtname():
    return tempfile.mktemp()

def find_cid(html_body):
    matches = re.search(r"cid=(\d+)", html_body).groups()
    if matches:
        return matches[0]

def danmu2ass(srt_file):
    ass_filename = srt_file + ".ass"
    convert_call = subprocess.Popen(["danmuku2ass.py", "-s", "1080x720", "-ds", "5", "-dm", "10", "-o", ass_filename, srt_file])
    retcode = convert_call.wait()
    return ass_filename if retcode == 0 else None

def download_srt(url):
    if has_danmu(url):
        html_body = you_get.common.get_content(url)
        cid = find_cid(html_body)
        if cid:
            srt_data = you_get.common.get_content("http://comment.bilibili.com/%s.xml" % cid)
            srt_filename = tempfile.mktemp()
            with open(srt_filename, "w") as srtfile:
                srtfile.write(srt_data)
            return danmu2ass(srt_filename)    
    else:
        return False

def show_notify(title=None):
    subprocess.Popen(["/usr/bin/notify-send", "-t", "10000", "-a", "totem", "-i", "totem", title if title else "正在加载视频,请稍等..."])

def play_video(url):
    show_notify()
    srtname = download_srt(url)
    if srtname:
        subprocess.Popen(["/usr/local/bin/you-get", "-p", "/usr/bin/mpv --sub-file=%s" % srtname, url])
    else:
        subprocess.Popen(["/usr/local/bin/you-get", "-p", "/usr/bin/mpv", url])
    
if __name__ == '__main__':
    main(sys.argv[1])
