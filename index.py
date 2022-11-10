# UF CS 121 Search Engine M1

def get_batch(D):
    # TODO
    pass

def parse(D):
    # TODO
    pass

def remove_duplicates(tokens):
    # TODO
    pass

def postings(n):
    # TODO
    pass

def sort_and_write_to_disk(index, name):
    # TODO
    pass

def build_index(self, D):
    # Partial index pseudocode from lecture slides
    index = {}
    n = 0
    b = []              # Batch of documents
    while len(D) != 0:  # While D is not empty
        b = get_batch(D)
        for document in b:
            n += 1
            tokens = parse(D) 
            remove_duplicates(tokens)
            for token in tokens:
                if token not in index:
                    index[token] = [] 
                index[token].append(postings(n))
        sort_and_write_to_disk(index, name)
        index.empty()
