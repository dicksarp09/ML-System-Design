# mongodb_app_logging.py
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
from datetime import datetime
import joblib

app = Flask(__name__)




model = joblib.load("performance_pipeline.pkl")


# ----------------------
# Logging configuration
# ----------------------
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ----------------------
# MongoDB connection
# ----------------------
connection_string = "mongodb+srv://ml_user:vTKlJJ72GlMgJ10H@student-db.ghv0bvv.mongodb.net/?retryWrites=true&w=majority&appName=student-db"
client = MongoClient(connection_string)
db = client["student_performance"]
collection = db["records"]

# ----------------------
# Helper function
# ----------------------
def check_mongo_connection():
    try:
        client.admin.command('ping')
        return True, "SUCCESS"
    except Exception as e:
        logging.error(f"MongoDB connection failed: {str(e)}")
        return False, str(e)

# ----------------------
# Routes
# ----------------------
@app.route('/')
def home():
    connected, status = check_mongo_connection()
    logging.info("Accessed home route")
    return jsonify({
        "message": "Student Pass Prediction API is running!",
        "mongo_status": status
    })

@app.route('/students', methods=['GET'])
def get_students():
    logging.info("GET /students called")
    connected, status = check_mongo_connection()
    if not connected:
        logging.error(f"MongoDB connection failed: {status}")
        return jsonify({"error": f"MongoDB connection failed: {status}"}), 500

    try:
        students = list(collection.find())
        for student in students:
            student["_id"] = str(student["_id"])
        logging.info(f"Retrieved {len(students)} students")
        return jsonify(students)
    except Exception as e:
        logging.error(f"Error fetching students: {str(e)}")
        return jsonify({"error": "Failed to fetch students"}), 500

@app.route('/students', methods=['POST'])
def add_student():
    logging.info(f"POST /students called | Data: {request.json}")
    connected, status = check_mongo_connection()
    if not connected:
        logging.error(f"MongoDB connection failed: {status}")
        return jsonify({"error": f"MongoDB connection failed: {status}"}), 500

    try:
        data = request.json
        result = collection.insert_one(data)
        logging.info(f"Inserted student with ID: {result.inserted_id}")
        return jsonify({"inserted_id": str(result.inserted_id)})
    except Exception as e:
        logging.error(f"Error inserting student: {str(e)}")
        return jsonify({"error": "Failed to insert student"}), 500

@app.route('/students/<id>', methods=['GET'])
def get_student(id):
    logging.info(f"GET /students/{id} called")
    connected, status = check_mongo_connection()
    if not connected:
        logging.error(f"MongoDB connection failed: {status}")
        return jsonify({"error": f"MongoDB connection failed: {status}"}), 500

    try:
        student = collection.find_one({"_id": ObjectId(id)})
        if student:
            student["_id"] = str(student["_id"])
            logging.info(f"Student found: {id}")
            return jsonify(student)
        logging.warning(f"Student not found: {id}")
        return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        logging.error(f"Error fetching student {id}: {str(e)}")
        return jsonify({"error": "Invalid ID format"}), 400

# ----------------------
# Dummy /predict endpoint (for logging)
# ----------------------
# Add this inside mongodb_app_logging.py, replacing the old /predict route

# Required columns your model expects
REQUIRED_COLUMNS = [
    "school", "sex", "age", "address", "Medu", "Fedu",
    "higher", "romantic", "dataset", "Fjob", "activities",
    "Walc", "health", "Mjob", "freetime", "failures", "goout",
    "schoolsup", "G2", "nursery", "Pstatus", "traveltime",
    "studytime", "G3", "famsize", "paid", "guardian", "Dalc",
    "internet", "famsup", "absences", "G1", "reason", "famrel"
]

# Default values for missing columns
DEFAULTS = {col: 0 if col in ["age", "Medu", "Fedu", "G1", "G2", "G3", "failures",
                              "absences","goout","freetime","Dalc","Walc","health","famrel","studytime"]
            else "none" for col in REQUIRED_COLUMNS}

@app.route('/predict', methods=['POST'])
def predict():
    logging.info(f"POST /predict called | Headers: {request.headers}")

    # API key check
    api_key = request.headers.get("x-api-key")
    if api_key != "mysecretkey":
        logging.warning("Unauthorized API key attempt")
        return jsonify({"error": "Unauthorized. Invalid API key."}), 401

    # Parse JSON
    try:
        data = request.get_json(force=True)
    except Exception as e:
        logging.error(f"Failed to decode JSON: {str(e)}")
        return jsonify({"error": f"Failed to decode JSON: {str(e)}"}), 400

    if data is None:
        logging.error("Invalid JSON received")
        return jsonify({"error": "Invalid JSON received"}), 400

    # Wrap single dict in list for batch processing
    if isinstance(data, dict):
        data = [data]

    # Auto-fill missing columns
    for record in data:
        for col in REQUIRED_COLUMNS:
            if col not in record:
                record[col] = DEFAULTS[col]

    logging.info(f"Processed input data: {data}")

    # Convert to DataFrame for model
    import pandas as pd
    df = pd.DataFrame(data)

    # Ensure column order matches training
    df = df[REQUIRED_COLUMNS]

    # Make predictions using your trained model
    predictions = model.predict(df)

    # Convert predictions to JSON-friendly list
    response = [{"prediction": pred} for pred in predictions]

    logging.info(f"Predictions: {response}")
    return jsonify(response)

# Main
# ----------------------
if __name__ == '__main__':
    logging.info("Starting Flask app with logging")
    app.run(debug=True)
