from __future__ import annotations

from datetime import datetime
from typing import Optional

import strawberry

# Types
from app.account.schema import UserType


@strawberry.type
class ImageType:
    id: int
    name: Optional[str]
    token: str
    can_edit: bool
    post: PostType


@strawberry.type
class PostType:
    id: int
    title: str
    content: str
    added_on: datetime
    edited_on: datetime
    image: ImageType
    author: UserType
    comments: list[CommentType]


@strawberry.type
class CommentType:
    id: int
    content: Optional[str]
    added_on: datetime
    edited_on: datetime
    post: PostType
    author: Optional[UserType]
    replies: list[CommentType]


#
# @strawberry.type
# class ReplyType:
#     id: int
#     content: str
#     added_on: datetime
#     edited_on: datetime
#     comment: PostType
#     author: UserType


# Inputs
@strawberry.input
class ListPostInput:
    limit: Optional[int] = 10
    offset: Optional[int] = 0


@strawberry.input
class DetailPostInput:
    id: int


@strawberry.input
class CreatePostInput:
    title: str
    content: str


@strawberry.input
class UpdatePostInput:
    id: int
    title: str
    content: str


@strawberry.input
class DeletePostInput:
    id: int


@strawberry.input
class EditImageInput:
    id: int


@strawberry.input()
class ListCommentInput:
    post_id: int


@strawberry.input()
class CreateCommentInput:
    content: str
    post_id: int
    parent_id: Optional[int]


@strawberry.input()
class UpdateCommentInput:
    id: int
    content: str


@strawberry.input()
class DeleteCommentInput:
    id: int
