from fastapi import APIRouter, Security
from fastapi.security import APIKeyHeader

from Handlers.processMultiplePdfHandler import processMultiplePdfHandler
from Handlers.process_pdf import process_pdf
from Middlwares.Auth import get_api_key

root_router = APIRouter()
api_key_header = APIKeyHeader(name="X-API-Key")

@root_router.get("/")
async def handle_pdf(URL : str,api_key: str = Security(get_api_key)):
    return await process_pdf(URL,api_key=api_key)


@root_router.post("/multiple")
async def handleMultiplePdf(URL : list[str],api_key: str = Security(get_api_key)):
    return await processMultiplePdfHandler(URL)
