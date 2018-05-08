Web scraping with Python and BeautifulSoup for top 1000 IMDB movies.

### Prerequisites
Script requires **beautifulsoup4** and **flask** to run.
Install missing packages with **pip3**:
```
pip3 install <package-name>
```

### Running and Testing
Run `crawler.py` first if `top_1000.db` hasn't been generated:
```
python3 crawler.py
```
To test API responses, run `app.py` and visit `localhost:5000` in your web browser.
Try query the database with
* full/partial title: `localhost:5000/title=?`
* year: `localhost:5000/year=?`
* director's full/partial name: `localhost:5000/director=?`
* IMDB rating: `localhost:5000/rating>=?`

### TODOs:
As of 4/5/18:
* Connect SQLAlchemy to database for convenience and security (minimize SQL code, handle changes to the schema, prevent SQL injection, etc.)
* Accept multiple parameters (e.g. `localhost:5000/year=?&rating>=?`)
* Create a simple UX
