from blog_app.data import AppUser, db
from blog_app.service import bcrypt


def generate_hash(password):
    return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")


def check_hash(pw_hash, password):
    return bcrypt.check_password_hash(pw_hash, password)


def get_user_by_username(username):
    return db.session.query(AppUser)\
        .filter(AppUser.app_username == username).first()


def get_user_by_id(user_id):
    return db.session.query(AppUser).filter(AppUser.id == user_id).first()


def get_all_users():
    return db.session.query(AppUser).all()


def create_user(username, user_password):
    return AppUser(
        app_username=username,
        user_password=user_password
    )

