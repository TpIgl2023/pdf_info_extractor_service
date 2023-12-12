
from fastapi import FastAPI
from starlette.responses import JSONResponse

from Services.ArticleBuilder import ArticleBuilder
from Services.FileHandler import FileHandler
from Services.PDFProcessor import PDFProcessor
from env import *
import concurrent.futures
from pydantic import BaseModel

#docker run --rm -d --init --ulimit core=0 -p 8070:8070 lfoppiano/grobid:0.8.0
#uvicorn main:app --reload

# URL = "https://drive.google.com/uc?id=1eZy2sbuF1TD5dJg0ZGJwXUGycp4rc61m&export=download"

app = FastAPI()


class PostUrlModel(BaseModel):
    URL: str

@app.post("/")
async def read_root(data: PostUrlModel):

    url = data.URL

    FileHandler.downloadFileLink(url, FILE_PATH)

    pdfProcessor = PDFProcessor()
    # Turn the PDF into text/dict

    # Execute in parallel using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        text_future = executor.submit(pdfProcessor.extractText, FILE_PATH)
        dict_future = executor.submit(pdfProcessor.extractDict, FILE_FOLDER_PATH)

    # Get results
    fileText = text_future.result()
    fileDict = dict_future.result()



    # Takes fileText and FileDict to build the articlee
    articleBuilder = ArticleBuilder(fileText,fileDict)

    # Build the article object
    myArticle = articleBuilder.build()
    myArticle.URL = url

    return JSONResponse(content=myArticle.__dict__())
