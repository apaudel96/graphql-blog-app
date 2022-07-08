from __future__ import annotations

from typing import Union, Awaitable, Any

from strawberry.permission import BasePermission
from strawberry.types import Info
from starlette.requests import HTTPConnection

from app.account.models import Token


def _get_token_from_headers(info: Info) -> Token | None:
    conn: HTTPConnection = info.context["request"]

    if "Authorization" in conn.headers:
        try:
            scheme, cred = conn.headers["Authorization"].split()
            if scheme.lower() == "token":
                token = await Token.get_or_none(token=cred)
                if token and not token.expired:
                    info.context["user"] = await token.user
                    return token
            return None
        except ValueError:
            return None


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    async def has_permission(
        self, source: Any, info: Info, **kwargs
    ) -> Union[bool, Awaitable[bool]]:
        token = _get_token_from_headers(info)
        if token:
            return True
        return False
