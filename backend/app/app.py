from starlette.applications import Starlette
from tortoise.contrib.starlette import register_tortoise
from app.gql_app import gql_app


app = Starlette()
app.mount("/", gql_app)

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={
        "models": [
            "app.account.models",
            "app.blog.models",
        ],
    },
    generate_schemas=True,
)
