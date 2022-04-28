from urllib import request as re
from bs4 import BeautifulSoup as BS
import pandas as pd

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
html = re.urlopen(url)
bs = BS(html.read(), 'html.parser')


bs_links = bs.find_all('td', {'class' : 'titleColumn'})
links = ['https://www.imdb.com' + tag.a['href'] for tag in bs_links]
df = pd.DataFrame(links[0:100])
print(df)