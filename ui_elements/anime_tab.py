from typing import TypedDict

import requests
from bs4 import BeautifulSoup
from customtkinter import *
from PIL.Image import Image

from managers import ImageManager

from .episode_box import EpisodeSelectionBox


class Anime(TypedDict):
    image      :  Image
    title      :  str
    alt_title  :  str
    episodes   :  int
    score      :  float
    status     :  str
    synopsis   :  str
    genre      :  list[str]
    link       :  str
    
class AnimeDetailsTab(CTkFrame):
    
    headers = { 'Accept-Language' : 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0'}
    episodes : list[EpisodeSelectionBox] = []
    download_queue : dict[str, int] = {}
    
    def __init__(self,
                 master,
                 width : int, 
                 height : int,
                 link : str
                 ):
        super().__init__(master,
                    width,
                    height) 
        self._link = link
        self.thumb_size : tuple[float, float] = ((width/3), (width*290/(3*205)))
        
        self.create_grid(self, 2, 3, 1)
        
        
        self.thumbnail_frame = CTkFrame(self,
                                        self.thumb_size[0],
                                        self.thumb_size[1])
        self.info_frame = CTkFrame(self,
                                   width - self.thumb_size[0], self.thumb_size[1])
        self.eps_container = CTkScrollableFrame(self,
                                                width, height - self.thumb_size[1])
        
        self.thumbnail = CTkLabel(self.thumbnail_frame,
                                  text= "")
        
        self.title = CTkTextbox(self.info_frame,
                                width - self.thumb_size[0], 72,
                                font= CTkFont(None, 20),
                                fg_color= "transparent",
                                wrap="word",
                                activate_scrollbars=False)
        
        self.age = CTkLabel(self.info_frame,
                            font= CTkFont(None, 15),
                            # fg_color= self.age_colors.get(age),
                            corner_radius= 25)
        
        self.status = CTkLabel(self.info_frame)
        
        self.genre = CTkLabel(self.info_frame)
        
        self._draw_tab()
            

    def _draw_episode_list(self, name : str, quantity : int) -> None:
        
        for episode in range(1, quantity+1):
            episode_selection = EpisodeSelectionBox(self.eps_container, 
                                      self.winfo_width() - 35, 20,
                                      self._fg_color,                                     
                                      title=  name,
                                      episode= episode,
                                      command= self._add_download_queue)
            self.episodes.append(episode_selection)
                   
            
    def _add_download_queue(self, event=None) -> None:
        selection : EpisodeSelectionBox = event.widget.master
        
        

    
    def _draw_tab(self):
        anime = self.get_anime_details()
        
        self.thumbnail.configure(image = CTkImage(anime["image"], 
                                 size = self.thumb_size))
        
        self.title.insert("0.0", anime["title"])
        self.title.configure(state= DISABLED)
        
        self.update_idletasks()
        # self.age.configure(text = anime["age"])
        
        self.status.configure(text = anime["status"])
        
        self._draw_episode_list(anime["title"], anime["episodes"])
        
        
    def get_anime_details(self) -> Anime:
        response = requests.get(self._link).content 
        soup = BeautifulSoup(response, 'html.parser')
        anime : BeautifulSoup = soup.find("div", class_= "divMainNomeAnime")
        
        anime_details : Anime = {
            "image" :     ImageManager.web_image(anime.find("img").get("data-src")),
            "title" :     anime.find("h1", class_ = "quicksand400 mt-2 mb-0").get_text(),
            "alt_title" : anime.find("h6", class_ = "text-gray").get_text(),
            "episodes" :  len(soup.find_all("a", class_= "lEp epT divNumEp smallbox px-2 mx-1 text-left d-flex")),
            "score" :     float(score)
                            if (score := soup.find("h4", id= "anime_score").get_text()).replace(".", "").isnumeric()
                            else float("nan"),
            "status" :    anime.find_all("span", class_= "spanAnimeInfo")[4].get_text(),
            "synopsis" :  soup.find("div", class_ = "divSinopse mb-3 mt-3 ml-2 ml-sm-1 ml-md-2 mr-2").get_text(),
            "genre" :     [genre.get_text() for genre in anime.find_all("a", class_= "mr-1 spanAnimeInfo spanGeneros spanGenerosLink")],
            } 
        return anime_details
   

    def create_grid(self, base, max_rows : int, max_columns : int, weight=1):
    
        """
        Creates a grid with the specified number of rows and columns.
        """
        for i in range(max_rows):
            base.grid_rowconfigure(i, weight=weight)
            for j in range(max_columns):
                base.grid_columnconfigure(j, weight=weight)
   
        
    def grid(self, **kwargs):
        super().grid(**kwargs)
        
        self.thumbnail_frame.grid(row=0, column=0, rowspan=1, columnspan=1)
        self.info_frame.grid(row=0, column=1, rowspan=1, columnspan=2)
        self.eps_container.grid(row=1, column=0, rowspan=2, columnspan=3, pady=5)
        
        self.thumbnail.pack()
        self.title.pack(pady= 3)
        self.age.pack(pady= 3)
        self.status.pack(pady= 3)
        self.genre.pack(pady= 3)
        
        [episode_selection.pack() for episode_selection in self.episodes]
