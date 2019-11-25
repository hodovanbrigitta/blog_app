import setuptools

setuptools.setup(
    name="blog_app",
    version="0.0.01",
    author="Brigitta Hodovan",
    author_email="hodovan.brigitta@gmail.com",
    description="An awesome blog app",
    url="http://127.0.0.1:5000/",
    packages=setuptools.find_packages(),
    install_requires=[
        'flask==1.1.*',
        'Flask-SQLAlchemy==2.4.*'
    ],
    classifiers=(
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ),
)
