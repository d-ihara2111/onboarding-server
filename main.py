# FastAPIインポート
from fastapi import FastAPI
from typing import Union


# 作成したモデル定義ファイルと設定ファイルをインポート
from databases.settings import session
from databases.models import ArticleQueryParams
from databases.handle import select_articles


# FastAPIのインスタンス作成
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# GETメソッドで /articlesにアクセスしたときの処理
# 記事取得
@app.get("/articles")
async def read_articles(title: Union[str, None] = None, offset: int = 0, limit: int = 50):
    #DBからユーザ情報を取得
    # 記事オブジェクトにデータを入れる
    params = ArticleQueryParams(title=title, offset=offset, limit=limit)
    result = select_articles(params)
    return result


