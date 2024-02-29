import uuid
from datetime import datetime

import shortuuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime

from .base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    token = Column(String, nullable=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    @property
    def short_id(self):
        return shortuuid.encode(self.id)

    def to_json(self) -> dict:
        return {
            "id": self.short_id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }
