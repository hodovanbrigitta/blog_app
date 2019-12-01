from flask import Blueprint, request, g, jsonify, make_response

from blog_app.controller import invalid_json_response
from blog_app.service import save
from blog_app.service.authentication import auth
from blog_app.service.blog_service import get_blog_by_id
from blog_app.service.comment_service import get_all_comments

comment_api = Blueprint('comment', __name__)


@comment_api.route("/comment", methods=["GET"])
def get_comments():
    """
    # TODO limit to 1 blog
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


@comment_api.route("/blog/<blog_id>/comment", methods=["POST"])
@auth.auth_required
def create_comment(blog_id):
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

# TODO edit comment

# TODO delete comment