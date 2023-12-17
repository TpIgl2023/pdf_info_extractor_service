from fastapi import FastAPI, Security , APIRouter
from Routers.root_router import root_router
from Middlwares.Auth import get_api_key

#Start grobid with : docker run --rm -d --init --ulimit core=0 -p 8070:8070 lfoppiano/grobid:0.8.0
#Start the API with : uvicorn main:app --reload

app = FastAPI()

app.include_router(root_router)


@app.get("/")
def protected_route(api_key: str = Security(get_api_key)):
    # Process the request for authenticated users
    return {"message": "Access granted!"}