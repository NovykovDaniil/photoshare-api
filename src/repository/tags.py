from sqlalchemy.orm import Session

from src.database.models import Tag
from src.schemas import TagModel


async def create_tag(body: TagModel, db: Session) -> Tag:
    tag = Tag(name=body.tag)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


async def is_exists(body: TagModel, db: Session) -> Tag:
    tag = db.query(Tag).filter(Tag.name == body.tag).first()
    return True if tag else False