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
    searcher = Searcher(hosts=hosts, index=news_index)
    responses = searcher.search("신용카드")
    for hit in responses:
        print(hit.news_id, hit.title)
