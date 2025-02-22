from pydantic import BaseModel, EmailStr, ConfigDict


class StreamUserRequest(BaseModel):
    userId: str
    name: str
    image: str
    email: EmailStr


class StreamUserResponse(BaseModel):
    token: str

    model_config = ConfigDict(from_attributes=True)
