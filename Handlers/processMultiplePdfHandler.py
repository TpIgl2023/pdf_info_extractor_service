from starlette.responses import JSONResponse

from Services.ArticleBuilder import ArticleBuilder
from Services.FileHandler import FileHandler
from Services.GrobidServicesHandler import GrobidServicesHandler
from env import FILE_FOLDER_PATH

import os
from multiprocessing import Pool


def download_file(args):
    file_handler, folder_path, url, index = args
    file_name = f"file{index}.pdf"
    file_path = os.path.join(folder_path, file_name)
    file_handler.downloadFileLink(url, file_path)
    print(f"File {file_name} downloaded successfully.")


def download_multiple_files_parallel(file_handler, folder_path, urls):
    args_list = [(file_handler, folder_path, url, index + 1) for index, url in enumerate(urls)]

    with Pool(processes=len(urls)) as pool:
        pool.map(download_file, args_list)

def convert_to_xml_filename(pdf_filename):
    base_name, _ = os.path.splitext(pdf_filename)
    xml_filename = f"{base_name}.grobid.tei.xml"
    return xml_filename

async def processMultiplePdfHandler(URLs):
    try:
        print("Starting the download process")
        # Download every file in the list

        download_multiple_files_parallel(FileHandler, FILE_FOLDER_PATH, URLs)

        GrobidServicesHandler.pdfToXML(FILE_FOLDER_PATH)

        extractedPDFs = []
        extractedCounter = 0

        for filename in os.listdir(FILE_FOLDER_PATH):
            if filename.startswith("file") and filename.endswith(".pdf"):
                # Assuming the file follows the naming convention like "file1.pdf", "file2.pdf", etc.
                file_path = os.path.join(FILE_FOLDER_PATH, filename)
                xml_path = os.path.join(FILE_FOLDER_PATH, convert_to_xml_filename(filename))

                try:
                    if not FileHandler.checkPDFCorruption(file_path):
                        raise Exception("Corrupted PDF file")
                    dict = GrobidServicesHandler.xmlToDict(xml_path)
                    FileHandler.dictToJSON(dict, "dict.json")
                    FileHandler.deleteFile(xml_path)
                    FileHandler.deleteFile(file_path)
                    articleBuilder = ArticleBuilder()
                    articleBuilder.dict = dict
                    myArticle = articleBuilder.build()
                    myArticle.URL = URLs[int(filename[4:-4]) - 1]
                    extractedPDFs.append(myArticle.__dict__())
                    extractedCounter += 1



                except Exception as e:
                    print(f"Error while processing the PDF {filename}: {str(e)}")


        return JSONResponse({"success":"true",
                             "numberExtracted":extractedCounter,
                             "articles":extractedPDFs})
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={
                                "message": "Error while processing the PDFs",
                                "error": str(e)
                            })