# Interface pour la stratégie d'extraction de texte
import json
import os


from Models.Article import Article

from Services.Strategies.ExtractTitle import ExtractTitle
from Services.Strategies.ExtractText import ExtractText
from Services.Strategies.ExtractAbstract import ExtractAbstract
from Services.Strategies.ExtractAuthors import ExtractAuthors
from Services.Strategies.ExtractBibliography import ExtractBibliography
from Services.Strategies.ExtractKeywords import ExtractKeywords
from Services.Strategies.ExtractInstitutions import ExtractInstitutions
from Services.Strategies.ExtractPublicationDate import ExtractPublicationDate




class ArticleBuilder(ExtractAuthors, ExtractBibliography, ExtractAbstract, ExtractTitle, ExtractText, ExtractKeywords, ExtractInstitutions, ExtractPublicationDate):
    def __init__(self,articleDict):
        self.article = Article()
        self.dict = articleDict

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
