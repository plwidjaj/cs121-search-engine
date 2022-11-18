import index
import os
import shelve

def map_docid(D):
    # Takes all the documents from set D and assigns each URL to an integer (docid) and returns the mapping as a dictionary.
    curr_docid = 0
    docid_hashmap = {}
    for path in os.listdir(D):
        path = D + "/" + path
        if os.path.isdir(path):
            # Is a directory
            # Our dataset seems to be at most one level deep, so it only looks so far but might have to change if necessary.
            for path_inner in os.listdir(path):
                docid_hashmap[curr_docid] = path + "/" + path_inner
                curr_docid += 1
        elif os.path.isfile(path):
            # Is a normal file
            docid_hashmap[curr_docid] = path
    return docid_hashmap        

def report(inverted_index):
    # The number of indexed documents;
    # The number of unique tokens;
    # The total size (in KB) of your index on disk.
    # Note for the developer option: at this time, you do not need to have the optimized index, but you may save time if you do.
    filename = 'inv_index_dev' 
    #filesize = os.path.getsize(filename+'.db')
    inv_index = shelve.open(filename)
    print(f"Number of documents indexed: {inverted_index}")
    print(f"Number of unique tokens: {len(inv_index)}")
    #print(f'Total size of index on disk: {filesize} ')
    inv_index.close()

def save_docids(docids):
    filename = 'docids_dev'
    docids_file = shelve.open(filename)
    for k, v in docids.items():
        docids_file[str(k)] = v
    docids_file.close()

def execute():
    D = "../DEV"
    docids = map_docid(D)
    #save_docids(docids)
    print(len(docids))
    print(type(docids))
    inverted_index = index.build_index(docids)
    report(inverted_index)

if __name__ == '__main__':
    execute()