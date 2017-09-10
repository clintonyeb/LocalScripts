#!/usr/bin/env python3
from __future__ import unicode_literals
import subprocess
import sys
import argparse
import os
import youtube_dl
from size import size

"""
Youtube downloader
External modules requires
    1. aria2c
    2. ffmpeg
    3. youtube-dl
"""
FILE_NAME = 'no_name'

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    global FILE_NAME
    v= d['status']
    if v == 'downloading':
        printProgressBar(d['downloaded_bytes'], d['total_bytes'], prefix='Progress:', suffix=size(d['speed']), fill='.', length=90)
    elif v == 'finished':
        FILE_NAME = d['filename']
    else:
        print('Error during download.')


def add_audio_options(opts):
    opts['format'] = 'bestaudio/best'
    opts['postprocessors'] = [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]

    return opts


def parseArgs():
    """Parse arguments given at command line"""
    parser = argparse.ArgumentParser(
        description="Options to download youtube video")
    parser.add_argument('url', type=str, help='Youtube Video Link')
    parser.add_argument('dest', type=str, help='Destination of file')
    parser.add_argument('--conv', help="Should convert file to mp3 after download", action="store_true")

    return parser


def download(video_link, threads=2):
    global FILE_NAME
    parser = parseArgs()
    args = parser.parse_args()

    dest = args.dest or '.'  # make current directory default
    if dest[-1] == '/':
        dest = dest[:-1]

    ydl_opts = {
        'logger': MyLogger(),
        'outtmpl': "{}/%(title)s.%(ext)s".format(dest),
        'progress_hooks': [my_hook],
        'nooverwrites': True
    }

    if args.conv:
        ydl_opts = add_audio_options(ydl_opts)

    print("Starting download...")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_link])

    print("Downloaded:", FILE_NAME)


def move_to_dir():
    pass

def notify():
    pass

def main():
    parser = parseArgs()
    args = parser.parse_args()
    download(args.url)

if __name__ == '__main__':
    main()
