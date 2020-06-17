#!/bin/bash

CUR=`pwd`
DB=$CUR/../navernews-db-query
CONFIG=$CUR/../config.yaml
SEARCH=$CUR/../search
UTIL=$CUR/../util

mkdir -p news news_merge

START_DATE="20200610"
END_DATE=`date +%Y%m%d`
# END_DATE="20200106"
while [ "$START_DATE" != $END_DATE ]; do 
  echo $START_DATE
  # for mac
  START_DATE_PLUS_ONE=`date -j -f %Y%m%d -v+1d $START_DATE +%Y%m%d`
  node $DB/navernews-db-query.js all $START_DATE $START_DATE_PLUS_ONE > news/"$START_DATE"_news.json
  START_DATE=$START_DATE_PLUS_ONE
done

for fn in news/*;
do
    FFN=`basename $fn`
    python $UTIL/preprocessor.py --input $fn --output "news_merge/$FFN"
done

for fn in news_merge/*;
do
    echo "try to insert $fn news"
    python $SEARCH/news_inserter.py --config $CONFIG --file $fn
done
