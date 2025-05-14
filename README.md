# 🎯 ML Lead Scoring Prediction API

This project is a machine learning-based REST API that predicts the conversion probability of marketing leads. It uses a trained classification model wrapped in a preprocessing pipeline and exposes predictions via a FastAPI service.

---

## 📦 Features

- 🔍 Predicts lead conversion probability based on lead attributes.
- 🧠 ML model with preprocessing pipeline (handling missing values, encoding).
- 🗃️ Stores leads and prediction scores in a PostgreSQL database.
- 📤 Accepts JSON input and returns a conversion score percentage.

---

## ⚙️ Tech Stack

- **Backend:** Python, FastAPI
- **Modeling:** scikit-learn (RandomForest)
- **Database:** PostgreSQL (SQLAlchemy ORM)
- **Packaging:** `pickle` for model persistence

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/IdanEngel/ML-Leads-Prediction.git
cd ML-Leads-Prediction
```

### 2. Set up the environment and install dependcies
```bash
DATABASE_PASSWORD=your_password
DATABASE_PORT = your_port
DATABASE_HOST = your_host
```
```bash
pip install -r requirements.txt
```

### 3. Run the server
```bash
uvicorn predictor.main:app --reload
```
