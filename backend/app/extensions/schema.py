import strawberry


@strawberry.type()
class MessageType:
    message: str
