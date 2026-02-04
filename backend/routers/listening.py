from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from datetime import datetime, timedelta
from bson import ObjectId
from db import listening_col
from services.listening import generate_ielts_listening_test

router = APIRouter(prefix="/listening", tags=["Listening"])

# Generate Listening test
@router.get("/generate", response_class=PlainTextResponse)
def generate_listening(level: str = Query("Academic", description="Academic or General")):
    test_text = generate_ielts_listening_test(level)

    count = listening_col.count_documents({})
    test_name = f"IELTS Listening Mock {count + 1}"

    listening_col.insert_one({
        "name": test_name,
        "level": level,
        "test": test_text,
        "created_at": datetime.utcnow()
    })

    return test_text

# List Listening tests with search, date filter & pagination
@router.get("/tests")
def list_listening(
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

    total_items = listening_col.count_documents(query)
    total_pages = max((total_items + page_size - 1) // page_size, 1)

    cursor = listening_col.find(query).sort("created_at", -1).skip((page-1)*page_size).limit(page_size)
    data = [{
        "id": str(t["_id"]),
        "name": t.get("name", "N/A"),
        "level": t.get("level"),
        "created_at": t["created_at"].isoformat()
    } for t in cursor]

    return JSONResponse(content={"tests": data, "total_pages": total_pages, "total_items": total_items})

# Get Listening test
@router.get("/tests/{test_id}", response_class=PlainTextResponse)
def get_listening(test_id: str):
    test = listening_col.find_one({"_id": ObjectId(test_id)})
    if not test:
        raise HTTPException(404, "Not found")
    return test["test"]

# Delete Listening test
@router.delete("/tests/{test_id}")
def delete_listening(test_id: str):
    result = listening_col.delete_one({"_id": ObjectId(test_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"message": f"Test {test_id} deleted successfully"}
