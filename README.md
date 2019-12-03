# Introduction
I developed this web application as an assignment that provides JSON REST endpoints for a blog application using technologies that I have chosen.
I wrote this service using Python 3.6 with the popular Flask web framework and SQLAlchemy ORM. For simplicity I use an internal SQLite database. The application uses JSON web tokens for authentication.

For details about the stack see the blog_app/setup.py file.
# How to run the application

  - create and source a virtual environment
  - install all dependencies with `pip install -e .`
  - create the database with running the `scripts/initdb.py` script
  - run the application with `FLASK_APP=my_app.py` flask run command
  