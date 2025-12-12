from fastapi import APIRouter, HTTPException,status
from typing import List

from fastapi.params import Depends

from field_task.auth.models.user_model import UserModel
from field_task.task.models.task_model import TaskModel
from field_task.task.schemas.task_schemas import TaskCreate, TaskUpdate, TaskResponse
from field_task.utils.user_info import get_user_info

router = APIRouter(prefix="/tasks", tags=["tasks"])

# GET all tasks
@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_tasks(skip: int = 0, limit: int = 10):
    
    """
    Get all tasks with pagination
    """
    response=[]

    tasks = await TaskModel.find_all().skip(skip).limit(limit).to_list()

    for task in tasks:
        task_dict = {}
        db_user=await UserModel.get(task.agent_id)
        task_dict["id"]=task.id
        task_dict["tittle"]=task.tittle
        task_dict["longi"]=task.longi
        task_dict["lati"]=task.lati
        task_dict["agent_id"]=task.agent_id
        task_dict["task_status"]=task.task_status
        task_dict["parent_id"]=task.parent_id
        task_dict["created_at"]=task.created_at
        task_dict["updated_at"]=task.updated_at
        task_dict["agent_name"]=db_user.first_name
        response.append(task_dict)


    return response

# GET task by ID
@router.get("/{id}", response_model=TaskResponse,status_code=status.HTTP_200_OK)
async def get_task(id: str):
    
    """
    Get task by ID
    """
    task = await TaskModel.get(id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task is not found")
    return task


# GET task by UserID
@router.get("/user/{id}", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
async def get_task_by_uid(id: str):
    """
    Get task by ID
    """
    db_user=await UserModel.get(id)

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    tasks = await TaskModel.find(TaskModel.agent_id==id).to_list()

    return tasks




# GET task by UserID
@router.get("/users/my-task", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
async def get_task_token(user_data:dict=Depends(get_user_info)):
    """
    Get task by ID
    """
    id=user_data["user_id"]
    db_user=await UserModel.get(id)

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    tasks = await TaskModel.find(TaskModel.agent_id==id).to_list()

    return tasks


# POST create new task
@router.post("/", response_model=TaskResponse,status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreate):
    
    """
    Create a new task
    """
    task_dict = task_data.model_dump()
    task = TaskModel(**task_dict)
    await task.create()
    return task

# PATCH update task
@router.patch("/{id}", response_model=TaskResponse,status_code=status.HTTP_200_OK)
async def update_task(id: str, task_data: TaskUpdate):
    
    """
    Update task information
    """
    task = await TaskModel.get(id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    update_data = task_data.model_dump(exclude_unset=True)
    await task.update({"$set": update_data})
    return await TaskModel.get(id)

# DELETE task
@router.delete("/{id}",status_code=status.HTTP_200_OK)
async def delete_task(id: str):
    
    """
    Delete task by ID
    """
    task = await TaskModel.get(id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    await task.delete()
    return {"message": "Task deleted successfully"}


# DELETE all tasks
@router.delete("/delete/all", status_code=status.HTTP_200_OK)
async def delete_all_tasks():
    """
    Delete all tasks from the database.
    """

    delete_result = await TaskModel.delete_all()


    if delete_result.deleted_count == 0:

        return {"message": "No tasks found to delete. The collection was already empty."}

    return {
        "message": f"Successfully deleted {delete_result.deleted_count} tasks."
    }