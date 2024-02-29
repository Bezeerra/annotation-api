import uuid
from datetime import datetime

import shortuuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Annotation(Base):
    __tablename__ = "annotations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    user = relationship("User")

    @property
    def short_id(self):
        return shortuuid.encode(self.id)

    def to_json(self) -> dict:
        return {
            "id": self.short_id,
            "user_id": shortuuid.encode(self.user_id),
            "title": self.title,
            "text": self.text,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

