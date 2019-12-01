from flask import Blueprint, request, g, jsonify, make_response

from blog_app.controller import invalid_json_response
from blog_app.service import save, delete
from blog_app.service.authentication import auth
from blog_app.service.blog_service import get_blog_by_id
from blog_app.service.comment_service import get_all_comments, \
    get_comments_by_blog_id, create_comment, get_comment_by_id, \
    update_comment_in_db

comment_api = Blueprint('comment', __name__)


@comment_api.route("/comment", methods=["GET"])
def get_comments():
    """
    Returns every comment from our application

    :return: every comment from our application
    """
    comment_models = get_all_comments()
    return jsonify([{
        "id": comment.id,
        "content": comment.content,
        "user_id": comment.user_id,
        "blog_id": comment.blog_id
    } for comment in comment_models])


@comment_api.route("/blog/<blog_id>/comment", methods=["GET"])
def get_comments_by_blog(blog_id):
    """
    Returns every comment from our application with the given blog ID

    :return: every comment from our application with the given blog ID
    """
    comment_models = get_comments_by_blog_id(blog_id=blog_id)
    return jsonify([{
        "id": comment.id,
        "content": comment.content,
        "user_id": comment.user_id,
        "blog_id": comment.blog_id
    } for comment in comment_models])


@comment_api.route("/blog/<blog_id>/comment", methods=["POST"])
@auth.auth_required
def create_new_comment(blog_id):
    """
    Creates a comment

    :return: the created comment
    """
    data = request.get_json()
    try:
        comment = create_comment(content=data["content"],
                                 user_id=g.user.get('user_id'), blog_id=blog_id)
    except KeyError as e:
        return invalid_json_response(f"missing property: {e}")
    try:
        blog_id = int(blog_id)
    except ValueError:
        return invalid_json_response("invalid input type")
    blog = get_blog_by_id(blog_id)
    if blog is None:
        return invalid_json_response(f"blog with ID {blog_id} does not exist")
    save(comment)
    comment_resource = jsonify({
        "id": comment.id,
        "content": comment.content,
        "user_id": comment.user_id,
        "blog_id": comment.blog_id
    })
    return make_response(comment_resource, 201)


@comment_api.route("/comment/<comment_id>", methods=["PUT"])
@auth.auth_required
def update_comment(comment_id):
    """
    Update a comment

    :return: the updated comment
    """
    data = request.get_json()
    if not data["content"] or not g.user.get('user_id'):
        return invalid_json_response(f"missing property")
    comment = get_comment_by_id(comment_id)
    try:
        comment_id = int(comment_id)
    except ValueError:
        return invalid_json_response("invalid input type")
    if comment is None:
        return invalid_json_response(
            f"comment with ID {comment_id} does not exist")
    if comment.user_id != g.user.get('user_id'):
        return invalid_json_response("permission denied")
    update_comment_in_db(comment, data)
    return jsonify({
        "id": comment.id,
        "content": comment.content,
        "user_id": comment.user_id,
        "blog_id": comment.blog_id
    })


@comment_api.route("/comment/<comment_id>", methods=["DELETE"])
@auth.auth_required
def delete_comment(comment_id):
    """
    Delete a comment from our application

    :return: 204 No Content
    """
    try:
        comment_id = int(comment_id)
    except ValueError:
        return invalid_json_response("invalid input type")
    comment = get_comment_by_id(comment_id)
    if not comment:
        return invalid_json_response("blog not found")
    if comment.user_id != g.user.get('user_id'):
        return invalid_json_response("permission denied")
    if comment:
        delete(comment)
    return '', 204
