__author__ = 'azhar'
"""
This module contains general purpose utility functions.
"""

from bs4 import BeautifulSoup
import urllib2
from pymongo import MongoClient
from pymongo import errors


class Crawler(object):

    def __init__(self):

        self.HEADER = {'User-Agent': 'Mozilla/5.0'}  # Needed to prevent 403 error on Wikipedia

        """
        International Statistical Classification of Diseases and Related Health Problems (ICD),
        a medical classification list by the World Health Organization (WHO)
        """

        self.icd_url = 'https://en.wikipedia.org/wiki/ICD-10'
        self.url_start = 'https://en.wikipedia.org'

    def get_html_content(self, url):
        """
        Takes a url and return a beautiful soap object
        :param url: url string
        :return: soup object
        """

        req = urllib2.Request(url, headers=self.HEADER)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page)

        return soup

    def get_icd_category_urls(self, soup_obj):
        """
        get the urls of all the categories mentioned on this page: https://en.wikipedia.org/wiki/ICD-10
        :param soup_obj: beautiful soup object
        :return: list of categories
        """

        category_urls = []
        for anchor in soup_obj.findAll('a'):
            if 'class' in anchor.attrs:
                # Irrelevant anchor tags
                pass
            else:
                # since the categories are in a table, looking for 'td' tag
                if anchor.parent.name == 'td':
                    category_urls.append({'category': anchor['title'],
                                          'url': self.url_start + anchor['href']})

        return category_urls

    def get_sub_category_urls(self, soup_obj, category):
        """
        Takes the beautiful soup object of the category web page and returns the list of subcategory urls.
        :param soup_obj: beautiful soup object
        :param category: ICD category
        :return: list of disease sub category urls
        """

        # By removing links containing these words, we may lose some of the diseases
        # TODO: Fine for now, fix later
        remove_these = ['Template', 'ICD', 'Wikipedia', 'Help', 'Main_Page', '%',
                        'Portal', 'Special', 'World_Health_Organization', 'Category']
        urls = []

        for anchor in soup_obj.findAll('a'):
            # This will filter some of the unnecessary tags
            if "title" in anchor.attrs and "href" in anchor.attrs:
                bad_tag = False
                for word in remove_these:
                    if word in anchor["href"]:
                        bad_tag = True
                        break
                if bad_tag:
                    pass
                elif anchor["href"][:6] == "/wiki/":
                    urls.append({"title": anchor["title"],
                                 "url": self.url_start + anchor["href"],
                                 'category': category,
                                 "crawled": "No",
                                 'content': 'None'})

        return urls


class MongoUtilities(object):

    def __init__(self):

        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = 'Wikipedia'

    def insert_one_document(self, collection, doc):
        """

        :param collection: collection name string
        :param doc: document to be inserted dictionary
        :return: Inserts a document, returns nothing
        """

        self.client[self.db][collection].insert(doc)

    def insert_documents(self, collection, docs):
        """

        :param collection: collection name string
        :param docs: documents to be inserted list of dictionaries
        :return: Inserts multiple documents, returns nothing
        """
        try:
            self.client[self.db][collection].insert_many(docs)
        except errors.PyMongoError as e:
            print "Exception", e

    def get_all_documents(self, collection):
        """
        Collects all the documents in a collection
        :param collection: collection name string
        :return: list of dictionaries
        """

        return self.client[self.db][collection].find()

    def update_document(self, collection, query, mongo_id):
        """
        Executes the update query
        :param collection: collection name string
        :param query: update query dictionary
        :param mongo_id: mongo's unique identifier
        :return: updates a document, returns nothing
        """

        try:
            self.client[self.db][collection].update_one(
                {'_id': mongo_id},
                query)
        except errors.PyMongoError as e:
            print "Exception", e

    def get_uncrawled_docs(self):
        """
        Gets the uncrawled documents. Document which have 'crawled' field set to 'No'
        :return: list of dictionaries
        """

        return self.client[self.db]['medical_corpus'].find({
            'crawled': 'No'
        })
