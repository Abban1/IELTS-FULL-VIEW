from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from datetime import datetime
from bson import ObjectId
from db import listening_col
from services.listening import generate_ielts_listening_test

router = APIRouter(prefix="/listening", tags=["Listening"])

# Generate Listening test
@router.get("/generate", response_class=PlainTextResponse)
def generate_listening(level: str = Query("Academic", description="Academic or General")):
    test_text = generate_ielts_listening_test(level)

    # Generate name automatically
    count = listening_col.count_documents({})
    test_name = f"IELTS Listening Mock {count + 1}"

    listening_col.insert_one({
        "name": test_name,
        "level": level,
        "test": test_text,
        "created_at": datetime.utcnow()
    })

    return test_text

# List all Listening tests
@router.get("/tests")
def list_listening():
    data = []
    for t in listening_col.find().sort("created_at", -1):
        data.append({
            "id": str(t["_id"]),
            "name": t.get("name", "N/A"),
            "level": t.get("level"),
            "created_at": t["created_at"].isoformat()
        })
    return JSONResponse(content=data)

# Get a specific Listening test
@router.get("/tests/{test_id}", response_class=PlainTextResponse)
def get_listening(test_id: str):
    test = listening_col.find_one({"_id": ObjectId(test_id)})
    if not test:
        raise HTTPException(404, "Not found")
    return test["test"]

# Delete a Listening test
@router.delete("/tests/{test_id}")
def delete_listening(test_id: str):
    result = listening_col.delete_one({"_id": ObjectId(test_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"message": f"Test {test_id} deleted successfully"}
