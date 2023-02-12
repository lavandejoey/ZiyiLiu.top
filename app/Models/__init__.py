#!/usr/bin/env python
# __init__.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2021-2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "lavandejoey"
__email__ = "lavandejoey@outlook.com"

# standard library
# 3rd party packages
# local source
from app.Models.admin import Users

"""
class UsersBlogs(db.Model):
    __tablename__ = "Users_Blogs"
    users_usr_id = Column("Users_usr_id", Integer, ForeignKey("Users.usr_id"), primary_key=True)
    blogs_blog_id = Column("Blogs_blog_id", Integer, ForeignKey("Blogs.blog_id"), primary_key=True)

    users = relationship("Users", foreign_keys=users_usr_id)
    blogs = relationship("Blogs", foreign_keys=blogs_blog_id)


class BlogscommentsBlogs(db.Model):
    __tablename__ = "BlogsComments_Blogs"
    blogscomments_com_usr_id = Column("BlogsComments_com_usr_id", Integer, ForeignKey("BlogsComments.com_usr_id"),
                                      primary_key=True)
    blogscomments_com_blog_id = Column("BlogsComments_com_blog_id", Integer, ForeignKey("BlogsComments.com_blog_id"),
                                       primary_key=True)
    blogscomments_com_datetime = Column("BlogsComments_com_datetime", DateTime,
                                        ForeignKey("BlogsComments.com_datetime"), primary_key=True)
    blogs_blog_id = Column("Blogs_blog_id", Integer, ForeignKey("Blogs.blog_id"), primary_key=True)

    blogs = relationship("Blogs", foreign_keys=blogs_blog_id)


class BlogsBlogslikes(db.Model):
    __tablename__ = "Blogs_BlogsLikes"
    blogs_blog_id = Column("Blogs_blog_id", Integer, ForeignKey("Blogs.blog_id"), primary_key=True)
    blogslikes_like_usr_id = Column("BlogsLikes_like_usr_id", Integer, ForeignKey("BlogsLikes.like_usr_id"),
                                    primary_key=True)
    blogslikes_like_blogs_id = Column("BlogsLikes_like_blogs_id", Integer, ForeignKey("BlogsLikes.like_blogs_id"),
                                      primary_key=True)

    blogs = relationship("Blogs", foreign_keys=blogs_blog_id)


class UsersBlogscomments(db.Model):
    __tablename__ = "Users_BlogsComments"
    users_usr_id = Column("Users_usr_id", Integer, ForeignKey("Users.usr_id"), primary_key=True)
    blogscomments_com_usr_id = Column("BlogsComments_com_usr_id", Integer, ForeignKey("BlogsComments.com_usr_id"),
                                      primary_key=True)
    blogscomments_com_blog_id = Column("BlogsComments_com_blog_id", Integer, ForeignKey("BlogsComments.com_blog_id"),
                                       primary_key=True)
    blogscomments_com_datetime = Column("BlogsComments_com_datetime", DateTime,
                                        ForeignKey("BlogsComments.com_datetime"), primary_key=True)

    users = relationship("Users", foreign_keys=users_usr_id)


class BlogslikesUsers(db.Model):
    __tablename__ = "BlogsLikes_Users"
    blogslikes_like_usr_id = Column("BlogsLikes_like_usr_id", Integer, ForeignKey("BlogsLikes.like_usr_id"),
                                    primary_key=True)
    blogslikes_like_blogs_id = Column("BlogsLikes_like_blogs_id", Integer, ForeignKey("BlogsLikes.like_blogs_id"),
                                      primary_key=True)
    users_usr_id = Column("Users_usr_id", Integer, ForeignKey("Users.usr_id"), primary_key=True)

    users = relationship("Users", foreign_keys=users_usr_id)
"""
