from __future__ import annotations

import strawberry
from app.account.models import User, Token
from app.account.schema import (
    UserType,
    TokenType,
    LoginInput,
    LogoutInput,
    RegisterInput,
    ChangePasswordInput,
    TokenCheckInput,
)
from app.extensions.schema import MessageType
from passlib.hash import argon2


@strawberry.mutation
async def login(data: LoginInput) -> TokenType:
    user_model = await User.get_or_none(email=data.email)
    if user_model:
        token = await Token.create(user=user_model)

        return token
    raise Exception("Email and password did not match. Please try again.")


@strawberry.mutation
async def logout(data: LogoutInput) -> MessageType:
    token = await Token.get_or_none(token=data.token)
    if token:
        await token.delete()
        return MessageType(message="Successfully logged out.")
    raise Exception("Token is not valid.")


@strawberry.mutation
async def register(data: RegisterInput) -> TokenType:
    user = await User.get_or_none(email=data.email)
    if user:
        raise Exception("A account with that email already exists.")
    else:
        user = User()
        user.email = data.email
        user.password_hash = argon2.hash(data.password)
        await user.save()

        token = await Token.create(user=user)
        return token


@strawberry.mutation
async def change_password(data: ChangePasswordInput) -> MessageType:
    user = await User.get_or_none(email=data.email)
    if user and argon2.verify(data.password, user.password_hash):
        user.password_hash = argon2.hash(data.new_password)
        await user.save()
        await user.tokens.delete()
        return MessageType("Password changed successfully.")
    raise Exception("Email and password combination did not match.")


@strawberry.field
async def check_token(data: TokenCheckInput) -> TokenType:
    token = await Token.get_or_none(token=data.token)
    if token and not token.expired:
        return token
    raise Exception("Token is invalid or has expired.")
