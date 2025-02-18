from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from pymongo import MongoClient
from typing import Optional, List, Dict
import json
from bson import ObjectId

app = FastAPI()

# MongoDB Connection
client = MongoClient("mongodb+srv://ktchandru1234:k.t.chandru1234@cluster0.afircsf.mongodb.net/backee")
db = client["backee"]
assignments_collection = db["assignments"]
teachers_collection = db["teachers"]
principals_collection = db["principals"]
students_collection = db["students"]

# ==================== Models ====================
class AssignmentCreate(BaseModel):
    content: str

class AssignmentUpdate(BaseModel):
    id: str
    content: str

class AssignmentSubmit(BaseModel):
    id: str
    teacher_id: int

class AssignmentGrade(BaseModel):
    id: str
    grade: str

# ==================== Header Authentication ====================
def get_principal(x_principal: str = Header(...)) -> int:
    """ Extract principal_id from X-Principal header """
    try:
        principal_data = json.loads(x_principal)
        return principal_data.get("principal_id")
    except:
        raise HTTPException(status_code=400, detail="Invalid X-Principal header")

def get_student_id(x_principal: str = Header(...)) -> int:
    """ Extract student_id from X-Principal header """
    try:
        principal_data = json.loads(x_principal)
        return principal_data.get("student_id")
    except:
        raise HTTPException(status_code=400, detail="Invalid X-Principal header")

def get_teacher_id(x_principal: str = Header(...)) -> int:
    """ Extract teacher_id from X-Principal header """
    try:
        principal_data = json.loads(x_principal)
        return principal_data.get("teacher_id")
    except:
        raise HTTPException(status_code=400, detail="Invalid X-Principal header")

# ==================== Helper Function to Convert ObjectId ====================
def convert_objectid_to_str(obj):
    """ Convert Mongo ObjectId to string for JSON serialization """
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, dict):
        return {key: convert_objectid_to_str(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [convert_objectid_to_str(item) for item in obj]
    return obj

# ==================== Student APIs ====================
@app.get("/student/assignments")
async def list_student_assignments(student_id: int = Depends(get_student_id)):
    """ List all assignments created by a student """
    assignments = list(assignments_collection.find({"student_id": student_id}))
    return {"data": [convert_objectid_to_str(a) for a in assignments]}

@app.post("/student/assignments")
async def create_assignment(
    assignment: AssignmentCreate,
    student_id: int = Depends(get_student_id)
):
    """ Create an assignment (Draft) """
    new_assignment = {
        "content": assignment.content,
        "student_id": student_id,
        "state": "DRAFT",
        "teacher_id": None,
        "grade": None
    }
    result = assignments_collection.insert_one(new_assignment)
    return {"message": "Assignment created", "id": str(result.inserted_id)}

@app.post("/student/assignments/edit")
async def edit_assignment(
    assignment: AssignmentUpdate,
    student_id: int = Depends(get_student_id)
):
    """ Edit an assignment if it's still in Draft state """
    assignment_data = assignments_collection.find_one({"_id": ObjectId(assignment.id), "student_id": student_id})
    if not assignment_data or assignment_data["state"] != "DRAFT":
        raise HTTPException(status_code=403, detail="Cannot edit assignment")
    
    assignments_collection.update_one(
        {"_id": ObjectId(assignment.id)},
        {"$set": {"content": assignment.content}}
    )
    return {"message": "Assignment updated"}

@app.post("/student/assignments/submit")
async def submit_assignment(
    assignment: AssignmentSubmit,
    student_id: int = Depends(get_student_id)
):
    """ Submit a Draft assignment to a teacher """
    assignment_data = assignments_collection.find_one({"_id": ObjectId(assignment.id), "student_id": student_id})
    if not assignment_data or assignment_data["state"] != "DRAFT":
        raise HTTPException(status_code=403, detail="Cannot submit assignment")

    assignments_collection.update_one(
        {"_id": ObjectId(assignment.id)},
        {"$set": {"state": "SUBMITTED", "teacher_id": assignment.teacher_id}}
    )
    return {"message": "Assignment submitted"}

# ==================== Teacher APIs ====================
@app.get("/teacher/assignments")
async def list_teacher_assignments(teacher_id: int = Depends(get_teacher_id)):
    """ List all assignments submitted to this teacher """
    assignments = list(assignments_collection.find({"teacher_id": teacher_id, "state": "SUBMITTED"}))
    return {"data": [convert_objectid_to_str(a) for a in assignments]}

@app.post("/teacher/assignments/grade")
async def grade_assignment(
    assignment: AssignmentGrade,
    teacher_id: int = Depends(get_teacher_id)
):
    """ Grade an assignment submitted to the teacher """
    assignment_data = assignments_collection.find_one({"_id": ObjectId(assignment.id), "teacher_id": teacher_id})
    if not assignment_data:
        raise HTTPException(status_code=403, detail="Cannot grade this assignment")

    assignments_collection.update_one(
        {"_id": ObjectId(assignment.id)},
        {"$set": {"state": "GRADED", "grade": assignment.grade}}
    )
    return {"message": "Assignment graded"}

# ==================== Principal APIs ====================
@app.get("/principal/teachers")
async def list_all_teachers(principal_id: int = Depends(get_principal)):
    """ List all teachers """
    teachers = list(teachers_collection.find())
    return {"data": [convert_objectid_to_str(t) for t in teachers]}

@app.get("/principal/assignments")
async def list_all_assignments(principal_id: int = Depends(get_principal)):
    """ List all submitted and graded assignments """
    assignments = list(assignments_collection.find({"state": {"$in": ["SUBMITTED", "GRADED"]}}))
    return {"data": [convert_objectid_to_str(a) for a in assignments]}

@app.post("/principal/assignments/grade")
async def regrade_assignment(
    assignment: AssignmentGrade,
    principal_id: int = Depends(get_principal)
):
    """ Principal can re-grade an assignment """
    assignment_data = assignments_collection.find_one({"_id": ObjectId(assignment.id)})
    if not assignment_data or assignment_data["state"] != "GRADED":
        raise HTTPException(status_code=403, detail="Cannot regrade this assignment")

    assignments_collection.update_one(
        {"_id": ObjectId(assignment.id)},
        {"$set": {"grade": assignment.grade}}
    )
    return {"message": "Assignment regraded"}

# ==================== Run Server ====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
