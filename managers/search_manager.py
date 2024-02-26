from io import BytesIO
from typing import TypedDict

import requests
from bs4 import BeautifulSoup
from PIL import Image

from .image_manager import ImageManager


class Anime(TypedDict):
    image      :  Image.Image
    title      :  str
    alt_title  :  str
    episodes   :  int
    score      :  float
    status     :  str
    synopsis   :  str
    genre      :  list[str]
    link       :  str
age_colors = {
    "N/A": "#382a29",
    "L"  : "#15941",
    "A10": "#00a5ff",
    "A14": "#e36722",
    "A16": "#d50606",
    "A18": "#000",
    }


class SearchManager:
    
    
    
    def search_animes(self, query : str, dub : bool) -> list[Anime]:
        """
            Searches for animes based on the given query and dub preference.

            Parameters:
            - query (str): The search query.
            - dub (bool): Whether to search for dubbed animes or not.

            Returns:
            - list[Anime]: A list of Anime objects that match the search query and dub preference.

            """
        
        headers : dict  =  { 'Accept-Language' : 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0'}
        link    : str   =  "https://animefire.plus/pesquisar/"
        query   : str   =  "-".join(query.lower().split())
        url     : str   =  link+query
        print(url)
        
        
        if get_connection():
            
            response = requests.get(url, headers = headers).content 
            soup = BeautifulSoup(response, 'html.parser')
            
            animes : list[BeautifulSoup] = soup.find_all('article', class_ = "card cardUltimosEps")
            list_animes : list[Anime] = []
            
            for anime in animes:
        
              name : str = anime.find("h3", class_ = "animeTitle").get_text().translate({ord(i): None for i in "/?*:<>|"})
              if (dub and "Dublado" in name):
               
                result = Anime({
                    "title"     : name.replace(" (Dublado)", ""),
                    "age"       : anime.find("span", class_ = "pr-1").get_text(),
                    "score"     : to_float(anime.find("span", class_ = "horaUltimosEps").get_text()),
                    "image"     : self.get_image(anime.find("img").get("data-src")),
                    "link"      : anime.find("a").get("href")
                                    })            
                list_animes.append(result)
              elif (not dub and not "Dublado" in name):
            
                result = Anime({
                    "title"     : name,
                    "age"       : anime.find("span", class_ = "pr-1").get_text(),
                    "score"     : to_float(anime.find("span", class_ = "horaUltimosEps").get_text()),
                    "image"     : self.get_image(anime.find("img").get("data-src")),
                    "link"      : anime.find("a").get("href")
                                   })
                list_animes.append(result)
                 
                                
            list_animes.sort(key= lambda d: d.get('title'))
            
            return list_animes
    
    
    def get_anime_details(self, url : str) -> Anime:
        """
        Get the details of an anime.

        Parameters:
        - url (str): The URL of the anime.

        Returns:
        - Anime: A dictionary containing the details of the anime, including the image, title, alt_title, episodes, score, status, synopsis, and genre.
        """
        
        response = requests.get(url).content 
        soup = BeautifulSoup(response, 'html.parser')
        anime : BeautifulSoup = soup.find("div", class_= "divMainNomeAnime")
        
        anime_details = Anime({
            "title" :     anime.find("h1", class_ = "quicksand400 mt-2 mb-0").get_text(),
            "alt_title" : anime.find("h6", class_ = "text-gray").get_text(),
            "episodes" :  len(soup.find_all("a", class_= "lEp epT divNumEp smallbox px-2 mx-1 text-left d-flex")),
            "score" :     to_float(soup.find("h4", id= "anime_score").get_text()),
            "status" :    anime.find_all("span", class_= "spanAnimeInfo")[4].get_text(),
            "synopsis" :  soup.find("div", class_ = "divSinopse mb-3 mt-3 ml-2 ml-sm-1 ml-md-2 mr-2").get_text(),
            "genre" :     [genre.get_text() for genre in anime.find_all("a", class_= "mr-1 spanAnimeInfo spanGeneros spanGenerosLink")],
            "image" :     ImageManager.web_image(anime.find("img").get("data-src"))
            })
        return anime_details
        

    def get_image(self, url : str) -> Image.Image:
        response = requests.get(url)
        bytes_image = BytesIO(response.content)
        image = Image.open(bytes_image)
        return image


def to_float(string : str) -> float:
    if string.strip(".").isnumeric():
        return float(string)
    return float("nan")


def get_connection() -> bool:
    """
    Checks the internet connection by sending a GET request to "https://www.google.com".

    Returns:
    - bool: True if the connection is successful, False otherwise.
    """
    
    try:
        response = requests.get("https://www.google.com")
        return True
    except:
        return False
