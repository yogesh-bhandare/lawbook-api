from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone
from src.db.connect import Base


# Cases Model
class Case(Base):
    __tablename__ = "cases"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    case_id = Column(String(120), unique=True, nullable=False)
    url = Column(String, unique=True, nullable=False)
    img_url = Column(String, nullable=True)
    title = Column(String(240), nullable=False, unique=True)
    content = Column(String, nullable=False)
    summary = Column(String, nullable=True)
    documents = Column(String, nullable=True)
    category = Column(String, nullable=True)
    created_at = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Case(id={self.id}, case_id={self.case_id}, title={self.title}, category={self.category})>"
