from flask_bcrypt import Bcrypt

from blog_app.data import db


bcrypt = Bcrypt()


def save(model):
    """
    saves the given model to our database
    :param model: the given model to save
    :return:
    """
    db.session.add(model)
    db.session.commit()
    db.session.refresh(model)


def delete(model):
    """
    deletes the given model from our database
    :param model: the given model to delete
    :return:
    """
    db.session.delete(model)
    db.session.commit()
