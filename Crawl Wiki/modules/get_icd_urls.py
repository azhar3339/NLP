__author__ = 'azhar'
"""
GetIcdUrls

This module collects the urls of 22 disease categories.
The list is provided by  International Statistical Classification of Diseases and Related Health Problems (ICD),
a medical classification list by the World Health Organization (WHO)
"""

from utils import Crawler
from utils import MongoUtilities


class GetIcdUrls(object):

    def __init__(self):
        self.output_collection = 'disease_categories'
        self.crawler = Crawler()
        self.mongo = MongoUtilities()

    def run(self):
        """
        Collects the urls of all the categories listed on this page:
        https://en.wikipedia.org/wiki/ICD-10
        :return: returns nothing. Inserts documents into disease_categories
        """
        # Get html content
        soup = self.crawler.get_html_content(self.crawler.icd_url)
        # Extract category and urls
        categories = self.crawler.get_icd_category_urls(soup)
        # Write to Mongo DB
        self.mongo.insert_documents(self.output_collection, categories)
