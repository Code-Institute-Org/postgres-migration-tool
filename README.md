![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

# Reel2Reel

## What is it?

This is a tool for Code Institute students and alumni. It allows you to dump a database from Heroku and upload it to Render/ElephantSQL.

## How do I use it?

You will need to have created a new database on ElephantSQL.

1. Open this repo in Gitpod
2. Run `reel2reel`
3. In a different browser tab, go to your app in Heroku and select the *Settings* tab
4. Click the *Reveal Config Vars* button
5. Copy the value in the `DATABASE_URL` Config Var. It will start with `postgres://`
6. Return to Gitpod and paste in the URL you just copied
7. In a different browser tab, get your ElephantSQL database URL. Again, it will start with `postgres://`
8. Return to Gitpod and paste in the URL where prompted
9. The data will now be downloaded from Heroku and uploaded to your ElephantSQL database

## Problems

Ensure that the URLs are copied correctly. Reel2Reel will throw an error if the URL doesn't start with `postgres://`.
Make sure that you run the process as soon as you copy the Heroku `DATABASE_URL`. Heroku periodically rotates the credentials, which means an old `DATABASE_URL` may not work.

## FAQs

*Can I use this with VSCode?*

Yes, but we'd really prefer you to use it with Gitpod. This repo has the latest versions of the Postgres tools installed to ensure compatibility with Heroku and Render/ElephantSQL. We like VSCode too, but just this once, please use Gitpod.

*I'm a power user. Is there an easier way to use this?*

Absolutely. You can supply the URLs as arguments like so:

`reel2reel <Heroku URL> <ElephentSQL URL>`

*What does it actually do?*

1. Connects to Heroku and dumps the database to a local `dump.sql` file
2. Modifies the `dump.sql` file so that it contains the database name and username for the new database
3. Runs the modified `dump.sql` file against the specified Render/ElephantSQL database

Feel free to examine the code and see if you understand how it works.

## Reel2Reel??

Because we like to <a href="https://www.youtube.com/watch?v=vuo8kD5zF5I" target="_blank">move it, move it.</a>

---

Happy coding!
