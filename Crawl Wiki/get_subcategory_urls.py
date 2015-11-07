__author__ = 'azhar'

from utils.mongo_utilities import MongoUtilities
from utils.crawler import Crawler

# Get extracted urls from ICD
m = MongoUtilities()
c = Crawler()
docs = m.get_all_documents("disease_categories")
subcategories = []
for doc in docs:
    soup = c.get_html_content(doc["url"])
    subcategories.append(c.get_sub_category_urls(soup, doc["category"]))

# Insert the subcategory urls to Mongo
m.insert_documents("disease_subcategories", subcategories)

