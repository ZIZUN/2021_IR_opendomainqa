from elasticsearch import Elasticsearch
from pororo import Pororo
from colorama import Fore, Back, Style
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-query", default='바그너는 괴테의 파우스트를 읽고 무엇을 쓰고자 했는가?', type=str)
parser.add_argument("-topk", default=5, type=int)

args = parser.parse_args()

mrc = Pororo(task="mrc", lang="ko")
es = Elasticsearch("http://127.0.0.1:9200/")
es.info()

query = args.query
index_name = 'texts'
results = es.search(index=index_name, body={'from':0, 'size':args.topk, 'query':{'match':{'text': query}}})

print('query: ' + Back.RED + Fore.BLACK + query + Style.RESET_ALL)
for i, result in enumerate(results['hits']['hits']):
    mrc_result = mrc(query, result['_source']['text'], postprocess=True)

    id = result['_source']['id']
    score = result['_score']
    text = result['_source']['text']

    answer = mrc_result[0]
    start = text.find(answer)
    end = start + len(answer)
    print('-----------------------------------------------------------')
    print('rank: ', i+1, '\nid:', id, '\nscore:', score)
    print('text: ' + text[:start] + Back.CYAN + Fore.BLACK + answer + Style.RESET_ALL + text[end:])