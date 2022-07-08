from __future__ import annotations
from datetime import datetime, timedelta
from secrets import token_urlsafe

from tortoise.models import Model
import tortoise.fields as f


class Image(Model):
    @staticmethod
    def create_edit_time():
        return (datetime.utcnow() + timedelta(minutes=10)).replace(tzinfo=None)

    name = f.CharField(255)
    token = f.CharField(255, default=lambda: token_urlsafe()[:12])
    edit_by = f.DatetimeField(default=lambda: datetime.utcnow() + timedelta(minutes=10))
    image = f.BinaryField(null=True)
    post: f.OneToOneRelation[Post]

    @property
    def can_edit(self):
        return datetime.utcnow() < self.edit_by


class Post(Model):
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


class Comment(Model):
    content = f.TextField()
    added_on = f.DatetimeField(auto_now_add=True)
    edited_on = f.DatetimeField(auto_now=True)
    post = f.ForeignKeyField(
        "models.Post", related_name="comments", on_delete="CASCADE"
    )
    author = f.ForeignKeyField(
        "models.User", related_name="comments", on_delete="SET NULL", null=True
    )
    replies = f.ForeignKeyRelation["Reply"]


class Reply(Model):
    content = f.TextField()
    added_on = f.DatetimeField(auto_now_add=True)
    edited_on = f.DatetimeField(auto_now=True)
    comment = f.ForeignKeyField(
        "models.Post", related_name="replies", on_delete="CASCADE"
    )
    author = f.ForeignKeyField(
        "models.User", related_name="replies", on_delete="SET NULL", null=True
    )
