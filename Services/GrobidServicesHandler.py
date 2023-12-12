import xmltodict

from Services.FileHandler import FileHandler
from Services.GrobidClientSingleton import GrobidClientSingleton


class GrobidServicesHandler:
    def __init__(self):
        pass

    grobidClient = GrobidClientSingleton()

    @staticmethod
    def pdfToXML(file_path,nb=1):
        GrobidClientSingleton._instance.grobid_client.process("processFulltextDocument", file_path, n=nb)

    @staticmethod
    def xmlToDict(xml_path):
        with open(xml_path, 'r', encoding="utf-8") as xml_file:
            xml_data = xml_file.read()
            dict_data = xmltodict.parse(xml_data)
            if 'TEI' in dict_data:
                return dict_data['TEI']
            else:
                return {}

    @staticmethod
    def extractDict(pdf_folder,xml_path):

        GrobidServicesHandler.pdfToXML(pdf_folder)
        dict =  GrobidServicesHandler.xmlToDict(xml_path)
        FileHandler.deleteFile(xml_path)
        return dict