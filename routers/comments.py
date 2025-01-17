from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import Annotated

from handler.comments import CommentDeleteIn, CommentGetIn, CommentPostIn, create_comment, delete_comments_handler, select_comments

router = APIRouter()

# コメント取得
@router.get("/comments")
async def get_comments(params: Annotated[CommentGetIn, Query()]):
    response = select_comments(params)
    return response

# コメント投稿
@router.post("/comments")
async def post_comments(payload: CommentPostIn):
    try:
        result = create_comment(payload)
        return JSONResponse(status_code=200, content=result)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

# コメント編集はオンボーディング課題では未実装

# コメント削除
@router.delete("/comments")
async def delete_comments(payload: CommentDeleteIn):
    try:
        result = delete_comments_handler(payload)
        return JSONResponse(status_code=200, content=result)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})