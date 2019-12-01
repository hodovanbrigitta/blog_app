from flask import Blueprint, request, jsonify, make_response, g

from blog_app.controller import invalid_json_response
from blog_app.data import Blog, db
from blog_app.service import save, delete
from blog_app.service.authentication import auth
from blog_app.service.blog_service import get_blog_by_id, update_blog_in_db, \
    create_blog

blog_api = Blueprint('blog', __name__)


@blog_api.route("/blog", methods=["GET"])
def get_blogs():
    """
    Returns every blog from our application

    :return: every blog from our application
    """
    blog_models = db.session.query(Blog).all()
    return jsonify([{
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "user_id": blog.user_id
    } for blog in blog_models])


@blog_api.route("/blog/<blog_id>", methods=["GET"])
def get_blog(blog_id):
    """
    Returns a blog from our application with the given ID

    :param blog_id: the blog's ID to return
    :return: a blog from our application with the given ID
    """
    blog = db.session.query(Blog).filter(Blog.id == blog_id).first()
    try:
        blog_id = int(blog_id)
    except ValueError:
        return invalid_json_response("invalid input type")
    if blog is None:
        return invalid_json_response(f"blog with ID {blog_id} does not exist")

    return jsonify({
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "user_id": blog.user_id
    })


@blog_api.route("/blog", methods=["POST"])
@auth.auth_required
def create_new_blog():
    """
    Creates a blog

    :return: the created blog
    """
    data = request.get_json()
    try:
        # TODO ???? recursive
        blog = create_blog(title=data["title"], content=data["content"],
                           user_id=g.user.get('user_id'))
    except KeyError as e:
        return invalid_json_response(f"missing property: {e}")
    save(blog)
    blog_resource = jsonify({
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "user_id": blog.user_id,
    })
    return make_response(blog_resource, 201)


@blog_api.route("/blog/<blog_id>", methods=["PUT"])
@auth.auth_required
def update_blog(blog_id):
    """
    Update a blog

    :return: the updated blog
    """
    data = request.get_json()
    try:
        # TODO calls wrong method
        blog = create_blog(title=data["title"], content=data["content"],
                           user_id=g.user.get('user_id'))
    except KeyError as e:
        return invalid_json_response(f"missing property: {e}")

    blog = get_blog_by_id(blog_id)
    try:
        blog_id = int(blog_id)
    except ValueError:
        return invalid_json_response("invalid input type")
    if blog is None:
        return invalid_json_response(
            f"recipe with ID {blog_id} does not exist")
    if blog.user_id != g.user.get('user_id'):
        return invalid_json_response("permission denied")
    update_blog_in_db(blog, data)
    return jsonify({
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "user_id": blog.user_id
    })


@blog_api.route("/blog/<blog_id>", methods=["DELETE"])
@auth.auth_required
def delete_blog(blog_id):
    """
    Delete a blog from our application

    :return: 204 No Content
    """
    # TODO what happens if blog has comments in the database?
    try:
        blog_id = int(blog_id)
    except ValueError:
        return invalid_json_response("invalid input type")
    blog = get_blog_by_id(blog_id)
    if not blog:
        return invalid_json_response("blog not found")
    if blog.user_id != g.user.get('user_id'):
        return invalid_json_response("permission denied")
    if blog:
        delete(blog)
    return '', 204
