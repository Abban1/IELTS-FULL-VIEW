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

# List all Reading tests with pagination and search
@router.get("/tests")
def list_tests(page: int = 1, page_size: int = 10, search: str = None):
    query = {}
    if search:
        try:
            obj_id = ObjectId(search)
            query = {"$or": [{"name": search}, {"_id": obj_id}]}
        except:
            query = {"name": search}

    total_items = reading_col.count_documents(query)
    total_pages = (total_items + page_size - 1) // page_size

    cursor = reading_col.find(query).sort("created_at", -1).skip((page-1)*page_size).limit(page_size)
    data = [{
        "id": str(t["_id"]),
        "name": t.get("name", "N/A"),
        "level": t.get("level"),
        "difficulty": t.get("difficulty"),
        "created_at": t["created_at"].isoformat()
    } for t in cursor]

    return JSONResponse(content={"tests": data, "total_pages": total_pages, "total_items": total_items})

# Get a specific Reading test
@router.get("/tests/{test_id}", response_class=PlainTextResponse)
def get_test(test_id: str):
    test = reading_col.find_one({"_id": ObjectId(test_id)})
    if not test:
        raise HTTPException(404, "Not found")
    return test["content"]

# Delete a Reading test
@router.delete("/tests/{test_id}")
def delete_reading(test_id: str):
    result = reading_col.delete_one({"_id": ObjectId(test_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"message": f"Test {test_id} deleted successfully"}
