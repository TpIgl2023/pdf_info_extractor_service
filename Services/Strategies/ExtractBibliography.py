
from Services.Strategies.ExtractAuthors import ExtractAuthors


class ExtractBibliography():
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
                bib_authors_cleaned = ExtractAuthors.handleAuthorsArray(authors)
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
    def extractBibliography(self):
            try:
                divs = self.dict['text']['back']['div']
                bibliography = self.extract_biblio_from_divs(divs)['listBibl']['biblStruct']

                bibliography_elements = []
                for element in bibliography:
                    bibliography_elements.append(self.extract_bibliography(element))
                self.article.bibliography = bibliography_elements
            except:
                self.article.bibliography = []
            return self