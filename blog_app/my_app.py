from flask import Flask

from blog_app.controller.app_user import app_user_bp
from blog_app.data import db


def create_app(db_url):
    app_ = Flask(__name__)
    app_.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app_.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app_.config['SQLALCHEMY_ECHO'] = True
    app_.register_blueprint(app_user_bp)

    return app_


app = create_app('sqlite:///mydatabase.db')
db.init_app(app)