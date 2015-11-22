__author__ = 'azhar'

from bs4 import BeautifulSoup
import urllib2
from pymongo import MongoClient


class Crawler(object):

    def __init__(self):

        self.HEADER = {'User-Agent': 'Mozilla/5.0'}  # Needed to prevent 403 error on Wikipedia

        """
        International Statistical Classification of Diseases and Related Health Problems (ICD),
        a medical classification list by the World Health Organization (WHO)
        """

        self.icd_url = "https://en.wikipedia.org/wiki/ICD-10"
        self.url_start = "https://en.wikipedia.org"

    def get_html_content(self, url):

        req = urllib2.Request(url, headers=self.HEADER)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page)

        return soup

    def get_icd_category_urls(self, soup_obj):

        category_urls = []
        for anchor in soup_obj.findAll('a'):
            if "class" in anchor.attrs:
                # Irrelevant anchor tags
                pass
            else:
                if anchor.parent.name == "td":
                    category_urls.append({"category": anchor["title"],
                                          "url": self.url_start + anchor["href"]})
                    # categories.append(url_start + anchor["href"])

        return category_urls

    def get_sub_category_urls(self, soup_obj, category):

        # By removing links containing these words, we may lose some of the diseases
        # Fix: Fine for now, fix later
        remove_these = ["Template", "ICD", "Wikipedia", "Help", "Main_Page", "%",
                        "Portal", "Special", "World_Health_Organization", "Category"]
        urls = []

        for anchor in soup_obj.findAll('a'):
            ####This will filter some of the unnecessary tags
            if "title" in anchor.attrs and "href" in anchor.attrs:
                bad_tag = False
                for word in remove_these:
                    if word in anchor["href"]:
                        bad_tag = True
                        break
                if bad_tag:
                    pass
                elif anchor["href"][:6] == "/wiki/":
                    # print anchor["href"]
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

