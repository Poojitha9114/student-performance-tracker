# 🎓 Student Performance Tracker

A full-stack web application to manage student records, track grades, and identify toppers.

## 🔗 Live Demo
[Add Streamlit Cloud link here after deployment]

## 🛠️ Tech Stack
- **Backend:** FastAPI, Python, Pydantic
- **Frontend:** Streamlit
- **Storage:** JSON file persistence
- **API Docs:** Auto-generated Swagger UI

## ✨ Features
- Add students with automatic grade calculation
- Search student by roll number
- Find class topper (handles tied scores)
- Live stats dashboard — average, highest, lowest marks
- All students table view
- Data persists across server restarts

## 🚀 Run Locally
```bash
# Terminal 1 - Backend
pip install fastapi uvicorn
python -m uvicorn student_api:app --reload

# Terminal 2 - Frontend  
pip install streamlit
python -m streamlit run app.py
```

## 📡 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /add-student | Add new student |
| GET | /student/{roll_no} | Get student by roll |
| GET | /all-students | Get all students |
| GET | /topper | Get class topper(s) |
| GET | /stats | Get class statistics |
