from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from datetime import datetime, timedelta
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

# List all Reading tests with search, date filter & pagination
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
        # Try to search by ObjectId if it's a valid ObjectId format
        search_conditions = [{"name": {"$regex": search, "$options": "i"}}]
        
        # Check if search string is a valid ObjectId (24 hex characters)
        if len(search) == 24 and all(c in '0123456789abcdefABCDEF' for c in search):
            try:
                search_conditions.append({"_id": ObjectId(search)})
            except:
                pass
        
        query["$or"] = search_conditions
    
    # Date filters
    if from_date:
        # Start of the day (00:00:00)
        from_datetime = datetime.strptime(from_date, "%Y-%m-%d")
        query["created_at"] = {"$gte": from_datetime}
    
    if to_date:
        # End of the day (23:59:59)
        to_datetime = datetime.strptime(to_date, "%Y-%m-%d")
        to_datetime = to_datetime.replace(hour=23, minute=59, second=59)
        if "created_at" not in query:
            query["created_at"] = {}
        query["created_at"]["$lte"] = to_datetime
    
    # Sorting: -1 for desc (newest first), 1 for asc (oldest first)
    sort_order = -1 if sort_by == "desc" else 1
    
    # Count total
    total = reading_col.count_documents(query)
    total_pages = (total + page_size - 1) // page_size
    
    # Fetch with sorting
    tests = list(reading_col.find(query)
                 .sort("created_at", sort_order)
                 .skip((page - 1) * page_size)
                 .limit(page_size))
    
    for test in tests:
        test["_id"] = str(test["_id"])
        test["id"] = str(test["_id"])
    
    return {"tests": tests, "total": total, "total_pages": total_pages}

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