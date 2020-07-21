import argparse
import yaml

from search.search_handler import Searcher


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search by topic index')
    parser.add_argument('--config', default='config.yaml', help='Config file.')
    args = parser.parse_args()

    with open(args.config, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)

    hosts = cfg['elasticsearch']['host']
    news_index = cfg['elasticsearch']['news_index']
    topic_index = cfg['elasticsearch']['topic_index']
    searcher = Searcher(hosts=hosts, news_index=news_index, topic_index=topic_index)

    searcher.count()
    for news in searcher.search_longterm_topics():
        print(news.news_id, news.longterm_topic)

    from_date = "2020-01-01"
    for news in searcher.search_by_longterm_topic("L_20200716_003", from_date):
        print(news.meta.id, news.news_id, news.title, news.longterm_topic)
