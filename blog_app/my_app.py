from flask import Flask

from blog_app.controller import bcrypt
from blog_app.controller.app_user import user_api
from blog_app.controller.blog import blog_api
from blog_app.controller.comment import comment_api
from blog_app.controller.like import like_api
from blog_app.data import db


def create_app(db_url):
    app_ = Flask(__name__)
    app_.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app_.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app_.config['SQLALCHEMY_ECHO'] = True
    app_.config['JWT_SECRET_KEY'] = 'hhgaghhgsdhdhdd'
    app_.register_blueprint(user_api)
    app_.register_blueprint(blog_api)
    app_.register_blueprint(comment_api)
    app_.register_blueprint(like_api)

    return app_


app = create_app('sqlite:///mydatabase.db')
bcrypt.init_app(app)
db.init_app(app)
