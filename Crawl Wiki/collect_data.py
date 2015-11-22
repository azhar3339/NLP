__author__ = 'azhar'
from modules.get_icd_urls import GetIcdUrls
from modules.create_medical_corpus import CreateMedicalCorpus

# Collect ICD urls
g = GetIcdUrls()
# g.run()
# Collect sub category urls
c = CreateMedicalCorpus()
# c.get_all_urls()
# Collect content for all URLs
# c.get_content()
