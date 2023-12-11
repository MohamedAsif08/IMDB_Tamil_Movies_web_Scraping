import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

S = Service('E:/Selenium/chromedriver.exe')
driver = webdriver.Chrome(service=S)
url = 'https://www.imdb.com/search/title/?title_type=feature&sort=moviemeter,asc&primary_language=ta'
driver.get(url)
time.sleep(5)
try:
    while True:
        try:
            # Scroll to the bottom of the page
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

            # Use WebDriverWait for the button to be clickable
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#__next > main > div.ipc-page-content-container.ipc-page-content-container'
                                            '--center.sc-872d7ac7-0.fqEQWL > '
                                            'div.ipc-page-content-container.ipc-page-content-container--center > section '
                                            '> section > div > section > section > div:nth-child(2) > div > section > '
                                            'div.ipc-page-grid.ipc-page-grid--bias-left.ipc-page-grid__item.ipc-page'
                                            '-grid__item--span-2 > div.ipc-page-grid__item.ipc-page-grid__item--span-2 > '
                                            'div.sc-619d2eab-0.fOxpqs > div > span > button'))
            )
            # Click the button
            driver.execute_script('arguments[0].click();', button)

            # Sleep for a while
            driver.implicitly_wait(25)
        except TimeoutException:
            print("Button not found. Exiting the loop.")
            break

        except Exception as e:
            print(e)

    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')
    data_sec = soup.find('ul',
                         class_="""ipc-metadata-list""")
    data = data_sec.find_all('li')
    rows = []

    for movie in data:
        other_info = []
        rating_info = []
        movie_name = movie.find('h3').text.split(". ")[1]
        others = movie.find('div', class_="""sc-43986a27-7 dBkaPT dli-title-metadata""")
        rating = movie.find('span',
                            class_="""ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating""")
        votes = movie.find('div', class_="""sc-53c98e73-0 kRnqtn""")
        descr = movie.find('div', class_="""ipc-html-content-inner-div""")

        if rating:
            for data in rating:
                rating_info.append(data.text)
        if others is not None:
            for data in others:
                other_info.append(data.text)
        rating_stars = rating_info[1] if rating_info else 'Nil'
        reviewers = rating_info[2].replace("\xa0(", "").replace(')', "") if rating_info else 'Nil'
        duration = other_info[1] if len(other_info) > 1 else 'Nil'
        year = other_info[0] if len(other_info) > 0 else 'Nil'
        description = descr.text if descr else 'Nil'
        voting = votes.text.split("s")[1] if votes else 'Nil'

        rows.append([movie_name, year, duration, rating_stars, voting, description])
        title = ['Movie', 'Year', 'Duration', 'Rating', 'Voting', 'Description']

        #print([movie_name, year, duration, rating_stars, voting, description])
    data = pd.DataFrame(data=rows, columns=title)
    data.to_csv('Tamil_Movies.csv')
    print("Done successfully")
except Exception as e:
    print(e)
