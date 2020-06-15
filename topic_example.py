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

    from_date = "2020-01-01"
    to_date = "2020-01-02"

    # Get news id & content and then do the topic modeling
    # for news in searcher.search_by_date(from_date, to_date):
    #     news_id = news.news_id  # get news_id
    #     content = news.content  # get content
    #     title = news.title      # get title
    #     # do somthing

    unique_news_ids, news_ids, topic_ids = [], [], []
    # search_by_date for all category
    for news in searcher.search_by_date(from_date, to_date):
        unique_news_ids.append(news.meta.id)
        news_ids.append(news.news_id)
    print(len(news_ids))

    unique_news_ids, news_ids, topic_ids = [], [], []
    # search_by_date given categories
    for news in searcher.search_by_date(from_date, to_date, category=['258', '259']):
        unique_news_ids.append(news.meta.id)
        news_ids.append(news.news_id)
    print(len(news_ids))

    # label topic id per each news
    # imbue random topic ids for test
    unique_news_ids, news_ids, topic_ids = [], [], []
    for news in searcher.search_by_date(from_date, to_date, category=['258', '259']):
        unique_news_ids.append(news.meta.id)
        news_ids.append(news.news_id)
        topic_ids.append(['D_20200101_0' + str(random.randint(1, 5)) for _ in range(random.randint(1, 3))])

    # update
    searcher.update_daily_topics(unique_news_ids, topic_ids)

    sleep(3)
    # get 10 news given the topic id
    for news in searcher.search_by_daily_topic("D_20200101_01", from_date, to_date):
        print(news.meta.id, news.news_id, news.title, news.daily_topic)

    # return 10 news whose topic id
    for news in searcher.search_by_daily_topic("D_20200101_02", from_date, to_date):
        print(news.meta.id, news.news_id, news.title, news.daily_topic)

    # return 10 news whose topic id
    for news in searcher.search_by_daily_topic(["D_20200101_01", "D_20200101_02"], from_date, to_date):
        print(news.meta.id, news.news_id, news.title, news.daily_topic)

    # clear daily_topic only given news_ids
    sleep(3)
    searcher.clear_daily_topic(news_ids=unique_news_ids[:100])

    sleep(3)
    for news in searcher.search_by_daily_topic("D_20200101_02", from_date, to_date):
        print(news.meta.id, news.news_id, news.title, news.daily_topic)

    sleep(3)
    searcher.clear_daily_topic(from_date=from_date, to_date=to_date)

    sleep(3)
    for news in searcher.search_by_daily_topic("D_20200101_02", from_date, to_date):
        print(news.meta.id, news.news_id, news.title, news.daily_topic)
