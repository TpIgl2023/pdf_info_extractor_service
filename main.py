from datetime import datetime

from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.responses import JSONResponse

from Services.ArticleBuilder import ArticleBuilder
from Services.FileHandler import FileHandler

from Services.PDFProcessor import PDFProcessor
from env import *
from pydantic import BaseModel
from Middlwares.Auth import get_api_key


api_key_header = APIKeyHeader(name="X-API-Key")
#docker run --rm -d --init --ulimit core=0 -p 8070:8070 lfoppiano/grobid:0.8.0
#uvicorn main:app --reload

# URL = "https://drive.google.com/uc?id=1eZy2sbuF1TD5dJg0ZGJwXUGycp4rc61m&export=download"

app = FastAPI()


class PostUrlModel(BaseModel):
    URL: str

@app.post("/")
async def read_root(data: PostUrlModel,api_key: str = Security(get_api_key),):

    url = data.URL

    print("Starting the download process")

    FileHandler.downloadFileLink(url, FILE_PATH)
    starting_time = datetime.now()

    if not FileHandler.checkPDFCorruption(FILE_PATH):
        return JSONResponse(content={"error": "Corrupted PDF file"})


    pdfProcessor = PDFProcessor()
    # Turn the PDF into text/dict

    fileDict = pdfProcessor.extractDict()


    # Takes FileDict to build the article
    articleBuilder = ArticleBuilder(fileDict)

    # Build the article object
    myArticle = articleBuilder.build()
    myArticle.URL = url

    time_elapsed = datetime.now() - starting_time
    print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))

    return JSONResponse(content=myArticle.__dict__())


@app.get("/")
def protected_route(api_key: str = Security(get_api_key)):
    # Process the request for authenticated users
    return {"message": "Access granted!"}