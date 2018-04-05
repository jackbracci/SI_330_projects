#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict, OrderedDict
import json
import hashlib
import sqlite3 as sqlite

YOUR_UNIQNAME = 'jbracci'  # Fill in your uniqname
MOVIE_DATA_PATH = 'step3.txt'
DB_PATH = "si-330-hw8-{}.db".format(YOUR_UNIQNAME)


def parse_imdb_id(imdb_id):
    return int(imdb_id[2:])


def replace_na(value):
    return value if value != "N/A" else None


def parse_int(value):
    try:
        return int(value)
    except:
        return None


def parse_float(value):
    try:
        return float(value)
    except:
        return None


def main():
    movies = read_movie_data(MOVIE_DATA_PATH)
    actors = get_actors(movies)
    create_database_tables()
    insert_data(movies, actors)
    run_queries()


#STEP 1
def read_movie_data(filename):
    """Read movie data as a list of dictionaries"""
    movies = []

    with open(filename, encoding="utf-8") as f:
        for line in f:
            movie = json.loads(line)

            movies.append({

                'Actors': movie["Actors"].split(", "), 'imdb_id':movie['imdbID']
            })

            # # Parse the movie data, split the actors into a list, and append to `movies`
            # movie = None                       # YOUR CODE HERE: Parse the movie data here
            # movie['Actors'] = movie['Actors']  # YOUR CODE HERE: Change this line to split `movie['Actors']` into a
            #                                    # list instead of leaving it the same. If it helps, look back at your
            #                                    # solution in Homework 5.
            # movies.append(movie)

    return (movies)


#STEP 2
def get_actors(movies):
    """Create a list of actors. Actors are tuples of (imdb_id, first_name, last_name)."""
    all_actors = []

    for movie in movies:
        actors = movie['Actors']
        imdb_id = movie['imdb_id']
        for actor in actors:

            actor = actor.split(" ")
            imdb_id = imdb_id.split(" ")


            # Split each actor into a first name and last name. Take care for actors that don't have a first name and
            # last name. The first name should be BEFORE the FIRST SPACE, and the last name should be the rest of the
            # name. Set the last name to `None` if there is no last name.
            first_name = actor[0]
            try:
                last_name = actor[1]
            except:
                last_name = None
                # YOUR CODE HERE: Re-write to assign last_name to the correct value
            imdb_id = imdb_id[0]    # YOUR CODE HERE: Re-write to assign imdb_id to the correct value
            all_actors.append((imdb_id, first_name, last_name))

    return (all_actors)


# STEP 3
def create_database_tables():
    with sqlite.connect(DB_PATH) as conn:
        cur = conn.cursor()

        # DROP the "movie" table if it exists
        cur.execute("DROP TABLE IF EXISTS movie")
        #
        # CREATE the "movie" table with the following schema:
        # imdb_id (INTEGER PRIMARY KEY)
        # title (TEXT)
        # year (INTEGER)
        # director (TEXT)
        # metascore (INTEGER)
        # imdb_rating (REAL)
        #
        # The "movie" table will store metadata about movies from IMDB/OMDB.
        cur.execute("""
                        CREATE TABLE movie
                        (
                        imdb_id INTEGER PRIMARY KEY,
                        title TEXT,
                        year INTEGER,
                        director TEXT,
                        metascore INTEGER,
                        imdb_rating REAL
                        )
                        """)

        # DROP the "actor" table if it exists
        cur.execute("DROP TABLE IF EXISTS actor")

        # CREATE the "actor" table with the following schema:
        # id (INTEGER PRIMARY KEY)
        # first_name (TEXT)
        # last_name (TEXT)
        #
        # The "actor" table will store the names of all actors.
        cur.execute("""
                        CREATE TABLE actor
                        (
                        id INTEGER PRIMARY KEY,
                        first_name TEXT,
                        last_name TEXT
                        )
                        """)

        # CREATE a UNIQUE INDEX on actors' names to ensure no duplicates
        # See the assignment description for more information

        cur.execute("CREATE UNIQUE INDEX actor_unique ON actor (first_name, last_name)")

        # DROP the "movie_cast" table if it exists
        cur.execute("DROP TABLE IF EXISTS movie_cast")

        # CREATE the "movie_cast" table with the following schema:
        # movie_imdb_id (INTEGER)
        # actor_id (INTEGER)
        #
        # The "movie_cast" table stores the correspondences between each actor
        # and the movies that he or she appeared in.
        cur.execute("""
                        CREATE TABLE movie_cast
                        (
                        movie_imdb_id INTEGER,
                        actor_id INTEGER
                        )
                        """)
        conn.commit()


