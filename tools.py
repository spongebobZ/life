from elasticsearch import Elasticsearch
from conf import cnf


def query_es_by_match(index, doc_type, condition_dict, *get_keys):
    # return dict
    es = Elasticsearch(hosts=cnf.es_host, port=cnf.es_port)
    body = {'query': {'match': condition_dict}}
    r = es.search(index=index, doc_type=doc_type, body=body)
    rd = {}
    if len(r['hits']['hits']) != 0:
        for k in get_keys:
            try:
                rd[k] = r['hits']['hits'][0]['_source'][k]
            except KeyError as e:
                continue
    return rd


def query_es_by_index_and_type(index, doc_type, *get_keys):
    # return dict
    es = Elasticsearch(hosts=cnf.es_host, port=cnf.es_port)
    r = es.search(index=index, doc_type=doc_type)
    rd = {}
    if len(r['hits']['hits']) != 0:
        for k in get_keys:
            try:
                rd[k] = r['hits']['hits'][0]['_source'][k]
            except KeyError as e:
                continue
    return rd


def query_es_by_aggs(index, doc_type, aggs_method, aggs_field, condition_dict=None):
    # only support single condition
    # return value
    es = Elasticsearch(hosts=cnf.es_host, port=cnf.es_port)
    if condition_dict and len(condition_dict) == 1:
        query = {'match': condition_dict}
    else:
        query = {'match_all': {}}
    body = {'size': 0, 'query': query, 'aggs': {'aggs_result': {aggs_method: {'field': aggs_field}}}}
    r = es.search(index=index, doc_type=doc_type, body=body)
    ri = r['aggregations']['aggs_result']['value']
    return ri


def query_es_by_sort(index, doc_type, n=1, filter_dict=None, *order_condition):
    # support multi field sort
    # order condition like '{"a":{"order":"desc"}}'
    # n means get n result record
    es = Elasticsearch(hosts=cnf.es_host, port=cnf.es_port)
    if filter_dict and len(filter_dict) == 1:
        query = {'match': filter_dict}
    else:
        query = {'match_all': {}}
    body = {'size': n, 'query': query, 'sort': [*order_condition]}
    r = es.search(index=index, doc_type=doc_type, body=body)
    return r['hits']['hits']


def select(file, *row, **condition):
    with open(file, 'r', encoding='utf-8') as fr:
        r = []
        lines = fr.readlines()
        if condition and len(lines) > 0:
            for i in lines:
                i = i.split(',')
                for k, v in condition.items():
                    if v != i[int(k)].strip():
                        break
                else:
                    if row:
                        r.append(list(map(lambda x: i[x], row)))
                    else:
                        r.append(i)
        else:
            for i in lines:
                if row:
                    r.append(list(map(lambda x: i[x], row)))
                else:
                    r.append(i.split(','))
        return r


def insert(file, s):
    with open(file, 'a', encoding='utf-8') as fa:
        fa.write(s + '\n')


def update(file, new_kv, **condition):
    with open(file, 'r', encoding='utf-8') as fr:
        lines = fr.readlines()
    with open(file, 'w', encoding='utf-8') as fw:
        for line in lines:
            line = line.strip()
            if condition:
                line_list = line.split(',')
                for k, v in condition.items():
                    if v != line_list[int(k)]:
                        fw.write(','.join(line_list) + '\n')
                        break
                else:
                    for m, n in new_kv.items():
                        line_list[int(m)] = n
                    fw.write(','.join(line_list) + '\n')
            else:
                line_list = line.split(',')
                for m, n in new_kv.items():
                    line_list[int(m)] = n
                fw.write(','.join(line_list) + '\n')


def delete(file, **condition):
    with open(file, 'r', encoding='utf-8') as fr:
        lines = fr.readlines()
    with open(file, 'w', encoding='utf-8') as fw:
        if condition:
            for line in lines:
                line = line.strip()
                line_list = line.split(',')
                for k, v in condition.items():
                    if v != line_list[int(k)]:
                        fw.write(','.join(line_list))
                        break
