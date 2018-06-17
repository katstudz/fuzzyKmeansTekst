import numpy as np
import glob
from Document import Document
from Corpus import Corpus


class Fuzzy:

    def __init__(self, K, corpus):
        self.K = K
        self.corpus = corpus
        self.u = np.empty([2, 2])
        pass


def create_corpus():
    corpus = Corpus()
    for folder in glob.iglob('texts/*'):
        for filename in glob.iglob(folder + "/*"):
            corpus.add_document(Document(filename))
            # corpus.add_document(Document(folder))

    corpus.build_vocabulary()
    return corpus


if __name__ == "__main__":
    corpus = create_corpus()
    corpus.count_term_doc_matrix()
    corpus.kmeans(3)

