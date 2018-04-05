import tweepy
import csv
from textblob import TextBlob
import os


#This code will use the tweepy module and access the Twitter API based on a key word search

# Unique code from Twitter
access_token = "331897710-t8nnZuAh1ofe0lCUSfKBQNlqBOMHgGUooIy5UN4x"
access_token_secret = "FNc3y1c8FgzFezvAf0ml5ofVEAE3JE7f1zSsyq7W8OeFE"
consumer_key = "ixWyhyZ1BDfiy2qgSLGjrA57y"
consumer_secret = "m1rjKpFhfXhRBzET9dEPIciaY4HHHQAj5urznBlm7yY7273BYk"

# Authenticating my consumer_keys and access_tokens
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

#setting the variable api equal to tweepy with my authentications
api = tweepy.API(auth)

#Setting the variables to call and name the csv files that will be created
star_wars = 'Star_Wars_Results.csv'
avatar = 'Avatar_Results.csv'
jurassic_World ='Jurassic_Results.csv'
Avengers ='Avengers_Results.csv'
Dark_Knight = 'Dark_Knight_Results.csv'

#Setting variables to call the Keywords in each function
starwars_keyword = "Star Wars"
avatar_keyword = "Avatar"
jurassic_keyword = "Jurassic World"
avengers_keyword = "Avengers"
darkknight_keyword = "Dark Knight"


#Main Function for each individual one to then call the files to call above
def main():
    print("Fetching Star_Wars Twitter Data")
    fetch_Star_Wars(star_wars)
    print("Fetching Avatar Twitter Data")
    fetch_Avatar(avatar)
    print("Fetching Jurassic_World Twitter Data")
    fetch_jurassic_world(jurassic_World)
    print("Fetching The Avengers Twitter Data")
    fetch_avengers(Avengers)
    print("Fetching The Dark Knight Twitter Data")
    fetch_dark_knight(Dark_Knight)

#First Function to fetch and retrive the Starwars Tweets
def fetch_Star_Wars(filename):
    # If the name of the file already exists then skip this function, if not proceed forward
    # if os.path.exists(filename):
    #     return
# Open/create a file to append data to
    csvFile = open(filename, 'w')
    #Writing the Names to the top of the CSV file
    csvFile.write("Created,Polarity,Favorite_Count,Retweet_Count,ID, User_Name,Tweet\n")
    csvWriter = csv.writer(csvFile)
    #Setting ids to a set so there will not be any repeats in a set
    ids = set()
    # Using a for loop to iterate using Tweepy.Cursor and then passing in the specified key word for individual results
    print("Writing into " + str(filename))
    for tweet in tweepy.Cursor(api.search,
                               q= starwars_keyword,
                               count=200,
                               rpp = 100,
                               since = "2017-04-01",
                               until = "2017-04-9",
                               lang = "en").items(1000):
        #Using TextBlob in order to later use the polarity function to analyze each tweet
        analysis = TextBlob(tweet.text)

        #Making sure that each tweet is only posted once and there are no retweets
        if (not tweet.retweeted) and ('RT @' not in tweet.text):
        # Write a row to the CSV file with the specified values for each tweet
            csvWriter.writerow(
                [tweet.created_at, analysis.polarity , tweet.favorite_count, tweet.retweet_count, tweet.id,
                tweet.user.screen_name,tweet.text.encode('utf-8')])
            ids.add(tweet.id)  # add new id
    print("number of unique ids ", format(len(ids)),"\n")
    csvFile.close()

def fetch_Avatar(filename):
    # If the name of the file already exists then skip this function, if not proceed forward
    if os.path.exists(filename):
        return

# Open/create a file to append data to
    csvFile = open(filename, 'w')

    #Writing the Names to the top of the CSV file
    csvFile.write("Created,Polarity,Favorite_Count,Retweet_Count,ID, User_Name,Tweet\n")
    csvWriter = csv.writer(csvFile)

    #Setting ids to a set so there will not be any repeats in a set
    ids = set()

    # Using a for loop to iterate using Tweepy.Cursor and then passing in the specified key word for individual results
    print("Writing into " + str(filename))
    for tweet in tweepy.Cursor(api.search,
                               q= avatar_keyword,
                               count=200,
                               rpp = 100,
                               since = "2017-04-01",
                               until = "2017-04-9",
                               lang = "en").items(1000):
        #Using TextBlob in order to later use the polarity function to analyze each tweet
        analysis = TextBlob(tweet.text)

        #Making sure that each tweet is only posted once and there are no retweets
        if (not tweet.retweeted) and ('RT @' not in tweet.text):
        # Write a row to the CSV file with the specified values for each tweet

            csvWriter.writerow(
                [tweet.created_at, analysis.polarity , tweet.favorite_count, tweet.retweet_count, tweet.id,
                tweet.user.screen_name,tweet.text.encode('utf-8')])

            ids.add(tweet.id)  # add new id
    print("number of unique ids ", format(len(ids)),"\n")

    csvFile.close()

