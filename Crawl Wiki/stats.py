__author__ = 'azhar'
from utils.mongo_utilities import MongoUtilities
m = MongoUtilities()
docs = m.get_all_documents("disease_subcategories")
for doc in docs:
    print doc 
