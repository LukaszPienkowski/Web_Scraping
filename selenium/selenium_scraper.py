from pickle import TRUE
from regex import F
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions
import time
import pandas as pd

limit_100_pages = True
#limit_100_pages = False

## Scrapping pages of top100 movies rated in IMDB using Selenium package 
opts = FirefoxOptions()
opts.add_argument("--headless")
driver = webdriver.Firefox(options=opts)
url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
driver.get(url)
if limit_100_pages:
    links_list = [x.get_attribute('href') for x in driver.find_elements(By.XPATH, '//td[@class = "titleColumn"]/a')][:100]
else:
    links_list = [x.get_attribute('href') for x in driver.find_elements(By.XPATH, '//td[@class = "titleColumn"]/a')]

## Empty lists for movies data
titles = list()
ratings = list()
popularity_scores = list()
genres = list()

counter = 1
start = time.time()

## Scraping selected data from each page
for link in links_list:
    print(f'Scraping {counter} page')
    driver.get(link)
    time.sleep(2)

    try:
        titles.append(driver.find_element(By.XPATH, '//h1').text)
    except:
        titles.append('')

    try:
        ratings.append(driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[2]/div/div[1]/a/div/div/div[2]/div[1]/span[1]').text)
    except:
        ratings.append('')

    try:
        popularity_scores.append(driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[2]/div/div[3]/a/div/div/div[2]/div[1]').text)
    except:
        popularity_scores.append('Not rated')

    try:
        genres.append(driver.find_element(By.XPATH, '//div[@data-testid = "genres"]').text.split('\n'))
    except:
        genres.append('')

    counter += 1

driver.quit()

## This line changes substring in genres list to end up with proper style of data
genres = [[w.replace("\n", ',') for w in x] for x in genres]
df = pd.DataFrame({'Title': titles, 'IMDb rating': ratings, 'Popularity': popularity_scores, 'Genre': genres})
print(df)

end = time.time()
print("Elapsed time: ", end - start)