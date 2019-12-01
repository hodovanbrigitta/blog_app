from blog_app.data import Like, db


def create_like(user_id, blog_id):
    return Like(
        user_id=user_id,
        blog_id=blog_id
    )


def check_like(act_user_id, blog_id):
    return db.session.query(Like).filter(Like.user_id == act_user_id,
                                         Like.blog_id == blog_id).first()
