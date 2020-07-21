import logging
from datetime import datetime, timedelta

from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from elasticsearch_dsl import Search, UpdateByQuery, Q

logging.basicConfig(level=getattr(logging, 'INFO'))
logger = logging.getLogger(__name__)


class Searcher(object):
    def __init__(self, hosts, news_index, topic_index=None):
        self.client = Elasticsearch(hosts=hosts)
        self.news_index = news_index
        self.topic_index = topic_index

    def search(self, keyword):
        s = Search(using=self.client, index=self.news_index)\
            .query("match", content=keyword)

        response = s.execute()
        return response

    def _covert_to_datetime(self, from_datetime, to_datetime):
        if not to_datetime:
            to_datetime = datetime.now()

        if not from_datetime:
            from_datetime = to_datetime - timedelta(days=1)

        if not isinstance(from_datetime, datetime):
            from_datetime = datetime.strptime(from_datetime, '%Y-%m-%d')

        if not isinstance(to_datetime, datetime):
            to_datetime = datetime.strptime(to_datetime, '%Y-%m-%d')

        to_datetime = to_datetime.strftime("%Y-%m-%d %H:%M:%S")
        from_datetime = from_datetime.strftime("%Y-%m-%d %H:%M:%S")

        return from_datetime, to_datetime

    def search_by_date(self, from_date, to_date, category=[]):
        from_datetime, to_datetime = self._covert_to_datetime(from_date, to_date)

        should = []
        for value in category:
            if value[0] == '1':
                should.append(Q('match', sid1=value))
            elif value[0] in ['2', '3', '5', '7']:
                should.append(Q('match', sid2=value))

        q = Q('bool', should=should)
        s = Search(using=self.client, index=self.news_index) \
            .query(q) \
            .filter('range', publish_datetime={'from': from_datetime, 'to': to_datetime})

        for hit in s.scan():
            yield hit

    def search_topic_news_by_date(self, from_date, to_date, category=[]):
        from_datetime, to_datetime = self._covert_to_datetime(from_date, to_date)

        should = []
        for value in category:
            if value[0] == '1':
                should.append(Q('match', sid1=value))
            elif value[0] in ['2', '3', '5', '7']:
                should.append(Q('match', sid2=value))

        must_not = [Q('match', daily_topic='0')]
        q = Q('bool', should=should, must_not=must_not)
        s = Search(using=self.client, index=self.news_index) \
            .query(q) \
            .filter('range', publish_datetime={'from': from_datetime, 'to': to_datetime})

        for hit in s.scan():
            yield hit

    def search_longterm_topics(self):
        must_not = [Q('match', longterm_topic='0')]
        q = Q('bool', must_not=must_not)
        s = Search(using=self.client, index=self.news_index) \
            .query(q) \

        for hit in s.scan():
            yield hit

    def search_by_daily_topic(self, topic, from_date=None, to_date=None):
        should = []
        if isinstance(topic, list):
            should.extend([Q('match', daily_topic=t) for t in topic])
        else:
            should.append(Q('match', daily_topic=topic))

        q = Q('bool', should=should)

        if from_date or to_date:
            from_datetime, to_datetime = self._covert_to_datetime(from_date, to_date)
            s = Search(using=self.client, index=self.news_index) \
                .query(q) \
                .filter('range', publish_datetime={'from': from_datetime, 'to': to_datetime})
        else:
            s = Search(using=self.client, index=self.news_index) \
                .query(q)

        for hit in s.scan():
            yield hit

    def search_by_longterm_topic(self, topic, from_date=None, to_date=None):
        from_datetime, to_datetime = self._covert_to_datetime(from_date, to_date)

        should = []
        if isinstance(topic, list):
            should.extend([Q('match', longterm_topic=t) for t in topic])
        else:
            should.append(Q('match', longterm_topic=topic))

        q = Q('bool', should=should)
        s = Search(using=self.client, index=self.news_index) \
            .query(q) \
            .filter('range', publish_datetime={'from': from_datetime, 'to': to_datetime})

        for hit in s.scan():
            yield hit

    def clear_daily_topic(self, news_ids=None, from_date=None, to_date=None):
        # # TODO: Rewrite this update using UpdateByQuery
        # from_datetime, to_datetime = self._covert_to_datetime(from_datetime, to_datetime)
        #
        # ubq = UpdateByQuery(using=self.client, index=self.index) \
        #       .filter('range', publish_datetime={'from': from_datetime, 'to': to_datetime}) \
        #       .script(source="ctx._source.daily_topic=0")
        #
        # response = ubq.execute()
        # logger.info("%s" % response)

        if news_ids:
            topic_ids = [0] * len(news_ids)

        if not news_ids and from_date and to_date:
            from_datetime, to_datetime = self._covert_to_datetime(from_date, to_date)
            s = Search(using=self.client, index=self.news_index) \
                .filter('range', publish_datetime={'from': from_datetime, 'to': to_datetime})

            news_ids = [hit.meta.id for hit in s.scan()]
            topic_ids = [0] * len(news_ids)

        for ok, result in streaming_bulk(self.client, self._update_daily_topic(news_ids, topic_ids),
                                         index=self.news_index, chunk_size=100):
            action, result = result.popitem()
            doc_id = "/%s/doc/%s" % (self.news_index, result["_id"])

            if not ok:
                logger.warning("Failed to %s document %s: %r" % (action, doc_id, result))
            else:
                logger.info(doc_id)

    def clear_longterm_topic(self, news_ids=None, from_date=None, to_date=None):
        if news_ids:
            topic_ids = [0] * len(news_ids)

        if not news_ids and from_date and to_date:
            from_datetime, to_datetime = self._covert_to_datetime(from_date, to_date)
            s = Search(using=self.client, index=self.news_index) \
                .filter('range', publish_datetime={'from': from_datetime, 'to': to_datetime})

            news_ids = [hit.meta.id for hit in s.scan()]
            topic_ids = [0] * len(news_ids)

        for ok, result in streaming_bulk(self.client, self._update_longterm_topic(news_ids, topic_ids),
                                         index=self.news_index, chunk_size=100):
            action, result = result.popitem()
            doc_id = "/%s/doc/%s" % (self.news_index, result["_id"])

            if not ok:
                logger.warning("Failed to %s document %s: %r" % (action, doc_id, result))
            else:
                logger.info(doc_id)

    def _update_daily_topic(self, news_ids, topic_ids):
        for news_id, topic_id in zip(news_ids, topic_ids):
            yield {
                '_id': news_id, '_op_type': 'update', 'doc': {'daily_topic': topic_id}
            }

    def _update_longterm_topic(self, news_ids, topic_ids):
        for news_id, topic_id in zip(news_ids, topic_ids):
            yield {
                '_id': news_id, '_op_type': 'update', 'doc': {'longterm_topic': topic_id}
            }

    def _insert_topic_info(self, topic_ids, information, field):
        for topic_id, info in zip(topic_ids, information):
            yield {
                '_id': topic_id, 'topic_id': topic_id, field: info
            }

    def _update_topic_info(self, topic_ids, information, field):
        for topic_id, info in zip(topic_ids, information):
            yield {
                '_id': topic_id, '_op_type': 'update', 'doc': {field: info}
            }

    def update_daily_topics(self, news_ids, topic_ids):
        for ok, result in streaming_bulk(self.client, self._update_daily_topic(news_ids, topic_ids),
                                         index=self.news_index, chunk_size=100):
            action, result = result.popitem()
            doc_id = "/%s/doc/%s" % (self.news_index, result["_id"])

            if not ok:
                logger.warning("Failed to %s document %s: %r" % (action, doc_id, result))
            else:
                logger.info(doc_id)

    def update_longterm_topics(self, news_ids, topic_ids):
        for ok, result in streaming_bulk(self.client, self._update_longterm_topic(news_ids, topic_ids),
                                         index=self.news_index, chunk_size=100):
            action, result = result.popitem()
            doc_id = "/%s/doc/%s" % (self.news_index, result["_id"])

            if not ok:
                logger.warning("Failed to %s document %s: %r" % (action, doc_id, result))
            else:
                logger.info(doc_id)

    def insert_topic_info(self, topic_ids, values, topic_info):
        for ok, result in streaming_bulk(self.client, self._insert_topic_info(topic_ids, values, topic_info),
                                         index=self.topic_index, chunk_size=100):
            action, result = result.popitem()
            doc_id = "/%s/doc/%s" % (self.topic_index, result["_id"])

            if not ok:
                logger.warning("Failed to %s document %s: %r" % (action, doc_id, result))
            else:
                logger.info(doc_id)

    def update_topic_info(self, topic_ids, values, topic_info):
        for ok, result in streaming_bulk(self.client, self._update_topic_info(topic_ids, values, topic_info),
                                         index=self.topic_index, chunk_size=100):
            action, result = result.popitem()
            doc_id = "/%s/doc/%s" % (self.topic_index, result["_id"])

            if not ok:
                logger.warning("Failed to %s document %s: %r" % (action, doc_id, result))
            else:
                logger.info(doc_id)

    def get_topic_from_topic_index(self, topic):
        should = []
        if isinstance(topic, list):
            should.extend([Q('match', topic_id=t) for t in topic])
        else:
            should.append(Q('match', topic_id=topic))

        q = Q('bool', should=should)
        s = Search(using=self.client, index=self.topic_index) \
            .query(q)

        response = s.execute()
        for hit in response:
            yield hit

    def aggregate(self, keyword):
        s = Search(using=self.client, index=self.news_index).query("match", content=keyword)
        response = s.execute()
        for tag in response.aggregations:
            print(tag)

    def count(self):
        news_res = self.client.count(index=self.news_index)
        topic_res = self.client.count(index=self.topic_index)
        logger.info("news_index: %s, news_count: %d" % (self.news_index, news_res['count']))
        logger.info("topic_index: %s, topic_count: %d" % (self.topic_index, topic_res['count']))
        return news_res['count'], topic_res['count']

