import argparse
import io
import json
import logging

import yaml
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=getattr(logging, 'INFO'))
logger = logging.getLogger(__name__)

news_ids = set()


def load_news(fn):
    with io.open(fn, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for news in data:
            unique_news_id = int(news['oid'] + news['aid'])
            news_id = int(news['id'])
            if news_id in news_ids:
                continue

            sid1 = news['sid1']
            sid2 = news['sid2']

            news_ids.add(news_id)
            title = news['기사제목']
            publish_datetime = news['최종수정']
            if not publish_datetime:
                publish_datetime = news['기사입력']

            naver_url = news['네이버URL']
            origin_url = news['기사원문URL']
            publisher = news['신문사']
            category = news['대분류']
            content = news['기사원문-글자추출']

            yield {
                '_id': unique_news_id, 'news_id': news_id, 'type': 'news', 'sid1': sid1, 'sid2': sid2,
                'title': title, 'naver_url': naver_url, 'origin_url': origin_url,
                'category': category, 'publisher': publisher, 'publish_datetime': publish_datetime,
                'content': content, 'daily_topic': 0, 'longterm_topic': 0
            }


def main(args):
    with open(args.config, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)

    client = Elasticsearch(hosts=cfg['elasticsearch']['host'])
    index = cfg['elasticsearch']['news_index']

    for ok, result in streaming_bulk(client, load_news(args.file), index=index, chunk_size=500):
        action, result = result.popitem()
        doc_id = "/%s/doc/%s" % (index, result["_id"])

        if not ok:
            logger.warning("Failed to %s document %s: %r" % (action, doc_id, result))
        else:
            logger.info(doc_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Indexing news.')
    parser.add_argument('--config', default='../config.yaml', help='Config file.')
    parser.add_argument('--file', default='../news.json', help='News json file.')
    args = parser.parse_args()
    main(args)
