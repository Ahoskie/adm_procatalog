from fastapi import FastAPI

from api.routes import api_router
from db import initialize_cluster, initialize_buckets, ClusterHolder

app = FastAPI()

app.include_router(api_router)


@app.on_event('startup')
async def startup_event():
    cluster = await initialize_cluster()
    ClusterHolder.cluster = cluster
    await initialize_buckets()
