from flask import Blueprint, request, jsonify, make_response, g
from werkzeug.exceptions import BadRequest

from blog_app.controller import invalid_json_response
from blog_app.data import Blog, db
from blog_app.service.app_user_service import get_user_by_id, Auth

blog_api = Blueprint('blog', __name__)


@blog_api.route("/blog", methods=["POST"])
@Auth.auth_required
def create_blog():
    """
    Creates a blog

    :return: the created blog
    """
    data = request.get_json()
    try:
        blog = Blog(
            title=data["title"],
            content=data["content"],
            user_id=g.user.get('user_id')
        )
    except KeyError as e:
        return invalid_json_response(f"missing property: {e}")
    db.session.add(blog)
    db.session.commit()
    db.session.refresh(blog)
    blog_resource = jsonify({
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "user_id": blog.user_id,
    })
    return make_response(blog_resource, 201)


@blog_api.route("/blog/<int:blog_id>", methods=["PUT"])
@Auth.auth_required
def update_blog(blog_id):
    """
    Update a blog

    :return: the updated blog
    """
    try:
        data = request.get_json()
    except BadRequest:
        return invalid_json_response("invalid request body")

    blog = db.session.query(Blog).filter(Blog.id == blog_id).first()
    if blog is None:
        return invalid_json_response(
            f"recipe with ID {blog_id} does not exist")
    if blog.user_id != g.user.get('user_id'):
        return invalid_json_response("permission denied")
    blog.title = data["title"]
    blog.content = data["content"]
    db.session.commit()
    db.session.refresh(blog)
    return jsonify({
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "user_id": blog.user_id
    })