from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from models.project import Project, Status
import schemas.project_schema


def create_project(db: Session, project: schemas.project_schema.ProjectCreate):
    project_db = Project(client_id=project.client_id, name=project.name, start_date=project.start_date, end_date=project.end_date, hourly_rate=project.hourly_rate, fixed_price=project.fixed_price)
    db.add(project_db)
    db.commit()
    db.refresh(project_db)
    return project_db

def update_projects(db: Session, project_id: int, project: schemas.project_schema.ProjectUpdate):
    project_db = db.query(Project).filter(Project.id == project_id).first()

    if project_db:
        update_data = project.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(project_db, key, value)
        
        db.commit()
        db.refresh(project_db)

    return project_db

def update_project_status(db: Session, project_id: int, status: Status) -> Project | None:
    project = db.get(Project, project_id)
    if not project:
        return None
    
    project.state = status
    db.commit()
    db.refresh(project)
    return project

def delete_project(db: Session, project_id: int) -> bool:
    project_db = db.query(Project).filter(Project.id == project_id).first()

    if project_db:
        db.delete(project_db)
        db.commit()
        return True
    
    return False


def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

def get_projects(db: Session, skip: int = 0, limit:int = 100):
    return db.query(Project).offset(skip).limit(limit).all()

def get_all_active_projects(db: Session):
    return db.query(Project).filter(Project.state == Status.ACTIVE).all()

def get_project_by_client(db: Session, client_id: int):
    return db.query(Project).filter(Project.client_id == client_id).first()

def get_all_projects_with_client(db: Session):
    query = (
        select(Project).options(selectinload(Project.client))
    )
    result = db.scalars(query).all()
    return result

def delete_project(project_id: int, db: Session):
    project_db = db.get(Project, project_id)

    if not project_db:
        return False
    
    db.delete(project_db)
    db.commit()
    return True