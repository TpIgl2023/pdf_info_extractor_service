from Models.Article import Article
from Services.GrobidServicesHandler import GrobidServicesHandler

from Services.Strategies.ExtractTitle import ExtractTitle
from Services.Strategies.ExtractText import ExtractText
from Services.Strategies.ExtractAbstract import ExtractAbstract
from Services.Strategies.ExtractAuthors import ExtractAuthors
from Services.Strategies.ExtractBibliography import ExtractBibliography
from Services.Strategies.ExtractKeywords import ExtractKeywords
from Services.Strategies.ExtractInstitutions import ExtractInstitutions
from Services.Strategies.ExtractPublicationDate import ExtractPublicationDate
from env import FILE_FOLDER_PATH, XML_FILE_PATH


class ArticleBuilder(ExtractAuthors, ExtractBibliography, ExtractAbstract, ExtractTitle, ExtractText, ExtractKeywords, ExtractInstitutions, ExtractPublicationDate):
    def __init__(self):
        self.objectHandler = GrobidServicesHandler
        self.article = Article()
        self.dict = None

    grobidClient = GrobidServicesHandler.grobid_client

    def initDict(self, pdf_path=FILE_FOLDER_PATH, xml_path=XML_FILE_PATH):
        self.dict = self.objectHandler.extractDict(pdf_path, xml_path)

    def buildInstance(self):
        return self.article

    def build(self):
        return self.extractTitle()\
            .extractAbstract()\
            .extractAuthors()\
            .extractInstitutions()\
            .extractKeywords()\
            .extractText()\
            .extractBibliography()\
            .extractPublicationDate()\
            .buildInstance()
