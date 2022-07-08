import strawberry
from .resolvers import post, image


@strawberry.type
class BlogQuery:
    # post
    list_posts = post.list_posts
    detail_post = post.detail_post


@strawberry.type
class BlogMutation:
    # post
    create_post = post.create_post
    update_post = post.update_post
    delete_post = post.delete_post
    # image
    update_image = image.update_image
