from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from prometheus_flask_exporter import PrometheusMetrics
import logging
import time

app = Flask(__name__)

# --- Logging setup ---
logging.basicConfig(
    filename="api_monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Prometheus Metrics ---
metrics = PrometheusMetrics(app)

# Custom metrics
metrics.info('app_info', 'Student Pass Prediction API Info', version='1.0')

# MongoDB connection
connection_string = "mongodb+srv://ml_user:vTKlJJ72GlMgJ10H@student-db.ghv0bvv.mongodb.net/?retryWrites=true&w=majority&appName=student-db"
client = MongoClient(connection_string)
db = client["student_performance"]
collection = db["records"]

# Helper function to check MongoDB connection
def check_mongo_connection():
    try:
        client.admin.command('ping')
        return True, "SUCCESS"
    except Exception as e:
        return False, str(e)

# Middleware to track latency & errors
@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def track_request(response):
    latency = time.time() - request.start_time
    logging.info(
        f"Endpoint: {request.path}, Method: {request.method}, Status: {response.status_code}, Latency: {latency:.4f}s"
    )
    return response

# Home route with MongoDB status
@app.route('/')
def home():
    connected, status = check_mongo_connection()
    return jsonify({
        "message": "Student Pass Prediction API is running!",
        "mongo_status": status
    })

# Get all students
@app.route('/students', methods=['GET'])
def get_students():
    connected, status = check_mongo_connection()
    if not connected:
        logging.error(f"MongoDB connection failed: {status}")
        return jsonify({"error": f"MongoDB connection failed: {status}"}), 500

    students = list(collection.find())
    for student in students:
        student["_id"] = str(student["_id"])
    return jsonify(students)

# Add a new student
@app.route('/students', methods=['POST'])
def add_student():
    connected, status = check_mongo_connection()
    if not connected:
        logging.error(f"MongoDB connection failed: {status}")
        return jsonify({"error": f"MongoDB connection failed: {status}"}), 500

    data = request.json
    try:
        result = collection.insert_one(data)
        logging.info(f"Student added: {str(result.inserted_id)}")
        return jsonify({"inserted_id": str(result.inserted_id)})
    except Exception as e:
        logging.error(f"Error inserting student: {str(e)}")
        return jsonify({"error": "Failed to add student"}), 500

# Get a student by ID
@app.route('/students/<id>', methods=['GET'])
def get_student(id):
    connected, status = check_mongo_connection()
    if not connected:
        logging.error(f"MongoDB connection failed: {status}")
        return jsonify({"error": f"MongoDB connection failed: {status}"}), 500

    try:
        student = collection.find_one({"_id": ObjectId(id)})
    except:
        logging.warning(f"Invalid ID format: {id}")
        return jsonify({"error": "Invalid ID format"}), 400

    if student:
        student["_id"] = str(student["_id"])
        return jsonify(student)
    logging.warning(f"Student not found: {id}")
    return jsonify({"error": "Student not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
