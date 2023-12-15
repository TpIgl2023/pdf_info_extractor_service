from fastapi import FastAPI, Security , APIRouter
from Routers.root_router import root_router
from Middlwares.Auth import get_api_key



#docker run --rm -d --init --ulimit core=0 -p 8070:8070 lfoppiano/grobid:0.8.0
#uvicorn main:app --reload
# URL = "https://drive.google.com/uc?id=1eZy2sbuF1TD5dJg0ZGJwXUGycp4rc61m&export=download"

app = FastAPI()

app.include_router(root_router)


@app.get("/")
def protected_route(api_key: str = Security(get_api_key)):
    # Process the request for authenticated users
    return {"message": "Access granted!"}