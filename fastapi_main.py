from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID,uuid4

app = FastAPI()

class Task(BaseModel):
    id : Optional[UUID] = None
    title : str
    description : Optional[str] = None
    complete : bool = False

tasks = []

@app.post("/tasks/",response_model=Task)

def create_task(task: Task):
    task.id = uuid4()
    tasks.append(task)
    return task
@app.get("/tasks/", response_model=List[Task])
def read_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: UUID):
    for task in tasks:
        if task.id == task_id:
            return task
        
    return HTTPException(status_code=404, detail ="task not found")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, task_update: Task):
    for idx, task in enumerate(tasks) :
        if task.id == task_id:
            updated_task = task.copy(update=task_update.dict (exclude_unset=True) )
            tasks[idx] = update_task
            return update_task
        
    raise HTTPException(status_code=404, detail="task is not found")


@app.delete("/tsks/{task_id}" ,response_model=Task)
def delete_task(task_id: UUID):
    for idx, task in enumerate(tasks) :
        if task.id == task_id:
            return tasks.pop(idx)
        
    raise HTTPException(status_code=404, detail="task is not found")
    
                        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