# STEP 4
def insert_data(movies, actors):
    with sqlite.connect(DB_PATH) as conn:
        cur = conn.cursor()

        # Transform movies data into a list of tuples.
        # Each tuple should have its elements in the following order:
        # (imdbID, Title, Year, Director, Metascore, imdbRating)
        #
        # For integer and float fields, replace non-integers (e.g. year ranges like "2008–2013", or
        # "N/A" strings) with None, which will be translated into `NULL` in SQL. There is a
        # `parse_int()` and a `parse_float()` function provided.
        #
        # For text fields, replace "N/A" with None. There is a `replace_na()` function provided.
        movie_rows = []
        for m in movies:
            movie_rows.append(None)     # YOUR CODE HERE: Replace None with a tuple

        # INSERT movie metadata
        cur.executemany("**YOUR SQL QUERY HERE**", movie_rows)
        conn.commit()

        # Transform actor data into a list of (first_name, last_name) tuples.
        # Use a data structure that eliminates duplicates.
        # For each field, replace "N/A" strings with None, which will
        # correspond to `NULL` in SQL. There is a `replace_na()` function
        # provided.
        actor_rows = None  # YOUR CODE HERE: Replace None with a suitable data structure #
        for a in actors:
            # YOUR CODE HERE #
            pass

        # INSERT actors. Let the database create actor IDs by specifying NULL as the first value field of your INSERT, corresponding to the `actor_id`.
        cur.executemany("**YOUR SQL QUERY HERE**", actor_rows)
        conn.commit()

        # Look up the Actor IDs that the database created for each actor.
        # Your query should return the Actor ID, the first name, and the last name.
        cur.execute("**YOUR SQL QUERY HERE**")
        result_set = cur.fetchall()

        # Store them in a dictionary mapping actor names to actor IDs.
        actor_ids = {}
        for row in result_set:
            actor_ids[(row[1], row[2])] = row[0]

        # Build up a set of movie/actor pairs to insert into the "movie_cast" table
        movie_actor_pairs = []
        for a in actors:
            actor_id = None         # YOUR CODE HERE: Replace None with correct value
            movie_imdb_id = None    # YOUR CODE HERE: Replace None with correct value
            movie_actor_pairs.append((movie_imdb_id, actor_id))

        # INSERT connections between movies and actors
        cur.executemany("**YOUR SQL QUERY HERE**", movie_actor_pairs)
        conn.commit()


