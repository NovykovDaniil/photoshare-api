import random
import time
from datetime import timedelta
from enum import Enum as PyEnum

from sqlalchemy import Column, String, Boolean, Table, Integer, Float, Enum, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base


def generate_id():
    timestamp = int(time.time() * 1000)  # Get current timestamp in milliseconds
    random_num = random.randint(1000, 9999)  # Generate a random 4-digit number
    id_ = str(timestamp) + str(random_num)  # Concatenate timestamp and random number
    return str(id_)


Base = declarative_base()


tag_photo_association = Table(
    "tag_photo_association",
    Base.metadata,
    Column("tag_id", Integer, ForeignKey("tags.id")),
    Column("photo_id", Integer, ForeignKey("photos.id", ondelete="CASCADE")),
)



class UserRole(PyEnum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=generate_id, unique=True)
    username = Column(String(64), unique=True)
    bio = Column(String, nullable=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    photo_count = Column(Integer, default=0, nullable=False)
    subscriptions = Column(Integer, default=0)
    subscribers = Column(Integer, default=0)
    reset_code = Column(Integer, nullable=True)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(String, primary_key=True, default=generate_id, unique=True)
    name = Column(String(32), nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())
    photos = relationship("Photo", secondary=tag_photo_association, back_populates="tags", viewonly=True)


class Estimate(Base):
    __tablename__ = "estimates"
    id = Column(String, primary_key=True, default=generate_id, unique=True)
    estimate = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    photo_id = Column("photo_id", ForeignKey("photos.id", ondelete="CASCADE"))
    user_id = Column("user_id", ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", backref="estimates", viewonly=True)


class Comment(Base):
    __tablename__ = "comments"
    id = Column(String, primary_key=True, default=generate_id, unique=True)
    text = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=None, nullable=True)
    photo_id = Column("photo_id", ForeignKey("photos.id", ondelete="CASCADE"))
    user_id = Column("user_id", ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", backref="comments", viewonly=True)
    photo = relationship("Photo", backref="comments_", viewonly=True)



class Photo(Base):
    __tablename__ = "photos"
    id = Column(String, primary_key=True, default=generate_id, unique=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    user_id = Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), default=None, nullable=False)
    url = Column(String, default=None, nullable=True)
    qr_code = Column(String, default=None, nullable=True)
    user = relationship("User", backref="photos", viewonly=True)
    tags = relationship("Tag", secondary=tag_photo_association, back_populates="photos", passive_deletes=True)
    comments = relationship("Comment", backref="photos", overlaps="comments_,photo", passive_deletes=True)
    filename = Column(String, nullable=True)
    filtername = Column(String, default="Default")
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    rating = Column(Float, nullable=True, default=None)


class Story(Base):
    __tablename__ = "stories"
    id = Column(String, primary_key=True, default=generate_id, unique=True)
    url = Column(String, default=None, nullable=True)
    user_id = Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), default=None, nullable=False)
    created_at = Column(DateTime, default=func.now())
    expire_to = Column(DateTime, default=func.now() + timedelta(hours=24))


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(String, primary_key=True, default=generate_id, unique=True)
    subscriber_id = Column("subscriber_id", ForeignKey("users.id", ondelete="CASCADE"), default=None, nullable=False)
    author_id = Column(String, nullable=False)
    





