from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from datetime import datetime
from bson import ObjectId
from db import speaking_col
from services.speaking import generate_ielts_speaking

router = APIRouter(prefix="/speaking", tags=["Speaking"])

@router.get("/generate", response_class=PlainTextResponse)
def generate_speaking(level: str = Query("Academic"), context_question: str = Query(None)):
    questions = generate_ielts_speaking(level, context_question)
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

@router.get("/tests")
def list_speaking(page: int = 1, page_size: int = 10, search: str = None):
    query = {}
    if search:
        try:
            obj_id = ObjectId(search)
            query = {"$or": [{"name": search}, {"_id": obj_id}]}
        except:
            query = {"name": search}

    total_items = speaking_col.count_documents(query)
    total_pages = (total_items + page_size - 1) // page_size

    cursor = speaking_col.find(query).sort("created_at", -1).skip((page-1)*page_size).limit(page_size)
    data = [{
        "id": str(t["_id"]),
        "name": t.get("name", "N/A"),
        "level": t.get("level"),
        "created_at": t["created_at"].isoformat()
    } for t in cursor]

    return JSONResponse(content={"tests": data, "total_pages": total_pages, "total_items": total_items})

@router.get("/tests/{test_id}", response_class=PlainTextResponse)
def get_speaking(test_id: str):
    test = speaking_col.find_one({"_id": ObjectId(test_id)})
    if not test:
        raise HTTPException(404, "Not found")
    return test["questions"]

@router.delete("/tests/{test_id}")
def delete_speaking(test_id: str):
    result = speaking_col.delete_one({"_id": ObjectId(test_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"message": f"Test {test_id} deleted successfully"}
