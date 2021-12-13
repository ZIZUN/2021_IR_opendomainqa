from elasticsearch import Elasticsearch
from pororo import Pororo
from util.korquad_eval_script import f1_score, exact_match_score
import json
import tqdm

mrc = Pororo(task="mrc", lang="ko")

es = Elasticsearch("http://127.0.0.1:9200/")
es.info()

topk = 100
em_result = 0
f1_result = 0

with open('data/KorQuAD_v1.0_dev.json', 'r') as f:
    f = json.load(f)
    num = 0

    for data in tqdm.tqdm(f['data']):
        for para in data['paragraphs']:
            for qas in para['qas']:
                results = es.search(index='texts',
                                    body={'from': 0, 'size': topk, 'query': {'match': {'text': qas['question']}}})
                try:
                    for i in range(topk):
                        mrc_result = mrc(qas['question'], results['hits']['hits'][i]['_source']['text'],
                                         postprocess=True)
                        answer = mrc_result[0]
                        if answer != '' and len(answer) < 40:
                            break
                except:
                    answer = ''

                em_result += exact_match_score(answer, qas['answers'][0]['text'])
                f1_result += f1_score(answer, qas['answers'][0]['text'])

                num+=1

    em_result = em_result / num * 100
    f1_result = f1_result / num * 100
    print('EM: ', em_result)
    print('F1: ', f1_result)