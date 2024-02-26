from customtkinter import *

from .anime_card import AnimeCard
from managers.image_manager import Image, ImageManager


class SearchTab(CTkFrame):
    
    link : str = "https://animefire.plus/pesquisar/"
    headers = { 'Accept-Language' : 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0'}
    
    
    def __init__(self, master, width, height, fg_color= "transparent"):
        super().__init__(master, width, height, fg_color= fg_color)
        self.master = master.master
        self.animes : list[tuple[AnimeCard, str]] = []
        
        
        self.search_bar = CTkFrame(self,
                                   width, 80,
                                   fg_color= fg_color)        
        
        self.search_entry = CTkEntry(self.search_bar,
                                     425, 35, 
                                     corner_radius= 22,
                                     placeholder_text= "Search")
        
        self.search_button = CTkButton(self.search_bar,
                                       40, 40,
                                       text= "",
                                       image= CTkImage(
                                            ImageManager.LIGHT_SEARCH_IMAGE,
                                            ImageManager.DARK_SEARCH_IMAGE,
                                           size=(40, 40)),
                                       fg_color="transparent",
                                       hover= False, 
                                       cursor = "hand2",
                                       )
        
        self.animes_container = CTkScrollableFrame(self,
                                                   width, height - 75, 
                                                   fg_color= fg_color)      

        self.dub_state : bool = True
        
        self.enable_search(True)
    
    def search(self, event = None) -> None:
        self.enable_search(False)
        self.clear_cards()
        self.draw_cards()
        
        
    def enable_search(self, state : bool = True) -> None:
        if state == True:
            self.search_button.configure(command= self.search)
            self.search_entry.bind("<Return>", self.search)
            return
        
        self.search_button.configure(command= None)
        self.search_entry.unbind("<Return>", None)  
    
    
    def draw_cards(self) -> None:
        results = self.master.search_animes(self.search_entry.get(), self.dub_state)
        print(len(results))
        for item in results:
            args = list(item.values())
            print(args)
            card = AnimeCard(
                      self.animes_container, 
                      self.winfo_width() - 10,
                      200,
                      *args[0:4],
                      command= self.get_anime
                       )
            card.pack(pady=5, padx=2) 
            self.animes.append((card, args[-1]))
            self.update_idletasks()
        self.enable_search(True)
           

    def clear_cards(self):
        try:
            for widget in self.animes_container.winfo_children():
                widget.destroy()
                self.animes.clear()    
        except:
            pass
     

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self.search_bar.pack(fill= BOTH, pady= 5)
        self.search_entry.grid(column=0, row=0, padx= 10, pady= 3)
        self.search_button.grid(column=1, row=0, sticky=W, pady=3, padx=0)
        self.animes_container.pack(fill = BOTH, pady=8)
    
    
    def get_anime(self, event=None):
        anime_card = event.widget
        while not isinstance(anime_card, AnimeCard):
            anime_card = anime_card.master
        
        for item in self.animes:
            if item[0] == anime_card:
                self.master.open_anime(item[1])
                