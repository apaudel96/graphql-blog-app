import strawberry
from .resolvers import post, image, comment


@strawberry.type
class BlogQuery:
    # post
    list_posts = post.list_posts
    detail_post = post.detail_post
    # comment
    list_comments = comment.list_comments


@strawberry.type
class BlogMutation:
    # post
    create_post = post.create_post
    update_post = post.update_post
    delete_post = post.delete_post
    # image
    update_image = image.update_image
    # comment
    create_comment = comment.create_comment
    update_comment = comment.update_comment
    delete_comment = comment.delete_comment
