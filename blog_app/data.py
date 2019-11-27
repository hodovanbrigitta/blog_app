from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AppUser(db.Model):
    __tablename__ = 'app_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_username = db.Column(db.String, unique=True, nullable=False)
    user_password = db.Column(db.String, nullable=False)

    blogs = db.relationship("Blog", back_populates="app_user")

    comments = db.relationship("Comment", back_populates="app_user")

    likes = db.relationship("Like", back_populates="app_user")


class Blog(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'))
    app_user = db.relationship("AppUser", back_populates="blogs")

    comments = db.relationship("Comment", back_populates="blog")

    likes = db.relationship("Like", back_populates="blog")


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'))
    app_user = db.relationship("AppUser", back_populates="comments")

    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    blog = db.relationship("Blog", back_populates="comments")


class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'))
    app_user = db.relationship("AppUser", back_populates="likes")

    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    blog = db.relationship("Blog", back_populates="likes")


