#!/usr/bin/env python3

import sys
from pymongo import MongoClient
from pymongo.errors import PyMongoError

try:
    client = MongoClient(
        "mongodb://studentsphere-mongodb:27017",
        serverSelectionTimeoutMS=3000
    )

    client.admin.command("ping")

    print("OK - MongoDB is responding successfully")
    client.close()
    sys.exit(0)

except PyMongoError as error:
    print(f"CRITICAL - MongoDB health check failed: {error}")
    sys.exit(2)