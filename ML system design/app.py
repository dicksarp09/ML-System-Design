from flask import Flask, request, jsonify
import pandas as pd
import joblib

# Load the trained pipeline/model
model = joblib.load("performance_pipeline.pkl")  # Make sure this is the pipeline object

app = Flask(__name__)

@app.route("/")
def home():
    return "Student Pass Prediction API is running"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()  # Expect JSON input
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Convert JSON to DataFrame (pipeline handles preprocessing)
        df = pd.DataFrame([data])

        # Make prediction
        prediction = model.predict(df)

        return jsonify({"passed": int(prediction[0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
