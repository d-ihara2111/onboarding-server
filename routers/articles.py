from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
from handler.articles import ArticlePutIn, delete_articles_handler, select_articles, create_article, ArticleGetIn, ArticlePostIn, update_article, ArticleDeleteIn
from typing import Annotated

router = APIRouter()

# 記事取得
@router.get("/articles")
async def get_articles(params: Annotated[ArticleGetIn, Query()]):
    response = select_articles(params)
    return response

# 記事投稿
@router.post("/articles")
async def post_articles(payload: ArticlePostIn):
    try:
        result = create_article(payload)
        return JSONResponse(status_code=200, content=result)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

# 記事編集
@router.put("/articles/{id}")
async def put_articles(id: int, payload: ArticlePutIn):
    try:
        result = update_article(id, payload)
        return JSONResponse(status_code=200, content=result)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

# 記事削除
@router.delete("/articles")
async def delete_articles(ids: ArticleDeleteIn):
    try:
        result = delete_articles_handler(ids)
        return JSONResponse(status_code=200, content=result)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
