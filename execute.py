import os
import time
import pyautogui as pg


from managers import DownloadManager, SearchManager


def wait(file : str | os.PathLike, timeout=5):
    while True:
        time.sleep(timeout)
        if os.path.exists(file):
          break

if __name__ == "__main__":
    sm = SearchManager()
    anime = sm.search_animes(input("Anime:  "), True)[0]
    episodes = sm.get_anime_details(anime["link"])["episodes"]
    print(episodes)

    dl = DownloadManager()

    for i in range(1, 3):
        dl.add_episode_to_download(
                anime.get("title"),
                i,
                anime.get("link")
                                  )
    for proc in dl.procs:
        dl.start_next_download()
        wait(proc.file)
