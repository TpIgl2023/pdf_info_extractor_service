from Services.GrobidClientSingleton import GrobidClientSingleton
from Services.AdobeSerivcesHandler import AdobeServicesHandler

# ArticleBuilder utilisant des stratégies
from Services.GrobidServicesHandler import GrobidServicesHandler
from Services.Strategies.TextExtractionStrategy import TextExtractionStrategy
from Services.Strategies.DictExtractionStrategy import DictExtractionStrategy
from env import XML_FILE_PATH

class PDFProcessor(TextExtractionStrategy, DictExtractionStrategy):
    def __init__(self):
        self.textHandler = AdobeServicesHandler
        self.objectHandler = GrobidServicesHandler

    grobidClient = GrobidClientSingleton().grobid_client


    def extractText(self,pdf_path):
        return self.textHandler.extractText(pdf_path)

    def extractDict(self, pdf_path,xml_path=XML_FILE_PATH):
        return self.objectHandler.extractDict(pdf_path,xml_path)



