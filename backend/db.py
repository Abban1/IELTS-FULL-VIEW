import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["ielts_db"]

reading_col   = db["ielts_reading_tests"]
writing_col   = db["generated_tasks"]
listening_col = db["listening_tests"]
speaking_col  = db["generated_speaking_tasks"]
