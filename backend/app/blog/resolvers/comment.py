from typing import List

import strawberry
from strawberry.types import Info
from app.blog.models import Comment
from app.blog import schema
from tortoise.exceptions import BaseORMException
from app.extensions.permissions import IsAuthenticated


@strawberry.field()
async def list_comments(data: schema.ListCommentInput) -> List[schema.CommentType]:
    comments = (
        await Comment.all().filter(post__id=data.post_id).prefetch_related("replies")
    )
    return comments


@strawberry.mutation(permission_classes=[IsAuthenticated])
async def create_comment(
    data: schema.CreateCommentInput, info: Info
) -> schema.CommentType:
    comment = Comment()
    parent_comment = await Comment.get_or_none(id=data.parent_id)
    comment.author = info.context["user"]
    comment.content = data.content
    comment.post_id = data.post_id
    if parent_comment:
        if await parent_comment.parent:
            comment.parent = parent_comment.parent
        else:
            comment.parent = parent_comment
        # comment.parent_id = data.parent_id
    try:
        await comment.save()
        return comment
    except BaseORMException:
        raise Exception("There was an error saving the comment.")


@strawberry.mutation(permission_classes=[IsAuthenticated])
async def update_comment(
    data: schema.UpdateCommentInput, info: Info
) -> schema.CommentType:
    comment = await Comment.get_or_none(id=data.id)
    if not comment:
        raise Exception("That comment does not exist.")
    if await comment.author != info.context["user"]:
        raise Exception(
            f"You cannot edit this comment as you are not the original author."
        )
    comment.content = data.content
    try:
        await comment.save()
        await comment.refresh_from_db()
        return comment
    except BaseORMException:
        raise Exception("There was an error saving changes to the database.")


@strawberry.mutation(permission_classes=[IsAuthenticated])
async def delete_comment(
    data: schema.DeleteCommentInput, info: Info
) -> schema.CommentType:
    comment = await Comment.get_or_none(id=data.id)
    if not comment:
        raise Exception("That comment does not exist.")
    if await comment.author != info.context["user"]:
        raise Exception(
            "You cannot delete this comment as you are not the original author."
        )
    comment.content = None
    comment.author = None
    try:
        await comment.save()
        await comment.refresh_from_db()
        return comment
    except BaseORMException:
        raise Exception("There was an error deleting the comment.")
