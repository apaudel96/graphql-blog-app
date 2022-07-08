from starlette.requests import Request
from starlette.responses import StreamingResponse, PlainTextResponse
from starlette.routing import Router, Route
from app.blog.models import Image
from app.blog import schema
import strawberry
from strawberry.types import Info
import io
from app.extensions.permissions import IsAuthenticated


@strawberry.mutation(permission_classes=[IsAuthenticated])
async def update_image(data: schema.EditImageInput, info: Info) -> schema.ImageType:
    image = await Image.get_or_none(id=data.id).prefetch_related("post__author")
    if image:
        if image.post.author == info.context["user"]:
            image.edit_by = image.create_edit_time()
            image.token = image.create_token()
            await image.save()
            return image
        else:
            raise Exception("You can't edit this image as you are not the author.")
    else:
        raise Exception("No image found with that id.")


async def upload(request: Request):
    image_id = request.path_params["image_id"]
    image = await Image.get_or_none(id=image_id)

    form_data = await request.form()
    token = form_data.get("token")
    image_data = form_data.get("image")

    if image and image.can_edit and image.token == token:
        image.image = await image_data.read()
        image.name = form_data.get("name") or image_data.filename
        await image.save()
        return PlainTextResponse(status_code=202)
    return PlainTextResponse(status_code=400)


async def download(request: Request):
    image_id = request.path_params["image_id"]
    image = await Image.get_or_none(id=image_id)
    if image:
        return StreamingResponse(io.BytesIO(image.image), media_type="image/jpg")
    return PlainTextResponse(status_code=404)


routes = Router(
    routes=[
        Route(path="/{image_id}", name="upload", endpoint=upload, methods=["post"]),
        Route(path="/{image_id}", name="download", endpoint=download, methods=["get"]),
    ],
)
