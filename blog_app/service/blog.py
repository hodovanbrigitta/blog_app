from blog_app.data import db, Blog


def get_blog_by_id(blog_id):
    """
    Returns the blog from our applications with the given ID
    :param blog_id: The blog's ID to return
    :return: the blog from our applications with the given ID
    """
    return db.session.query(Blog).filter(Blog.id == blog_id).first()


def update_blog_in_db(blog, data):
    """
    Update a blog in our database
    :param blog: the blog to update
    :param data: the given data
    :return: the updated blog
    """
    blog.title = data["title"]
    blog.content = data["content"]
    db.session.commit()
    db.session.refresh(blog)


def create_blog(title, content, user_id):
    """
    creates a new blog with the given parameters
    :param title: the given title
    :param content: the given content
    :param user_id: the actual user's ID
    :return: the created blog
    """
    return Blog(
        title=title,
        content=content,
        user_id=user_id
    )
