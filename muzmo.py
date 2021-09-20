import requests
from bs4 import BeautifulSoup
import threading
import os


class Muzmo:
    def __init__(self, limit: int = 0, save_expl: str = None) -> None:
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
                        "Accept": "text/html, */*; q=0.01",
                        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "X-PJAX": "true",
                        "X-PJAX-Container": "#mcont",
                        "X-Requested-With": "XMLHttpRequest",
                        "Connection": "keep-alive",
                        "Referer": "https://ru.muzmo.cc/",
                        "Cookie": "sid=rq5pifbdhipnqtamhu90ukrufo; __atuvc=1%7C18; __atuvs=60904670aae554cf000; _ym_uid=1620067954241670169; _ym_d=1620067954; _ym_isad=2"}
        self.save_expl = save_expl
        self.limit = limit

    def download_with_name(self, music_name: str, ):
        html = requests.get(f'https://ru.muzmo.cc/search?q={music_name}&_pjax=#mcont',
                            headers=self.headers).content
        self.musicName = music_name
        self.create_foolder(self.musicName)
        self.download_music(self.take_href(html))

    def create_foolder(self, name):
        if not self.save_expl:
            self.save_expl_name = name
            if self.save_expl_name not in os.listdir():
                os.mkdir(self.save_expl_name)
        else:
            if self.save_expl not in os.listdir(self.save_expl):
                os.mkdir(self.save_expl)

    def wtih_album_music(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        href = []
        for album in soup.find('div', {"id": "ajax-wrap"}).find_all('a', {"class": "block"})[:self.limit]:
            href.append('https://ru.muzmo.cc/' + album['href'])
        for album in href:
            html = requests.get(album,
                                headers=self.headers).content
            self.download_music(self.take_href(html))


    def download_top_day(self):
        html = requests.get('https://ru.muzmo.cc/albums_top?sort=0',
                            headers=self.headers).content
        self.create_foolder('daytop')
        self.wtih_album_music(html)



    def download_top_week(self):
        html = requests.get('https://ru.muzmo.cc/albums_top?sort=1',
                            headers=self.headers).content
        self.create_foolder('weektop')
        self.wtih_album_music(html)


    def download_top_month(self):
        html = requests.get('https://ru.muzmo.cc/albums_top?sort=2',
                            headers=self.headers).content
        self.create_foolder('monthtop')
        self.wtih_album_music(html)

    def download_top_all(self):
        html = requests.get('https://ru.muzmo.cc/albums_top?sort=3',
                            headers=self.headers).content
        self.create_foolder('alltop')
        self.wtih_album_music(html)

    def take_href(self, html) -> list:
        count_download = 0
        soup = BeautifulSoup(html, 'html.parser')
        niceMusic = []
        for music in soup.find_all('tr'):
            desc = music.find('a')
            if desc and len(desc.contents) > 3:
                dataFile = music.find('td').get('data-file')
                if dataFile:
                    count_download += 1
                    niceMusic.append("https://ru.muzmo.cc" + dataFile)
                if self.limit != 0 and count_download >= self.limit:
                    break

        return niceMusic

    def download_music(self, music_list: list) -> None:
        for music in music_list:
            threading.Thread(target=self.start_thread_download, args=(music,)).start()

    def start_thread_download(self, url: str) -> None:
        byteCode = requests.get(url).content
        fileName = url.split('/')
        musicLen = len(fileName) - 1
        with open(self.save_expl_name + "/" + fileName[musicLen], 'wb') as f:
            f.write(byteCode)


