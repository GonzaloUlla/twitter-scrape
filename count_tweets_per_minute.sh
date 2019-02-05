#!/bin/bash

# Script to run count_tweets_per_minute.py with Docker

TERM=$1

docker run -v $(pwd):/home/jovyan/ jupyter/pyspark-notebook \
/usr/local/spark-2.4.0-bin-hadoop2.7/bin/spark-submit \
/home/jovyan/count_tweets_per_minute.py -t ${1:-"Trump"}