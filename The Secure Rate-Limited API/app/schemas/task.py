from pydantic import BaseModel, Field, field_validator

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)

    @field_validator("title")
    @classmethod
    def clean_title(cls, v: str) -> str:
        return v.strip()

    @field_validator("description")
    @classmethod
    def clean_desc(cls, v: str | None) -> str | None:
        return v.strip() if isinstance(v, str) else v

class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None

    class Config:
        from_attributes = True
