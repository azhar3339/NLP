__author__ = 'azhar'

from pymongo import MongoClient

class MongoUtilities(object):

    def __init__(self):

        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = "Wikipedia"

    def insert_documents(self, collection, docs):

        self.client[self.db][collection].insert_many(docs)

    def get_all_documents(self, collection):

        return self.client[self.db][collection].find()



