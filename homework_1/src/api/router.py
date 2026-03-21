from fastapi import APIRouter, Response, status, Depends
from fastapi.responses import JSONResponse

from schemas import AddTask, UpdateTask
from service import TaskService

router = APIRouter(prefix= "/tasks", tags=["Tasks"])

@router.post("/", status_code = 201)
def add_task(response: Response, task: AddTask, service: TaskService = Depends()):
    add_result = service.add_task(task)
    response.status_code = status.HTTP_201_CREATED
    return {"message": "Task added", "task": add_result}

@router.get("/", status_code = status.HTTP_200_OK)
def get_all_tasks(service: TaskService = Depends()) -> JSONResponse:
    get_result = service.get_all_tasks()
    if not get_result:
        return JSONResponse({
            "status": "error",
            "message": "No tasks found"
        }, status.HTTP_404_NOT_FOUND)
        
    return get_result

@router.get("/{task_id}", status_code = status.HTTP_200_OK)
def get_task_by_id(task_id: int, service: TaskService = Depends()):
    get_result = service.get_task_by_id(task_id)
    return get_result

@router.patch("/{task_id}", status_code = status.HTTP_200_OK)
def update_task_by_id(task_id: int, task_update: UpdateTask, service: TaskService = Depends()):
    update_result = service.update_specific_task(task_id, task_update)
    return {"message": "Task updated", "task": update_result}


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task_by_id(task_id: int, service: TaskService = Depends()):
    del_result = service.delete_task_by_id(task_id)
    return {"message": "Task deleted", "task": del_result}