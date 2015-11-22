__author__ = 'azhar'
"""
CreateMedicalCorpus

This module crawls more than 20000 URLs from wikipedia and inserts the record into mongo db.
Run this module after running the GetIcdUrls module.
There are two steps in creating the medical corpus.
1. Get subcategory URLs for each category in disease_categories collection and put them in medical_corpus collection.
   get_all_urls()
2. Get the actual content from each of these URLs and put it in the same collection 'medical_corpus'.
   This takes a lot of time you can run in multiple times until all the documents are crawled.
   get_content()

"""

from utils import MongoUtilities
from utils import Crawler


class CreateMedicalCorpus(object):

    def __init__(self):
        # TODO: read the collection names from config file
        self.input_collection = 'disease_categories'
        self.output_collection = 'medical_corpus'
        self.mongo_utilities = MongoUtilities()
        self.crawler = Crawler()

    def get_all_urls(self):
        """
        Collects all the URLs from each disease category from disease_categories collection.
        The column 'crawled' is set to 'No' for all the documents.
        :return: returns nothing, inserts documents into medical_corpus
        """

        docs = self.mongo_utilities.get_all_documents(self.input_collection)
        for doc in docs:
            print doc['category']
            soup = self.crawler.get_html_content(doc["url"])
            urls = self.crawler.get_sub_category_urls(soup, doc['category'])
            self.mongo_utilities.insert_documents(self.output_collection, urls)

    def get_content(self):
        """
        Crawls the actual content for each disease in medical corpus.
        For each crawled document the column 'crawled' is set to 'Yes'
        :return: returns nothing, modifies documents in medical_corpus
        """

        docs = self.mongo_utilities.get_uncrawled_docs()
        count = 0
        for doc in docs:
            count += 1
            print count
            url = doc['url']
            text = ""
            soup = self.crawler.get_html_content(url)
            # Get all the paragraph tags
            for p_tag in soup.findAll('p'):
                text += '<para start>'+p_tag.text+'<para end>'

            self.mongo_utilities.update_document(self.output_collection, {
                '$set': {
                    'content': text,
                    'crawled': 'Yes'
                }
            }, doc['_id'])
