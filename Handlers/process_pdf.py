from fastapi import Security
from starlette.responses import JSONResponse

from Middlwares.Auth import get_api_key
from Services.ArticleBuilder import ArticleBuilder
from Services.FileHandler import FileHandler
from env import FILE_PATH


async def process_pdf(URL : str,api_key: str = Security(get_api_key)):
    try:
        print("Starting the download process")
        FileHandler.downloadFileLink(URL, FILE_PATH)

        if not FileHandler.checkPDFCorruption(FILE_PATH):
            return JSONResponse(content={"error": "Corrupted PDF file"})

        # Takes FileDict to build the article
        articleBuilder = ArticleBuilder()

        # Initialize the article builder
        articleBuilder.initDict()

        # Build the article object
        myArticle = articleBuilder.build()
        myArticle.URL = URL

        return JSONResponse(content=myArticle.__dict__())
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={
                                "message": "Error while processing the PDF",
                                "error": str(e)
                            })