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
        self.info = None
        self.ydl_download_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav'
            }],
            'logger': MyLogger(),
            'progress_hooks': [self.download_hook]
        }
        self.ydl_info_opts = {
            'skip_download': True,
            'logger': MyLogger(),
            'progress_hooks': [self.info_hook]
        }

    def get_info(self, id):
        try:
            with youtube_dl.YoutubeDL(self.ydl_info_opts) as ydl:
                object = ydl.extract_info('https://www.youtube.com/watch?v={}'.format(str(id)), download=False)
            return object
        except youtube_dl.utils.DownloadError:
            return None

    def info_hook(self, d):
        if d['status'] == 'finished':
            self.info = d

    def download_hook(self, d):
        if d['status'] == 'finished':
            self.path = os.path.splitext(os.path.abspath(d['filename']))[0]+'.wav'

    def __call__(self, id):
        with youtube_dl.YoutubeDL(self.ydl_download_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v={}'.format(str(id))])
        return self.path
