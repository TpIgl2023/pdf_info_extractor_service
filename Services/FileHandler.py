import json
import os
from zipfile import ZipFile

import PyPDF2 as PyPDF2
import requests
import xmltodict



class FileHandler:
    @staticmethod
    def unzip(zip_path, output_path):
        # loading the temp.zip and creating a zip object
        with ZipFile(zip_path, 'r') as zObject:
            # Extracting all the members of the zip
            # into a specific location.
            zObject.extractall(path=output_path)

    @staticmethod
    def loadText(structuredDataPath):
        with open(structuredDataPath) as f:
            data = json.load(f)
            text = JsonToTextHandler.apply(data)
            return text

    @staticmethod
    def XMLToDict(file_path):
        with open(file_path, 'r', encoding="utf-8") as xml_file:
            xml_data = xml_file.read()
            dict_data = xmltodict.parse(xml_data)
            return dict_data



    @staticmethod
    def dictToJSON(dict, file_path):
        # Open the file and write the dictionary as JSON
        with open(file_path, 'w') as file:
            json.dump(dict, file, indent=4)  # indent parameter for pretty formatting

    @staticmethod
    def deleteFile(fileName):
        if os.path.exists(fileName):
            os.remove(fileName)

    @staticmethod
    def downloadFileLink(URL,filePath):
        # Download the file
        response = requests.get(URL)
        with open(filePath, "wb") as pdf_file:
            pdf_file.write(response.content)

    @staticmethod
    def extractGoogleDownloadLink(file_id):
        return f"https://drive.google.com/uc?id={file_id}&export=download"

    @staticmethod
    def extractGoogleFileId(previewLink):
        # Extract file ID from the preview link
        return previewLink.split("/file/d/")[1].split("/view")[0]

    @staticmethod
    def checkPDFCorruption(pdfPath):
        try:
            with open(pdfPath, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def jsonToDict(path):
        with open(path) as f:
            data = json.load(f)
            return data

    @staticmethod
    def writeText(text, path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)






class JsonToTextHandler():
    def __init__(self):
        pass

    @staticmethod
    def apply(json):
        elements = json['elements']
        text = ""
        for element in elements:
            if 'Text' in element:
                text += element['Text'] + '\n'
            if 'Kids' in element:
                for kid in element['Kids']:
                    if 'Text' in kid:
                        text += kid['Text']
                text += '\n'
        return text