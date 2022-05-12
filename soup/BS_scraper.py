from urllib import request as re
from bs4 import BeautifulSoup as BS
import pandas as pd
import time

limit_100_pages = True
#limit_100_pages = False

## Scrapping pages of top100 movies rated in IMDB using BeautifulSoup package
url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
html = re.urlopen(url)
bs = BS(html.read(), 'html.parser')
bs_links = bs.find_all('td', {'class' : 'titleColumn'})
if limit_100_pages:
    links = ['https://www.imdb.com' + tag.a['href'] for tag in bs_links][:100]
else:
    links = ['https://www.imdb.com' + tag.a['href'] for tag in bs_links]

## Empty lists for movies data
titles = list()
ratings = list()
popularity_scores = list()
genres = list()

start = time.time() 
counter = 1

## Scraping selected data from each page
for i in links:
    print(f'Scraping {counter} page')
    html = re.urlopen(i)
    bs = BS(html.read(), 'html.parser')

    try:
        titles.append(bs.find('h1').text)
    except:
        titles.append('')

    try:
        ratings.append((bs.find('div', {'data-testid': 'hero-rating-bar__aggregate-rating__score'}).text)[:3])
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

## Output as a Data Frame
df = pd.DataFrame({'Title': titles, 'IMDb rating': ratings, 'Popularity': popularity_scores, 'Genre': genres})
print(df)

end = time.time()
print("Elapsed time: ", end - start)