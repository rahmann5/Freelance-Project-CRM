from sqlalchemy.orm import Session
from models.task import Task, Status
import schemas.task_schema

def create_task(db: Session, task: schemas.task_schema.TaskCreate):
    task_db = Task(project_id=task.project_id, title=task.title, description=task.description, status=task.status, estimated_hours=task.estimated_hours, actual_hours=task.actual_hours)
    db.add(task_db)
    db.commit()
    db.refresh(task_db)
    return task_db

def update_task(db: Session, task_id: int, task: schemas.task_schema.TaskUpdate):
    task_db = db.query(Task).filter(task_id == Task.id).first()

    if not task_db:
        return None

    task_update = task.model_dump(exclude_unset=True)
    for key, value in task_update.items():
        setattr(task_db, key, value)
    db.commit()
    db.refresh(task_db)

    return task_db 

def update_task_status(db: Session, task_id: int, status: Status):
    task_db = db.query(Task).filter(task_id == Task.id).first()

    if not task_db:
        return None

    task_db.status = status
    db.commit()
    db.refresh(task_db)
    return task_db

def list_task_by_status(db: Session, status: str):  
    task_db = db.query(Task).filter(Task.status == status).all()

    output = []
    for task in task_db:
        output.append({
            "id": task.id,
            "project_id": task.project_id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "estimated_hours": task.estimated_hours,
            "actual_hours": task.actual_hours,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        })

    return output
