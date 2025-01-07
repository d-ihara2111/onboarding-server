# FastAPIインポート
from fastapi import FastAPI


# 作成したモデル定義ファイルと設定ファイルをインポート
import models as m 
import databases as s 


# FastAPIのインスタンス作成
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# GETメソッドで /articlesにアクセスしたときの処理
# 記事取得
@app.get("/articles", tags=["articles"])
async def read_articles():
    #DBからユーザ情報を取得
    result = s.session.query(m.Article).all()
    return result


