from blog_app.data import db, Comment


def get_all_comments():
    """
    returns every comment from our applications
    :return: every comment from our applications
    """
    return db.session.query(Comment).all()


def get_comments_by_blog_id(blog_id):
    """
    Returns Returns every comments from our application with the given given
    blog ID
    :param blog_id: The blog's ID
    :return: every comments from our application with the given given blog ID
    """
    return db.session.query(Comment).filter(Comment.blog_id == blog_id).all()


def get_comment_by_id(comment_id):
    """
    Returns the comment from our applications with the given ID
    :param comment_id: The comment's ID to return
    :return: the comment from our applications with the given ID
    """
    return db.session.query(Comment).filter(Comment.id == comment_id).first()


def create_comment(content, user_id, blog_id):
    """
    creates a new comment with the given parameters
    :param content: the given content
    :param user_id: the actual user's ID
    :param blog_id: the given blog ID
    :return: the created comment
    """
    return Comment(
        content=content,
        user_id=user_id,
        blog_id=blog_id
    )


def update_comment_in_db(comment, data):
    """
    Update a comment in our database with the given data
    :param comment: the comment to update
    :param data: the given data
    :return: the updated comment
    """
    comment.content = data["content"]
    db.session.commit()
    db.session.refresh(comment)
