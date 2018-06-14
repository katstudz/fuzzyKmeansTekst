class Corpus(object):
    '''
    A collection of documents.
    '''

    def __init__(self):
        '''
        Initialize empty document list.
        '''
        self.documents = []

    def add_document(self, document):
        '''
        Add a document to the corpus.
        '''
        self.documents.append(document)

    def build_vocabulary(self):
        '''
        Construct a list of unique words in the corpus.
        '''
        # ** ADD ** #
        # exclude words that appear in 90%+ of the documents
        # exclude words that are too (in)frequent
        discrete_set = set()
        for document in self.documents:
            for word in document.words:
                discrete_set.add(word)
        self.vocabulary = list(discrete_set)
