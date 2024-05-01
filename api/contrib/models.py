from uuid import uuid4
from sqlalchemy import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as pgUUID


class BaseModel(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(pgUUID(as_uuid=True), nullable=False, default=uuid4)
