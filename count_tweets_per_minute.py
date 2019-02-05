import os
import sys
import argparse
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import array_contains


parser = argparse.ArgumentParser(
    description='Load JSON Tweets files and count Tweets per minute that contain a term in their message.')
parser.add_argument("-t", "--term", dest="term", default="None",
                    help="term to count in Tweets messages", metavar="TERM")
args = parser.parse_args()
print("Arguments passed: {0}".format(str(args)[10:-1]))

spark = SparkSession.builder.appName("TweetsCounterApp").getOrCreate()

path_to_json = str(os.path.abspath(os.path.dirname(sys.argv[0])))
json_files = [pos_json for pos_json in os.listdir(
    path_to_json) if pos_json.endswith('.json')]

df = spark.read.json(json_files.pop(0), multiLine=True)
for json_file in json_files:
    df = df.union(spark.read.json(json_file, multiLine=True))

counter = 0
for row in df.rdd.collect():
    for tweet in row['results']:
        if tweet['text'].find(args.term) != -1:
            counter += 1

print("Term '{0}' appears in {1} Tweets per minute.".format(
    args.term, counter/df.count()))

# df.filter(array_contains(col=df.results['text'], value='term'))
