import settings
import tweepy
import dataset
from textblob import TextBlob
from datafreeze import freeze
from datetime import datetime


def dump_db(db, date_now):
    file_name = "tweets-{0}.json".format(date_now)
    result = db[date_now].all()
    print("[{0}] Exporting to {1}...".format(str(datetime.now()), file_name))
    freeze(result, format='json', filename="tweets-{0}.json".format(date_now))