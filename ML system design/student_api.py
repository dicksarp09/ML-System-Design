from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib

# Load your trained pipeline (must be a fitted pipeline)
try:
    model = joblib.load("performance_pipeline.pkl")
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

# Define input schema
class StudentData(BaseModel):
    school: str
    sex: str
    age: int
    address: str
    famsize: str
    Pstatus: str
    Medu: int
    Fedu: int
    Mjob: str
    Fjob: str
    reason: str
    guardian: str
    traveltime: int
    studytime: int
    failures: int
    schoolsup: str
    famsup: str
    paid: str
    activities: str
    nursery: str
    higher: str
    internet: str
    romantic: str
    famrel: int
    freetime: int
    goout: int
    Dalc: int
    Walc: int
    health: int
    absences: int
    G1: int
    G2: int
    G3: int
    dataset: str

# Initialize FastAPI app
app = FastAPI(title="Student Pass Prediction API")

@app.get("/")
def read_root():
    return {"message": "Student Pass Prediction API is running"}

@app.post("/predict")
def predict(student: StudentData):
    try:
        # Convert input to DataFrame
        df = pd.DataFrame([student.dict()])
        
        # DEBUG: print DataFrame received
        print("DataFrame for prediction:\n", df)
        
        # Make prediction
        prediction = model.predict(df)
        
        return {"passed": int(prediction[0])}
    
    except Exception as e:
        # DEBUG: print exact error in terminal
        print("Prediction error:", e)
        # Return JSON error
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib

# Load your trained pipeline (must be a fitted pipeline)
try:
    model = joblib.load("performance_pipeline.pkl")
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

# Define input schema
class StudentData(BaseModel):
    school: str
    sex: str
    age: int
    address: str
    famsize: str
    Pstatus: str
    Medu: int
    Fedu: int
    Mjob: str
    Fjob: str
    reason: str
    guardian: str
    traveltime: int
    studytime: int
    failures: int
    schoolsup: str
    famsup: str
    paid: str
    activities: str
    nursery: str
    higher: str
    internet: str
    romantic: str
    famrel: int
    freetime: int
    goout: int
    Dalc: int
    Walc: int
    health: int
    absences: int
    G1: int
    G2: int
    G3: int
    dataset: str

# Initialize FastAPI app
app = FastAPI(title="Student Pass Prediction API")

@app.get("/")
def read_root():
    return {"message": "Student Pass Prediction API is running"}

@app.post("/predict")
def predict(student: StudentData):
    try:
        # Convert input to DataFrame
        df = pd.DataFrame([student.dict()])
        
        # DEBUG: print DataFrame received
        print("DataFrame for prediction:\n", df)
        
        # Make prediction
        prediction = model.predict(df)
        
        return {"passed": int(prediction[0])}
    
    except Exception as e:
        # DEBUG: print exact error in terminal
        print("Prediction error:", e)
        # Return JSON error
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
