"""
Reel2Reel - a script to move a database from one Postgres
server to to another because we like to move it, move it.

Usage:
    python3 reel2reel.py <Source URL> <Destination URL>
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

    e = urlparse(db_url)

    if not e.hostname or not e.username or not e.password or not e.path:
        print("Error: The URL seems incorrectly formatted.")
        sys.exit(1)

    return e


def parse_dump(h_user, h_db, e_user, e_db):
    """
    Takes the dumped SQL file and replaces the database details
    with the new user and database
    """

    with open("dump.sql", "r", encoding="utf8") as f:

        data = f.read()

        data = re.sub(h_user, e_user, data)
        data = re.sub(h_db, e_db, data)

    with open("dump.sql", "w", encoding="utf8") as f:
        # Why not just open the file as r+ earlier and
        # f.seek(0) to the beginning? Because not all of the
        # file would get overwritten.
        f.write(data)


def do_source(s):
    """
    Performs the dump of the source data
    """

    os.environ["PGPASSWORD"] = s.password

    print("Extracting the source database.")

    res = os.system(f"pg_dump --host={s.hostname} \
        --username={s.username} --dbname={s.path[1:]} -w > dump.sql")

    if res != 0:
        print("Error: Cannot connect to source database server.")
        sys.exit(2)

    print("Extraction successful. File saved to dump.sql.")


def do_dest(d):
    """
    Uploads the modified data to the destination server
    """

    print("Uploading to destination server")

    os.environ["PGPASSWORD"] = d.password

    res = os.system(f"psql --host={d.hostname} --username={d.username} \
                --dbname={d.path[1:]} -w < dump.sql >/dev/null 2>&1")

    if res != 0:
        print("Error: Cannot upload the data to destination.")
        sys.exit(2)

    print("Upload complete. Please check your destination database.")


def main(s_url, d_url):
    """
    The main function. Calls other functions to perform the migration
    """

    s = split_url(s_url)
    d = split_url(d_url)

    do_source(s)

    print("Modifying the downloaded data.")

    parse_dump(s.username, s.path[1:], d.username, d.path[1:])

    do_dest(d)


if __name__ == "__main__":
    print("Reel2Reel - PostgreSQL to PostgreSQL Mover")
    print("Code Institute, 2022\n")

    if len(sys.argv) == 2:
        print("You can supply the source and destination URLs as arguments")
        print("Usage: python3 reel2reel.py <Source DB URL> <Destination DB URL>")
        sys.exit(1)
    if len(sys.argv) > 1:
        source = sys.argv[1]
        dest = sys.argv[2]
    else:
        source = input("Paste your source DATABASE_URL here: ")
        dest = input("Paste your destination DATABASE_URL here: ")

    main(source, dest)
