import pytest
from fastapi.testclient import TestClient
from app import app  # Assuming your FastAPI app is in 'app.py'

client = TestClient(app)

# ==================== Helper function to create an assignment ====================

def create_assignment():
    data = {"content": "This is a test assignment"}
    response = client.post("/student/assignments", json=data, headers={"X-Principal": '{"student_id": 1}'})
    assert response.status_code == 200
    return response.json()["id"]

# ==================== Test Student APIs ====================

def test_list_student_assignments():
    headers = {"X-Principal": '{"student_id": 1}'}
    response = client.get("/student/assignments", headers=headers)
    assert response.status_code == 200
    assert "data" in response.json()

def test_create_student_assignment():
    headers = {"X-Principal": '{"student_id": 1}'}
    data = {"content": "This is a new assignment"}
    response = client.post("/student/assignments", json=data, headers=headers)
    assert response.status_code == 200
    assert "message" in response.json()
    assert "id" in response.json()

def test_edit_student_assignment():
    # Create a test assignment and get the assignment ID
    assignment_id = create_assignment()
    
    headers = {"X-Principal": '{"student_id": 1}'}
    data = {"id": assignment_id, "content": "Updated assignment content"}
    response = client.post("/student/assignments/edit", json=data, headers=headers)
    assert response.status_code == 200
    assert "message" in response.json()

def test_submit_student_assignment():
    # Create a test assignment and get the assignment ID
    assignment_id = create_assignment()
    
    headers = {"X-Principal": '{"student_id": 1}'}
    data = {"id": assignment_id, "teacher_id": 2}
    response = client.post("/student/assignments/submit", json=data, headers=headers)
    assert response.status_code == 200
    assert "message" in response.json()

# ==================== Test Teacher APIs ====================

def test_list_teacher_assignments():
    headers = {"X-Principal": '{"teacher_id": 2}'}
    response = client.get("/teacher/assignments", headers=headers)
    assert response.status_code == 200
    assert "data" in response.json()

def test_grade_teacher_assignment():
    # Create a test assignment and get the assignment ID
    assignment_id = create_assignment()
    
    # Submit the assignment (it should have state 'SUBMITTED')
    headers = {"X-Principal": '{"student_id": 1}'}
    data = {"id": assignment_id, "teacher_id": 2}
    response = client.post("/student/assignments/submit", json=data, headers=headers)
    assert response.status_code == 200  # Ensure submission is successful
    
    # Now grade the assignment (state should be 'SUBMITTED')
    headers = {"X-Principal": '{"teacher_id": 2}'}
    data = {"id": assignment_id, "grade": "A"}
    response = client.post("/teacher/assignments/grade", json=data, headers=headers)
    assert response.status_code == 200  # Grading should succeed now
    assert "message" in response.json()
# ==================== Test Principal APIs ====================

def test_list_all_teachers():
    headers = {"X-Principal": '{"principal_id": 3}'}
    response = client.get("/principal/teachers", headers=headers)
    assert response.status_code == 200
    assert "data" in response.json()

def test_list_all_assignments():
    headers = {"X-Principal": '{"principal_id": 3}'}
    response = client.get("/principal/assignments", headers=headers)
    assert response.status_code == 200
    assert "data" in response.json()

def test_regrade_assignment():
    # Create a test assignment and get the assignment ID
    assignment_id = create_assignment()
    
    # Submit and grade the assignment first (it needs to be graded before regrading)
    headers = {"X-Principal": '{"student_id": 1}'}
    data = {"id": assignment_id, "teacher_id": 2}
    response = client.post("/student/assignments/submit", json=data, headers=headers)
    assert response.status_code == 200  # Ensure submission is successful
    
    # Grade the assignment
    headers = {"X-Principal": '{"teacher_id": 2}'}
    data = {"id": assignment_id, "grade": "A"}
    response = client.post("/teacher/assignments/grade", json=data, headers=headers)
    assert response.status_code == 200  # Ensure grading is successful
    
    # Regrade the assignment (state should be 'GRADED')
    headers = {"X-Principal": '{"principal_id": 3}'}
    data = {"id": assignment_id, "grade": "B+"}
    response = client.post("/principal/assignments/grade", json=data, headers=headers)
    assert response.status_code == 200  # Regrading should succeed now
    assert "message" in response.json()