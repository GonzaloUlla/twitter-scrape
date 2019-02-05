import settings
import tweepy
import dataset
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import json
import argparse
from datetime import datetime
import time
import threading
from dump import dump_db

db = dataset.connect(settings.CONNECTION_STRING)


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.retweeted:
            return

        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        geo = status.geo
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color
        blob = TextBlob(text)
        sent = blob.sentiment

        if geo is not None:
            geo = json.dumps(geo)

        if coords is not None:
            coords = json.dumps(coords)

        table = db[datetime.now().strftime("%Y-%m-%d-%H_%M")]
        try:
            table.insert(dict(
                user_description=description,
                user_location=loc,
                coordinates=coords,
                text=text,
                geo=geo,
                user_name=name,
                user_created=user_created,
                user_followers=followers,
                id_str=id_str,
                created=created,
                retweet_count=retweets,
                user_bg_color=bg_color,
                polarity=sent.polarity,
                subjectivity=sent.subjectivity,
            ))
        except ProgrammingError as err:
            print(err)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY,
                           settings.TWITTER_APP_SECRET)
auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)


parser = argparse.ArgumentParser(
    description='Scrape and publish Tweets to a .json file each minute.')

parser.add_argument("-l", "--language", dest="language", nargs='*', default=None,
                    help="BCP 47 language identifier of delivered Tweets", metavar="LAN")
parser.add_argument("-t", "--track", dest="track", nargs='*', default=None,
                    help="phrase used to determine delivered Tweets", metavar="TERM")
parser.add_argument("-f", "--follow", dest="follow", nargs='*', default=None,
                    help="user ID of whose Tweets should be delivered", metavar="ID")
parser.add_argument("-g", "--geolocation", dest="geolocation", nargs='*', default=None,
                    help="a longitude,latitude pair specifying a set of bounding boxes to filter Tweets by", metavar="Lo1,La1,Lo2,La2")
parser.add_argument("-s", "--stall-warnings", dest="stall_warnings", default=False,
                    help="True will send periodic messages if the client is in danger of being disconnected", metavar="False")
parser.add_argument("-fl", "--filter-level", dest="filter_level", default=None,
                    help="None, low, or medium will set min value of the filter_level Tweet attribute required", metavar="None")

args = parser.parse_args()
print("Arguments passed: {0}".format(str(args)[10:-1]))


def dump_json_worker():
    while True:
        date_now = datetime.now().strftime("%Y-%m-%d-%H_%M")
        time_sleep = 60 if datetime.now().second < 50 else 10
        time.sleep(time_sleep)
        db = dataset.connect(settings.CONNECTION_STRING)
        dump_db(db, date_now)
        db.executable.close()


if datetime.now().second is not 0:
    time_sleep = 60-datetime.now().second
    print("[{0}] Sleeping for {1} seconds...".format(str(datetime.now()), time_sleep))
    time.sleep(time_sleep)

print("[{0}] Starting daemon thread...".format(str(datetime.now())))
t = threading.Thread(target=dump_json_worker)
t.daemon = True
t.start()

print("[{0}] Filtering Tweets...".format(str(datetime.now())))
stream.filter(follow=args.follow, track=args.track, locations=args.geolocation,
              stall_warnings=args.stall_warnings, languages=args.language, filter_level=args.filter_level)

# stream.filter(track=settings.TRACK_TERMS)
