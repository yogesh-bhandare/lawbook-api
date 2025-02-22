from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum
from uuid import UUID


class CasesCategory(str, Enum):
    GENERAL = "General"
    LEGAL = "Legal"
    FINANCIAL = "Financial"
    TECHNICAL = "Technical"


class CasesBaseSchema(BaseModel):
    case_id: str
    url: str
    img_url: str
    title: str
    content: str
    summary: str
    documents: str
    category: str


class CasesCreateSchema(CasesBaseSchema):
    pass


class CasesUpdateSchema(CasesBaseSchema):
    pass


class CasesResponseSchema(CasesBaseSchema):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
