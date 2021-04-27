import json
from typing import List
from fastapi import APIRouter, HTTPException, Response

from db.utils import flush_db


router = APIRouter(
    prefix='/internal',
    tags=['internal']
)


@router.post('/flush-db/')
async def flush_database():
    await flush_db()
    return Response(json.dumps({'success': 'flushed'}), status_code=200)

