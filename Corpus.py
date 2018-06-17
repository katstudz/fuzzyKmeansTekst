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
        self.m = 1.1
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
            self.kmeans_set.append(2 * np.random.rand(1, len(self.vocabulary)))
        self.u = np.random.rand(len(self.documents), k)

        for k in self.kmeans_set:
            print(k)

        for i in range(700):
            self.update_u()
            self.update_c()

        self.show_result_clusters()


    def update_u(self):
        for k in range(self.k):
            for i in range(len(self.documents)):
                self.u[i][k] = 1 / self.Edcm(self.term_doc_matrix[i], k)


    def Edcm(self, document, i):
        suma = 0.0
        for k in range(self.k):
            suma +=((np.linalg.norm(document - self.kmeans_set[i])
                     / (np.linalg.norm(document - self.kmeans_set[k]))) ** (2 / (self.m - 1)))
        return suma

    def update_c(self):
        for ck in range(len(self.kmeans_set)):
            for i in range(len(self.documents)):
                self.kmeans_set[ck] = self.Euk(ck) / self.Eum(ck)
                pass

    def Euk(self, k):
        suma = 0
        for i in range(len(self.documents)):
            suma += (self.u[i][k] ** self.m) * self.term_doc_matrix[i]
        return suma

    def Eum(self, k):
        suma = 0.0
        for i in range(len(self.documents)):
            suma += self.u[i][k] ** self.m
        return suma


    def get_cluster_index(self, document):
        min_k = 0
        for k in range(len(self.kmeans_set)):
            if np.linalg.norm(self.kmeans_set[k] - document) < np.linalg.norm(self.kmeans_set[min_k] - document):
                min_k = k

        return min_k

    def show_result_clusters(self):
        result = []
        for doc in range(len(self.term_doc_matrix)):
            result.append([self.documents[doc].filepath,  self.get_cluster_index(self.term_doc_matrix[doc]) ])

        sort_result = sorted( result, key=lambda x: x[1])
        for i in sort_result:
            print(i)

        for cluster in self.kmeans_set:
            self.get_most_important_word_in_cluster(cluster)

    def get_most_important_word_in_cluster(self, cluster):
        cluster_most_important_list = []
        for i in range(10):
            best_word = cluster.argmax()
            cluster_most_important_list.append(self.vocabulary[best_word])
            cluster[best_word] = 0

        print(cluster_most_important_list)