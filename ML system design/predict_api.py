# predict_api.py
from flask import Flask, request, jsonify
import pickle

# Load the trained ML model
with open("performance_pipeline.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)

# Define required features
REQUIRED_FEATURES = ["school", "sex", "age", "address", "Medu", "Fedu"]

# Input validation
def validate_input(data):
    if isinstance(data, dict):
        data = [data]  # Convert single record to list

    validated = []
    errors = []

    for i, record in enumerate(data):
        missing = [f for f in REQUIRED_FEATURES if f not in record]
        if missing:
            errors.append({"index": i, "missing_features": missing})
        else:
            validated.append(record)

    return validated, errors

# Prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    # Validate input
    valid_records, errors = validate_input(data)
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    # Prepare features for the model (simple encoding example)
    X = []
    for record in valid_records:
        X.append([
            1 if record["school"] == "GP" else 0,
            1 if record["sex"] == "F" else 0,
            int(record["age"]),
            1 if record["address"] == "U" else 0,
            int(record["Medu"]),
            int(record["Fedu"])
        ])

    # Make predictions
    preds = model.predict(X)

    # Return predictions along with input
    results = []
    for record, pred in zip(valid_records, preds):
        results.append({"input": record, "prediction": int(pred)})

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
