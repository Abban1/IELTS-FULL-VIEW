from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from datetime import datetime
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from db import listening_col
from services.listening import generate_ielts_listening_test

router = APIRouter(prefix="/listening", tags=["Listening"])

# Generate new listening test
@router.get("/generate", response_class=PlainTextResponse)
def generate_listening(level: str = Query("Academic", description="Academic or General")):
    test_text = generate_ielts_listening_test(level)

    doc = {
        "level": level,
        "test": test_text,
        "created_at": datetime.utcnow()
    }
    listening_col.insert_one(doc)
    return test_text

# List all listening tests (metadata only)
@router.get("/tests")
def list_listening():
    data = []
    for t in listening_col.find().sort("created_at", -1):
        data.append({
            "id": str(t["_id"]),
            "level": t.get("level", "Unknown"),
            "created_at": t["created_at"].isoformat() if "created_at" in t else None
        })
    return JSONResponse(content=data)

# Get full test content by ID
@router.get("/tests/{test_id}", response_class=PlainTextResponse)
def get_listening(test_id: str):
    test = listening_col.find_one({"_id": ObjectId(test_id)})
    if not test:
        raise HTTPException(404, "Test not found")
    return test.get("test", "No content available")
