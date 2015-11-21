__author__ = 'azhar'

from pymongo import MongoClient

class MongoUtilities(object):

    def __init__(self):

        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = 'Wikipedia'

    def insert_one_document(self, collection, doc):

        self.client[self.db][collection].insert(doc)

    def insert_documents(self, collection, docs):
        try:
            self.client[self.db][collection].insert_many(docs)
        except:
            print 'Exception Handled'
            print 'Problematic doc:', docs

    def get_all_documents(self, collection):

        return self.client[self.db][collection].find()

    def update_document(self, collection, query, id):

        try:
            self.client[self.db][collection].update_one(
            {'_id': id},
            query)
        except:
            print "Exception", id


    def get_uncrawled_docs(self):

        return self.client[self.db]['medical_corpus'].find({
            'crawled': 'No'
        })




