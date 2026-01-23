# CKD Prediction App

**Chronic Kidney Disease Prediction System**  
*Group M - Scientific Programming Final Project (MHEDAS 2025-26)*

---

## Overview

A machine learning-powered web application for predicting Chronic Kidney Disease (CKD) based on clinical biomarkers. The system uses a K-Nearest Neighbors (KNN) classifier trained on patient data to provide real-time predictions through an intuitive web interface.

### Key Features

- **ML-Powered Predictions**: KNN model with 93.75% accuracy
- **Web Interface**: User-friendly form for inputting clinical values
- **Docker Ready**: Containerized for easy deployment
- **Model Metrics**: View detailed performance metrics

---

## Quick Start

### Option 1: Using Docker (Recommended)

```bash
# Pull and run the container
docker run -d --name ckd-app -p 8080:8000 inigoarriazu/ckd-prediction-app:latest
```

Then open your browser and go to: **http://localhost:8080**

### Option 2: Run Locally

```bash
# Clone the repository
git clone https://github.com/andreaperval-gap/SP_FinalProject.git
cd SP_FinalProject

# Install dependencies
pip install -r requirements.txt

# Run the application
cd app
uvicorn mlapi:app --host 0.0.0.0 --port 8000
```

Then open your browser and go to: **http://localhost:8000**

---

## Docker Commands

### Basic Commands

```bash
# Start the container
docker run -d --name ckd-app -p 8080:8000 inigoarriazu/ckd-prediction-app:latest

# Stop the container
docker stop ckd-app

# Remove the container
docker rm ckd-app

# View container logs
docker logs ckd-app
```

### Troubleshooting (Port Already in Use)

```bash
# Stop and remove existing container, then restart on a different port
docker stop ckd-app
docker rm ckd-app
docker run -d --name ckd-app -p 9000:8000 inigoarriazu/ckd-prediction-app:latest
```

Then access at: **http://localhost:9000**

---

## Project Structure

```
SP_FinalProject/
├── app/
│   ├── mlapi.py              # FastAPI application
│   ├── index.html            # Web interface
│   ├── img/                  # Static images
│   └── models/
│       ├── knn_k5.pkl        # Trained KNN model
│       └── knn_k5.metrics.txt # Model performance metrics
├── docs/
│   ├── Project_Report.md     # Full project report
│   ├── API_and_Docker_Guide.md
│   └── Docker_Commands_Guide.md
├── preprocessing.py          # Data preprocessing functions
├── Scientific_Programming.ipynb        # Analysis notebook
├── Scientific_Programming+modelos.ipynb # Models notebook
├── chronic_kindey_disease.csv          # Dataset
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Clinical Features

The model uses the following 11 clinical biomarkers for prediction:

| Feature | Description | Units |
|---------|-------------|-------|
| Age | Patient age | years |
| Blood Pressure | Diastolic BP | mmHg |
| Glucose | Blood glucose (random) | mgs/dl |
| Urea | Blood urea | mgs/dl |
| Creatinine | Serum creatinine | mgs/dl |
| Sodium | Serum sodium | mEq/L |
| Potassium | Serum potassium | mEq/L |
| Hemoglobin | Blood hemoglobin | gms |
| PCV | Packed cell volume | % |
| WBC | White blood cell count | cells/cumm |
| RBC Count | Red blood cell count | millions/cmm |

---

## Model Performance

| Metric | Value |
|--------|-------|
| **Accuracy** | 93.75% |
| **Precision (CKD)** | 0.96 |
| **Recall (CKD)** | 0.94 |
| **F1-Score (CKD)** | 0.95 |

**Confusion Matrix:**

```
              Predicted
              NOT CKD   CKD
Actual  NOT CKD   28      2
        CKD        3     47
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/models/` | GET | List available models |
| `/metrics/?model_name=<name>` | GET | Get model metrics |
| `/predict/` | POST | Submit prediction request |

---

## Team

**Group M** - Master in Health Data Science (MHEDAS 2025-26)

---

## License

This project was developed for educational purposes as part of the Scientific Programming course.

---

## Documentation

For more detailed information, see:

- [Project Report](docs/Project_Report.md)
- [API and Docker Guide](docs/API_and_Docker_Guide.md)
- [Docker Commands Guide](docs/Docker_Commands_Guide.md)
