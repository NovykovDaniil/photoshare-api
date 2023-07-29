from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from src.database.models import UserRole


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: str
    username: str
    bio: str | None
    email: EmailStr
    role: UserRole = UserRole.USER
    created_at: datetime
    avatar: str
    photo_count: int
    subscriptions: int
    subscribers: int
    confirmed: bool
    is_active: bool

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str


class UserResetPassword(BaseModel):
    email: EmailStr
    reset_code: int
    new_password: str


class UserEditModel(BaseModel):
    username: str
    bio: str


class UserBanModel(BaseModel):
    username: str


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr


class ChangePassword(BaseModel):
    current_password: str
    new_password: str


class TagModel(BaseModel):
    tag: str


class TagDb(BaseModel):
    id: str
    name: str
    created_at: datetime

    class Config:
        orm_mode = True


class TagResponse(BaseModel):
    tag: TagDb
    detail: str = "Tag successfully created"


class PhotoDb(BaseModel):
    id: str
    description: str | None
    created_at: datetime
    user_id: str
    url: str 
    qr_code: str | None
    filename: str
    filtername: str
    width: int 
    height: int 
    rating: float

    class Config:
        orm_mode = True


class PhotoResponse(BaseModel):
    photo: PhotoDb
    detail: str = "Photo successfully processed"


class PhotosResponse(BaseModel):
    photos: List[PhotoDb]
    detail: str


class PhotoEditModel(BaseModel):
    photo_id: str
    description: str


class PhotoTagModel(BaseModel):
    photo_id: str
    tags: List[str]


class PhotoFilterModel(BaseModel):
    photo_id: str
    filtername: str


class PhotoHandleModel(BaseModel):
    photo_id: str


class PhotoQrResponse(BaseModel):
    photo_id: str
    url: str
    qrcode: str


class CommentModel(BaseModel):
    photo_id: str
    text: str


class CommentDb(BaseModel):
    id: str
    text: str
    created_at: datetime
    updated_at: datetime | None
    photo_id: str
    user_id: str

    class Config:
        orm_mode = True


class CommentResponse(BaseModel):
    comment: CommentDb
    detail: str


class CommentsResponse(BaseModel):
    comments: List[CommentDb]
    detail: str


class CommentEditModel(BaseModel):
    comment_id: str
    new_text: str


class CommentHandleModel(BaseModel):
    comment_id: str


class EstimateModel(BaseModel):
    photo_id: str
    estimate: int = Field(ge=1, le=5)


class EstimateDb(BaseModel):
    id: str
    estimate: int
    created_at: datetime
    photo_id: str
    user_id: str

    class Config:
        orm_mode = True


class EstimateResponse(BaseModel):
    estimate: EstimateDb
    detail: str


class EstimatesResponse(BaseModel):
    estimates: List[EstimateDb]
    detail: str


class EstimateDeleteModel(BaseModel):
    estimate_id: str


class StoryIdModel(BaseModel):
    story_id: str
    

class StoryDb(BaseModel):
    id: str
    url: str
    user_id: str
    created_at: datetime
    expire_to: datetime

    class Config:
        orm_mode = True


class StoryResponse(BaseModel):
    story: StoryDb
    detail: str


class StoriesResponse(BaseModel):
    stories: List[StoryDb]
    detail: str


class SubscriptionDb(BaseModel):
    id: str
    subscriber_id: str
    author_id: str

    class Config:
        orm_mode = True


class SubscriptionResponse(BaseModel):
    subscription: SubscriptionDb
    detail: str


class SubscriptionsResponse(BaseModel):
    subscriptions: List[SubscriptionDb]
    detail: str


class ChatModel(BaseModel):
    interlocutor_id: str


class ChatDb(BaseModel):
    id: str
    interlocutor_1: str
    interlocutor_2: str
    created_at: datetime

    class Config:
        orm_mode = True


class ChatResponse(BaseModel):
    chat: ChatDb
    detail: str


class MessageModel(BaseModel):
    chat_id: str
    text: str


class MessageDb(BaseModel):
    id: str
    text: str
    sender: str
    recipient: str
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True

    
class MessageResponse(BaseModel):
    message: MessageDb
    detail: str


class MessageEditModel(BaseModel):
    message_id: str
    text: str


class MessagesResponse(BaseModel):
    messages: List[MessageDb]
    detail: str