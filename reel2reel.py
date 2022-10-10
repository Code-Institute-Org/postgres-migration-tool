"""
Reel2Reel - a script to move a database from Heroku to Render

Usage:
    python3 reel2reel.py <Heroku URL> <Render URL>
    or interactively:
    python3 reel2reel.py

Matt Rudge
Code Institute
October, 2022
"""
import os
import re
import sys
from urllib.parse import urlparse


def split_url(db_url):
    """
    Performs a cursory check on the URL and then
    parses it using urllib
    """

    if db_url[0:11] != "postgres://":
        print("Error: The URL seems incorrectly formatted.")
        sys.exit(1)
    
    return urlparse(db_url)


def parse_dump(h_user, h_db, r_user, r_db):
    """
    Takes the dumped SQL file and replaces the database details
    with the new user and database
    """
    
    with open("dump.sql", "r") as f:

        data = f.read()

        data = re.sub(h_user, r_user, data)
        data = re.sub(h_db, r_db, data)
    
    with open("dump.sql", "w") as f:
        f.write(data)

def main(heroku, render):
    """
    The main function. Connects to Heroku and ElephantSQL
    using built-in Postgres functions
    """

    h = split_url(heroku)
    r = split_url(render)

    os.environ["PGPASSWORD"] = h.password

    print("Extracting the database from Heroku.")

    try:
        os.system(f"pg_dump --host={h.hostname} --username={h.username} \
                    --dbname={h.path[1:]} -w > dump.sql")
    except:
        print("An error occurred connecting to Heroku.")
        sys.exit(2)
    
    print("Extraction successful. File saved to dump.sql.")
    print("Modifying the downloaded data.")

    parse_dump(h.username, h.path[1:], r.username, r.path[1:])

    print("Uploading to ElephantSQL")

    os.environ["PGPASSWORD"] = r.password

    try:
        os.system(f"psql --host={r.hostname} --username={r.username} \
                    --dbname={r.path[1:]} -w < dump.sql >/dev/null 2>&1")
    except:
        print("Error uploading the data to ElephantSQL")
        sys.exit(2)

    print("Upload complete. Please check your ElephantSQL database")


if __name__ == "__main__":
    print("Reel2Reel - Heroku to ElephantSQL Mover")
    print("Code Institute, 2022\n")

    if len(sys.argv) == 2:
        print("You can supply the Heroku and Render URLs as arguments")
        print("Usage: python3 reel2reel.py <Heroku DB URL> <Render DB URL>")
        sys.exit(1)
    if len(sys.argv) > 1:
        heroku = sys.argv[1]
        render = sys.argv[2]
    else:
        heroku = input("Paste your Heroku DATABASE_URL here: ")
        render = input("Paste your ElephantSQL DATABASE_URL here: ")
    
    main(heroku, render)
