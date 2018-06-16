from utils import normalize
import random
import numpy as np


class Corpus(object):
    '''
    A collection of documents.
    '''

    def __init__(self):
        '''
        Initialize empty document list.
        '''
        self.m = 1.5
        self.kmeans_set = []
        self.documents = []

    def add_document(self, document):
        '''
        Add a document to the corpus.
        '''
        document.split([])
        self.documents.append(document)

    def build_vocabulary(self):
        '''
        Construct a list of unique words in the corpus.
        '''
        discrete_set = set()
        for document in self.documents:
            for word in document.words:
                discrete_set.add(word)
        self.vocabulary = list(discrete_set)

    def count_term_doc_matrix(self):

        '''
        Model topics.
        '''
        # Get vocabulary and number of documents.
        self.build_vocabulary()
        number_of_documents = len(self.documents)
        vocabulary_size = len(self.vocabulary)

        # build term-doc matrix
        self.term_doc_matrix = np.zeros([number_of_documents, vocabulary_size], dtype=np.double)
        for d_index, doc in enumerate(self.documents):
            term_count = np.zeros(vocabulary_size, dtype=np.double)
            for word in doc.words:
                if word in self.vocabulary:
                    w_index = self.vocabulary.index(word)
                    term_count[w_index] = term_count[w_index] + 1
                    self.term_doc_matrix[d_index] = term_count

    def kmeans(self, k):
        self.k = k

        for i in range(k):
            self.kmeans_set.append(np.random.rand(1, len(self.vocabulary)))

        self.u = np.ones([len(self.documents), k], dtype=np.double)
        # for i in range(10):
        #     self.updateU()
        #     self.updateC()

        self.showResultClusters()

    def showResultClusters(self):
        for doc in range(len(self.term_doc_matrix)):
            print(self.documents[doc].filepath + "  " + str(self.get_cluster_index(self.term_doc_matrix[doc])))


    def updateC(self):
        for ck in range(len(self.kmeans_set)):
            for i in range(len(self.documents)):
                self.kmeans_set[ck] = self.Euk(ck) / max(self.Eum(ck), 0.0001)
                pass

    def updateU(self, ):
        for k in range(self.k):
            for i in range(len(self.documents)):
                d1 = (np.linalg.norm(self.term_doc_matrix[i] - self.kmeans_set[k]) ** (2 / (self.m - 1)))
                d2 = self.Edcm(self.term_doc_matrix[i])
                self.u[i][k] = 1 / d1 * d2

    def Euk(self, k):
        suma = 0
        for i in range(len(self.documents)):
            suma += self.u[i][k] * self.term_doc_matrix[i]
        return suma

    def Eum(self, k):
        suma = 0
        for i in range(len(self.documents)):
            suma += self.u[i][k] ** self.m
        return suma

    def Edcm(self, document):
        suma = 0
        for k in range(self.k):
            suma += 1 / (np.linalg.norm(document - self.kmeans_set[k])) ** (2 / (self.m - 1))
        return suma

    def get_cluster_index(self, document):
        min_k = self.kmeans_set[0]
        for k in self.kmeans_set:
            if np.linalg.norm(k - document) < np.linalg.norm(min_k - document):
                min_k = k

        return self.kmeans_set.index(min_k)
