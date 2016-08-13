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
    ass_filename = ass_filename.replace("\\", "/")
    convert_call = subprocess.Popen(["C:\\Python35\\python.exe",
                                    "C:\\Python35\\Scripts\danmaku2ass.py",
                                    "-s", "1080x720", 
                                    "-ds", "5", 
                                    "-dm", "10", 
                                    "-o", ass_filename, srt_file])
    retcode = convert_call.wait()
    return ass_filename if retcode == 0 else None

def download_srt(url):
    if has_danmu(url):
        html_body = you_get.common.get_content(url)
        cid = find_cid(html_body)
        if cid:
            srt_data = you_get.common.get_content("http://comment.bilibili.com/%s.xml" % cid)
            srt_filename = tempfile.mktemp()
            with open(srt_filename, "wb") as srtfile:
                srtfile.write(bytes(srt_data, "utf-8"))
            return danmu2ass(srt_filename)    
    else:
        return False

def play_video(url):
    srtname = download_srt(url)
    if srtname:
        subprocess.Popen(["you-get", "-p", "mpv --sub-file=%s" % srtname, url])
    else:
        subprocess.Popen(["you-get", "-p", "mpv", url])

def main(action_params):
    video_url = action_params[6:]
    play_video(video_url)
    
if __name__ == '__main__':
    main(sys.argv[1])
