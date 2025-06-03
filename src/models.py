from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    followers: Mapped[list["Follower"]] = relationship(back_populates="followed", foreign_keys=["Follower.user_to_id"])
    following: Mapped[list["Follower"]] = relationship(back_populates="follower", foreign_keys=["Follower.user_from_id"])
    author: Mapped[list["Comment"]] = relationship(back_populates="author", foreign_keys=["Comment.author_id"])
    user_post: Mapped[list["Post"]] = relationship(back_populates="user", foreign_keys=["Post.user_id"])



    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "user_name": self.user_name    
        }

class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    follower: Mapped["User"] = relationship(back_populates="following", foreign_keys=[user_from_id])
    followed: Mapped["User"] = relationship(back_populates="followers", foreign_keys=[user_to_id])

    def serialize(self):
        return{
            "id": self.id,
        }


class Comment(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(300), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")


    def serialize(self):
        return{
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,  
            "post_id": self.post_id
        }



class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    comments: Mapped[list["Comment"]] = relationship(back_populates="post", foreign_keys=["Comment.post_id"])
    media: Mapped[list["Media"]]= relationship(back_populates="post", foreign_keys=["Media.posted_id"])

    def serialize(self):
        return{
            "id": self.id,
        }




class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(120), nullable=False)
    posted_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="media")
    



    def serialize(self):
        return{
            "id": self.id,
            "url": self.url
        }




