from fastapi import FastAPI
from routers import articles

# FastAPIのインスタンス作成
app = FastAPI()
app.include_router(articles.router)
