from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
import traceback
import pandas as pd
from database.models import Base, LeadRecord
from database.db import engine, SessionLocal
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

# Initialize DB and app
Base.metadata.create_all(bind=engine)
app = FastAPI()

# Load model and preprocessing artifacts
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
# Load encoders
with open("label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)

# with open("model_pipeline.pkl", "rb") as f:
#     pipeline_model = pickle.load(f)

from typing import Optional


class LeadInput(BaseModel):
    Lead_Number: int
    Lead_Origin: str
    Lead_Source: str
    Do_Not_Email: str
    Do_Not_Call: str
    TotalVisits: float
    Total_Time_Spent_on_Website: float
    Page_Views_Per_Visit: float
    Last_Activity: str
    Country: str
    Specialization: str
    How_did_you_hear_about_X_Education: Optional[str]
    What_is_your_current_occupation: str
    What_matters_most_to_you_in_choosing_a_course: str
    Search: str
    Magazine: str
    Newspaper_Article: str
    X_Education_Forums: str
    Newspaper: str
    Digital_Advertisement: str
    Through_Recommendations: str
    Receive_More_Updates_About_Our_Courses: str
    Tags: str
    Lead_Quality: str
    Update_me_on_Supply_Chain_Content: str
    Get_updates_on_DM_Content: str
    Lead_Profile: str
    City: Optional[str]
    Asymmetrique_Activity_Index: Optional[str]
    Asymmetrique_Profile_Index: Optional[str]
    Asymmetrique_Activity_Score: Optional[float]
    Asymmetrique_Profile_Score: Optional[float]
    I_agree_to_pay_the_amount_through_cheque: str
    A_free_copy_of_Mastering_The_Interview: str
    Last_Notable_Activity: str


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/predict")
def predict(lead: LeadInput):
    try:
        lead_dict = lead.model_dump()

        with get_db() as db:
            existing = db.query(LeadRecord).filter(LeadRecord.Lead_Number == lead_dict['Lead_Number']).first()
            if existing:
                print("Score:", existing.score)
                # If the lead already exists, return a message
                return { "message": "Lead already exists in the database."}

        normalized_dict = {key.replace('_', ' '): value for key, value in lead_dict.items()}
        df = pd.DataFrame([normalized_dict])
        # Ensure all columns are present
        missing = set(model.feature_names_in_) - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")

        for col in list(label_encoders):
            df[col] = df[col].fillna('unknown')  # Fill missing with placeholder
            df[col] = label_encoders[col].transform(df[col])

        df = df.astype(float)

        prob = model.predict_proba(df)[0][1]


        score = float(np.round(float(prob) * 100, 2))
        print("real score", score)
        logger.info("The Lead Score Is: %s", score)

        # Save  input + score to DB
        record = LeadRecord(**lead_dict, score=score)
        with get_db() as db:
            db.add(record)
            db.commit()
            db.refresh(record)
            db.close()

        return {"score": score}

    except Exception as e:
        print("Error occurred:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


#Pipeline test (Ignore this)
    # test_df = pd.DataFrame([normalized_dict])
    #
    # test_prob = pipeline_model.predict_proba(test_df)[0][1]
    # test_score = float(np.round(float(test_prob) * 100, 2))
    #
    # print("The Lead Score Is: %s", test_score)