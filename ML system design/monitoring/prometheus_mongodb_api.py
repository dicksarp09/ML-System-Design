from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# Initialize Prometheus metrics
metrics = PrometheusMetrics(app)

# Custom HTTP request counter (no conflict with defaults)
custom_counter = metrics.counter(
    'my_http_requests_total',
    'Custom HTTP Request Counter',
    labels={
        'method': lambda r: r.method,
        'endpoint': lambda r: r.path,
        'status': lambda r: r.status_code
    }
)

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

# Home route with MongoDB status
@app.route('/')
@metrics.do_not_track()
def home():
    connected, status = check_mongo_connection()
    return jsonify({
        "message": "Student Pass Prediction API is running!",
        "mongo_status": status
    })

def batch_predict(input_csv, output_csv):
    """
    Runs batch predictions on a CSV file and saves the results.

    Parameters:
    input_csv (str): Path to input CSV file containing features
    output_csv (str): Path where the predictions will be saved
    """
    # Load data
    data = pd.read_csv(input_csv)

    # Preprocess data if needed
    # Example: data = preprocess(data)

    # Run predictions
    predictions = model.predict(data)

    # Save results
    output_df = data.copy()
    output_df['prediction'] = predictions
    output_df.to_csv(output_csv, index=False)

    print(f"Batch predictions saved to {output_csv}")


# Example endpoint
@app.route("/hello")
def hello():
    return "Hello, Prometheus!"


# Get all students
@app.route('/students', methods=['GET'])
def get_students():
    connected, status = check_mongo_connection()
    if not connected:
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
        return jsonify({"error": f"MongoDB connection failed: {status}"}), 500

    data = request.json
    result = collection.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)})

# Get a student by ID
@app.route('/students/<id>', methods=['GET'])
def get_student(id):
    connected, status = check_mongo_connection()
    if not connected:
        return jsonify({"error": f"MongoDB connection failed: {status}"}), 500

    try:
        student = collection.find_one({"_id": ObjectId(id)})
    except:
        return jsonify({"error": "Invalid ID format"}), 400

    if student:
        student["_id"] = str(student["_id"])
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
