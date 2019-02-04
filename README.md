# Twitter Scrape

Scrape Tweets from Twitter into a DB.  Dump Tweets to a different JSON file each minute.

## Installation

* `pip install -r requirements.txt`

## Setup

* Create a file called `private.py`.
* Sign up for a Twitter [developer account](https://dev.twitter.com/).
* Create an application [here](https://apps.twitter.com/).
* Set the following keys in `private.py`.  You can get these values from the app you created:
    * `TWITTER_KEY`
    * `TWITTER_SECRET`
    * `TWITTER_APP_KEY`
    * `TWITTER_APP_SECRET`
* Set the following key in `private.py`.
    * `CONNECTION_STRING` -- use `sqlite:///tweets.db` as a default if you need to.  It's recommended to use postgresql, but not necessary.

## Usage

* `python scraper.py [ARGS]` to scrape.  Use `Ctrl + C` to stop.
* `python scraper.py --help` to get help.
