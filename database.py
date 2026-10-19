from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

MONGO_URI = "mongodb://127.0.0.1:27017"

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

try:
    client.admin.command("ping")
    print("MongoDB connected successfully!")

    db = client["studentsphere"]

    students_collection = db["students"]
    exam_records_collection = db["exam_records"]
    
    students_collection.create_index(
    "student_id",
    unique=True
    )

except ConnectionFailure as error:
    print("MongoDB connection failed:", error)
    raise
