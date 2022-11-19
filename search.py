import shelve
from nltk.stem import PorterStemmer
from collections import defaultdict
import time
import json

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

def get_top_docids(query):
    '''
    Find the documents that fulfill an AND query,
    sorted by relevance
    (For new indexer!)
    '''
    docs_scores = defaultdict(int)
    common_docids = set()

    inv_index = shelve.open(FILENAME)

    if len(query) != 0:
        try:
            common_docids = set(inv_index[query[0]].keys())
            for i in range(1, len(query)):
                common_docids = common_docids.intersection(set(inv_index[query[i]].keys()))
            for id in common_docids:
                for q in query:
                    docs_scores[id] += (inv_index[q][id])
        except:
            print('Query not found in index')
    
    inv_index.close()

    sorted_docs = list(docs_scores.items())
    sorted_docs.sort(key=lambda x: x[1], reverse=True)
    sorted_docs = [id for id, _ in sorted_docs]

    return sorted_docs

def display_top_n_urls(docids, num_to_display):
    docids_map = shelve.open('docids_dev')
    for i in range(num_to_display):
        try:
            f = open(docids_map[str(docids[i])])
            text = f.read()
            f.close()
            text = json.loads(text)
            print(text['url'])
        except:
            pass
    docids_map.close()

def display_top_n_files(docids, num_to_display):
    docids_map = shelve.open('docids_dev')
    for i in range(num_to_display):
        try:
            print(docids_map[str(docids[i])])
        except:
            pass
    docids_map.close()

def execute():
    query = get_query()

    #timer
    start_time = time.perf_counter()

    set_of_docs = get_top_docids(query)
    display_top_n_urls(set_of_docs, 5)
    #display_top_n_files(set_of_docs, 5)

    end_time = time.perf_counter()
    print(f'{end_time-start_time:0.4f} seconds elapsed')

if __name__ == '__main__':
    execute()