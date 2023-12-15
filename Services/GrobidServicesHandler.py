import json

import xmltodict
from grobid_client.grobid_client import GrobidClient
from Services.FileHandler import FileHandler
from env import XML_FILE_PATH


class GrobidServicesHandler:

    grobid_client = GrobidClient(config_path="./grobid_client_python/config.json")
    @staticmethod
    def pdfToXML(file_path,nb=1):
        GrobidServicesHandler.grobid_client.process("processFulltextDocument", file_path, n=nb)

    @staticmethod
    def xmlToDict(xml_path):
        dict_data = FileHandler.XMLToDict(xml_path)
        if 'TEI' in dict_data:
            return dict_data['TEI']
        else:
            return {}

    @staticmethod
    def extractDict(pdf_folder,xml_path):

        GrobidServicesHandler.pdfToXML(pdf_folder)
        dict = GrobidServicesHandler.xmlToDict(xml_path)
        FileHandler.dictToJSON(dict, "dict.json")
        FileHandler.deleteFile(xml_path)

        return dict

