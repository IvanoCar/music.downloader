import requests
from bs4 import BeautifulSoup
import json
from downloader.modules.utils.utility import Utility


class DataPreparator:
    def __init__(self):
        self.final_list = []

    def set_final_list(self, user_list):
        for link in user_list:
            if "www.youtube.com" not in link:
                continue
            if 'Wrong' in link:
                continue
            if "&list" in link:
                # self.extract_playlist_links(link)
                self.final_list.append(link)
            else:
                self.final_list.append(link)

        self.final_list = list(set(self.final_list))


    def extract_playlist_links(self, href):
        # add extraction code for youtube links from youtube playlist
        # and append to final_list
        pass
