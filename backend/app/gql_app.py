from strawberry.asgi import GraphQL
import strawberry
from app.account.gql import AccountQuery, AccountMutation
from app.blog.gql import BlogQuery, BlogMutation


@strawberry.type
class Query(AccountQuery, BlogQuery):
    pass


@strawberry.type
class Mutation(AccountMutation, BlogMutation):
    pass


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)

gql_app = GraphQL(schema, graphiql=True)
