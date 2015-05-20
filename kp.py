import requests
import codecs
# from time import sleep
import os.path

from bs4 import BeautifulSoup
import re
from imdb import find_popular_years, print_top

url_kp_top250 = 'http://www.kinopoisk.ru/top/'
url_kp_base = 'http://www.kinopoisk.ru'
workfile_kp = 'kp_top250.html'

kp_movies = []


def main():
    global kp_movies
    kp_movies = kp_parse_with_bs4(workfile_kp)

    print_top(kp_movies, 3)
    find_popular_years(kp_movies, 5)


def kp_parse_with_bs4(workfile_kp):
    if not os.path.isfile(workfile_kp):
        kp_get_page()
        print 'New workfile was created.\n'
    else:
        print 'Previously created workfile is opened.\n'

    with open(workfile_kp) as f:
        soup = BeautifulSoup(f.read())
        # tr = soup.findAll('tr')
        movies_raw = soup.findAll(attrs={'id': re.compile("top250_place_")})
        movies = []
        for m in movies_raw:
            title = m.find('span').text
            ru_title = m.find('a', attrs={'class': 'all'})
            year = ru_title.text[-5:-1]
            link = ru_title.attrs['href']
            movies.append([title, year, link])
        return movies


def kp_get_page():
    header = {'Accept-Language': 'ru,en-us;q=0.7,en;q=0.3',
              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'
            }
    page = requests.get(url_kp_top250, headers=header)
    f = codecs.open(workfile_kp, encoding='windows-1251', mode='w+')
    f.write(page.text)
    f.close()


main()
