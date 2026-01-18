from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    email: str | None
    provider: str
    provider_id: str

    class Config:
        from_attributes = True
