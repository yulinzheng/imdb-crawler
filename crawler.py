from requests import get
from bs4 import BeautifulSoup
import csv

with open('top_1000.csv', 'w') as csvfile:
    # TODO table title: top 1000 imdb movies
    fieldnames = ['Movie Title', 'Director', 'Cast', 'IMDB Rating']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'Movie Title': '0', 'Director': '0', 'Cast': '0', 'IMDB Rating': '0'})

url = 'http://www.imdb.com/search/title?groups=top_1000&sort=user_rating&view=simple&page=1'
response = get(url)
# create BeautifulSoup object
html_soup = BeautifulSoup(response.text, 'html.parser')
# extract 50 movie containers
movie_containers = html_soup.find_all('div', class_ = 'lister-col-wrapper')
first_movie = movie_containers[1]
header = first_movie.find('span', class_ = 'lister-item-header')
header = header.find_all('span')[1]
title = header.a.text
print(title)
ppl = header['title']
print(ppl)
year = header.find('span', class_ = 'lister-item-year text-muted unbold').text
print(year)
