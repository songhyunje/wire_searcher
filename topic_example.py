import argparse
from time import sleep

import yaml
import random

from search.search_handler import Searcher


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search by topic index')
    parser.add_argument('--config', default='config.yaml', help='Config file.')
    args = parser.parse_args()

    with open(args.config, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)

    hosts = cfg['elasticsearch']['host']
    news_index = cfg['elasticsearch']['news_index']
    searcher = Searcher(hosts=hosts, index=news_index)

    searcher.count()

    from_date = "2020-06-03"
    to_date = "2020-06-04"

    # Get news id & content and then do the topic modeling
    # for news in searcher.search_by_date(from_date, to_date):
    #     news_id = news.news_id  # get news_id
    #     content = news.content  # get content
    #     title = news.title      # get title
    #     # do somthing

    # label topic id per each news
    # imbue a random topic id for test
    news_ids, topic_ids = [], []
    for news in searcher.search_by_date(from_date, to_date):
        news_ids.append(news.news_id)
        topic_ids.append(random.randint(1, 5))

    # update
    searcher.update_daily_topics(news_ids, topic_ids)

    # get 10 news given the topic id (1)
    for news in searcher.search_by_daily_topic(1, from_date, to_date):
        print(news.news_id, news.title, news.daily_topic)
        # print(news.meta.id, news.title, news.daily_topic)

    # return 10 news whose topic id is 2
    for news in searcher.search_by_daily_topic(2, from_date, to_date):
        print(news.news_id, news.title, news.daily_topic)

    sleep(3)
    searcher.clear_daily_topic(from_date=from_date, to_date=to_date)
    # # clear daily_topic only given news_ids
    # searcher.clear_daily_topic(news_ids=news_ids)

    sleep(3)
    for news in searcher.search_by_daily_topic(1, from_date, to_date):
        print(news.news_id, news.title, news.daily_topic)
