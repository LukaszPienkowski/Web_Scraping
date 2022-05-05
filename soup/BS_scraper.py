from urllib import request as re
from bs4 import BeautifulSoup as BS
import pandas as pd

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
html = re.urlopen(url)
bs = BS(html.read(), 'html.parser')
bs_links = bs.find_all('td', {'class' : 'titleColumn'})
links = ['https://www.imdb.com' + tag.a['href'] for tag in bs_links][:100]

titles = list()
ratings = list()
popularity_scores = list()
genres = list()

counter = 1
for i in links:
    print(f'Scraping {counter} page')
    html = re.urlopen(i)
    bs = BS(html.read(), 'html.parser')

    try:
        titles.append(bs.find('h1').text)
    except:
        titles.append('')

    try:
        ratings.append(bs.find('div', {'data-testid': 'hero-rating-bar__aggregate-rating__score'}).text)
    except:
        ratings.append('')

    try:
        popularity_scores.append(bs.find('div', {'data-testid': 'hero-rating-bar__popularity__score'}).text)
    except:
        popularity_scores.append('Not rated')

    try:
        genres.append([x.text for x in bs.find('div', {'data-testid': 'genres'})])
    except:
        genres.append('')

    counter += 1


df = pd.DataFrame({'Title': titles, 'IMDb rating': ratings, 'Popularity': popularity_scores, 'Genre': genres})
print(df)