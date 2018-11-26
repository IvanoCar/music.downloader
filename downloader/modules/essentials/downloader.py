from downloader.modules.utils.utility import Utility
from downloader.modules.essentials.song import Song
from downloader.modules.utils.preparator import DataPreparator
from tkinter import *
from tkinter import ttk
import requests


class Downloader(DataPreparator):
    def __init__(self, gui_widgets, main_window, console):
        super().__init__()
        self.widgets = gui_widgets
        self.out_path = Utility.define_output_path()
        self.songs_no = 0

        self.songs_w_error = []

        self.times_repeated = 0
        self.info_console = console

        self.headers = {
            'user-agent': Utility.set_random_usr_agent(),
        }

        self.progress_convert_dload = ttk.Progressbar(main_window, orient=HORIZONTAL, value=0)
        self.progress_convert_dload.place(x=15, y=220, width=615)
        self.progress_overall = ttk.Progressbar(main_window, orient=HORIZONTAL, value=0)
        self.progress_overall.place(x=15, y=280, width=615)

        self.current_task_lbl = Label(main_window, text='Ready to begin.')
        self.ovrl_progress_lbl = Label(main_window, text='Overall progress')
        self.current_task_lbl.place(x=14, y=195)
        self.ovrl_progress_lbl.place(x=14, y=255)

        # self.current_task_lbl.place(x=14, y=165)
        # self.progress.place(x=15, y=190, width=338)

        # self.info_console.place(x=15, y=220, height=90, width=338)

    def iterate_final_list(self):
        if self.times_repeated >= 2:
            self.final_list = list(set(self.songs_w_error))
            if len(self.final_list) is not 0:
                self.info_console.insert(END, 'Songs left unconverted: \nPress download to retry.\n')
                for i in self.final_list:
                    self.info_console.insert(END, i + '\n')
                    self.info_console.see(END)
            else:
                self.info_console.insert(END, 'All songs successfully converted. \n')
                self.info_console.see(END)
            return
        self.times_repeated += 1
        self.songs_no = len(self.final_list)
        self.progress_overall.configure(mode='determinate', maximum=self.songs_no, value=0)
        self.progress_convert_dload.configure(mode='determinate', maximum=self.songs_no, value=0)

        for c, link in enumerate(self.final_list):
            self.current_task_lbl['text'] = 'Converting: %s/%s' % (str(c + 1), str(self.songs_no))
            self.convert_and_download(link)
            self.ovrl_progress_lbl['text'] = 'Overall progress: %s/%s' % (str(c + 1), str(self.songs_no))

        self.final_list = list(set(self.songs_w_error))
        self.current_task_lbl['text'] = 'Overall progress'
        self.iterate_final_list()

    def convert_and_download(self, youtube_url):
        self.progress_convert_dload.configure(mode='determinate', maximum=1, value=0)

        song = Song(youtube_url, self.progress_convert_dload)

        # if song.other_error

        if song.invalid_id:
            self.info_console.insert(END, 'Wrong id: ' + youtube_url + '\n')
            self.info_console.see(END)
            self.progress_overall['value'] += 1
        else:
            if song.is_conn_error:
                self.songs_w_error.append(youtube_url)
                self.progress_overall['value'] += 1
            else:
                try:
                    self.current_task_lbl['text'] = 'Converting ' + song.title + ' done.'
                    self.download_song(song)
                    try:
                        self.songs_w_error.remove(youtube_url)
                    except ValueError:
                        pass
                except TypeError:
                    self.songs_w_error.append(youtube_url)
                    self.progress_overall['value'] += 1

    def conversion_thread(self, youtube_url):
        pass  # MAKE SONG CLASS VAR

    def download_song(self, song):
        s = requests.session()
        self.current_task_lbl['text'] = 'Downloading ' + song.title + '....'
        url = song.dlink
        print(url)
        local_filename = self.out_path + song.title + '.mp3'
        r = s.head(url, headers=self.headers)
        with s.get(url, headers=self.headers, stream=True) as r:
            try:
                total_size = int(r.headers['Content-Length'])
            except KeyError:
                total_size = len(r.content)

            self.current_task_lbl['text'] += ' [ {} MB ]'.format(round(((total_size / 1024) / 1000), 2))

            self.progress_convert_dload.configure(mode='determinate', maximum=total_size)
            self.progress_convert_dload['value'] = 0

            with open(local_filename, 'wb') as f:
                i = 0
                # for chunk in r.iter_content(chunk_size=4096):
                for chunk in r.iter_content(chunk_size=512):
                    i += len(chunk)
                    f.write(chunk)
                    self.progress_convert_dload['value'] = i
            self.current_task_lbl['text'] = "Done."

            print(i, total_size)

            self.info_console.insert(END, song.title + ' downloaded.\n')
            self.info_console.see(END)

        self.progress_overall['value'] += 1
        self.progress_overall.update()  # ?
        self.progress_convert_dload['value'] = 0

        # self.info_console.insert(END, name + " downloaded.\n")
        # self.info_console.see(END)
