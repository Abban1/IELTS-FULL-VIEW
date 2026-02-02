from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from datetime import datetime
from bson import ObjectId

from db import reading_col
from services.reading import generate_section_1, generate_section_2, generate_section_3

router = APIRouter(prefix="/reading", tags=["Reading"])

# Generate new reading test
@router.get("/generate", response_class=PlainTextResponse)
def generate_reading(level: str = "General Training", difficulty: str = "Hard"):
    s1 = generate_section_1(level, difficulty)
    s2 = generate_section_2(level, difficulty)
    s3 = generate_section_3(level, difficulty)

    full_test = (
        "IELTS GENERAL TRAINING READING TEST\n"
        "Time allowed: 60 minutes\n\n"
        f"{s1}\n\n{'='*60}\n\n{s2}\n\n{'='*60}\n\n{s3}"
    )

    reading_col.insert_one({
        "level": level,
        "difficulty": difficulty,
        "content": full_test,
        "created_at": datetime.utcnow()
    })
    return full_test

# List all reading tests (metadata)
@router.get("/tests")
def list_tests():
    data = []
    for t in reading_col.find().sort("created_at", -1):
        data.append({
            "id": str(t["_id"]),
            "level": t.get("level", "Unknown"),
            "difficulty": t.get("difficulty", "Unknown"),
            "created_at": t["created_at"].isoformat() if "created_at" in t else None
        })
    return JSONResponse(content=data)

# Get full reading test by ID
@router.get("/tests/{test_id}", response_class=PlainTextResponse)
def get_test(test_id: str):
    test = reading_col.find_one({"_id": ObjectId(test_id)})
    if not test:
        raise HTTPException(404, "Test not found")
    return test.get("content", "No content available")
