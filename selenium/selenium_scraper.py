from __future__ import generator_stop
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions
import time
import pandas as pd


#Linux = True
Linux = False

if Linux == True:
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(options=opts)
else: 
    from selenium.webdriver.edge.service import Service
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
driver.get(url)
links_list = [x.get_attribute('href') for x in driver.find_elements(By.XPATH, '//td[@class = "titleColumn"]/a')]
links_list = links_list[:100]

titles = list()
ratings = list()
popularity_scores = list()
genres = list()

counter = 1

start = time.time()

for link in links_list:
    print(f'Scraping {counter} page')
    driver.get(link)
    time.sleep(2)

    try:
        titles.append(driver.find_element(By.XPATH, '//h1').text)
    except:
        titles.append('')

    try:
        #ratings.append(driver.find_elements(By.XPATH, '//div[@data-testid = "hero-rating-bar__aggregate-rating__score"]/span')[2].text)
        ratings.append(driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[2]/div/div[1]/a/div/div/div[2]/div[1]/span[1]').text)
    except:
        ratings.append('')

    try:
        #popularity_scores.append(driver.find_elements(By.XPATH, '//div[@data-testid = "hero-rating-bar__popularity__score"]')[1].text)
        popularity_scores.append(driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[2]/div/div[3]/a/div/div/div[2]/div[1]').text)
    except:
        popularity_scores.append('Not rated')

    try:
        #genres.append([x.text for x in driver.find_elements(By.XPATH, '//div[@data-testid = "genres"]/a/span')])
        genres.append([x.text for x in driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/div[1]')])
    except:
        genres.append('')

    counter += 1

driver.quit()

genres = [[w.replace("\n", ',') for w in x] for x in genres]
df = pd.DataFrame({'Title': titles, 'IMDb rating': ratings, 'Popularity': popularity_scores, 'Genre': genres})
print(df)

end = time.time()
print("Elapsed time: ", end - start)