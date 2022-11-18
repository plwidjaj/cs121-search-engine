class Posting:
    def __init__(self, docid, tfidf, fields=[]):
        self.docid = docid              
        self.tfidf = tfidf              # Use frequency for now
        self.fields = fields
    
    def get_docid(self):
        return self.docid
    
    def get_tfidf(self):
        return self.tfidf

    def get_fields(self):
        return self.fields

    def __eq__(self, other):
        return self.docid == other.docid
