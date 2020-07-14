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
    topic_index = cfg['elasticsearch']['topic_index']
    searcher = Searcher(hosts=hosts, news_index=news_index, topic_index=topic_index)

    searcher.count()

    # 기간을 설정하여 뉴스를 가져오며, news.daily_topic을 통해 부착된 daily_topic id를 얻을 수 있음.
    # for news in searcher.search_topic_news_by_date("2020-05-01", "2020-05-31"):
    #     print(news.meta.id, news.news_id, news.title, news.daily_topic)

    # daily_topic_id를 입력(기간은 optional)으로 문서들을 가져올 수 있음
    for news in searcher.search_by_daily_topic("D_20200526_01"):
        print(news.news_id, news.title, news.content)

    # topic_ids와 summaries를 입력으로 summary 등록
    # topic_ids = ["D_20200101_01", "D_20200101_02", "D_20200101_03", "D_20200101_04", "D_20200101_05",
    #              "D_20200102_01", "D_20200102_02", "D_20200102_03", "D_20200102_04", "D_20200102_05"]
    # summaries = ["I got pushed 떠밀려 왔어", "그리고 내곁에는 니가 있어", "외로워도 기댈 곳 없이",
    #              "힘차게 뛰어가 let\'s just try", "친구가 되어 함께 걸어줘",
    #              "오늘 같은 날 마주쳐 이게 뭐야", "상태가 말이 아니야",
    #              "내 맘이 방심할 때마다 불쑥 나타난 뒤", "또 물보라를 일으켜", "da da da da da da da da da" ]
    # searcher.insert_topic_info(topic_ids, summaries, "summary")
    # # sleep(3)

    # topic_ids = ["L_2020_01", "L_2020_02"]
    # texts = ["Into the I-LAND", "Dolphin"]
    # searcher.insert_topic_info(topic_ids, texts, "text")
    #
    # related_topic_ids = [["D_20200101_01", "D_20200101_02", "D_20200101_03", "D_20200101_04", "D_20200101_05"],
    #                      ["D_20200102_01", "D_20200102_02", "D_20200102_03", "D_20200102_04", "D_20200102_05"]]
    # searcher.update_topic_info(topic_ids, related_topic_ids, "related_topic_ids")
    # sleep(3)
    #
    # for topic in searcher.get_topic_from_topic_index("D_20200101_01"):
    #     print(topic.topic_id, topic.summary)
    #
    # for topic in searcher.get_topic_from_topic_index(["L_2020_01"]):
    #     print(topic.topic_id, topic.text, topic.related_topic_ids)
