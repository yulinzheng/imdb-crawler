from requests import get
from bs4 import BeautifulSoup
import csv, sqlite3, re

def create_csv():
    with open('top_1000.csv', 'w') as csvfile:
        # initialize csv headers
        fieldnames = ['title', 'year', 'duration', 'genre', 'imdb_rating', 'metascore_rating', 'director', 'cast']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # scrape page 1-20
        pages = [i for i in range(0, 1)]
        for page in pages:
            url = 'https://www.imdb.com/search/title/?groups=top_1000&view=advanced&sort=user_rating,desc&start=' + str(page*50)
            response = get(url)
            # create BeautifulSoup object
            html_soup = BeautifulSoup(response.text, 'html.parser')
            # extract 50 movie containers
            movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')
            for container in movie_containers:
                header = container.find('h3', class_ = 'lister-item-header')
                title = header.a.text.strip()
                year = container.find('span', class_ = "lister-item-year text-muted unbold").text[1:5].strip()
                duration = container.find('span', class_ = 'runtime').text[:-3].strip()                
                genre = container.find('span', class_ = 'genre').text.strip()
                imdb_rating = container.find('div', class_ = 'ratings-bar').find('strong').text.strip()
                try:
                    metascore_rating = container.find('div', class_ = 'inline-block ratings-metascore').span.text.strip()
                except:
                    metascore_rating = "-"
                people = container.find('p', class_ = '').find_all('a')
                director = people[0].text.strip()
                cast = ", ".join([i.text.strip() for i in people[1:]])
                writer.writerow({'title': title, 'year': year, 'duration': duration, 'genre': genre, 'imdb_rating': imdb_rating, 'metascore_rating': metascore_rating, 'director': director, 'cast': cast})


def create_db():
    create_csv()
    conn = sqlite3.connect('top_1000.db')
    c = conn.cursor()
    c.execute('CREATE TABLE top_1000 (title, year, duration, genre, imdb_rating, metascore_rating, director, cast);')
    with open('top_1000.csv', 'r') as csv_file:
        dr = csv.DictReader(csv_file)
        to_db = [(i['title'], i['year'], i['duration'], i['genre'], i['imdb_rating'], i['metascore_rating'], i['director'], i['cast']) for i in dr]
    c.executemany('INSERT INTO top_1000 (title, year, duration, genre, imdb_rating, metascore_rating, director, cast) VALUES (?, ?, ?, ?, ?, ?, ?, ?);', to_db)
    conn.commit()
    conn.close()

create_db()