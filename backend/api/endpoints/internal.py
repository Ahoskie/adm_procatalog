import json
from typing import List
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse

from db.utils import flush_db
from services.products import find_product_images


router = APIRouter(
    prefix='/internal',
    tags=['internal']
)


@router.post('/flush-db/')
async def flush_database():
    await flush_db()
    return Response(json.dumps({'success': 'flushed'}), status_code=200)


@router.get('/images-links/')
async def get_images_links(search_string):
    images = await find_product_images(search_string)
    return JSONResponse({'images': images}, status_code=200)

