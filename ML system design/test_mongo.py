from pymongo import MongoClient

# MongoDB connection string
connection_string = "mongodb+srv://ml_user:vTKlJJ72GlMgJ10H@student-db.ghv0bvv.mongodb.net/?retryWrites=true&w=majority&appName=student-db"

try:
    client = MongoClient(connection_string)
    # The ping command is cheap and checks connectivity
    client.admin.command('ping')
    print("MongoDB connection: SUCCESS")
except Exception as e:
    print(f"MongoDB connection: FAILED ({e})")
