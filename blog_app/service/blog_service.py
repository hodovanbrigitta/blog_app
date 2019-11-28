from blog_app.data import db, Blog


def get_blog_by_id(blog_id):
    return db.session.query(Blog).filter(Blog.id == blog_id).first()


def update_blog_in_db(blog, data):
    blog.title = data["title"]
    blog.content = data["content"]
    db.session.commit()
    db.session.refresh(blog)