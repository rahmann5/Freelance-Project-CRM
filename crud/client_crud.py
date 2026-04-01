from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload
from models.client import Client
from models.invoice import Invoice, Status
import schemas.client_schema

def create_client(db: Session, client: schemas.client_schema.ClientCreate):
    client_db = Client(name=client.name, email=client.email, phone=client.phone, company_name=client.company_name, is_active=client.is_active)
    db.add(client_db)
    db.commit()
    db.refresh(client_db)
    return client_db

def update_client(db: Session, client_id: int, client: schemas.client_schema.ClientUpdate):
    client_db = db.query(Client).filter(client_id == Client.id).first()

    if not client_db:
        return None
    
    client_update = client.model_dump(exclude_unset=True)
    for key, val in client_update.items():
        setattr(client_db, key, val)
    db.commit()
    db.refresh(client_db)
    
    return client_db

def get_client_with_total_invoice(db: Session, client_id: int):
    statement = (
        select(
            Client,
            func.coalesce(func.sum(Invoice.total_amount), 0).label("invoice_total_amount")
        )
        .join(Invoice, Invoice.client_id == Client.id, isouter=True)
        .where(Client.id == client_id)
        .group_by(Client.id)
    )
    result = db.execute(statement).first()
    if not result:
        return None

    client, total_invoice_amount = result
    return schemas.client_schema.ClientWithInvoiceTotal(
        **client.__dict__,
        total_invoice_amount=total_invoice_amount
    )

def get_client_with_total_unpaid_invoice(db: Session, client_id: int):
    statement = (
        select(
            Client,
            func.coalesce(func.sum(Invoice.total_amount), 0).label("unpaid_invoice_total_amount")
        )
        .join(
            Invoice,
            (Invoice.client_id == Client.id) & (Invoice.status != Status.PAID),
            isouter=True
        )
        .group_by(Client.id)
    )

    result = db.execute(statement=statement).first()
    if not result:
        return None
    
    client, total_unpaid_invoice_amount = result
    return schemas.client_schema.ClientWithUnpaidInvoiceTotal(
        **client.__dict__,
        total_unpaid_invoice_amount=total_unpaid_invoice_amount
    )

def get_client_with_projects(db: Session, client_id: int):
    statement = (
        select(
            Client
        )
        .where(Client.id == client_id)
        .options(selectinload(Client.projects))
    )

    result = db.execute(statement=statement).scalar_one_or_none()

    return schemas.client_schema.ClientWithProjects.model_validate(result)
    
def set_client_active_state(db: Session, client_id: int, is_active:bool):
    client = db.get(Client, client_id)

    if client:
        client.is_active = is_active
        db.commit()
        db.refresh(client)
        return True
    return False

def get_all_active_clients(db: Session):
    return db.query(Client).filter(Client.is_active == True).all()

