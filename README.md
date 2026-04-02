# Freelance Project CRM

A professional-grade Customer Relationship Manager built with **FastAPI** and **SQLAlchemy 2.0**. This project demonstrates database relationships, data validation, and full CRUD (Create, Read, Update, Delete) lifecycles.

## 🚀 Features
* **Relational Database:** Links Client, Projects, Tasks and Invoices in a complex relational model using foreign keys.
* **Full CRUD:** Endpoints for managing clients, projects and tracking costs.
* **Data Validation:** Powered by Pydantic for strict type checking.
* **Auto-Docs:** Built-in interactive API documentation via Swagger UI.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Framework:** FastAPI
* **ORM:** SQLAlchemy 2.0
* **Database:** SQLite (Development)

## 📦 Installation
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
   cd YOUR_REPO_NAME
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
## 🏃 How to Run
Start the local development server:
 ```bash
uvicorn main:app --reload
```
Once running, visit https://www.google.com/search?q=http://127.0.0.1:8000/docs to test the API endpoints.
## 📡 API Endpoints
| Method | Endpoint | Description | Example Request Body |  
|----------|----------|----------|----------|
| POST  | `/client/create/`  | Add a client to the database  | `{"name": "Test Name", "email": "test.name@domain.com","phone": "+441234567890","company_name": "My Company Ltd","is_active": true}`|
| POST  | `/client/update/{client_id}`  | Update an existing client's information  |`{"name": "Another Name","email": "Another.Name@domain.com"}`|
| GET  | `/client/active/`  | Retrieve all active clients  |None|
| GET  | `/client/total_invoice/{client_id}`  | Retrieve total invoice for a client |None|
| GET  | `/client/total_unpaid_invoice/{client_id}`  | Retrieve total unpaid invoice for a client |None|
| GET  | `/client/{client_id}/projects`  | Retrieve all projects for a client  |None|
| GET  | `/project/create/`  | Add a project to the database  |`{"client_id": 1, "name": "Website Development", "description": "Build a company website", "state": "active", "start_date": "2026-03-01T09:00:00Z", "end_date": "2026-04-01T17:00:00Z", "hourly_rate": 75.00, "fixed_price": null}`|
| POST  | `/project/update/{project_id}`  | Update an existing project's information  |`{"name": "Web Designer", "description": "Design web pages"}`|
| GET  | `/project/by_client/{client_id}`  | Retrieve project for a specific client  |None|
| GET  | `/project/all_with_clients/`  | Retrieve all projects and associated client information  |None|
| GET  | `/project/all_active/`  | Retrieve all active projects  |None|
| DELETE  | `/project/{project_id}/delete/`  | Delete a project  |None|
| POST  | `/task/create/`  | Add a task to the database  |{ "project_id": 1, "title": "Build homepage", "description": "Create layout and styling", "status": "in_progress", "estimated_hours": 10.0, "actual_hours": 8.5 }|
| GET  | `/task/update_status/{task_id}`  | Update an existing task's information  |`{"title": "Design a homepage"}`|
| GET  | `/task/list_by_status/{status}`  | Retrieve all active task by status  |None|
| POST  | `/invoice/create/`  | Add an invoice to the database  |`{ "client_id": 1, "project_id": 1, "issue_date": "2026-03-30T10:00:00Z", "due_date": "2026-04-15T10:00:00Z", "total_amount": 500.00, "status": "draft" }`|
| GET  | `/invoice/list_by/{status}`  | Retrieve all invoice by status  |None|
