"""
Reel2Reel - a script to move a database from Heroku to Render
because we like to move it, move it.

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
    Performs checks on the URL for completeness and then
    parses it using urllib
    """

    if db_url[0:11] != "postgres://":
        print("Error: The URL seems incorrectly formatted.")
        sys.exit(1)

    r = urlparse(db_url)

    if not r.hostname or not r.username or not r.password or not r.path:
        print("Error: The URL seems incorrectly formatted.")
        sys.exit(1)

    return r


def parse_dump(h_user, h_db, r_user, r_db):
    """
    Takes the dumped SQL file and replaces the database details
    with the new user and database
    """

    with open("dump.sql", "r", encoding="utf8") as f:

        data = f.read()

        data = re.sub(h_user, r_user, data)
        data = re.sub(h_db, r_db, data)

    with open("dump.sql", "w", encoding="utf8") as f:
        # Why not just open the file as r+ earlier and
        # f.seek(0) to the beginning? Because not all of the
        # file would get overwritten.
        f.write(data)


def do_heroku(h):
    """
    Performs the dump of the Heroku data
    """

    os.environ["PGPASSWORD"] = h.password

    print("Extracting the database from Heroku.")

    res = os.system(f"pg_dump --host={h.hostname} \
        --username={h.username} --dbname={h.path[1:]} -w > dump.sql")

    if res != 0:
        print("Error: Cannot connect to Heroku.")
        sys.exit(2)

    print("Extraction successful. File saved to dump.sql.")


def do_render(r):
    """
    Uploads the modified data to Render/ElephantSQL
    """

    print("Uploading to ElephantSQL")

    os.environ["PGPASSWORD"] = r.password

    res = os.system(f"psql --host={r.hostname} --username={r.username} \
                --dbname={r.path[1:]} -w < dump.sql >/dev/null 2>&1")

    if res != 0:
        print("Error: Cannot upload the data to ElephantSQL.")
        sys.exit(2)

    print("Upload complete. Please check your ElephantSQL database.")


def main(h_url, r_url):
    """
    The main function. Calls other functions to perform the migration
    """

    h = split_url(h_url)
    r = split_url(r_url)

    do_heroku(h)

    print("Modifying the downloaded data.")

    parse_dump(h.username, h.path[1:], r.username, r.path[1:])

    do_render(r)


if __name__ == "__main__":
    print("Reel2Reel - Heroku to ElephantSQL Mover")
    print("Code Institute, 2022\n")

    if len(sys.argv) == 2:
        print("You can supply the Heroku and ElephantSQL URLs as arguments")
        print("Usage: python3 reel2reel.py <Heroku DB URL> <Elephant DB URL>")
        sys.exit(1)
    if len(sys.argv) > 1:
        heroku = sys.argv[1]
        render = sys.argv[2]
    else:
        heroku = input("Paste your Heroku DATABASE_URL here: ")
        render = input("Paste your ElephantSQL DATABASE_URL here: ")

    main(heroku, render)
