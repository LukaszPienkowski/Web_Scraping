from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import pandas as pd

driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
driver.get(url)
links_list = [x.get_attribute('href') for x in driver.find_elements(By.XPATH, '//td[@class = "titleColumn"]/a')]

titles = list()
ratings = list()
popularity_scores = list()
genres = list()

for link in links_list:
    driver.get(link)
    time.sleep(2)

    try:
        titles.append(driver.find_element(By.XPATH, '//h1').text)
    except:
        titles.append('')

    try:
        ratings.append(driver.find_elements(By.XPATH, '//div[@data-testid = "hero-rating-bar__aggregate-rating__score"]/span')[2].text)
    except:
        ratings.append('')

    try:
        popularity_scores.append(driver.find_elements(By.XPATH, '//div[@data-testid = "hero-rating-bar__popularity__score"]')[1].text)
    except:
        popularity_scores.append('Not rated')

    try:
        genres.append([x.text for x in driver.find_elements(By.XPATH, '//div[@data-testid = "genres"]/a/span')])
    except:
        genres.append('')

    i = i + 1

driver.quit()

df = pd.DataFrame({'Title': titles, 'IMDb rating': ratings, 'Popularity': popularity_scores, 'Genre': genres})
print(df)