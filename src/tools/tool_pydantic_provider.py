from pydantic import BaseModel, Field
from typing import Optional, Any

class CreateTestCase(BaseModel):
    requirement: Optional[str] = Field(description="List of business and technical requirements")