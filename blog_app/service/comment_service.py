from blog_app.data import db, Comment


def get_all_comments():
    return db.session.query(Comment).all()


def get_comments_by_blog_id(blog_id):
    return db.session.query(Comment).filter(Comment.blog_id == blog_id).all()


def create_comment(content, user_id, blog_id):
    return Comment(
        content=content,
        user_id=user_id,
        blog_id=blog_id
    )
