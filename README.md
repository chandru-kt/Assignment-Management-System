# Assignment Management System

This project is an Assignment Management System built using FastAPI and MongoDB. It allows students, teachers, and principals to manage assignments, grades, and view related data through a RESTful API.

# To Run
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# To Test
pytest test_app.py

# API Endpoints
### Student Endpoints

#### GET /student/assignments
List all assignments created by a student.

#### POST /student/assignments
Create a new assignment (draft).

#### POST /student/assignments/edit
Edit an existing assignment (if it is in the draft state).

#### POST /student/assignments/submit
Submit an assignment for grading.

### Teacher Endpoints

#### GET /teacher/assignments
List all assignments submitted to the teacher.

#### POST /teacher/assignments/grade
Grade an assignment.

### Principal Endpoints

#### GET /principal/teachers
List all teachers.

#### GET /principal/assignments
List all assignments that have been submitted and graded.

#### POST /principal/assignments/grade
Re-grade an assignment.

## Features

1. **Student APIs:**
    - List all assignments created by a student.
    - Create, edit, and submit assignments.
  
2. **Teacher APIs:**
    - List all assignments submitted by students.
    - Grade assignments.
  
3. **Principal APIs:**
    - List all teachers and assignments.
    - Re-grade assignments.

## Tech Stack

- **Backend**: FastAPI
- **Database**: MongoDB
- **Authentication**: Header-based (using X-Principal to identify students, teachers, and principals)
- **Testing**: Pytest for API testing

## Requirements

- Python 3.8 or higher
- MongoDB Atlas account (for cloud database)

## Output

![image](https://github.com/user-attachments/assets/ad7986af-6dbb-4b5b-ac70-76e642869554)

![image](https://github.com/user-attachments/assets/a955747c-2917-4267-9063-c2b9073a0c9b)

![image](https://github.com/user-attachments/assets/3b012739-58d8-4360-aa04-b7b2afec762b)

![image](https://github.com/user-attachments/assets/11475fb7-e680-4dbd-97d7-29100e0b1c07)

![image](https://github.com/user-attachments/assets/dcdc7973-0712-4fa7-afe7-7835315c92bd)

![image](https://github.com/user-attachments/assets/69c2d7b4-e22b-4f14-a363-534c767a4316)

![image](https://github.com/user-attachments/assets/ae37dd73-fbdd-40f9-9cd2-7f295de87bd3)

![image](https://github.com/user-attachments/assets/c62159ce-add6-4e3a-927f-14f45b56ef0f)

![image](https://github.com/user-attachments/assets/4fe76327-784a-4ade-8213-173e23b967d9)
