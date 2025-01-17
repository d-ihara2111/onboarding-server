from fastapi import HTTPException
from databases.models import Article, Comment
from databases.settings import session
from typing import List, Optional
from datetime import date as Date
from pydantic import BaseModel, Field

# コメント取得
class CommentGetIn(BaseModel):
    article_id: int
    offset: Optional[int] = Field(0, ge=0)
    limit: Optional[int] = Field(50, ge=0, le=100)

class CommentListItem(BaseModel):
    id: int
    content: str
    created_at: Date
    updated_at: Date

class CommentGetOut(BaseModel):
    list: List[CommentListItem]
    total: int
    offset: int
    count: int

def select_comments(params: CommentGetIn):
    commentQuery = session.query(Comment).filter(Comment.article_id == params.article_id)
    
    # 総数を取得
    total = commentQuery.count()
    result = commentQuery.offset(params.offset).limit(params.limit).all()
    list = []
    for comment in result:
        list.append(CommentListItem(id=comment.id, content=comment.content, created_at=comment.created_at, updated_at=comment.updated_at))

    # resultの内容をCommentに詰め直す
    response = CommentGetOut(list=list, total=total, offset=params.offset, count=len(list))

    return response

# コメント投稿
class CommentPostIn(BaseModel):
    article_id: int
    content: str

def create_comment(payload: CommentPostIn):
    created_at = Date.today()
    updated_at = Date.today()
    comment = Comment(article_id=payload.article_id, content=payload.content, created_at=created_at, updated_at=updated_at)
    session.add(comment)
    session.commit()
    session.refresh(comment)

    return {"status": "success"}

# コメント削除
class CommentDeleteIn(BaseModel):
    ids: List[int]

def delete_comments_handler(payload: CommentDeleteIn):
    commentQuery = session.query(Comment)
    for id in payload.ids:
        comment = commentQuery.filter(Comment.id == id).first()
        if comment:
            session.delete(comment)
    session.commit()

    return {"status": "success"}