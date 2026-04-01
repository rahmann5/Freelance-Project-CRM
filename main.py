from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import crud.client_crud, crud.invoice_crud, crud.project_crud, crud.task_crud
import schemas.client_schema, schemas.invoices_schema, schemas.task_schema, schemas.project_schema
from database import SessionLocal

app = FastAPI(title="Freelance Project CRM")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CLIENT ROUTES
@app.post("/client/create/", response_model=schemas.client_schema.ClientCreate)
def create_client(client: schemas.client_schema.ClientCreate, db: Session = Depends(get_db)):
        new_client = crud.client_crud.create_client(db, client=client)

        if not new_client:
                raise HTTPException(status_code=400, detail="Failed to create a new project")

        return new_client

@app.post("/client/update/{client_id}", response_model=schemas.client_schema.ClientRead)
def update_client(client_id: int, client: schemas.client_schema.ClientUpdate, db: Session = Depends(get_db)):
        updated_client = crud.client_crud.update_client(db, client_id=client_id, client=client)

        if not updated_client:
                raise HTTPException(status_code=400, detail=f"Failed to update the project {client_id}")
        
        return updated_client

@app.get("/client/active", response_model=List[schemas.client_schema.ClientRead])
def get_active_clients(db: Session = Depends(get_db)):
        active_clients = crud.client_crud.get_all_active_clients(db=db)

        if not active_clients:
                raise HTTPException(status_code=404, detail="No active clients found")
        
        return active_clients

@app.get("/client/total_invoice/{client_id}", response_model=schemas.client_schema.ClientWithInvoiceTotal)
def get_client_with_total_invoice(client_id: int, db: Session = Depends(get_db)):
        client_db = crud.client_crud.get_client_with_total_invoice(db, client_id=client_id)

        if not client_db:
                raise HTTPException(status_code=404, detail=f"No clients found with id: {client_id}")

        return client_db

@app.get("/client/total_unpaid_invoice/{client_id}", response_model=schemas.client_schema.ClientWithUnpaidInvoiceTotal)
def get_client_with_total_unpaid_invoice(client_id: int, db: Session = Depends(get_db)):
        client_db = crud.client_crud.get_client_with_total_unpaid_invoice(db=db, client_id=client_id)

        if not client_db:
                raise HTTPException(status_code=404, detail=f"No clients found with id: {client_id}")

        return client_db

@app.get("/client/{client_id}/projects", response_model=schemas.client_schema.ClientWithProjects)
def get_client_with_projects(client_id: int, db: Session = Depends(get_db)):
        client_db = crud.client_crud.get_client_with_projects(db=db, client_id=client_id)
        
        if not client_db:
                raise HTTPException(status_code=404, detail=f"No clients found with id: {client_id}") 
        
        return client_db


#PROJECT ROUTES
@app.post("/project/create/", response_model=schemas.project_schema.ProjectCreate)
def create_project(project: schemas.project_schema.ProjectCreate, db: Session = Depends(get_db)):
        project_db = crud.project_crud.create_project(db=db, project=project)

        if not project_db:
                raise HTTPException(status_code=400, detail="Failed to create a new project")
        
        return project_db

@app.post("/project/update/{project_id}", response_model=schemas.project_schema.ProjectUpdate)
def update_project(project_id: int, project: schemas.project_schema.ProjectUpdate, db: Session = Depends(get_db)):
        project_db = crud.project_crud.update_projects(db=db, project_id=project_id, project=project)
                
        if not project_db:
                raise HTTPException(status_code=404, detail=f"No project found with id: {project_id}") 

        return project_db

@app.get("/project/by_client/{client_id}", response_model=schemas.project_schema.ProjectRead)
def get_client_by_id(client_id: int, db: Session = Depends(get_db)):
        project_db=crud.project_crud.get_project_by_client(db=db, client_id=client_id)

        if project_db is None:
                raise HTTPException(status_code=404, detail=f"No project exists for client with id: {client_id}")
        
        return project_db

@app.get("/project/all_with_clients/", response_model=List[schemas.project_schema.ProjectRead])
def get_projects_with_clients(db: Session = Depends(get_db)):
        project_db = crud.project_crud.get_all_projects_with_client(db=db)
        
        if not project_db:
                raise HTTPException(status_code=404, detail=f"No projects were retrieved")

        return project_db

@app.get("/project/all_active/", response_model=List[schemas.project_schema.ProjectRead])
def get_all_active_projects(db: Session = Depends(get_db)):
        project_db = crud.project_crud.get_all_active_projects(db=db)

        if not project_db:
                raise HTTPException(status_code=404, detail=f"No projects were retrieved")
        
        return project_db

@app.delete("/project/{project_id}/delete/", response_model=bool)
def delete_project(project_id: int, db: Session = Depends(get_db)):
        project_db = crud.project_crud.delete_project(project_id=project_id, db=db)

        if project_db is None:
                raise HTTPException(status_code=404, detail=f"No project exists with id: {project_id}")
                
        return project_db

#TASK ROUTES
@app.post("/task/create/", response_model=schemas.task_schema.TaskCreate)
def create_task(task: schemas.task_schema.TaskCreate, db: Session = Depends(get_db)):
        task_db = crud.task_crud.create_task(db=db, task=task)

        if not task_db:
                raise HTTPException(status_code=400, detail="Failed to create a new task")
        
        return task_db

@app.post("/task/update_status/{task_id}", response_model=schemas.task_schema.TaskUpdate)
def update_task_status(task_id: int, task: schemas.task_schema.TaskUpdate, db: Session = Depends(get_db)):
        task_db = crud.task_crud.update_task(db=db, task_id=task_id, task=task)
        
        if not task_db:
                raise HTTPException(status_code=404, detail=f"No task exists with id: {task_id}")

        return task_db

@app.get("/task/list_by_status/{status}", response_model=List[schemas.task_schema.TaskRead])
def list_task_by_status(status: str, db: Session = Depends(get_db)):
        task_db = crud.task_crud.list_task_by_status(db=db, status=status)
        
        if not task_db:
                raise HTTPException(status_code=400, detail=f"No tasks were retrieved")

        return task_db

#INVOICE ROUTES
@app.post("/invoice/create/", response_model=schemas.invoices_schema.InvoiceCreate)
def create_invoice(invoice: schemas.invoices_schema.InvoiceCreate, db: Session = Depends(get_db)):
        invoice_db = crud.invoice_crud.create_invoice(db=db, invoice=invoice)

        if not invoice_db:
                raise HTTPException(status_code=400, detail=f"No invoice could be created")

        return 

@app.get("/invoice/list_by/{status}", response_model=List[schemas.invoices_schema.InvoiceRead])
def list_overdue_invoices(status: str, db: Session = Depends(get_db)):
        invoice_db = crud.invoice_crud.list_invoice_by_status(db=db, status=status)
        
        if not invoice_db:
                raise HTTPException(status_code=400, detail=f"No invoices were retrieved")
        
        return invoice_db