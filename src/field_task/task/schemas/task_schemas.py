from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for creating new Task
class TaskCreate(BaseModel):
    tittle: str
    longi: str
    lati: str
    agent_id: str
    parent_id: str

# Schema for updating Task
class TaskUpdate(BaseModel):
    tittle: Optional[str] = None
    longi: Optional[str] = None
    lati: Optional[str] = None
    agent_id: Optional[str] = None
    task_status: Optional[str] = None
    parent_id: Optional[str] = None

# Schema for Task response
class TaskResponse(BaseModel):
    id: str
    tittle: str
    longi: str
    lati: str
    agent_id: str
    task_status: str
    parent_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
