from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for creating new CompleteTask
class CompletetaskCreate(BaseModel):
    task_id: str
    agent_id:str


# Schema for updating CompleteTask
class CompletetaskUpdate(BaseModel):
    task_id: Optional[str] = None

# Schema for CompleteTask response
class CompletetaskResponse(BaseModel):
    id: str
    task_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
