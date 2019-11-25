from blog_app.data import db
from blog_app.my_app import app

if __name__ == '__main__':
    with app.app_context():
        db.create_all()