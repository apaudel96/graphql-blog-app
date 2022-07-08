from strawberry.asgi import GraphQL
import strawberry
from app.account.gql import AccountQuery, AccountMutation


@strawberry.type
class Query(AccountQuery):
    # hello: str = strawberry.field(resolver=lambda: "world")
    pass


@strawberry.type
class Mutation(AccountMutation):
    pass


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)

gql_app = GraphQL(schema, graphiql=True)
