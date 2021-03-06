from __future__ import annotations
from datetime import datetime, timedelta
from secrets import token_urlsafe
from uuid import uuid4

from tortoise.models import Model
import tortoise.fields as f
from app.account.schema import UserType, TokenType
from app.blog.models import Post, Comment


class User(Model, UserType):
    email = f.CharField(255)
    password_hash = f.CharField(255)
    # auto generated
    verified = f.BooleanField(default=False)
    tokens: f.ReverseRelation[Token]
    posts: f.ReverseRelation[Post]
    comments: f.ReverseRelation[Comment]
    # replies: f.ReverseRelation[Reply]

    def __str__(self):
        return self.email


class Token(Model, TokenType):
    user = f.ForeignKeyField("models.User", related_name="tokens")
    # auto generated
    token = f.CharField(255, default=lambda: token_urlsafe()[:12])
    expires_on = f.DatetimeField(default=lambda: datetime.utcnow() + timedelta(1))

    @property
    def expired(self):
        return datetime.utcnow() > self.expires_on.replace(tzinfo=None)
