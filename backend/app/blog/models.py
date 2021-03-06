from __future__ import annotations
from datetime import datetime, timedelta
from secrets import token_urlsafe

from tortoise.models import Model
import tortoise.fields as f
from app.blog import schema


class Image(Model, schema.ImageType):
    @staticmethod
    def create_edit_time():
        return datetime.utcnow() + timedelta(minutes=10)

    @staticmethod
    def create_token():
        return token_urlsafe()[:12]

    name = f.CharField(255, null=True)
    token = f.CharField(255, default=create_token)
    edit_by = f.DatetimeField(default=create_edit_time)
    image = f.BinaryField(null=True)
    post: f.OneToOneRelation[Post]

    @property
    def can_edit(self):
        return datetime.utcnow() < self.edit_by.replace(tzinfo=None)


class Post(Model, schema.PostType):
    title = f.CharField(255)
    content = f.TextField()
    added_on = f.DatetimeField(auto_now_add=True)
    edited_on = f.DatetimeField(auto_now=True)
    image = f.OneToOneField(
        "models.Image",
        related_name="post",
    )
    author = f.ForeignKeyField(
        "models.User", related_name="posts", on_delete="SET NULL", null=True
    )
    comments: f.ForeignKeyRelation[Comment]


class Comment(Model, schema.CommentType):
    content = f.TextField(null=True)
    added_on = f.DatetimeField(auto_now_add=True)
    edited_on = f.DatetimeField(auto_now=True)
    post = f.ForeignKeyField(
        "models.Post", related_name="comments", on_delete="CASCADE"
    )
    author = f.ForeignKeyField(
        "models.User", related_name="comments", on_delete="SET NULL", null=True
    )
    parent = f.ForeignKeyField("models.Comment", null=True, related_name="replies")
    replies = f.ForeignKeyRelation["Comment"]


# class Reply(Model, schema.ReplyType):
#     content = f.TextField()
#     added_on = f.DatetimeField(auto_now_add=True)
#     edited_on = f.DatetimeField(auto_now=True)
#     comment = f.ForeignKeyField(
#         "models.Post", related_name="replies", on_delete="CASCADE"
#     )
#     author = f.ForeignKeyField(
#         "models.User", related_name="replies", on_delete="SET NULL", null=True
#     )
