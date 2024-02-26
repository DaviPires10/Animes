from typing import Any, Callable, Union

from customtkinter import *


class EpisodeSelectionBox(CTkFrame):
    def __init__(self,
                 master,
                 width : int, 
                 height : int,
                 fg_color: str | tuple[str, str] | None,
                 title : str,
                 episode : int,
                 command: Union[Callable[[], Any], None] = None,
                 ):
        super().__init__(master,
                    width,
                    height,
                    fg_color = fg_color,
                    corner_radius = 15 )
        
        self._command = command
        self._episode = episode
        
        self.title = CTkLabel(self, text= f"{title} - Episódio {episode}")
        
        self.button = CTkButton(self, text= "Download", command = self._download)
    
    def _download(self, event = None):
        self.button.configure(text= "Downloading", state= DISABLED)
        self._command()
        
    def get_episode(self) -> int:
        return self._episode        
        
    def pack(self, **kwargs):
        super().pack(**kwargs) 
        
        self.title.grid(row= 0, column= 0, sticky= W)
        self.button.grid(row= 0, column= 1, sticky= E)
        
        
    
    
    
    
    