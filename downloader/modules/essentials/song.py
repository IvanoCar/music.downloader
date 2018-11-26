import requests
import json
import time
from random import uniform
from downloader.modules.utils.utility import Utility


class Song:

    def __init__(self, youtube_url, progressbar):

        # self.link = youtube_url
        self.progressbar = progressbar
        self.title = None
        self.dlink = None

        self.is_conn_error = False
        self.invalid_id = False
        self.other_error = False
        self.api_error = False

        self.api_error_text = None

        self.conversion_progress = 0
        self.requests_sent = 0
        try:
            self._go(youtube_url)
        except requests.exceptions.ConnectionError:
            time.sleep(uniform(2, 5))
            try:
                self._go(youtube_url)
            except self._go(youtube_url):
                # print('Connection error.')
                self.is_conn_error = True

    def _go(self, yturl):
        ytid = yturl.split('v=')[1].split('&')[0]
        ytid = "".join(ytid)
        url = 'https://yt-mp3s.com/convert/@api/json/mp3/%s' % ytid
        headers = {
            'user-agent': Utility.set_random_usr_agent()
        }
        data = requests.get(url, headers=headers).text
        self.requests_sent += 1
        self.progressbar['value'] = 0.5

        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            self.other_error = True
            return
        try:
            self.dlink = 'https:%s' % data['vidInfo']['2']['dloadUrl']
            print(self.dlink)
        except KeyError:
            self.api_error = True
            try:
                self.api_error_text = data['errorMsg']
            except KeyError:
                self.other_error = True
            return

        self.title = data['vidTitle']
        self.progressbar['value'] = 1

        # test  - what to do with no of requests
