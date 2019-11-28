from flask import Blueprint, request, g, jsonify, make_response

from blog_app.controller import invalid_json_response
from blog_app.data import Like, db, Blog
from blog_app.service.app_user_service import Auth

like_api = Blueprint('like', __name__)


@like_api.route("/blog/<int:blog_id>/like", methods=["POST"])
@Auth.auth_required
def add_like(blog_id):
    """
    Add a like to a blog

    :return: the added like
    """
    blog = db.session.query(Blog).filter(Blog.id == blog_id).first()
    act_user_id = g.user.get('user_id')
    if blog is None:
        return invalid_json_response(f"blog with ID {blog_id} does not exist")
    like = db.session.query(Like).filter(Like.user_id == act_user_id, Like.blog_id == blog_id.first()
    if like:
        return invalid_json_response(f"like already exist")
    db.session.add(like)
    db.session.commit()
    db.session.refresh(like)
    like_resource = jsonify({
        "user_id": like.user_id,
        "blog_id": like.blog_id
    })
    return make_response(like_resource, 201)
