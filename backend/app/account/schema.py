from __future__ import annotations
from datetime import datetime

from strawberry import type, input, union


@type
class LoginSuccessType:
    token: TokenType


@type
class LoginErrorType:
    message: str = "Email and password combination did not match. Please try again."


@type
class UserType:
    email: str
    verified: bool


@type
class TokenType:
    user: UserType
    token: str
    expires_on: datetime
    expired: bool


# input types


@input
class LoginInput:
    email: str
    password: str


@input
class RegisterInput:
    email: str
    password: str


@input
class ChangePasswordInput:
    email: str
    password: str
    new_password: str


@input
class LogoutInput:
    token: str


@input
class TokenCheckInput:
    token: str