def fetch_jurassic_world(filename):
    # If the name of the file already exists then skip this function, if not proceed forward
    if os.path.exists(filename):
        return

# Open/create a file to append data to
    csvFile = open(filename, 'w')

    #Writing the Names to the top of the CSV file
    csvFile.write("Created,Polarity,Favorite_Count,Retweet_Count,ID, User_Name,Tweet\n")
    csvWriter = csv.writer(csvFile)

    #Setting ids to a set so there will not be any repeats in a set
    ids = set()

    # Using a for loop to iterate using Tweepy.Cursor and then passing in the specified key word for individual results
    print("Writing into " + str(filename))
    for tweet in tweepy.Cursor(api.search,
                               q= jurassic_keyword,
                               count=200,
                               rpp = 100,
                               since = "2017-04-01",
                               until = "2017-04-9",
                               lang = "en").items(1000):
        #Using TextBlob in order to later use the polarity function to analyze each tweet
        analysis = TextBlob(tweet.text)

        #Making sure that each tweet is only posted once and there are no retweets
        if (not tweet.retweeted) and ('RT @' not in tweet.text):
        # Write a row to the CSV file with the specified values for each tweet

            csvWriter.writerow(
                [tweet.created_at, analysis.polarity , tweet.favorite_count, tweet.retweet_count, tweet.id,
                tweet.user.screen_name,tweet.text.encode('utf-8')])

            ids.add(tweet.id)  # add new id
    print("number of unique ids ", format(len(ids)),"\n")

    csvFile.close()

def fetch_avengers(filename):
    # If the name of the file already exists then skip this function, if not proceed forward
    if os.path.exists(filename):
        return

# Open/create a file to append data to
    csvFile = open(filename, 'w')

    #Writing the Names to the top of the CSV file
    csvFile.write("Created,Polarity,Favorite_Count,Retweet_Count,ID, User_Name,Tweet\n")
    csvWriter = csv.writer(csvFile)

    #Setting ids to a set so there will not be any repeats in a set
    ids = set()

    # Using a for loop to iterate using Tweepy.Cursor and then passing in the specified key word for individual results
    print("Writing into " + str(filename))
    for tweet in tweepy.Cursor(api.search,
                               q= avengers_keyword,
                               count=200,
                               rpp = 100,
                               since = "2017-04-01",
                               until = "2017-04-9",
                               lang = "en").items(1000):
        #Using TextBlob in order to later use the polarity function to analyze each tweet
        analysis = TextBlob(tweet.text)

        #Making sure that each tweet is only posted once and there are no retweets
        if (not tweet.retweeted) and ('RT @' not in tweet.text):
        # Write a row to the CSV file with the specified values for each tweet

            csvWriter.writerow(
                [tweet.created_at, analysis.polarity , tweet.favorite_count, tweet.retweet_count, tweet.id,
                tweet.user.screen_name,tweet.text.encode('utf-8')])

            ids.add(tweet.id)  # add new id
    print("number of unique ids ", format(len(ids)),"\n")

    csvFile.close()

def fetch_dark_knight(filename):
    # If the name of the file already exists then skip this function, if not proceed forward
    if os.path.exists(filename):
        return

# Open/create a file to append data to
    csvFile = open(filename, 'w')

    #Writing the Names to the top of the CSV file
    csvFile.write("Created,Polarity,Favorite_Count,Retweet_Count,ID, User_Name,Tweet\n")
    csvWriter = csv.writer(csvFile)

    #Setting ids to a set so there will not be any repeats in a set
    ids = set()

    # Using a for loop to iterate using Tweepy.Cursor and then passing in the specified key word for individual results
    print("Writing into " + str(filename))
    for tweet in tweepy.Cursor(api.search,
                               q= darkknight_keyword,
                               count=200,
                               rpp = 100,
                               since = "2017-04-01",
                               until = "2017-04-9",
                               lang = "en").items(1000):
        #Using TextBlob in order to later use the polarity function to analyze each tweet
        analysis = TextBlob(tweet.text)

        #Making sure that each tweet is only posted once and there are no retweets
        if (not tweet.retweeted) and ('RT @' not in tweet.text):
        # Write a row to the CSV file with the specified values for each tweet

            csvWriter.writerow(
                [tweet.created_at, analysis.polarity , tweet.favorite_count, tweet.retweet_count, tweet.id,
                tweet.user.screen_name,tweet.text.encode('utf-8')])

            ids.add(tweet.id)  # add new id
    print("number of unique ids ", format(len(ids)),"\n")

    csvFile.close()

if __name__ == '__main__':
    main()



