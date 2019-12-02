from blog_app.data import AppUser, db
from blog_app.service import bcrypt


def generate_hash(password):
    """
    Generates hash code
    :param password: the given password
    :return: the generated hash code for the given password
    """
    return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")


def check_hash(pw_hash, password):
    """
    Check the user's password
    :param pw_hash: the hashed password
    :param password: the given password to check
    :return: True or False
    """
    return bcrypt.check_password_hash(pw_hash, password)


def get_user_by_username(username):
    """
    Returns the user from our applications with the given username
    :param username: The user's username to return
    :return: the user from our applications with the given username
    """
    return db.session.query(AppUser)\
        .filter(AppUser.app_username == username).first()


def get_user_by_id(user_id):
    """
    Returns the user from our applications with the given ID
    :param user_id: The user's ID to return
    :return: the user from our applications with the given ID
    """
    return db.session.query(AppUser).filter(AppUser.id == user_id).first()


def get_all_users():
    """
    returns every user from our applications
    :return: every user from our applications
    """
    return db.session.query(AppUser).all()


def create_user(username, user_password):
    """
    creates a new user with the given parameters
    :param username: the given username
    :param user_password: the given password
    :return: the created user
    """
    return AppUser(
        app_username=username,
        user_password=user_password
    )
