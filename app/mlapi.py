import os
import pickle

import pandas as pd
import uvicorn
from fastapi import FastAPI, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse

# Directory for model files
MODEL_DIR = "../../model_files/" # carpeta donde estaran cargados los modelos finales

# Initialize API
app = FastAPI()

# Load data processed and cleaned
data_path = "../../" # ruta para ubicar los datos limpios csv
data_df = pd.read_csv(data_path)

feature_max_min = {
    feature: (data_df[feature].max(), data_df[feature].min())
    for feature in data_df.columns
    if data_df[feature].dtype in ["float64", "int64"]
}  # para normalizar los datos antes de una prediccion, busca los datos float o int

@app.get("/", response_class=HTMLResponse) # cuando alguien entre a localhost entrara a un html
def read_root() -> HTMLResponse:
    """
    Use 'index.html' as HTML page.

    Inputs:
        - None.

    Outputs:
        - HTMLResponse: The content of 'index.html' served as an HTML page.
    """
    with open("index.html", "r") as f:
        return HTMLResponse(f.read()) # devolvera index.html 