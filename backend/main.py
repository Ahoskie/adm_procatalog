from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from api.routes import api_router
from db import initialize_cluster, initialize_buckets, ClusterHolder
from db.exceptions import DatabaseException
from services.exceptions import DocumentNotFound
from middleware.jwt_user import AppendUserToRequest

app = FastAPI()

app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_middleware(AppendUserToRequest)


@app.on_event('startup')
async def startup_event():
    cluster = await initialize_cluster()
    ClusterHolder.cluster = cluster
    await initialize_buckets()


@app.exception_handler(DocumentNotFound)
def document_not_found_handler(request, exc: DocumentNotFound):
    return JSONResponse(status_code=404, content={'detail': exc.message})


@app.exception_handler(DatabaseException)
def database_exception_handler(request, exc: DatabaseException):
    return JSONResponse(status_code=400, content={'detail': exc.message})

