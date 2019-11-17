# Varjo Sport Lambda Scraper

Scrapes the basic info (mainly business hours) of all Unisport gyms.

Why you ask? Because as of now you can't view them all on one page and they are two clicks away from the frontpage. Who designed such retarded system, I don't know, but to me it's annoying since I have no interest in other stuff than seeing how long its open today.

# How to run the scraper locally

Requires Python >=3.6 with preferably virtualenv. I use `virtualenv-wrapper`, some have said `pyenv` is pretty good too.

1. Activate your virtualenv eg `workon varjos`
2. Install dependencies: `pip install -r requirements.txt` (installs only [Scrapy](https://scrapy.org/))
3. Load the dev commands: `. cmds.sh`
4. Create the output folders: `init`
5. Run the spider: `crawl`

You should get `./frontend/unisport.json` file with the data scraped.

# How to run the test server

Requires Node.js >=10 (probably 8 works too).

1. Run: `node server.js`
2. The server should run at http://localhost:4040/

Reload the page after making changes to the files inside `frontend`-folder.