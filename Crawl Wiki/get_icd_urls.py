__author__ = 'azhar'

from utils.crawler import Crawler
from utils.mongo_utilities import MongoUtilities

# Get html content
c = Crawler()
soup = c.get_html_content(c.icd_url)
# Extract category and urls
categories = c.get_icd_category_urls(soup)
# Write to Mongo DB
m = MongoUtilities()
m.insert_documents("disease_categories", categories)

