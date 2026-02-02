from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from datetime import datetime
from bson import ObjectId
from db import speaking_col
from services.speaking import generate_ielts_speaking

router = APIRouter(prefix="/speaking", tags=["Speaking"])

# Generate Speaking test
@router.get("/generate", response_class=PlainTextResponse)
def generate_speaking(
    level: str = Query("Academic", description="Academic or General"),
    context_question: str = Query(None, description="Reference context for Part 2 and Part 3")
):
    questions = generate_ielts_speaking(level, context_question)

    # Generate name automatically
    count = speaking_col.count_documents({})
    test_name = f"IELTS Speaking Mock {count + 1}"

    speaking_col.insert_one({
        "name": test_name,
        "level": level,
        "context_question": context_question,
        "questions": questions,
        "created_at": datetime.utcnow()
    })

    return questions

# List all Speaking tests
@router.get("/tests")
def list_speaking():
    data = []
    for t in speaking_col.find().sort("created_at", -1):
        data.append({
            "id": str(t["_id"]),
            "name": t.get("name", "N/A"),
            "level": t.get("level"),
            "created_at": t["created_at"].isoformat()
        })
    return JSONResponse(content=data)

# Get a specific Speaking test
@router.get("/tests/{test_id}", response_class=PlainTextResponse)
def get_speaking(test_id: str):
    test = speaking_col.find_one({"_id": ObjectId(test_id)})
    if not test:
        raise HTTPException(404, "Not found")
    return test["questions"]

# Delete a Speaking test
@router.delete("/tests/{test_id}")
def delete_speaking(test_id: str):
    result = speaking_col.delete_one({"_id": ObjectId(test_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"message": f"Test {test_id} deleted successfully"}
