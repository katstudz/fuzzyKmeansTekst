import numpy as np
import glob
from Document import Document
from Corpus import Corpus

class Fuzzy:

    def __init__(self):
        self.u = np.empty([2, 2])
        pass


if __name__ == "__main__":
    corpus = Corpus()
    documents = []
    for folder in glob.iglob('texts/*'):
        for filename in glob.iglob(folder + "/*"):

            print(filename)
            doc = Document(filename)
            doc.split([])
            documents.append(doc)
            print(len(doc.words))

    print(documents.__len__())
    pass
