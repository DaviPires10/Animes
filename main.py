import sys

from async_tkinter_loop.mixins import AsyncCTk
from customtkinter import *

from managers import DownloadManager, SearchManager
from settings import Settings

from ui_elements.anime_card import AnimeCard
from ui_elements.anime_tab import AnimeDetailsTab
from ui_elements.episode_box import EpisodeSelectionBox
from ui_elements.search_tab import SearchTab
from ui_elements.tab_manager import TabManager



class AnimeScrapper(CTk, DownloadManager, SearchManager, AsyncCTk):

    link = ""

    def __init__(self):
        super().__init__(("white", "#171717"))

        self.title("AnimeFire")
        # self.iconbitmap(Settings.APP_ICON)
        self.geometry(f"{Settings.WIDTH}x{self.winfo_screenheight()}")
        self.maxsize(Settings.WIDTH, self.winfo_screenheight())
        self.update_idletasks()

        self.build_app()




    def build_app(self):
        self.tab_view = TabManager(self, self.winfo_width(), self.winfo_height())
        # , fg_color= ("white", "#171717"))
        self.tab_view.pack()

    def exit_app(self):
        self.destroy()
        sys.exit()

if __name__ =="__main__":
    # from pywinstyles import apply_style

    app = AnimeScrapper()
    # apply_style(app, "aero")

    app.async_mainloop()
