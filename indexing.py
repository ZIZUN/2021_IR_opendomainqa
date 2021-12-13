from elasticsearch import Elasticsearch
import tqdm

dataset = []

# Kowiki Dataset
from Korpora import Korpora

kowikitext = Korpora.load('kowikitext')
id = 0
for text in tqdm.tqdm(kowikitext.train.texts):
    if len(text) > 15:
        dataset.append({'id': id, 'text': text})
        id += 1
for text in tqdm.tqdm(kowikitext.dev.texts):
    if len(text) > 15:
        dataset.append({'id': id, 'text': text})
        id += 1
for text in tqdm.tqdm(kowikitext.test.texts):
    if len(text) > 15:
        dataset.append({'id': id, 'text': text})
        id += 1


# 일레스틱서치 IP주소와 포트(기본:9200)로 연결한다
es = Elasticsearch("http://127.0.0.1:9200/")
es.info()

# 인덱스는 독립된 파일 집합으로 관리되는 데이터 덩어리이다
def make_index(es, index_name):
    """인덱스를 신규 생성한다(존재하면 삭제 후 생성) """
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
    es.indices.create(index=index_name)

index_name = 'texts'
make_index(es, index_name)

# 데이터를 저장한다
for d in tqdm.tqdm(dataset):
    es.index(index=index_name, doc_type='string', body=d)

es.indices.refresh(index=index_name)