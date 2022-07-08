from starlette.applications import Starlette
from tortoise.contrib.starlette import register_tortoise
from app.gql_app import gql_app
from app.blog.resolvers.image import routes as image_routes

app = Starlette()
app.mount(path="/image", app=image_routes)
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
