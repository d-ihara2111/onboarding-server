from fastapi import FastAPI
from routers import articles, comments

# FastAPIのインスタンス作成
app = FastAPI()
app.include_router(articles.router)
app.include_router(comments.router)