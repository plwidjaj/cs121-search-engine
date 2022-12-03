import shelve
from nltk.stem import PorterStemmer
from collections import defaultdict
import time
import json
import math

FILENAME = 'inv_index_dev'

def get_query():
    '''
    Get the query from user input
    and lowercases+stems it
    '''
    ps = PorterStemmer()
    query = input('Enter your search query: ')
    query = query.split()
    query = [ps.stem(q.lower()) for q in query]
    return query

def get_top_docids(query, inv_index, num_of_docs):
    '''
    Find the documents that fulfill an AND query,
    sorted by relevance
    (For new indexer!)
    '''
    docs_scores = defaultdict(int)
    common_docids = set()
    idfs = dict()

    if len(query) != 0:
        try:
            #Calculate idf for each term
            for q in query:
                idfs[q] = math.log(num_of_docs, len(inv_index[q].keys()))
            
            query.sort(key=lambda q: len(inv_index[q].keys()))

            common_docids = set(inv_index[query[0]].keys())
            for i in range(1, len(query)):
                common_docids = common_docids.intersection(set(inv_index[query[i]].keys()))
            for id in common_docids:
                for q in query:
                    docs_scores[id] += (1 + math.log(inv_index[q][id])) * idfs[q]
        except:
            print('Query not found in index')

    sorted_docs = list(docs_scores.items())
    sorted_docs.sort(key=lambda x: x[1], reverse=True)
    sorted_docs = [id for id, _ in sorted_docs]

    return sorted_docs

def display_top_n_urls(docids, num_to_display, docids_map):
    for i in range(num_to_display):
        try:
            f = open(docids_map[str(docids[i])])
            text = f.read()
            f.close()
            text = json.loads(text)
            print(text['url'])
        except:
            pass

def display_top_n_files(docids, num_to_display, docids_map):
    for i in range(num_to_display):
        try:
            print(docids_map[str(docids[i])])
        except:
            pass

def execute():

    print('Search Engine')
    print('...loading...')

    inv_index = shelve.open(FILENAME)
    docids_map = shelve.open('docids_dev')
    num_of_docs = len(docids_map.keys())

    while True:
        query = get_query()

        #timer
        start_time = time.perf_counter()

        set_of_docs = get_top_docids(query, inv_index, num_of_docs)
        end_time = time.perf_counter()
        print(f'{end_time-start_time:0.4f} seconds elapsed')
        
        display_top_n_urls(set_of_docs, 10, docids_map)
        #display_top_n_files(set_of_docs, 5, docids_map)

        end = input('Press x to stop or any other key to continue...').lower()
        if end == 'x':
            break

    inv_index.close()
    docids_map.close()

if __name__ == '__main__':
    execute()