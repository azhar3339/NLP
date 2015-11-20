__author__ = 'azhar'

from utils.mongo_utilities import MongoUtilities
from utils.crawler import Crawler

class CreateMedicalCorpus(object):

    def __init__(self):

        self.input_collection = 'disease_subcategories'
        self.output_collection = 'medical_corpus'
        self.mongo_utilities = MongoUtilities()
        self.crawler = Crawler()

    def get_all_urls(self):

        docs = self.mongo_utilities.get_all_documents('disease_categories')
        for doc in docs:
            print doc['category']
            soup = self.crawler.get_html_content(doc["url"])
            urls = self.crawler.get_sub_category_urls(soup, doc['category'])
            self.mongo_utilities.insert_documents(self.output_collection, urls)

    def get_content(self):

        docs = self.mongo_utilities.get_uncrawled_docs()
        count = 0
        for doc in docs:
            count += 1
            print count
            url = doc['url']
            text = ""
            soup = self.crawler.get_html_content(url)
            for p_tag in soup.findAll('p'):
                text += '<para start>'+p_tag.text+'<para end>'

            self.mongo_utilities.update_document(self.output_collection,
                                                     {
                                                         '$set':
                                                             {
                                                                 'content': text,
                                                                 'crawled': 'Yes'
                                                             }
                                                     }, doc['_id'])

c = CreateMedicalCorpus()
# c.get_all_urls()
c.get_content()
