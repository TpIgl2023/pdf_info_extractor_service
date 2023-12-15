

# ArticleBuilder utilisant des stratégies
from Services.GrobidServicesHandler import GrobidServicesHandler
from Services.Strategies.DictExtractionStrategy import DictExtractionStrategy
from env import XML_FILE_PATH , FILE_FOLDER_PATH

class PDFProcessor(DictExtractionStrategy):
    def __init__(self):
        self.objectHandler = GrobidServicesHandler

    grobidClient = GrobidServicesHandler.grobid_client

    def extractDict(self, pdf_path= FILE_FOLDER_PATH,xml_path=XML_FILE_PATH):
        return self.objectHandler.extractDict(pdf_path,xml_path)