from flask import Blueprint, request, jsonify, make_response

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
            user_id=data["user_id"]
        )
    except KeyError as e:
        return invalid_json_response(f"missing property: {e}")
    user_in_db = get_user_by_id(data["user_id"])
    if not user_in_db:
        return invalid_json_response(f"user with id {data['user_id']} does not exist")
    db.session.add(blog)
    db.session.commit()
    db.session.refresh(blog)
    blog_resource = jsonify({
        "title": blog.title,
        "content": blog.content,
        "user_id": blog.user_id,
    })
    return make_response(blog_resource, 201)