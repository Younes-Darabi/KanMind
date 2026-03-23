# 📝 KanMind API - Task Management System (Backend)

KanMind is a comprehensive Task Management Backend API built with **Django REST Framework**. It provides a structured way to manage project boards, tasks, and team collaborations with robust permission handlings.

---

## 🚀 Key Features

### 🔐 Authentication
- **User Registration & Login:** Token-based authentication for secure access.
- **Email Availability Check:** Quickly verify if an email is already registered.

### 📋 Board Management
- **Create Boards:** Create projects and add members instantly.
- **Dynamic Stats:** Each board provides real-time counts for members, total tasks, "To-Do" tasks, and "High Priority" tasks.
- **Access Control:** Only owners or members can view/edit board details.

### 🛠 Task & Workflow
- **Assignment System:** Tasks can have both an **Assignee** (to do the work) and a **Reviewer** (to verify).
- **Custom Filters:** - `assigned-to-me`: Tasks where you are the executor.
  - `reviewing`: Tasks waiting for your approval.
- **Strict Validations:** Prevents changing the Board ID of an existing task and ensures only board members are assigned to tasks.

### 💬 Collaboration
- **Commenting System:** Users can discuss tasks through comments.
- **Ownership:** Only the author of a comment can delete it.

---

## 🛠 Tech Stack
- **Framework:** Django 6.0.3, Django REST Framework 3.16.1
- **Database:** SQLite (Default) / PostgreSQL compatible
- **Authentication:** DRF Token Authentication

---

## 🔧 Installation & Setup

1. **Clone the project:**

        git clone https://github.com/Younes-Darabi/KanMind
        cd kan-mind


3. Set up a Virtual Environment:

        python -m venv .venv
   
# Windows:

        .venv\Scripts\activate
        
# Linux/Mac:
   
        source .venv/bin/activate

3. Environment Configuration:
   Create a `.env` file in the root directory and add your secret key:
   ```env
   SECRET_KEY=your_secret_key_here

4. Install Dependencies:

        pip install -r requirements.txt

5. Apply Database Migrations:

        python manage.py migrate

6. Run the Development Server:

        python manage.py runserver


---

## 📍 API Endpoints Overview
### 🔐 Authentication

- POST /api/registration/ — Create a new user account.

- POST /api/login/ — Exchange credentials for an Auth Token.

- GET /api/email-check/ — Check if an email is already in use.

### 📂 Board Management

- GET /api/boards/ — List all boards you own or belong to.

- POST /api/boards/ — Create a new board (Members optional).

- GET /api/boards/{id}/ — Retrieve a specific board and its tasks.

- PATCH /api/boards/{id}/ — Update board title or member list.

- DELETE /api/boards/{id}/ — Delete a board (Owner Only).

### 📋 Task Management

- POST /api/tasks/ — Add a task to a board.

- GET /api/tasks/assigned-to-me/ — View tasks assigned to you.

- GET /api/tasks/reviewing/ — View tasks where you are the reviewer.

- PATCH /api/tasks/{id}/ — Modify task status, priority, or details.

- DELETE /api/tasks/{id}/ — Remove a task (Creator/Owner Only).

### 💬 Task Comments

- GET /api/tasks/{id}/comments/ — Get all comments for a task.

- POST /api/tasks/{id}/comments/ — Post a new comment.

- DELETE /api/tasks/{t_id}/comments/{c_id}/ — Delete a comment (Author Only).


### 🛡 Quick Permission Reference
- Board Access: Owner OR Member.

- Task Creation: Any Board Member.

- Task Deletion: Only the Task Creator OR Board Owner.

- Board Deletion: Only the Board Owner.

- Comment Deletion: Only the Comment Author.


---

## 🔗 Related Projects

This repository serves as the **Backend API** for the KanMind ecosystem. To explore the user interface and frontend implementation, please visit:

* **Frontend Repository:** [https://github.com/Developer-Akademie-Backendkurs/project.KanMind](https://github.com/Developer-Akademie-Backendkurs/project.KanMind)

---

Developed with ❤️ by Younes
