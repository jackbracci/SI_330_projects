from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import csv
import json

# My name is Jonathan Bracci and this is my final project for SI 330 Data Manipulation
#This code will parse through the imdb webpage and pull the html and also use the omdb api to extract data


# Main def to call the other functions fetch_top50_grossing_movies(),extract_movie_info(),imdb_meta(),extract_more()
def main():
    print("Fetching top 50 Grossing Movies into html\n")
    fetch_top50_grossing_movies()
    print("Extracting Movie Info into csv\n")
    extract_movie_info()
    print("Using IMDB To Get Metadata\n")
    imdb_meta()
    print("Extracting additional data\n")
    extract_more()

# Opening the imdb web page for top grossing movies and then defining Beautiful soup of that html as soup
with urlopen("http://www.imdb.com/search/title?genres=action&sort=boxoffice_gross_us,desc") as x:
    soup = BeautifulSoup(x, 'html.parser')

def fetch_top50_grossing_movies():
    # If the name of the html file already exists then skip this function, if not proceed forward
    if os.path.exists('top50_grossing.html'):
        return

    #Setting response equal to opening the webpage and html to reading the webpage to be parsed
    response = urlopen('http://www.imdb.com/search/title?genres=action&sort=boxoffice_gross_us,desc')
    html = response.read()
    #decoding html with utf-8
    html = html.decode('utf-8')

    # Writing response html into top50_grossing.html
    with open('top50_grossing.html', 'w', encoding="utf-8") as outfile:
        outfile.write(html)

def extract_movie_info():
    # If the name of the file already exists then skip this function, if not proceed forward
    if os.path.exists('movie_info.csv'):
        return

    #Opening a new csv file movie_info.csv and writing the three headers: IMDB_ID, Rank, Title
    csvFile = open("movie_info.csv", 'w')
    csvFile.write("IMDB_ID, Rank, Title\n")
    csvWriter = csv.writer(csvFile)

    # Reading top_grossing.html
    # Read in binary mode (... 'rb') instead of (... 'r', encoding='utf-8')
    # because BeautifulSoup will decode the file from utf-8 itself
    with open('top50_grossing.html', 'rb') as infile:
        html = infile.read()

    # Parse using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    #Finding all movie rows in the top 50 grossing movies html
    movie_rows = soup.find_all("div", class_="lister-item")

    # Creating an empty list to iterate through each row and extract IMDB_ID, Rank, and Title
    movie_list = []
    for row in movie_rows:
        movie = {
            "IMDB_ID": row.a.attrs["href"].split("/")[2],
            "Rank": row.span.string.rstrip("."),
            "Title": row.h3.a.string
        }
        movie_list.append(movie)

    # Writing into the csv as defined above
        csvWriter.writerow([movie["IMDB_ID"],movie["Rank"],movie["Title"]])

    # opening a txt file and appending movie list rows into the txt
    with open('top50.txt', 'w', newline='', encoding="utf-8") as outfile:
        data_writer = csv.DictWriter(outfile,
                                     fieldnames=['IMDB_ID', 'Rank', 'Title'],
                                     extrasaction='ignore',
                                     delimiter='\t', quotechar='"')
        data_writer.writeheader()
        data_writer.writerows(movie_list)
    csvFile.close()


def imdb_meta():
    # If the name of the file already exists then skip this function, if not proceed forward
    if os.path.exists('imdb_meta.txt'):
        return

    #Read top50.txt for IMDB_ID, which will be used in OMDB request
    with open('top50.txt', 'r', encoding="utf-8") as infile:
        movie_reader = csv.DictReader(infile, delimiter='\t', quotechar='"')

    #For each movie, use OMDB API to get JSON metadata and store it in 'out' list
        out = []
        count = 0
        total = 50
        for movie in movie_reader:
            response = urlopen ('http://www.omdbapi.com/?i=' + movie['IMDB_ID'] )
            read = response.read().decode("utf-8")
            out.append(read)
            count += 1
            print('{0:3}/{1}'.format(count, total))
        print("\n")

    # Store each JSON in that list as a line in imdb_meta.txt
    with open('imdb_meta.txt', 'w', encoding='utf-8') as outfile:
        json_strings = '\n'.join(out)
        outfile.write(json_strings)

def extract_more():
    # If the name of the file already exists then skip this function, if not proceed forward
    if os.path.exists('Final_Info.csv'):
        return
    csvFile = open("Final_Info.csv", 'w')
    csvFile.write("imdb, Gross_Earnings, Votes,imdb_rating, Year\n")
    csvWriter = csv.writer(csvFile)

    # For each imdb_id parsing through to find specific dictionary keys as desired
    with open('imdb_meta.txt', 'r', encoding='utf-8') as infile:
        for line in infile:
            movie = json.loads(line)
            imdb_id = movie['imdbID']
            Gross_Earnings = movie['BoxOffice']
            imdb_rating = movie['imdbRating']
            year = movie["Year"]
            votes = movie["imdbVotes"]

            csvWriter.writerow([imdb_id,Gross_Earnings, votes,imdb_rating,year])
        csvFile.close()

    print("\nFINISHED")

if __name__ == '__main__':
    main()
