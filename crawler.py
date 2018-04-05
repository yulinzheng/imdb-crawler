from requests import get
from bs4 import BeautifulSoup
import csv, sqlite3, re

def create_csv():
    with open('top_1000.csv', 'w') as csvfile:
        # initialize csv headers
        fieldnames = ['title', 'year', 'director', 'cast', 'imdb_rating']
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
                year = info.find('span', class_ = 'lister-item-year text-muted unbold').text
                match = re.search('([0-9]+)', year)
                year = year[match.start() : match.end()]
                rating = container.strong.text.strip()
                writer.writerow({'title': title, 'year': year, 'director': director, 'cast': cast, 'imdb_rating': rating})

def create_db():
    create_csv()
    conn = sqlite3.connect('top_1000.db')
    c = conn.cursor()
    c.execute('CREATE TABLE top_1000 (title, year, director, cast, imdb_rating);')
    with open('top_1000.csv', 'r') as csv_file:
        dr = csv.DictReader(csv_file)
        to_db = [(i['title'], i['year'], i['director'], i['cast'], i['imdb_rating']) for i in dr]
    c.executemany('INSERT INTO top_1000 (title, year, director, cast, imdb_rating) VALUES (?, ?, ?, ?, ?);', to_db)
    conn.commit()
    conn.close()

create_db()
