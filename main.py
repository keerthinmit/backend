from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend (index.html) to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (safe for local dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample data
courses = [
    {"title": "Python Basics", "difficulty": "Beginner", "prerequisite": None},
    {"title": "SQL Fundamentals", "difficulty": "Beginner", "prerequisite": "Python Basics"},
    {"title": "Machine Learning", "difficulty": "Intermediate", "prerequisite": "SQL Fundamentals"},
]

learners = [
    {"id": 1, "name": "Keerthi", "skills": ["Python"], "goal": "Data Scientist"},
    {"id": 2, "name": "Anita", "skills": ["Python", "SQL"], "goal": "AI Engineer"}
]

@app.get("/")
def home():
    return {"message": "Educational Agent is running!"}

@app.get("/courses")
def get_courses():
    return {"courses": courses}

@app.get("/learners")
def get_learners():
    return {"learners": learners}

@app.get("/skill-gap/{learner_id}")
def skill_gap(learner_id: int):
    learner = next(l for l in learners if l["id"] == learner_id)
    target_skills = ["Python", "SQL", "Machine Learning", "Deep Learning"]
    missing = [skill for skill in target_skills if skill not in learner["skills"]]
    return {"learner": learner["name"], "missing_skills": missing}
