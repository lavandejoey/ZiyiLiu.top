#!/usr/bin/env python
# blogs.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2021-2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "lavandejoey"
__email__ = "lavandejoey@outlook.com"

# standard library
# 3rd party packages
from sqlalchemy import Column, Integer, String, DateTime, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship

# local source
from app import db


class Blogs(db.Model):
    __tablename__ = "Blogs"
    blog_id = Column("blog_id", Integer, primary_key=True)
    blog_cate_id = Column("blog_cate_id", Integer)
    blog_title = Column("blog_title", Integer)
    blog_date = Column("blog_date", DateTime)
    blog_like_cnt = Column("blog_like_cnt", Integer)
    blog_com_cnt = Column("blog_com_cnt", Integer)
    blog_file_path = Column("blog_file_path", VARCHAR)
    blogscate_cate_id = Column("BlogsCate_cate_id", Integer, ForeignKey("BlogsCate.cate_id"))

    blogscate = relationship("Blogscate", foreign_keys=blogscate_cate_id)


# The table saves the record of comments on blogs
class Blogscomments(db.Model):
    __tablename__ = "BlogsComments"
    com_usr_id = Column("com_usr_id", Integer, primary_key=True)
    com_blog_id = Column("com_blog_id", Integer, primary_key=True)
    com_datetime = Column("com_datetime", DateTime, primary_key=True)
    # Unknown SQL type: "longtext"
    com_content = Column("com_content", String)


# The table saves the record of like on blogs
class Blogslikes(db.Model):
    __tablename__ = "BlogsLikes"
    like_usr_id = Column("like_usr_id", Integer, primary_key=True)
    like_blogs_id = Column("like_blogs_id", Integer, primary_key=True)
    like_date = Column("like_date", DateTime)


# The table saves one of the categories of blogs
class Blogscate(db.Model):
    __tablename__ = "BlogsCate"
    cate_id = Column("cate_id", Integer, primary_key=True)
    cate_name = Column("cate_name", Integer)
