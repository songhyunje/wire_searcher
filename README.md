# Search system in WIRE summarization

##### 준비사항
- pyyaml
- elasticsearch
- elasticsearch_dsl

```
pip install -r requirements.txt
```

- 서버 셋팅 (config.yaml) 파일을 아래와 같이 작성
```yaml
elasticsearch:
    host:  
    news_index: 
    topic_index: 
```

##### 키워드 검색 사용법
- search_example.py 참고

##### 데일리 토픽 아이디 부착 및 토픽 검색 사용법
- daily_topic_example.py 참고

##### 토픽 관련 정보 부착 및 사용법
- topic_example.py 참고

--------------------------------

참고: 뉴스 카테고리 정보 (대분류, 소분류) 정보

|대분류|소분류|ID|
|---|---|---|
|경제| All | 101 |
|사회| All | 102 |
|경제|   증권	|   	258|
|경제|	금융	|   	259|
|경제|	부동산|		260|
|경제|	산업/재계|	261|
|경제|	글로벌경제|	262|
|경제|	경제일반|	    263|
|경제|	생활경제|   	310|
|경제|	중기/벤처|	771|
|사회|	사건사고|   	249|
|사회|	교육	|   	250|
|사회|	노동	|   	251|
|사회|	환경	|   	252|
|사회|	언론	|   	254|
|사회|	식품/의료|	255|
|사회|	지역	|       256|
|사회|	사회일반|	    257|
|사회|	인물	|       276|
|사회|	인권/복지|    59b|

--------------------------------

참고: 현재 엘라스틱 서치에 구축된 mapping 정보

뉴스 관련
```json
{
  "wire_news_search" : {
    "mappings": {
      "properties": {
        "news_id": {   
            "type": "integer"
        },
        "sid1": {
            "type": "keyword"
        },
        "sid2": {
            "type": "keyword"
        },
        "type": {     
            "type": "keyword"
        },
        "naver_url": {
            "type": "keyword"
        },
        "origin_url": {
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
      }
    }         
  }
}
```

토픽 관련 (이건 향후 MongoDB로 옮길 예정)
```json
{
  "wire_topic" : {
    "mappings": {
      "properties": {
        "topic_id": {
          "type": "keyword"
        },
        "text": {
          "type": "keyword",
        },
        "summary": {
          "type": "keyword",
        },
        "related_topic_ids": {
          "type": "keyword"
        }
      }
    }
  }
}
```