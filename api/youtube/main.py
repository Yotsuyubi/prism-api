from __future__ import unicode_literals
import youtube_dl
import os


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


class YouTube:

    def __init__(self):
        self.path = None
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav'
            }],
            'logger': MyLogger(),
            'progress_hooks': [self.hook]
        }

    def hook(self, d):
        if d['status'] == 'finished':
            self.path = os.path.splitext(os.path.abspath(d['filename']))[0]+'.wav'

    def __call__(self, id):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v={}'.format(str(id))])
        return self.path
