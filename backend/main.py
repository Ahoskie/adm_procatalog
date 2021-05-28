from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import api_router
from db import initialize_cluster, initialize_buckets, ClusterHolder

app = FastAPI()

app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
async def startup_event():
    cluster = await initialize_cluster()
    ClusterHolder.cluster = cluster
    await initialize_buckets()
