## Assistant for WIRE system

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
```

-------------
참고: 현재 엘라스틱 서치에 구축된 mapping 정보
```json
{
  "wire_news_search" : {
    "mappings" : {
      "properties" : {
        "category" : {
          "type" : "keyword"
        },
        "content" : {
          "type" : "text",
          "analyzer" : "nori_analyzer"
        },
        "daily_topic" : {
          "type" : "integer",
          "null_value" : 0
        },
        "longterm_topic" : {
          "type" : "integer",
          "null_value" : 0
        },
        "naver_url" : {
          "type" : "keyword"
        },
        "news_id" : {
          "type" : "long"
        },
        "origin_url" : {
          "type" : "keyword"
        },
        "publish_datetime" : {
          "type" : "date",
          "format" : "yyyy-MM-dd HH:mm:ss"
        },
        "publisher" : {
          "type" : "keyword"
        },
        "title" : {
          "type" : "text",
          "analyzer" : "nori_analyzer"
        },
        "type" : {
          "type" : "keyword"
        }
      }
    }
  }
}
```