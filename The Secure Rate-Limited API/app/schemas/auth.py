from pydantic import BaseModel, EmailStr, Field, field_validator

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

    @field_validator("password")
    @classmethod
    def validate_password_bytes(cls, v: str) -> str:
        v = v.strip()
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password exceeds bcrypt 72-byte limit.")
        return v

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True