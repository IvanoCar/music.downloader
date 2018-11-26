from tkinter import *
from downloader.modules.gui.widgets import GUIWidgets
from downloader.modules.utils.utility import Utility

window = Tk()
window.geometry("650x350")
window.resizable(False, False)
window.title("Youtube MP3 Downloader")

if Utility.check_internet_conn():
    widgets = GUIWidgets(window)
else:
    label = Label(window, text='There is no internet at the moment.\nPlease restart the program when you have '
                               'internet connection.')
    label.place(x=50, y=150)

window.mainloop()
