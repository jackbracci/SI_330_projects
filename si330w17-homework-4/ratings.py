import re
from collections import defaultdict
import bs4
from bs4 import BeautifulSoup
from urllib.request import urlopen

with urlopen('http://www.imdb.com/search/title?at=0&sort=num_votes&count=100') as f:
    soup = BeautifulSoup(f)

headers = soup.final_all('h3', class)

ratings_divs = soup.find_all('div', class_ = 'inline-block ratings-imdb-rating')
ratings = []
for r in ratings_divs:
    ratings.append(r.strong.string)
print(ratings)
