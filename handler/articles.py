from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from databases.models import Article, Comment
from databases.settings import session
from dataclasses import dataclass
from typing import List
from datetime import date as Date
from pydantic import BaseModel

# 記事取得
@dataclass
class ArticleQueryParams:
    title: str = None
    offset: int = 0
    limit: int = 50

@dataclass
class ArticleListItem:
    id: int
    title: str
    content: str
    comment_count: int
    created_at: Date
    updated_at: Date

@dataclass
class ArticleResponse:
    list: List[ArticleListItem]
    total: int
    offset: int
    count: int

def select_articles(params: ArticleQueryParams):
    articleQuery = session.query(Article)
    
    if params.title:
        articleQuery = articleQuery.filter(Article.title.contains(params.title))
    
    # 総数を取得
    total = articleQuery.count()
    result = articleQuery.offset(params.offset).limit(params.limit).all()
    list = []
    commentQuery = session.query(Comment)
    for article in result:
        # 記事毎にコメント数を取得
        comment_count = commentQuery.filter(Comment.article_id == article.id).count()
        list.append(ArticleListItem(id=article.id, title=article.title, content=article.content, comment_count=comment_count, created_at=article.created_at, updated_at=article.updated_at))

    # resultの内容をArticleに詰め直す
    response = ArticleResponse(list=list, total=total, offset=params.offset, count=len(list))

    return response


# 記事作成
class ArticleBody(BaseModel):
    title: str
    content: str

def create_article(payload: ArticleBody):
    # title, contentのバリデーションエラーの時は400エラーとする
    if not payload.title:
        raise HTTPException(status_code=400, detail="title is empty")
    
    if len(payload.title) > 64:
        raise HTTPException(status_code=400, detail="Title must be 64 characters or less")
    
    if not payload.content:
        raise HTTPException(status_code=400, detail="content is empty")

    created_at = Date.today()
    updated_at = Date.today()
    article = Article(title=payload.title, content=payload.content,created_at=created_at, updated_at=updated_at)
    session.add(article)
    session.commit()
    session.refresh(article)

    return {"status": "success"}