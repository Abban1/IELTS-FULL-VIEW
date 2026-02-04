from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from datetime import datetime, timedelta
from bson import ObjectId
from db import writing_col
from services.writing import generate_ielts_task

router = APIRouter(prefix="/writing", tags=["Writing"])

# Generate Writing test
@router.get("/generate", response_class=PlainTextResponse)
def generate_writing(task_type: str = Query(..., description="task1 or task2"),
                     level: str = Query("Academic", description="Academic or General")):
    question = generate_ielts_task(task_type, level)

    count = writing_col.count_documents({})
    test_name = f"IELTS Writing Mock {count + 1}"

    writing_col.insert_one({
        "name": test_name,
        "task_type": task_type,
        "level": level,
        "question": question,
        "created_at": datetime.utcnow()
    })

    return question

# List Writing tests with search, date filter & pagination
@router.get("/tests")
async def get_tests(
    page: int = 1,
    page_size: int = 10,
    search: str = None,
    from_date: str = None,
    to_date: str = None,
    sort_by: str = "desc"
):
    query = {}
    
    # Search filter
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
        ]
    
    # Date filters
    if from_date:
        query["created_at"] = {"$gte": datetime.strptime(from_date, "%Y-%m-%d")}
    if to_date:
        if "created_at" not in query:
            query["created_at"] = {}
        query["created_at"]["$lte"] = datetime.strptime(to_date, "%Y-%m-%d")
    
    # Sorting: -1 for desc (newest first), 1 for asc (oldest first)
    sort_order = -1 if sort_by == "desc" else 1
    
    # Count total
    total = writing_col.count_documents(query)
    total_pages = (total + page_size - 1) // page_size
    
    # Fetch with sorting
    tests = list(writing_col.find(query)
                 .sort("created_at", sort_order)
                 .skip((page - 1) * page_size)
                 .limit(page_size))
    
    for test in tests:
        test["_id"] = str(test["_id"])
        test["id"] = str(test["_id"])  # Add this for frontend compatibility
    
    return {"tests": tests, "total": total, "total_pages": total_pages}

# Get Writing test
@router.get("/tests/{test_id}", response_class=PlainTextResponse)
def get_writing(test_id: str):
    test = writing_col.find_one({"_id": ObjectId(test_id)})
    if not test:
        raise HTTPException(404, "Not found")
    return test["question"]

# Delete Writing test
@router.delete("/tests/{test_id}")
def delete_writing(test_id: str):
    result = writing_col.delete_one({"_id": ObjectId(test_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"message": f"Test {test_id} deleted successfully"}