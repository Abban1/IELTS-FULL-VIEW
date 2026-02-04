from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from datetime import datetime, timedelta
from bson import ObjectId
from db import speaking_col
from services.speaking import generate_ielts_speaking

router = APIRouter(prefix="/speaking", tags=["Speaking"])

# Generate Speaking test
@router.get("/generate", response_class=PlainTextResponse)
def generate_speaking(level: str = Query("Academic", description="Academic or General"),
                      context_question: str = Query(None, description="Reference context")):
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

# List Speaking tests with search, date filter & pagination
@router.get("/tests")
def list_speaking(
    page: int = 1,
    page_size: int = 10,
    search: str = None,
    from_date: str = None,
    to_date: str = None
):
    query = {}
    if search:
        query["name"] = {"$regex": search, "$options": "i"}

    if from_date:
        query["created_at"] = {"$gte": datetime.strptime(from_date, "%Y-%m-%d")}
    if to_date:
        end_day = datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)
        if "created_at" in query:
            query["created_at"]["$lte"] = end_day
        else:
            query["created_at"] = {"$lte": end_day}

    total_items = speaking_col.count_documents(query)
    total_pages = max((total_items + page_size - 1) // page_size, 1)

    cursor = speaking_col.find(query).sort("created_at", -1).skip((page-1)*page_size).limit(page_size)
    data = [{
        "id": str(t["_id"]),
        "name": t.get("name", "N/A"),
        "level": t.get("level"),
        "created_at": t["created_at"].isoformat()
    } for t in cursor]

    return JSONResponse(content={"tests": data, "total_pages": total_pages, "total_items": total_items})

# Get Speaking test
@router.get("/tests/{test_id}", response_class=PlainTextResponse)
def get_speaking(test_id: str):
    test = speaking_col.find_one({"_id": ObjectId(test_id)})
    if not test:
        raise HTTPException(404, "Not found")
    return test["questions"]

# Delete Speaking test
@router.delete("/tests/{test_id}")
def delete_speaking(test_id: str):
    result = speaking_col.delete_one({"_id": ObjectId(test_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"message": f"Test {test_id} deleted successfully"}
