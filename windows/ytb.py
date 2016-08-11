# -*- coding:utf-8 -*-
import sys
import subprocess

def main(action_params):
    video_url = action_params[6:]
    play_video(video_url)

def play_video(url):
    #subprocess.Popen(["you-get", "-p", "mpv", "--format=flvhd", url])
    subprocess.Popen(["you-get", "-p", "mpv", url])
    
if __name__ == '__main__':
    main(sys.argv[1])
