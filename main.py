from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from handler.articles import select_articles, create_article, ArticleQueryParams, ArticleBody


# FastAPIのインスタンス作成
app = FastAPI()

# GETメソッドで /articlesにアクセスしたときの処理
# 記事取得
@app.get("/articles")
async def get_articles(title: Optional[str] = None, offset: int = 0, limit: int = 50):
    params = ArticleQueryParams(title=title, offset=offset, limit=limit)
    response = select_articles(params)

    return response

@app.post("/articles")
async def post_article(payload: ArticleBody):
    try:
        result = create_article(payload)
        return JSONResponse(status_code=200, content=result)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})


