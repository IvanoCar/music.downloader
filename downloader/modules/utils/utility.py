import requests
import os
import json
from tkinter import messagebox
from random import choice
from bs4 import BeautifulSoup


class Utility:
    @staticmethod
    def filter_name(name):
        d = {'OFFICIAL': '', 'Official': '',
             '.': '', ',': '', '|': '', '!': '',
             'VIDEO': '', 'live': '', 'LIVE': '', 'Live': '',
             'video': '','Video': '', '[': '', ']': '',
             'AUDIO': '', 'Audio': '', '"': ' ', 'ARTWORK': '',
             '(': '',
             ')': '',
             '©': '',
             '®': '',
            }
        names = name.split(sep='-')
        if len(names) > 2:
            name = "-".join([names[0], names[1]])

        for i, j in d.items():
            name = name.replace(i, j)
        return name.rstrip().lstrip()

    @staticmethod
    def check_internet_conn():
        try:
            r = requests.head('https://www.google.com')
            return True
        except requests.ConnectionError:
            messagebox.showinfo("Connection error",
                                "Please check your internet connection before continuing.")  # DIZAJNIATI
            return False

    @staticmethod
    def define_output_path():
        opath = os.path.dirname(os.path.abspath('main.py')) + "\Downloads\\"
        try:
            os.makedirs(os.path.dirname(opath))
        except FileExistsError:
            pass
        return opath


    @staticmethod
    def set_random_usr_agent():

        agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
                  'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
                  'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/41.0.2227.1 Safari/537.36',
                  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0'
                  'Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko)'
                  'Chrome/53.0.2785.143 Safari/537.36']
        return choice(agents)

