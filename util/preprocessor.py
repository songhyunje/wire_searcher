import argparse
import io
import json

news_pools = {}
KEYS = ['sid1', 'sid2', '대분류', '소분류']


def convert_news(fin, fout):
    with io.open(fin, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for news in data:
            unique_news_id = int(news['oid'] + news['aid'])

            for k in KEYS:
                news[k] = [news[k]]

            if unique_news_id not in news_pools:
                news_pools[unique_news_id] = news
                continue

            prev_news = news_pools[unique_news_id]
            for k in KEYS:
                prev_news[k].extend(news[k])

    news_list = []
    for news in news_pools.values():
        for k, v in news.items():
            if k in KEYS:
                news[k] = list(set(v))
        news_list.append(news)

    with io.open(fout, 'w', encoding='utf-8') as f:
        f.write(json.dumps(news_list, ensure_ascii=False, indent=4))


def main(args):
    convert_news(args.input, args.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Indexing news.')
    parser.add_argument('--input', help='input json file.')
    parser.add_argument('--output', help='output json file.')
    args = parser.parse_args()
    main(args)
