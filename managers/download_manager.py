import ctypes
import os
from threading import Thread

import requests
from yt_dlp import YoutubeDL

from .search_manager import get_connection


def terminate(self) -> None: 
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.ident), ctypes.py_object(SystemExit))
    print("KILLING YOU")
 
Thread.terminate = terminate

class DownloadManager:

    animes_dir: str = f"{os.path.expanduser('~')}/Animes"
    procs : list[Thread] = []
    _download_in_progress : bool = False

    def add_episode_to_download(self, anime : str, episode: int, url : str) -> None:
        filename = self._generarate_output(anime).format(episode)
        if os.path.exists(filename):
            return   
        
        if (url := self._get_ep_url(url, episode)) is not None:
       
            new_process = Thread(target= self._download, args= (url, filename))
            new_process.file = filename
            self.procs.append(new_process)


    def add_movie_to_download(self, movie : str, url : str) -> None:
        filename = self._generarate_output(movie, is_movie= True)
        
        
        if os.path.exists(filename):
            return
        
        if (url := self._get_ep_url(url, 1)) is not None:
            
            
            new_process = Thread(target= self._download, args= (url, filename))
            new_process.file = filename
            self.procs.append(new_process)
            
        
    def start_download(self, process : Thread) -> None:
        self._download_in_progress = True
        process.start()

    
    def pause_download(self, process : Thread) -> None:
        self._download_in_progress = False
        process.terminate()


    def cancel_download(self, process : Thread) -> None:
        if self.is_downloading():
            self.pause_download(process)
            os.remove(f"{process.file}.part")
            self._on_finish_downloading()
        else:
            self.pause_download(process)
            os.remove(process.file)  
       
        
    def start_next_download(self) -> None:
        if self.procs:
            print(f"Length : {len(self.procs)}")
            print(f"Next : {self.procs[0].file}")
            print("\n")
            
            self.start_download(self.procs[0])
    
        
    def is_downloading(self) -> bool:
        return self._download_in_progress

           
    def _generarate_output(self, anime : str, is_movie : bool = False) -> str:
        anime : str = anime.translate({ord(i): None for i in "/?*:<>|"})
        path  : str = f"{self.animes_dir}/{anime}"
        
        if not os.path.exists(path):
            os.makedirs(path)
        
        if is_movie:
            return f"{path}/{anime} - Filme.mp4"
        else:
            return f"{path}/{anime} - EP " + "{:02d}.mp4"
        
         
    def _download(self, url : str, filename : str) -> None:
        this_process = [proc for proc in self.procs if proc.file == filename][0]
        try:
            #Download the file
            with YoutubeDL({"outtmpl" : filename}) as video:
                print("DOWN")
                video.download([url])
                print("UP")
                self._download_in_progress = False   
                self._on_finish_downloading(this_process)     
            
        except:
            
            if not get_connection():
                print("connection error")
                this_process.terminate()
            
                
        
    def _on_finish_downloading(self, process : Thread) -> None:
        self.procs.remove(process)
        process.terminate()       
   
    
    def _get_ep_url(self, url : str, episode : int) -> str:
        url = url.replace("-todos-os-episodios", "/").replace("/animes/", "/video/") + str(episode)
        
        try:
            response : dict = requests.get(url).json()
            data : list[dict] = response.get("data")
            
            if (link := response.get("token")):
                return link
            
            for item in data:
                if ("1080p" in item.values()):
                    return item.get("src")
                
                if ("720p" in item.values()):
                    return item.get("src")
                
            return data[0].get("src")
        except:
            return None
     
   