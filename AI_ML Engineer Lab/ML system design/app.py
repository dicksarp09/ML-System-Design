# app.py
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import pickle
import pandas as pd

# Load the trained pipeline
try:
    with open("performance_pipeline.pkl", "rb") as f:
        model = pickle.load(f)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

app = FastAPI(title="Student Pass Prediction API")

@app.get("/")
def read_root():
    return {"message": "Student Pass Prediction API is running"}

@app.get("/predict")
def predict(
    school: str = Query(...),
    sex: str = Query(...),
    age: int = Query(...),
    address: str = Query(...),
    famsize: str = Query(...),
    Pstatus: str = Query(...),
    Medu: int = Query(...),
    Fedu: int = Query(...),
    Mjob: str = Query(...),
    Fjob: str = Query(...),
    reason: str = Query(...),
    guardian: str = Query(...),
    traveltime: int = Query(...),
    studytime: int = Query(...),
    failures: int = Query(...),
    schoolsup: str = Query(...),
    famsup: str = Query(...),
    paid: str = Query(...),
    activities: str = Query(...),
    nursery: str = Query(...),
    higher: str = Query(...),
    internet: str = Query(...),
    romantic: str = Query(...),
    famrel: int = Query(...),
    freetime: int = Query(...),
    goout: int = Query(...),
    Dalc: int = Query(...),
    Walc: int = Query(...),
    health: int = Query(...),
    absences: int = Query(...),
    G1: int = Query(...),
    G2: int = Query(...),
    G3: int = Query(...),
    dataset: str = Query(...)
):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        # Build DataFrame from query parameters
        data = {
            "school": school, "sex": sex, "age": age, "address": address,
            "famsize": famsize, "Pstatus": Pstatus, "Medu": Medu, "Fedu": Fedu,
            "Mjob": Mjob, "Fjob": Fjob, "reason": reason, "guardian": guardian,
            "traveltime": traveltime, "studytime": studytime, "failures": failures,
            "schoolsup": schoolsup, "famsup": famsup, "paid": paid, "activities": activities,
            "nursery": nursery, "higher": higher, "internet": internet, "romantic": romantic,
            "famrel": famrel, "freetime": freetime, "goout": goout, "Dalc": Dalc,
            "Walc": Walc, "health": health, "absences": absences, "G1": G1, "G2": G2,
            "G3": G3, "dataset": dataset
        }
        df = pd.DataFrame([data])

        # Predict
        prediction = model.predict(df)
        return {"passed": int(prediction[0])}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
