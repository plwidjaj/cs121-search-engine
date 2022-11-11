# UF CS 121 Search Engine M1

from postings import Posting
from nltk.stem import PorterStemmer
import shelve
import json
from bs4 import BeautifulSoup
import re

def get_batch(D, batch_num):
    # Split total number of documents into 3 
    batch = []
    if batch_num == 1:
        i = 0
        for i in range(len(D) // 3):
            batch.append(D[i])
    elif batch_num == 2:
        i = batch_num // 3
        for i in range(int(len(D) * (2.0/3.0))):
            batch.append(D[i])         
    elif batch_num == 3:
        i = int(len(D) * (2.0/3.0))
        for i in range(len(D)):
            batch.append(D[i])         

    return batch

def parse(document):
    #Opens and parses through the document and returns a list of its tokens
    try:
        f = open(document)
        text = f.read()
        text = json.loads(text)
        soup = BeautifulSoup(text['content'], features="xml")

        text_content = soup.get_text()

        # Stemming
        ps = PorterStemmer()

        res = []
        for line in text_content.split('\n'):
            for word in line.split():
                if bool(re.match('^[a-zA-Z0-9]+$', word)): # if the word is alphanumeric
                    res.append(ps.stem(word).lower())
                else:
                    addTokens = [] # stores the words that we must add
                    currWord = []
                    for c in word:
                        if not bool(re.match('^[a-zA-Z0-9]$', c)): # if not alphanumeric char, we will reset the currWord = ""
                            if currWord != []: 
                                addTokens.append("".join(currWord)) # we only want to append currWord if it's not ""
                                currWord = [] 
                        else:
                            currWord.append(c.lower())

                    if currWord != []: # if after we finish looping through the whole word and there's a word we haven't added
                        addTokens.append("".join(currWord)) # we add that word that we haven't added yet
                    res += addTokens # then we add all these words to the result!

        f.close()
        return res
        
    except (OSError, IOError) as e:
        return []
    

def remove_duplicates(tokens):
    # Removes duplicate tokens from document.
    no_duplicates = list(set(tokens))
    return no_duplicates

def sort_and_write_to_disk(index, name):

    try:
        inv_index = shelve.open(name)
        for i in index.keys():
            if i in inv_index:
                temp = inv_index[i]
                temp.extend(index[i])
                inv_index[i] = temp
            else:
                inv_index[i] = index[i]
        inv_index.close()
        
    except:
        print('could not open file')


def calculate_tfidf(D, token, tokens):
    # tf-idf = term frequency of a word in a document
    # TODO

    return tokens.count(token) #tokens.count(token) * (len(D) / )


def build_index(D):                           # D = set of text documents
    index = {}          # Inverted list storage
    n = 0               # Document numbering
    b = []              # Batch of documents
    num_indexed = 0
    total_unique_tokens = 0
    batch_num = 1
    inverted_index_file = 'inv_index'
    while batch_num <= 3:  # While D is not empty
        b = get_batch(D, batch_num)
        for document in b:
            tokens = parse(document)                # Tokenize document in current batch
            if tokens == []:
                n += 1                              # Make sure to still skip the one we couldn't open
                break
            remove_duplicates(tokens)
            for token in tokens:
                if token not in index:
                    index[token] = [] 
                index[token].append(Posting(n, calculate_tfidf(D, token, tokens)))
            n += 1
            num_indexed += 1
        #total_unique_tokens += len(index)
        # print(index.keys())
        sort_and_write_to_disk(index, inverted_index_file)
        index = {}
        batch_num += 1
    return num_indexed #, total_unique_tokens
