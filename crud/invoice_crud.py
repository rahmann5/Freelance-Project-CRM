from sqlalchemy.orm import Session
from models.invoice import Invoice, Status
import schemas.invoices_schema

def create_invoice(db: Session, invoice: schemas.invoices_schema.InvoiceCreate):
    invoice_db = Invoice(client_id=invoice.client_id, project_id=invoice.project_id, issue_date=invoice.issue_date, total_amount=invoice.total_amount, status=invoice.status, due_date=invoice.due_date)
    db.add(invoice_db)
    db.commit()
    db.refresh(invoice_db)
    return invoice_db

def update_invoice(db: Session, invoice_id: int, invoice: schemas.invoices_schema.InvoiceUpdate):
    invoice_db = db.query(Invoice).filter(invoice_id == Invoice.id).first()

    if not invoice_db:
        return None
    
    invoice_update = invoice.model_dump(exclude_unset=True)
    for key, value in invoice_update.items():
        setattr(invoice_db, key, value)

    db.commit()
    db.refresh(invoice_db)
    return invoice_db

def list_invoice_by_status(db: Session, status: Status):
    return db.query(Invoice).filter(Invoice.status == status).all()