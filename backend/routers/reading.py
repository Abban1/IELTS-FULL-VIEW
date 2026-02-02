from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from datetime import datetime
from bson import ObjectId
from db import reading_col
from services.reading import generate_section_1, generate_section_2, generate_section_3

router = APIRouter(prefix="/reading", tags=["Reading"])

# Generate new Reading test
@router.get("/generate", response_class=PlainTextResponse)
def generate_reading(level: str = "General Training", difficulty: str = "Hard"):
    s1 = generate_section_1(level, difficulty)
    s2 = generate_section_2(level, difficulty)
    s3 = generate_section_3(level, difficulty)
    full_test = (
        f"IELTS READING TEST\nTime allowed: 60 minutes\n\n{s1}\n\n{'='*60}\n\n{s2}\n\n{'='*60}\n\n{s3}"
    )

    # Generate name automatically
    count = reading_col.count_documents({})
    test_name = f"IELTS Reading Mock {count + 1}"

    reading_col.insert_one({
        "name": test_name,
        "level": level,
        "difficulty": difficulty,
        "content": full_test,
        "created_at": datetime.utcnow()
    })

    return full_test

# List all Reading tests
@router.get("/tests")
def list_tests():
    data = []
    for t in reading_col.find().sort("created_at", -1):  # Newest first
        data.append({
            "id": str(t["_id"]),
            "name": t.get("name", "N/A"),
            "level": t.get("level"),
            "difficulty": t.get("difficulty"),
            "created_at": t["created_at"].isoformat()
        })
    return JSONResponse(content=data)


# Delete a Reading test
@router.delete("/tests/{test_id}")
def delete_reading(test_id: str):
    result = reading_col.delete_one({"_id": ObjectId(test_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"message": f"Test {test_id} deleted successfully"}
