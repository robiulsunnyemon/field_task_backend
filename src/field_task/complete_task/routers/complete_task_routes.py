from fastapi import APIRouter, HTTPException,status
from typing import List

from field_task.auth.models.user_model import UserModel
from field_task.complete_task.models.complete_task_model import CompleteTaskModel
from field_task.complete_task.schemas.complete_task_schemas import CompletetaskCreate, CompletetaskUpdate, CompletetaskResponse
from field_task.task.models.task_model import TaskModel
from field_task.task.schemas.task_schemas import TaskResponse

router = APIRouter(prefix="/complete_tasks", tags=["complete_tasks"])

# GET all complete_tasks
@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_complete_tasks(skip: int = 0, limit: int = 10):
    
    """
    Get all complete_tasks with pagination
    """
    response=[]
    complete_tasks = await CompleteTaskModel.find_all().skip(skip).limit(limit).to_list()
    for complete_task in complete_tasks:
        db_task=await TaskModel.get(complete_task.task_id)
        db_user=await UserModel.get(db_task.agent_id)
        res_dict={}
        res_dict["id"]=complete_task.id
        res_dict["task_id"]=complete_task.task_id
        res_dict["task_name"]=db_task.tittle
        res_dict["agent_id"]=db_task.agent_id
        res_dict["agent_name"]=db_user.first_name
        res_dict["completed_at"]=complete_task.created_at

        response.append(res_dict)

    return response

# GET complete_task by ID
@router.get("/{id}",status_code=status.HTTP_200_OK)
async def get_complete_task(id: str):
    
    """
    Get complete_task by ID
    """
    complete_task = await CompleteTaskModel.get(id)
    if not complete_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CompleteTask not found")

    db_task = await TaskModel.get(complete_task.task_id)
    db_user = await UserModel.get(db_task.agent_id)
    res_dict = {}
    res_dict["id"] = complete_task.id
    res_dict["task_id"] = complete_task.task_id
    res_dict["task_name"] = db_task.tittle
    res_dict["agent_id"] = db_task.agent_id
    res_dict["agent_name"] = db_user.first_name
    res_dict["completed_at"] = complete_task.created_at


    return res_dict


# POST create new complete_task
@router.post("/", response_model=CompletetaskResponse, status_code=status.HTTP_201_CREATED)
async def create_complete_task(complete_task_data: CompletetaskCreate):
    """
    Create a new complete_task
    """
    # Get the task first
    db_task = await TaskModel.get(complete_task_data.task_id)

    # Check if task exists
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {complete_task_data.task_id} not found"
        )

    # Check if the agent is authorized for this task
    if db_task.agent_id != complete_task_data.agent_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,  # Changed to 403 Forbidden
            detail="Agent is not authorized to complete this task"
        )

    # Check if task is already completed
    if db_task.task_status=="complete":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task is already completed"
        )

    # Create the complete task
    complete_task_dict = complete_task_data.model_dump()
    complete_task = CompleteTaskModel(**complete_task_dict)
    db_task.task_status = "complete"
    await db_task.save()
    await complete_task.create()

    # Optional: Update the original task status to completed
    # Uncomment if you want to mark the task as completed in TaskModel
    # await TaskModel.update(complete_task_data.task_id, {"is_completed": True})

    return complete_task


# POST create new complete_task
@router.post("/check-in", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_complete_task(complete_task_data: CompletetaskCreate):
    """
    Create a new complete_task
    """
    # Get the task first
    db_task = await TaskModel.get(complete_task_data.task_id)

    # Check if task exists
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {complete_task_data.task_id} not found"
        )

    # Check if the agent is authorized for this task
    if db_task.agent_id != complete_task_data.agent_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,  # Changed to 403 Forbidden
            detail="Agent is not authorized to complete this task"
        )

    # Check if task is already completed
    if db_task.task_status == "complete":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task is already completed"
        )

    db_task.task_status = "inprogress"
    await db_task.save()

    # Optional: Update the original task status to completed
    # Uncomment if you want to mark the task as completed in TaskModel
    # await TaskModel.update(complete_task_data.task_id, {"is_completed": True})

    return db_task




# PATCH update complete_task
@router.patch("/{id}", response_model=CompletetaskResponse,status_code=status.HTTP_200_OK)
async def update_complete_task(id: str, complete_task_data: CompletetaskUpdate):
    
    """
    Update complete_task information
    """
    complete_task = await CompleteTaskModel.get(id)
    if not complete_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CompleteTask not found")

    update_data = complete_task_data.model_dump(exclude_unset=True)
    await complete_task.update({"$set": update_data})
    return await CompleteTaskModel.get(id)

# DELETE complete_task
@router.delete("/{id}",status_code=status.HTTP_200_OK)
async def delete_complete_task(id: str):
    
    """
    Delete complete_task by ID
    """
    complete_task = await CompleteTaskModel.get(id)
    if not complete_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CompleteTask not found")

    await complete_task.delete()
    return {"message": "CompleteTask deleted successfully"}


# DELETE all complete_tasks
@router.delete("/all", status_code=status.HTTP_200_OK)
async def delete_all_complete_tasks():
    """
    Delete all complete_tasks from the database.
    """

    delete_result = await CompleteTaskModel.delete_all()


    if delete_result.deleted_count == 0:
        return {"message": "No complete tasks found to delete. The collection was already empty."}

    return {
        "message": f"Successfully deleted {delete_result.deleted_count} complete tasks."
    }