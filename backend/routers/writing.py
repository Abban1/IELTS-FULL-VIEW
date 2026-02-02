from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from datetime import datetime
from bson import ObjectId
from db import writing_col
from services.writing import generate_ielts_task

router = APIRouter(prefix="/writing", tags=["Writing"])

# Generate new Writing test
@router.get("/generate", response_class=PlainTextResponse)
def generate_writing(task_type: str = Query(..., description="task1 or task2"),
                     level: str = Query("Academic", description="Academic or General")):
    question = generate_ielts_task(task_type, level)

    # Generate name automatically
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

# List all Writing tests
@router.get("/tests")
def list_tests():
    data = []
    for t in writing_col.find().sort("created_at", -1):
        data.append({
            "id": str(t["_id"]),
            "name": t.get("name", "N/A"),
            "task_type": t.get("task_type"),
            "level": t.get("level"),
            "created_at": t["created_at"].isoformat()
        })
    return JSONResponse(content=data)



# Delete a Writing test
@router.delete("/tests/{test_id}")
def delete_writing(test_id: str):
    result = writing_col.delete_one({"_id": ObjectId(test_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"message": f"Test {test_id} deleted successfully"}
