import uuid
from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI()

class StudentRegisterInput(BaseModel):
    full_name: str = Field(..., min_length=3)
    # Thay EmailStr bằng str thông thường
    email: str = Field(..., min_length=5, description="Địa chỉ email")
    age: int = Field(..., ge=15, le=60)
    phone: str = Field(..., min_length=10, max_length=11, pattern=r"^\d+$")
    course: str = Field(..., min_length=1)
    note: str = Field(None, max_length=200)

@app.post("/students/register", status_code=status.HTTP_201_CREATED)
def register_student(student_in: StudentRegisterInput):
    normalized_name = " ".join([word.capitalize() for word in student_in.full_name.strip().split()])
    
    student_id = f"STU_{uuid.uuid4().hex[:6].upper()}"
    
    processed_data = {
        "student_id": student_id,
        "full_name": normalized_name,
        "email": student_in.email,
        "age": student_in.age,
        "phone": student_in.phone,
        "course": student_in.course.lower(),
        "note": student_in.note
    }
    
    return {
        "message": "Đăng ký học viên thành công",
        "data": processed_data
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)