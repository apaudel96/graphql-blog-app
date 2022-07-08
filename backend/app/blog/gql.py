import strawberry
from .resolvers import post


@strawberry.type
class BlogQuery:
    list_posts = post.list_posts
    detail_post = post.detail_post


@strawberry.type
class BlogMutation:
    create_post = post.create_post
    update_post = post.update_post
    delete_post = post.delete_post
