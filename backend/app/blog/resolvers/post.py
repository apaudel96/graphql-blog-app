import strawberry

from app.account.models import User
from app.blog.models import Post, Image
from app.blog import schema
from strawberry.types import Info
from app.extensions.permissions import IsAuthenticated


@strawberry.field()
async def list_posts(data: schema.ListPostInput) -> list[schema.PostType]:
    max_limit = 10
    posts = await Post.all().limit(min(data.limit, max_limit)).offset(data.offset)
    return posts


@strawberry.field()
async def detail_post(data: schema.DetailPostInput) -> schema.PostType:
    post = await Post.get_or_none(id=data.id)
    if post:
        return post
    raise Exception("Post does not exist")


@strawberry.mutation(permission_classes=[IsAuthenticated])
async def create_post(data: schema.CreatePostInput, info: Info) -> schema.PostType:
    image = await Image.create()
    post = Post()
    post.title = data.title
    post.content = data.content
    post.author = info.context["user"]
    post.image = image
    await post.save()
    await post.refresh_from_db()
    return post


@strawberry.mutation(permission_classes=[IsAuthenticated])
async def update_post(data: schema.UpdatePostInput, info: Info) -> schema.PostType:
    post = await Post.get_or_none(id=data.id).prefetch_related("author")
    current_user: User = info.context["user"]
    if post:
        # post exists
        if post.author == current_user:
            #  can edit
            post = post.update_from_dict(vars(data))
            await post.save()
            await post.refresh_from_db()
            return post
        else:
            raise Exception(f"You can't edit this post because you are not the author.")
    else:
        raise Exception("No post with that id was found")


@strawberry.mutation(permission_classes=[IsAuthenticated])
async def delete_post(data: schema.DeletePostInput, info: Info) -> schema.PostType:
    post = await Post.get_or_none(id=data.id).prefetch_related("author")
    if post:
        # post exists
        if post.author == info.context["user"]:
            #  can delete
            await post.delete()
            return post
        else:
            raise Exception(
                "You can't delete this post because you are not the author."
            )
    else:
        raise Exception("No post with that id was found")
