import shelve
from nltk.stem import PorterStemmer
from collections import defaultdict
import time
import json

def get_query():
    '''
    Get the query from user input
    '''
    query = input('Enter your search query: ')
    query = query.split()
    return query

def get_top_docids(query):
    '''
    Find the documents that fulfill an AND query,
    sorted by relevance
    '''
    docs_scores = dict()
    #postings_lists = []
    doc_freq = defaultdict(dict)
    common_docids = set()

    filename = 'inv_index' 
    inv_index = shelve.open(filename)

    #get the Postings list for each word in query
    for word in query:
        word_docids = set()
        if word in inv_index:
            postings = inv_index[word]
            for p in postings:
                doc_freq[word][p.get_docid()] = p.get_tfidf()
                word_docids.add(p.get_docid())
        else:
            return [] #return empty list if any of the words does not exist in the inverted index
        if len(common_docids) == 0:
            common_docids = word_docids
        else:
            common_docids = common_docids.intersection(word_docids)

    inv_index.close()

    #for every Posting:
    #if the doc appears for all words in the query, then calculate the score and store it
    for docid in common_docids:
        score = 0
        for word in query:
            #TODO make sure this works ok for calculating score, maybe use cosine similarity?
            score += doc_freq[word][docid]
        docs_scores[docid] = score

    #sort the documents by score in descending order
    docs = list(docs_scores.items())
    docs.sort(key=lambda x: x[1], reverse=True)
    docs = [id for id, _ in docs]

    return docs

def display_top_n_urls(docids, num_to_display):
    docids_map = shelve.open('docids')
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

def find_docs(query):
    '''
    Find the documents that fulfill an AND query
    (OLD)
    '''
    #ps = PorterStemmer()
    filename = 'inv_index' 
    inv_index = shelve.open(filename)
    set_of_docs = set() #Postings
    first_word = True
    for word in query:
        print(word)
        if word in inv_index:
            print('found')
            #word = word.lower()
            docs_list = inv_index[word]
            for x in docs_list:

                print(x.get_tfidf())
            docs_list = set([d.docid for d in docs_list])
            if first_word == True:
                set_of_docs = set(docs_list)
                first_word = False
            else:
                set_of_docs = set_of_docs.intersection(docs_list)
            
    return set_of_docs

def execute():
    query = get_query()

    #timer
    start_time = time.perf_counter()

    set_of_docs = get_top_docids(query)
    display_top_n_urls(set_of_docs, 5)

    end_time = time.perf_counter()
    print(f'{end_time-start_time:0.4f} seconds elapsed')

if __name__ == '__main__':
    execute()