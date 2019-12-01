from flask import Blueprint, g, jsonify, make_response

from blog_app.controller import invalid_json_response
from blog_app.data import Like, db, Blog
from blog_app.service import save
from blog_app.service.authentication import auth
from blog_app.service.like_service import create_like, check_like

like_api = Blueprint('like', __name__)


@like_api.route("/like", methods=["GET"])
def get_likes():
    """
    Returns every like from our application

    :return: every like from our application
    """
    like_models = db.session.query(Like).all()
    return jsonify([{
         "user_id": like.user_id,
         "blog_id": like.blog_id
    } for like in like_models])


@like_api.route("/blog/<blog_id>/like", methods=["POST"])
@auth.auth_required
def add_like(blog_id):
    """
    Add a like to a blog

    :return: the added like
    """
    blog = db.session.query(Blog).filter(Blog.id == blog_id).first()
    act_user_id = g.user.get('user_id')
    try:
        blog_id = int(blog_id)
    except ValueError:
        return invalid_json_response("invalid input type")
    if blog is None:
        return invalid_json_response(f"blog with ID {blog_id} does not exist")
    like = check_like(act_user_id, blog_id)
    if like:
        return invalid_json_response(f"you have already liked this blog")
    try:
        like = create_like(user_id=g.user.get('user_id'), blog_id=blog_id)
    except KeyError as e:
        return invalid_json_response(f"missing property: {e}")
    save(like)
    like_resource = jsonify({
        "user_id": like.user_id,
        "blog_id": like.blog_id
    })
    return make_response(like_resource, 201)
