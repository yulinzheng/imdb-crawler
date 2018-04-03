from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import csv

def create_csv():
    with open('top_1000.csv', 'w') as csvfile:
        # initialize csv headers
        fieldnames = ['Movie Title', 'Year', 'Director', 'Cast', 'IMDB Rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # scrape page 1-20
        pages = [str(i) for i in range(1, 21)]
        for page in pages:
            url = 'http://www.imdb.com/search/title?groups=top_1000&sort=user_rating&view=simple&page=' + page
            response = get(url)
            # create BeautifulSoup object
            html_soup = BeautifulSoup(response.text, 'html.parser')
            # extract 50 movie containers
            movie_containers = html_soup.find_all('div', class_ = 'lister-col-wrapper')
            for container in movie_containers:
                header = container.find('span', class_ = 'lister-item-header')
                info = header.find_all('span')[1]
                title = info.a.text
                people = info['title']
                director = people[:people.find('(')].strip()
                cast = people[people.find(')')+2:].strip()
                year = info.find('span', class_ = 'lister-item-year text-muted unbold').text[1:-1]
                rating = container.strong.text.strip()
                writer.writerow({'Movie Title': title, 'Year': year, 'Director': director, 'Cast': cast, 'IMDB Rating': rating})
#create_csv()
