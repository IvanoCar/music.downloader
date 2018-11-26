from tkinter import *
from downloader.modules.essentials.downloader import Downloader
from downloader.modules.utils.utility import Utility
from threading import Thread
import pyperclip


class GUIWidgets(Downloader):
    def __init__(self, main_window):
        self.user_input_links = Text(main_window)
        super().__init__(self, main_window, self.user_input_links)
        self.download_btn = Button(main_window, text="Download", command=self.download_btn)
        self.paste_btn = Button(main_window, text="Paste", command=self.fpaste_btn)
        self.clear_btn = Button(main_window, text="Clear", command=self.fclear_btn)

        self.user_input_links.insert(END, 'Paste Youtube links here.\n')

        self.scrollbar = Scrollbar(main_window, command=self.user_input_links.yview)
        self.user_input_links['yscrollcommand'] = self.scrollbar.set
        self.set_widget_positions()

    def fpaste_btn(self):
        self.user_input_links.insert(END, '%s\n' % pyperclip.paste().strip())

    def fclear_btn(self):
        self.user_input_links.delete('1.0', END)

    def download_btn(self):
        if Utility.check_internet_conn():
            Thread(target=self.download_but_fn).start()

    def download_but_fn(self):
        self.times_repeated = 0
        self.download_btn['state'] = 'disabled'
        data = self.user_input_links.get(1.0, END)
        self.user_input_links.delete(1.0, END)
        data = data.split('\n')

        self.current_task_lbl['text'] = 'Preparing data...'
        self.set_final_list(data)

        if len(self.final_list) is not 0:
            self.current_task_lbl['text'] = 'Done setting up. Preparing to convert...'
            self.iterate_final_list()
            self.current_task_lbl['text'] = 'All done.'
        else:
            self.user_input_links.insert(END, 'No links provided. Please insert valid Youtube links here.\n')
            self.current_task_lbl['text'] = 'Ready to begin.'

        self.download_btn['state'] = 'normal'

    def set_widget_positions(self):
        self.download_btn.place(x=550, y=160)
        self.paste_btn.place(x=15, y=160)
        self.clear_btn.place(x=70, y=160)

        self.scrollbar.place(x=620, y=20, height=130, width=20)
        self.user_input_links.place(x=15, y=20, height=130, width=600)


