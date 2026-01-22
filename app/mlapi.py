from pathlib import Path
import joblib
import numpy as np

from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# --- Paths (relative to this file) ---
APP_DIR = Path(__file__).parent                 # .../app
MODELS_DIR = APP_DIR / "models"                # .../app/models
INDEX_HTML = APP_DIR / "index.html"            # .../app/index.html

# Create the FastAPI application
app = FastAPI()

# Static image from /img/*
app.mount("/img", StaticFiles(directory=str(APP_DIR / "img")), name="img")

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def read_root() -> HTMLResponse:
    """
    Use 'index.html' as HTML page.

    Inputs:
        - None.

    Outputs:
        - HTMLResponse: The content of 'index.html' as an HTML page.
    """
    index_path = APP_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html not found")
    return HTMLResponse(index_path.read_text(encoding="utf-8"))

@app.get("/models/")
def list_models() -> list[str]:
    """
    List the model file stored in the models.

    Inputs:
        - None.

    Outputs:
        - list[str]: Model filename.
    """
    if not MODELS_DIR.exists():
        return []
    return sorted([p.name for p in MODELS_DIR.glob("*.pkl")])

@app.get("/metrics/", response_class=PlainTextResponse)
def get_metrics(model_name: str) -> str:
    """
    Return the metrics for the model.

    Inputs:
        - model_name (str): The model filename in the UI.

    Outputs:
        - str: Text content from the corresponding metrics file.
    """
    metrics_path = MODELS_DIR / (Path(model_name).stem + ".metrics.txt")
    if not metrics_path.exists():
        raise HTTPException(status_code=404, detail="Metrics not found")
    return metrics_path.read_text(encoding="utf-8")

@app.post("/predict/")
def predict(
    model_name: str = Form(...),

    age: float = Form(...),
    blood_pressure: float = Form(...),
    glucose: float = Form(...),
    urea: float = Form(...),
    creatinine: float = Form(...),
    sodium: float = Form(...),
    potassium: float = Form(...),
    hemoglobin: float = Form(...),
    pcv: float = Form(...),
    wbc: float = Form(...),
    rbc_count: float = Form(...),
) -> JSONResponse:
    """
    Predict CKD using model and clinical values.

    Notes:
        - The user inputs are "raw".
        - The model was trained on min-max normalized features (0-1).
        - We load mins/maxs from the model and normalize before predicting.

    Inputs:
        - model_name (str)
        - age (float)
        - blood_pressure (float)
        - glucose (float)
        - urea (float)
        - creatinine (float)
        - sodium (float)
        - potassium (float)
        - hemoglobin (float)
        - pcv (float)
        - wbc (float)
        - rbc_count (float)

    Outputs:
        - JSONResponse: JSON containing the model name, numeric prediction, and label.
    """
    model_path = MODELS_DIR / model_name
    if not model_path.exists():
        raise HTTPException(status_code=404, detail="Model not found")
    bundle = joblib.load(model_path)
    model = bundle["model"]
    features = bundle["features"]
    mins = bundle["mins"]
    maxs = bundle["maxs"]
    row = {
        "age": age,
        "blood_pressure": blood_pressure,
        "glucose": glucose,
        "urea": urea,
        "creatinine": creatinine,
        "sodium": sodium,
        "potassium": potassium,
        "hemoglobin": hemoglobin,
        "pcv": pcv,
        "wbc": wbc,
        "rbc_count": rbc_count,
    }
    # Normalize using training min/max
    x_norm = []
    for f in features:
        denom = (maxs[f] - mins[f])
        x_norm.append(0.0 if denom == 0 else (row[f] - mins[f]) / denom)
    # Convert to numpy array 
    X = np.array([x_norm], dtype=float)
    # Predict
    pred = int(model.predict(X)[0])
    label = "CKD" if pred == 1 else "NOT CKD"
    # Return JSON
    return JSONResponse({"model": model_name, "prediction": pred, "label": label})