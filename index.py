# UF CS 121 Search Engine M1

from postings import Posting
from nltk.stem import PorterStemmer
import shelve
import json
from bs4 import BeautifulSoup
import re
from collections import defaultdict

main_index = defaultdict(lambda: defaultdict(int)) #stores index in the format {token: {docid: freq}}

def get_batch(D, batch_num, total_batches):
    # Split total number of documents into 3 
    batch = []
    x = True
    start_i_list = [0]
    for i in range(1, total_batches):
        start_i_list.append(start_i_list[i-1] + len(D) // total_batches)
    print(start_i_list)
    start_i_list.append(len(D))

    for i in range(start_i_list[batch_num-1], start_i_list[batch_num]):
        batch.append(D[i])

    print('batch len', len(batch), batch[0], batch[(len(batch)-1)])
    return batch

def tokenize(text, docid):
    '''
    Tokenizes and adds the tokens to the main_index
    '''
    ps = PorterStemmer()
    for line in text:
        try:
            words = re.sub(r'[^a-zA-Z0-9]+', ' ', line)
            words = words.split()
            for word in words:
                word = ps.stem(word.lower())
                main_index[word][docid] += 1
        except:
            pass

def get_text_content(document):
    '''
    Gets the text content from a json file
    '''
    text_content = ''

    try:
        f = open(document)
        text = f.read()
        f.close()
        text = json.loads(text)
        soup = BeautifulSoup(text['content'], features="html.parser")
        text_content = soup.get_text()
    except:
        print('Failed to get content from', document)

    return text_content


def parse(document, docid):
    '''
    Opens and parses the document
    '''

    text_content = get_text_content(document)
    text_content = text_content.split('\n')

    #test
    print('parsing', docid, document)
    tokenize(text_content, docid)
    

def remove_duplicates(tokens):
    # Removes duplicate tokens from document.
    no_duplicates = list(set(tokens))
    return no_duplicates

def sort_and_write_to_disk(name):
    '''
    writes to file and clears the main_index
    '''

    print('writing to file')

    try:
        inv_index = shelve.open(name)
        for i in main_index.keys():
            if i in inv_index:
                temp = inv_index[i]
                temp.update(main_index[i])
                inv_index[i] = temp
            else:
                inv_index[i] = main_index[i]
        inv_index.close()
        
    except:
        print('could not open file')

    main_index.clear()

def calculate_tfidf(D, token, tokens):
    # tf-idf = term frequency of a word in a document
    # TODO

    return tokens.count(token) #tokens.count(token) * (len(D) / )


def build_index(D):                           # D = set of text documents
    '''
    Builds an inverted index on main_index.
    Goes through documents in D in separate batches,
    parsing and tokenizing each one.
    Writes the inverted index to file after every batch.
    '''
    n = 0               # Document numbering
    b = []              # Batch of documents
    batch_num = 1
    total_batches = 3
    #inverted_index_file = 'inv_index'
    inverted_index_file = 'inv_index_dev'
    
    while batch_num <= total_batches:  # While D is not empty
        b = get_batch(D, batch_num, total_batches)
        x = input()
        print('batch num', batch_num)

        for i in range(len(b)):
            document = b[i]
            parse(document, n)
            n += 1

        sort_and_write_to_disk(inverted_index_file)

        batch_num += 1

    return n #, total_unique_tokens