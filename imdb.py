import requests
import codecs  # page have some u2018(') characters which can't be writ to file
from time import sleep
import os.path
from collections import Counter

from bs4 import BeautifulSoup
from lxml import html

url_imdb_top250 = 'http://www.imdb.com/chart/top'
url_imdb_base = 'http://www.imdb.com'
workfile_imdb = 'imdb_top250.html'

imdb_movies = []


def main():
    global imdb_movies  # can be avoided, but inconvinient to work from console
    imdb_movies = imdb_parse_with_lxml(workfile_imdb)
    # OR imdb_movies = imdb_parse_with_bs4(workfile_imdb)

    print_top(imdb_movies, 3)
    find_popular_years(imdb_movies, 5)

    print '\nYou can also print cast by typing "imdb_get_cast_with_bs4(qty)"'
    # imdb_get_cast_with_bs4(3)


def imdb_parse_with_lxml(workfile_imdb):
    if not os.path.isfile(workfile_imdb):
        imdb_get_page(url_imdb_top250)
        print 'New workfile was created.\n'
    else:
        print 'Previously created workfile is opened.\n'

    doc = html.parse(workfile_imdb)
    tbody = doc.find('.//tbody[@class="lister-list"]')
    titleColumns = tbody.findall('.//td[@class="titleColumn"]')
    movies = []
    for titleColumn in titleColumns:
        a = titleColumn.find('a')
        title = a.text
        link = a.attrib['href']
        secondary_info = titleColumn.find('span[@class="secondaryInfo"]')
        year = secondary_info.text
        movies.append([title, year, link])
    return movies


def imdb_get_page(url):
    header = {'Accept-Language': 'en'}  # wo it localized titles returned
    page = requests.get(url, headers=header)
    with codecs.open(workfile_imdb, encoding='utf-8', mode='w+') as f:
        f.write(page.text)


def imdb_parse_with_bs4(workfile_imdb):
    if not os.path.isfile(workfile_imdb):
        imdb_get_page(url_imdb_top250)
        print 'New workfile was created.\n'
    else:
        print 'Previously created workfile is opened.\n'

    with open(workfile_imdb) as f:
        soup = BeautifulSoup(f.read())
        table = soup.find('table', 'chart')
        tbody = table.find('tbody', 'lister-list')
        movies = []
        titleColumns = tbody.findAll('td', 'titleColumn')
        for titleColumn in titleColumns:
            a = titleColumn.find('a')
            link = a.attrs['href']
            title = a.text
            secondary_info = titleColumn.find('span', 'secondaryInfo')
            year = secondary_info.text
            movies.append([title, year, link])
    return movies


def print_top(movies, qty):
    print '\n', 'Top %s movies:' % (qty)
    for rank in range(qty):
        print '\t', rank+1, movies[rank][0].ljust(30),\
            movies[rank][1].ljust(10),\
            movies[rank][2].ljust(30)


def find_popular_years(movies, qty):
    years_li = []
    for movie in movies:
        years_li.append(movie[1])
    most_common = Counter(years_li).most_common(qty)
    print '\n', '%d most popular years in top250:' % (qty)
    for mc in most_common:
        print '\t', mc[0].strip('()'), ' -- ', mc[1]


def imdb_get_cast_with_bs4(qty):
    for movie in imdb_movies[:qty]:
        print '\n', movie[0], movie[1]
        r = requests.get(url_imdb_base+movie[2])
        soup = BeautifulSoup(r.text)
        cast_list = soup.find('table', 'cast_list')
        actors_raw = cast_list.findAll('td', {'itemprop': 'actor'})
        for actor in actors_raw:
            print '\t', actor.text.strip()
        sleep(1)


if __name__ == '__main__':
    main()