# STEP 5
def run_queries():
    # "output" will contain all of the data you queried.
    output = {}

    ### FRAMEWORK CODE: DO NOT EDIT ###
    def dict_factory(cursor, row):
        d = OrderedDict([(x[0], None) for x in cursor.description])
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    ### END FRAMEWORK CODE

    with sqlite.connect(DB_PATH) as conn:
        conn.row_factory = dict_factory
        cur = conn.cursor()

        # 1. What is the total number of movies?
        # Your result should have: 1 column, 1 row.
        cur.execute("**YOUR SQL QUERY HERE**")
        result_set = cur.fetchall()
        print("Question 1: What is the total number of movies?")
        check_results(1, result_set)
        print_as_table(result_set)
        output[1] = result_set

        # 2. What is the total number of actors?
        # Your result should have: 1 column, 1 row.
        cur.execute("**YOUR SQL QUERY HERE**")
        result_set = cur.fetchall()
        print("Question 2: What is the total number of actors?")
        check_results(2, result_set)
        print_as_table(result_set)
        output[2] = result_set

        # 3. What are the 3 most common last names among actors? List the last names, and the number of actors with those last names.
        # Your result should have: 2 columns, 3 rows.
        # Hint: look up the syntax for the SELECT statement; there is a subclause we have not used that will help you
        # restrict the number of rows in your output.
        cur.execute("**YOUR SQL QUERY HERE**")
        result_set = cur.fetchall()
        print("Question 3: What are the 3 most common last names among actors?")
        check_results(3, result_set)
        print_as_table(result_set)
        output[3] = result_set

        # 4. What are the *titles* of IMDB users’ top 10 movies? Query for the titles only. (Hint: use the imdb_rating column)
        # Your result should have: 1 column, 10 rows
        cur.execute("**YOUR SQL QUERY HERE**")
        result_set = cur.fetchall()
        print("Question 4: What are the titles of IMDB users’ top 10 movies?")
        check_results(4, result_set)
        print_as_table(result_set)
        output[4] = result_set

        # 5. Who are the top 10 directors (the 10 directors with the highest average meta score)? Query for the
        # directors and their average metascores (call this column `average_metascore`). Exclude directors that are
        # missing (NULL).
        # Your result should have: 2 column, 10 rows
        cur.execute("**YOUR SQL QUERY HERE**")
        result_set = cur.fetchall()
        print("Question 5: Who are the top 10 directors?")
        check_results(5, result_set)
        print_as_table(result_set)
        output[5] = result_set

        # 6. Who are the top 10 actors: actors with the highest average movie meta score)? Include the actors' first
        # *and* last names, as well as the average meta scores (call this column `average_metascore`). Exclude movies
        # where their metascore is missing.
        # Your result should have: 3 columns, 10 rows
        cur.execute("**YOUR SQL QUERY HERE**")
        result_set = cur.fetchall()
        print("Question 6: Who are the top 10 actors?")
        check_results(6, result_set)
        print_as_table(result_set)
        output[6] = result_set

        # 7. What are the 5 most divisive movies (movies with the largest absolute difference between metascore and
        # (imdb_rating × 10))? List the movie titles as well as their differences in score (call this column
        # `rating_difference`). Exclude movies where their metascore or IMDB rating is missing.
        # Your result should have: 2 columns, 5 rows
        cur.execute("**YOUR SQL QUERY HERE**")
        result_set = cur.fetchall()
        print("Question 7: What are the 5 most divisive movies?")
        check_results(7, result_set)
        print_as_table(result_set)
        output[7] = result_set

        # 8. What were the 5 best years for movies? Rank the years by average metascore, and include the
        # average metascore (as `average_metascore`) in the result.
        # Your result should have: 2 columns, 5 rows
        cur.execute("**YOUR SQL QUERY HERE**")
        result_set = cur.fetchall()
        print("Question 8: What were the 5 best years for movies?")
        check_results(8, result_set)
        print_as_table(result_set)
        output[8] = result_set

        ## BONUS. Who are the 10 longest working actors (actors with the largest timespan between earliest and latest
        ## movie by year)? List the actors as well as the timespan.
        ## Your result should have: 3 columns, 10 rows
        # cur.execute("**YOUR SQL QUERY HERE**")
        # result_set = cur.fetchall()
        # print("BONUS: Who are the 10 longest working actors?")
        # check_results(9, result_set)
        # print_as_table(result_set)
        # output[9] = result_set

    with open("si-330-hw6-{}.json".format(YOUR_UNIQNAME), 'w') as f:
        f.write(json.dumps(output))


### FRAMEWORK CODE: DO NOT EDIT BELOW THIS LINE ###
def print_as_table(d):
    def uniq(l):
        s = {}
        return [s.setdefault(x, x) for x in l if x not in s]

    print("---")
    t = defaultdict(list)
    keys = uniq(sum([list(i.keys()) for i in d], []))
    for k in keys:
        values = [r[k] for r in d]
        t[k].extend(values)
    print(("{:<25} " * len(keys)).format(*iter(keys)))
    for v in zip(*(t[k] for k in keys)): print(("{:<25} " * len(v)).format(*v))
    print("===\n")


def hash_results(results):
    return hashlib.sha1(
        "".join(sorted(sum([list(str(z) for z in y.values()) for y in results], []))).encode()).hexdigest()


def check_results(question, results):
    hashes = {
        1: '310b86e0b62b828562fc91c7be5380a992b2786a',
        2: '6e21fce62b88ee824118ee6f3d791d78a748f9a5',
        3: '5737107525439887161ca0305c18129e6f45ea13',
        4: '7617f46fbb8f045bf014655eb4def2b0b896f357',
        5: '858197c604644ff09f996c34c2affc5403c3031a',
        6: 'dde04241b682343a3c67cf716913040da32e7e55',
        7: 'c1a9816e7e1e22c76fb768bdc67a8fa83c386245',
        8: '5aafec0e1900dbed036e77951feb7f96abc32fc3',
        9: '16890aedf945a25098a404e71c675a1b8e910d5f'
    }
    hashed_results = hash_results(results)
    verdict = "PASS!" if hashes[question] == hashed_results else "FAIL."
    print("{}: {}".format(hashed_results, verdict))


### END FRAMEWORK CODE ###

if __name__ == '__main__':
    main()
