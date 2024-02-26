from tkinter import Misc

from customtkinter import *

from ui_elements import AnimeDetailsTab, SearchTab

DownloadTab = CTkFrame()

class TabManager(CTkTabview):
    
    link : str = ""
    
    def __init__(self, master: Misc, width: int = 300, height: int = 250):
        super().__init__(master, width, height)
    
        self.add("Home")
        self.add("Anime")
        self.add("Search")
        self.add("Downloads")
        
    def add_tabs(self):
        self.home_tab = self.tab("Home")
        
        self.search_tab = SearchTab(self, self.winfo_width(), self.winfo_screenheight())
        self._tab_dict["Search"] = self.search_tab
        
        self.downloads_tab = DownloadTab(self, self.winfo_width, self.winfo_screenheight())
        self._tab_dict["Downloads"] = self.downloads_tab
        
    
    def open_anime(self, link : str):
        if self.link != link:   
            
            self.anime_tab = AnimeDetailsTab(self, self.winfo_width(), self.winfo_screenheight(), link)
            
            self._tab_dict["anime"] = self.anime_tab
            self.set("anime")
            
        else:
            self.link = link
            self.set("anime")

    
    def open_search(self):
        self.set("Search")
        