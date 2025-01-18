from typing import Callable, Union

import requests
from customtkinter import *
from PIL import Image

from managers.search_manager import age_colors


class AnimeCard(CTkFrame):
    def __init__(self,
                 master,
                 width: int,
                 height: int,
                 title: str,
                 age: str,
                 score : float | str,
                 thumbnail: Image.Image,
                 command: Union[Callable[[], None], None] = None
                 ):
        super().__init__(master,
                         width,
                         height)

        self.t = thumbnail
        self.height = height

        self.thumbnail = CTkLabel(self,
                                  text= None)

        self.info_frame = CTkFrame(self,
                                   width - 212, height,
                                   fg_color= "transparent")

        self.title = CTkTextbox(self.info_frame,
                                width-212, 65,
                                font= CTkFont(None, 18),
                                fg_color= "transparent",
                                wrap="word",
                                activate_scrollbars=False)
        self.title.insert("0.0", title)
        self.title.configure(state= DISABLED)


        self.age_restriction = CTkLabel(self.info_frame,
                                        text= age,
                                        font= CTkFont(None, 15),
                                        fg_color= age_colors.get(age),
                                        corner_radius= 25)

        self.score = CTkLabel(self.info_frame,
                              text= f"Nota: {score}",
                              font= CTkFont(None, 15),
                              fg_color= "transparent",)

        self.configure(cursor= "hand2")

        self.bind("<ButtonPress-1>", command)

    def pack(self, **kwargs):

        self.thumbnail.configure(image= (CTkImage(self.t,
                                  size=(self.height*(205/290), self.height))))
        super().pack(**kwargs)
        self.thumbnail.grid(column= 0, row= 0, sticky= W, pady=3, padx= 3)
        self.title.pack(pady=1, anchor= NW)

        self.info_frame.grid(column= 1, row= 0, padx= 1)
        self.age_restriction.pack(side= LEFT, padx= 18)
        self.score.pack(side= LEFT, padx= 10)


    def configure(self, require_redraw=False, **kwargs):
        super().configure(require_redraw, **kwargs)
        [widget.configure(cursor= kwargs.get("cursor")) for widget in self.winfo_children()]
        [widget.configure(cursor= kwargs.get("cursor")) for widget in self.info_frame.winfo_children()]

    def bind(self, sequence=None, command=None, add=True):
        super().bind(sequence, command, add)
        [widget.bind(sequence, command) for widget in self.winfo_children()]
        [widget.bind(sequence, command) for widget in self.info_frame.winfo_children()]

        return self
