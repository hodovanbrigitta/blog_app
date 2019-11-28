import os

from flask import Flask

from blog_app.controller import bcrypt
from blog_app.controller.app_user import user_api
from blog_app.controller.blog import blog_api
from blog_app.controller.comment import comment_api
from blog_app.controller.like import like_api
from blog_app.data import db


def create_app(filename):
    db_path = os.path.join(os.path.dirname(__file__), filename)
    db_uri = 'sqlite:///{}'.format(db_path)

    app_ = Flask(__name__, instance_relative_config=False)
    app_.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app_.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app_.config['SQLALCHEMY_ECHO'] = True
    app_.config['JWT_SECRET_KEY'] = 'hhgaghhgsdhdhdd'
    app_.register_blueprint(user_api)
    app_.register_blueprint(blog_api)
    app_.register_blueprint(comment_api)
    app_.register_blueprint(like_api)

    return app_


app = create_app('mydatabase.db')
bcrypt.init_app(app)
db.init_app(app)
