import argparse

import yaml
from elasticsearch import Elasticsearch, TransportError


def create_news_search_index(client, index):
    create_index_body = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 1,
            "analysis": {
                "tokenizer": {
                    "korean_nori_tokenizer": {
                        "type": "nori_tokenizer",
                        "decompound_mode": "mixed",
                        "user_dictionary": "userdict_ko.txt"
                    }
                },
                "analyzer": {
                    "nori_analyzer": {
                        "type": "custom",
                        "tokenizer": "korean_nori_tokenizer",
                        "filter": ["posfilter"]
                    }
                },
                "filter": {
                    "posfilter": {
                        "type": "nori_part_of_speech",
                        "stoptags": ["E", "IC", "J", "MAG", "MM", "SC", "SE", "SF", "SN", "SP", "SSC",
                                     "SSO", "SY", "UNA", "UNKNOWN", "VA", "VCN", "VCP", "VSV", "VV", "VX",
                                     "XPN", "XR", "XSA", "XSN", "XSV"]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "news_id": {        # 뉴스 ID
                    "type": "long"
                },
                "sid1": {
                    "type": "keyword"
                },
                "sid2": {
                    "type": "keyword"
                },
                "type": {           # news
                    "type": "keyword"
                },
                "naver_url": {      # 네이버URL
                    "type": "keyword"
                },
                "origin_url": {     # 기사원문URL
                    "type": "keyword"
                },
                "category": {
                    "type": "keyword"
                },
                "publisher": {
                    "type": "keyword"
                },
                "publish_datetime": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                },
                "title": {
                    "type": "text",
                    "analyzer": "nori_analyzer"
                },
                "content": {
                    "type": "text",
                    "analyzer": "nori_analyzer"
                },
                "daily_topic": {
                   "type": "keyword",
                },
                "longterm_topic": {
                   "type": "keyword",
                }
                # "title_vector": {
                #     "type": "dense_vector",
                #     "dims": 768
                # },
                # "text_vector": {
                #     "type": "dense_vector",
                #     "dims": 768
                # }
            }
        }
    }

    # create empty index
    try:
        client.indices.create(index=index, body=create_index_body)
    except TransportError as e:
        # ignore already existing index
        if e.error == "resource_already_exists_exception":
            pass
        else:
            raise


def delete_news_search_index(client, index):
    # delete empty index
    try:
        client.indices.delete(index=index)
    except TransportError as e:
        raise



def main(args):
    with open(args.config, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)

    client = Elasticsearch(hosts=cfg['elasticsearch']['host'])
    index = cfg['elasticsearch']['news_index']
    delete_news_search_index(client, index)
    create_news_search_index(client, index)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creating elasticsearch index.')
    parser.add_argument('--config', default='../config.yaml', help='Config file.')
    args = parser.parse_args()
    main(args)
