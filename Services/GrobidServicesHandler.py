import xmltodict
from grobid_client.grobid_client import GrobidClient
from Services.FileHandler import FileHandler



class GrobidServicesHandler:

    grobid_client = GrobidClient(config_path="./grobid_client_python/config.json")
    def __init__(self):
        pass

    @staticmethod
    def pdfToXML(file_path,nb=1):
        GrobidServicesHandler.grobid_client.process("processFulltextDocument", file_path, n=nb)

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

