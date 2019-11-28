from flask import Blueprint, request, g, jsonify, make_response

from blog_app.controller import invalid_json_response
from blog_app.data import Comment, db, Blog
from blog_app.service.app_user_service import Auth

comment_api = Blueprint('comment', __name__)


@comment_api.route("/comment", methods=["GET"])
def get_comments():
    """
    Returns every comment from our application

    :return: every comment from our application
    """
    comment_models = db.session.query(Comment).all()
    return jsonify([{
        "id": comment.id,
        "content": comment.content,
        "user_id": comment.user_id,
        "blog_id": comment.blog_id
    } for comment in comment_models])


@comment_api.route("/blog/<blog_id>/comment", methods=["POST"])
@Auth.auth_required
def create_comment(blog_id):
    """
    Creates a comment

    :return: the created comment
    """
    data = request.get_json()
    try:
        comment = Comment(
            content=data["content"],
            user_id=g.user.get('user_id'),
            blog_id=blog_id
        )
    except KeyError as e:
        return invalid_json_response(f"missing property: {e}")
    try:
        blog_id = int(blog_id)
    except ValueError:
        return invalid_json_response("invalid input type")
    blog = db.session.query(Blog).filter(Blog.id == blog_id).first()
    if blog is None:
        return invalid_json_response(f"blog with ID {blog_id} does not exist")
    db.session.add(comment)
    db.session.commit()
    db.session.refresh(comment)
    comment_resource = jsonify({
        "id": comment.id,
        "content": comment.content,
        "user_id": comment.user_id,
        "blog_id": comment.blog_id
    })
    return make_response(comment_resource, 201)
