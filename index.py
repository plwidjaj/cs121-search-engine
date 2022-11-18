# UF CS 121 Search Engine M1

from postings import Posting
from nltk.stem import PorterStemmer
import shelve
import json
from bs4 import BeautifulSoup
import re

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
        #print(i)
        #print(D[i])
        batch.append(D[i])

    #start_i = (batch_num - 1) * len(D) // total_batches

    #batch 1: i = 0 to len(D) // 3
    '''
    if batch_num == 1:
        i = 0
        for i in range(len(D) // 3):
            if x ==True:
                print(i)
                x = False
            batch.append(D[i])
    elif batch_num == 2:
        # i = batch_num // 3
        for i in range(len(D) // 3, int(len(D) * (2.0/3.0))):
            if x ==True:
                print(i)
                x = False
            batch.append(D[i])         
    elif batch_num == 3:
        # i = int(len(D) * (2.0/3.0))
        for i in range(int(len(D) * (2.0/3.0)), len(D)):
            if x ==True:
                print(i)
                x = False
            batch.append(D[i])         
    
    '''
    print('batch len', len(batch), batch[0], batch[(len(batch)-1)])
    return batch

def parse(document):
    #Opens and parses through the document and returns a list of its tokens
    #print_tokens = False
    #if document == '../DEV/grape_ics_uci_edu/288efb3cf695c4647ffa91355363552cdc0d45fc7dd93fbd1804b8e8db25dcba.json':
        #print('TEST DOC')
        #print_tokens=True
    try:
        f = open(document)
        text = f.read()
        text = json.loads(text)
        soup = BeautifulSoup(text['content'], features="html.parser")

        text_content = soup.get_text()

        # Stemming
        ps = PorterStemmer()

        res = []

        #test
        print('parsing', document)
        for line in text_content.split('\n'):
            for word in line.split():
                #if print_tokens == True:
                    #print(word)
                if bool(re.match('^[a-zA-Z0-9]+$', word)): # if the word is alphanumeric
                    #res.append(ps.stem(word).lower())
                    res.append(word.lower())
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
        print('error in parsing')
        return []
    

def remove_duplicates(tokens):
    # Removes duplicate tokens from document.
    no_duplicates = list(set(tokens))
    return no_duplicates

def sort_and_write_to_disk(index, name):

    print('writing to file')

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
    #total_unique_tokens = 0
    batch_num = 1
    total_batches = 3
    #inverted_index_file = 'inv_index'
    inverted_index_file = 'inv_index_dev'
    
    while batch_num <= total_batches:  # While D is not empty
        b = get_batch(D, batch_num, total_batches)
        print('batch num', batch_num)

        print('LEN(b)=', len(b), b[len(b)-1])
        
        for i in range(len(b)):
            document = b[i]
            #print('on document no.', i)
            tokens = parse(document)                # Tokenize document in current batch
            #if tokens == []:
                #n += 1                              # Make sure to still skip the one we couldn't open
                #break
            unique_tokens = remove_duplicates(tokens)
            for token in unique_tokens:
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
