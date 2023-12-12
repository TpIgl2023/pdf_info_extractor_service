# Interface pour la stratégie d'extraction de texte
import json
import os
from datetime import datetime

from Models.Article import Article

from Strategies.ExtractTitle import ExtractTitle
from Strategies.ExtractText import ExtractText
from Strategies.ExtractAbstract import ExtractAbstract
from Strategies.ExtractAuthors import ExtractAuthors
from Strategies.ExtractBibliography import ExtractBibliography
from Strategies.ExtractKeywords import ExtractKeywords
from Strategies.ExtractInstitutions import ExtractInstitutions
from Strategies.ExtractPublicationDate import ExtractPublicationDate



class ArticleBuilder(ExtractAuthors, ExtractBibliography, ExtractAbstract, ExtractTitle, ExtractText, ExtractKeywords, ExtractInstitutions, ExtractPublicationDate):
    def __init__(self,articleText,articleDict):
        self.article = Article()
        self.text = articleText
        self.dict = articleDict

    @staticmethod
    def extract_affiliation_from_author(author):
        if 'affiliation' in author:
            affiliation_info = author['affiliation']
            if 'orgName' in affiliation_info:
                orgArray = affiliation_info['orgName']
                org_name = ""
                if isinstance(orgArray, list):
                    org_name = orgArray[0]['#text']
                elif isinstance(orgArray, dict):
                    org_name = orgArray['#text']
            else:
                org_name = "N/A"

            if isinstance(affiliation_info, list):
                affiliation_info = affiliation_info[0]

            address_info = affiliation_info.get('address', {})
            post_code = address_info.get('postCode', "N/A")
            country = address_info.get('country', {}).get('#text', "N/A")

            if (org_name == "N/A" and post_code == "N/A" and country == "N/A"):
                return None

            myString = str(org_name + ", " + post_code + ", " + country)

            return myString
        myString = "N/A"
        return myString

    @staticmethod
    def format_date(input_date):
        # Ajoutez le jour et le mois par défaut si seulement l'année est fournie
        if len(input_date) == 4:
            input_date += "-01-01"
        elif len(input_date) == 7:
            input_date += "-01"

        # Essayez de convertir la chaîne en objet datetime
        try:
            formatted_date = ArticleBuilder.datetime.strptime(input_date, "%Y-%m-%d")
            return formatted_date
        except ValueError:
            print("Format de date invalide. Utilisation du format par défaut.")
            return None

    @staticmethod
    def get_creation_date(file_path):
        # Obtenez les informations sur le fichier
        file_info = os.stat(file_path)

        # Récupérez la date de création du fichier (en secondes depuis l'époque)
        creation_time = file_info.st_ctime

        # Convertissez la date de création en format lisible
        creation_date = datetime.datetime.fromtimestamp(creation_time)

        return creation_date

    @staticmethod
    def extract_affiliations(authors):
        affiliations = set()
        if isinstance(authors, dict):
            myAffiliations = ArticleBuilder.extract_affiliation_from_author(authors)
            if myAffiliations != None:
                affiliations.add(myAffiliations)
        elif isinstance(authors, list):
            for author in authors:
                myAffiliations = ArticleBuilder.extract_affiliation_from_author(author)
                if myAffiliations != None:
                    affiliations.add(myAffiliations)
        affiliations.discard("N/A")
        if len(affiliations) == 0:
            return None
        return list(affiliations)

    @staticmethod
    def extract_full_name(data):
        if "persName" not in data:
            return ""
        if 'surname' in data['persName']:
            last_name = data['persName']['surname']
        else:
            last_name = ""
        if 'forename' in data['persName']:
            if isinstance(data['persName']['forename'], list):
                first_name = data['persName']['forename'][0]['#text']
                first_name += " " + data['persName']['forename'][1]['#text']
            else:
                first_name = data['persName']['forename']['#text']
        else:
            first_name = ""

        return f"{last_name} {first_name}"

    @staticmethod
    def handleAuthorsArray(authors):
        authors_cleaned = []
        if isinstance(authors, list):
            for author in authors:
                authors_cleaned.append(ArticleBuilder.extract_full_name(author))
            return authors_cleaned
        return [ArticleBuilder.extract_full_name(authors)]

    @staticmethod
    def extract_bibliography(data):
        bib_authors_cleaned = []
        title = ""
        if 'monogr' in data:
            if 'title' in data['monogr']:
                if (data['monogr']['title'] != None) and ('#text' in data['monogr']['title']):
                    title = data['monogr']['title']['#text']
                else:
                    title = "N/A"
        if 'analytic' in data:
            if 'author' in data['analytic']:
                authors = data['analytic']['author']
                bib_authors_cleaned = ArticleBuilder.handleAuthorsArray(authors)
        authors_string = ""
        if len(bib_authors_cleaned) > 0:
            authors_string = "Authors: " + ", ".join(bib_authors_cleaned)
        return f"{title} {authors_string}"

    @staticmethod
    def extract_biblio_from_divs(divs):
        if isinstance(divs, list):
            for item in divs:
                if item.get('@type') == 'references':
                    return item
        return divs



    def extractAuthors(self):
        try:
            authors = self.dict['teiHeader']['fileDesc']['sourceDesc']['biblStruct']['analytic']['author']
            self.article.authors = self.handleAuthorsArray(authors)
        except:
            pass
        return self

    def extractBibliography(self):
        try:
            divs = self.dict['text']['back']['div']
            bibliography = self.extract_biblio_from_divs(divs)['listBibl']['biblStruct']

            bibliography_elements = []
            for element in bibliography:
                bibliography_elements.append(self.extract_bibliography(element))
            self.article.bibliography = bibliography_elements
        except:
            pass
        return self

    def extractAbstract(self):
        if self.dict['teiHeader']['profileDesc']['abstract'] != None:
            self.article.abstract = self.dict['teiHeader']['profileDesc']['abstract']['div']['p']
        else:
            self.article.abstract = "N/A"
        return self

    def extractTitle(self):
        try:
            self.article.title = self.dict['teiHeader']['fileDesc']['titleStmt']['title']['#text']
        except:
            pass
        return self

    def extractText(self):
        self.article.text = self.text
        return self

    def extractKeywords(self):
        try:
            keywords = self.dict['teiHeader']['profileDesc']['textClass']['keywords']['term']
            self.article.keywords = keywords
        except:
            pass
        return self

    def extractInstitutions(self):
        try:
            authors = self.dict['teiHeader']['fileDesc']['sourceDesc']['biblStruct']['analytic']['author']
            affiliations = self.extract_affiliations(authors)
            self.article.institutions = affiliations
        except:
            pass
        return self

    def extractPublicationDate(self):
        try:
            filedesc = self.dict['teiHeader']['fileDesc']
            dateJSON = None
            if 'publicationStmt' in filedesc:
                if 'publisher' in filedesc['publicationStmt']:
                    publisher = filedesc['publicationStmt']
                    if 'date' in publisher:
                        date = publisher['date']['@when']
                        formatted_date = ArticleBuilder.format_date(date)
                        dateJSON = json.dumps({"formatted_date": formatted_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[
                                                                 :-3] + "Z"} if formatted_date else None)
            self.article.publishingDate = dateJSON
        except:
            pass
        return self

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




