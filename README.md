# Twitter Scrape

Scrapes Tweets from Twitter into a DB.  Dumps Tweets to a different JSON file each minute.

Calculates the number of tweets per minute that contain a particular term in their message.

## Installation

* `pip install -r requirements.txt`

## Usage
* `python scraper.py -h`
* `python count_tweets_per_minute.py -h` or `./count_tweets_per_minute.sh [TERM]` (Docker)

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
