from blog_app.data import Like, db


def create_like(user_id, blog_id):
    """
    creates a new like
    :param user_id: the user's ID
    :param blog_id: the blog's ID
    :return:  the created like
    """
    return Like(
        user_id=user_id,
        blog_id=blog_id
    )


def check_like(act_user_id, blog_id):
    """
    checks the like in our database
    :param act_user_id: the user's ID
    :param blog_id: the blog's ID
    :return: the like
    """
    return db.session.query(Like).filter(Like.user_id == act_user_id,
                                         Like.blog_id == blog_id).first()
