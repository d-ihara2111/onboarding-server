from fastapi import HTTPException
from databases.models import Article, Comment
from databases.settings import session
from typing import List, Optional
from datetime import date as Date
from pydantic import BaseModel, Field

# 記事取得
class ArticleGetIn(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=64)
    offset: Optional[int] = Field(0, ge=0)
    limit: Optional[int] = Field(50, ge=0, le=100)

class ArticleListItem(BaseModel):
    id: int
    title: str
    content: str
    comment_count: int
    created_at: Date
    updated_at: Date

class ArticleGetOut(BaseModel):
    list: List[ArticleListItem]
    total: int
    offset: int
    count: int

def select_articles(params: ArticleGetIn):
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
    response = ArticleGetOut(list=list, total=total, offset=params.offset, count=len(list))

    return response


# 記事作成
class ArticlePostIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=64)
    content: str

def create_article(payload: ArticlePostIn):
    created_at = Date.today()
    updated_at = Date.today()
    article = Article(title=payload.title, content=payload.content,created_at=created_at, updated_at=updated_at)
    session.add(article)
    session.commit()
    session.refresh(article)

    return {"status": "success"}


# 記事編集
class ArticlePutIn(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=64)
    content: Optional[str]

def update_article(id: int, payload: ArticlePutIn):
    article = session.query(Article).filter(Article.id == id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    
    if payload.title:
        article.title = payload.title
    if payload.content:
        article.content = payload.content
    
    article.updated_at = Date.today()
    session.commit()

    return {"status": "success"}


# 記事削除
class ArticleDeleteIn(BaseModel):
    ids: List[int]

def delete_articles_handler(ids: ArticleDeleteIn):
    for id in ids.ids:
        article = session.query(Article).filter(Article.id == id).first()
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")
        session.delete(article)

        # 記事に紐づくコメントも削除
        commentQuery = session.query(Comment).filter(Comment.article_id == id)
        for comment in commentQuery:
            session.delete(comment)    
    
    session.commit()

    return {"status": "success"}