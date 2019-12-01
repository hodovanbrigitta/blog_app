from flask_bcrypt import Bcrypt

from blog_app.data import db


bcrypt = Bcrypt()


def save(model):
    """
    saves the given model to a database
    :param model:
    :return:
    """
    db.session.add(model)
    db.session.commit()
    db.session.refresh(model)


def delete(model):
    """
    deletes a given model to a database
    :param model:
    :return:
    """
    db.session.delete(model)
    db.session.commit()
