![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

# Reel2Reel

## What is it?

This is a tool for Code Institute students and alumni. It allows you to dump a database from one Postgres server and upload it to another.

## How do I use it?

You will need to have created a new database using our [Database Creator app](https://dbs.ci-dbs.net).

1. Open this repo in your chosen IDE
2. Run `python3 reel2reel.py` (Note: If you use Gitpod or Codeanywhere/Daytona, you can simply type `reel2reel`)
3. Paste in the database URL of the source database - the one you want to copy from. It will start with `postgres://`
4. Now paste in the database URL of the target database, probably the one created by the Database Creator app. Again, it will start with `postgres://`
5. The data will now be downloaded from Heroku and uploaded to your ElephantSQL database

## Problems

- Ensure that the URLs are copied correctly. Reel2Reel will throw an error if the URL doesn't start with `postgres://`.
- If you are copying from a Heroky database instance then make sure that you run the process as soon as you copy the Heroku `DATABASE_URL`. Heroku periodically rotates the credentials, which means an old `DATABASE_URL` may not work.

## FAQs

*Can I use this with VSCode?*

Yes, you will need to install the latest versions of the Postgres command line client `psql`.

*I'm a power user. Is there an easier way to use this?*

Absolutely. You can supply the URLs as arguments like so:

`python3 reel2reel.py <Source URL> <Destination URL>`

*What does it actually do?*

1. Connects to the source database and dumps it to a local `dump.sql` file
2. Modifies the `dump.sql` file so that it contains the database name and username for the new database
3. Runs the modified `dump.sql` file against the specified destination database

Feel free to examine the code and see if you understand how it works.

## Reel2Reel??

Because we like to <a href="https://www.youtube.com/watch?v=vuo8kD5zF5I" target="_blank">move it, move it.</a>

---

Happy coding!
