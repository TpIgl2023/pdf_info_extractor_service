API_KEY = "d850g9d4-3c42-4858-9a4a-40c1e3b609ec"

import os

CLIENT_ID="7ec3040f690a4b5f85297d08867c91f2"
CLIENT_SECRET="p8e--nS2vIzbwJEO0DSjxGe5XVGAF41-H5xH"


# PATH CONSTANTS
PDF_PROCESSING_INPUT_FOLDERNAME = "PDF_PROCESSING_INPUT"
PDF_PROCESSING_OUTPUT_FOLDERNAME = "PDF_PROCESSING_OUTPUT"
EXTRACTED_MATERIAL_FOLDERNAME = "EXTRACTED_MATERIAL"
FILENAME = "file.pdf"


# PATH CONSTANTS CALCULATIONS
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
ZIP_PATH = BASE_PATH + "/" + PDF_PROCESSING_OUTPUT_FOLDERNAME + "/" + EXTRACTED_MATERIAL_FOLDERNAME + ".zip"
UNZIP_PATH = BASE_PATH + "/" + PDF_PROCESSING_OUTPUT_FOLDERNAME + "/" + EXTRACTED_MATERIAL_FOLDERNAME
FILE_FOLDER_PATH = BASE_PATH + "/" + PDF_PROCESSING_INPUT_FOLDERNAME
FILE_PATH = FILE_FOLDER_PATH + "/" + FILENAME
XML_FILE_PATH = FILE_FOLDER_PATH + "/" + "file.grobid.tei.xml"
STRUCTURED_DATA_PATH = os.path.join(UNZIP_PATH, "structuredData.json")