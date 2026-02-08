from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os

# Create FastAPI app
app = FastAPI()

# Enable CORS (so frontend can connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MongoDB Atlas (we’ll add the URI later in Render)
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["edu_database"]
courses = db["courses"]
students = db["students"]

@app.get("/")
def root():
    return {"message": "Educational Agent is running!"}

@app.post("/add_course")
def add_course(name: str, duration: int):
    courses.insert_one({"name": name, "duration": duration})
    return {"status": "Course added"}

@app.post("/add_student")
def add_student(name: str, progress: int):
    students.insert_one({"name": name, "progress": progress})
    return {"status": "Student added"}

@app.get("/recommend/{student_name}")
def recommend(student_name: str):
    student = students.find_one({"name": student_name})
    if not student:
        return {"error": "Student not found"}
    # Simple recommender: suggest shortest course if progress < 50
    if student["progress"] < 50:
        course = courses.find_one(sort=[("duration", 1)])
        return {"recommendation": f"Take {course['name']} next"}
    else:
        return {"recommendation": "Continue advanced courses"}
