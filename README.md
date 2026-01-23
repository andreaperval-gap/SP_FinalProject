# CKD Prediction App

**Chronic Kidney Disease Prediction using Machine Learning**

Proyecto final del curso Scientific Programming (MHEDAS 2025-26) - Grupo M

## Descripcion

Esta aplicacion web permite predecir la probabilidad de que un paciente tenga Enfermedad Renal Cronica (CKD - Chronic Kidney Disease) basandose en parametros clinicos y de laboratorio. Utiliza modelos de Machine Learning entrenados con datos reales de pacientes.

## Tabla de Contenidos

- [Caracteristicas](#caracteristicas)
- [Dataset](#dataset)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalacion](#instalacion)
  - [Con Docker (Recomendado)](#con-docker-recomendado)
  - [Instalacion Local](#instalacion-local)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [Variables de Entrada](#variables-de-entrada)
- [Modelos](#modelos)
- [Equipo](#equipo)

## Caracteristicas

- Interfaz web intuitiva para introducir datos clinicos
- Prediccion en tiempo real de CKD
- API REST con FastAPI
- Soporte para multiples modelos de ML
- Visualizacion de metricas del modelo
- Despliegue con Docker

## Dataset

El proyecto utiliza el dataset **Chronic Kidney Disease** que contiene 400 registros de pacientes con 25 atributos clinicos. Los datos incluyen:

- Datos demograficos (edad)
- Mediciones de presion arterial
- Analisis de orina (gravedad especifica, albumina, azucar, celulas)
- Analisis de sangre (glucosa, urea, creatinina, sodio, potasio, hemoglobina)
- Conteo de celulas sanguineas (WBC, RBC)
- Condiciones medicas previas (hipertension, diabetes, enfermedad coronaria)

**Fuente**: UCI Machine Learning Repository

## Estructura del Proyecto

```
SP_FinalProject/
├── app/
│   ├── mlapi.py           # API FastAPI principal
│   ├── index.html         # Interfaz web
│   ├── models/            # Modelos entrenados (.pkl)
│   │   ├── knn_k5.pkl
│   │   └── knn_k5.metrics.txt
│   └── img/               # Imagenes para la interfaz
├── Scientific_Programming.ipynb        # Notebook de analisis y desarrollo
├── Scientific_Programming+modelos.ipynb # Notebook con entrenamiento de modelos
├── preprocessing.py       # Funciones de preprocesamiento de datos
├── chronic_kindey_disease.csv  # Dataset
├── Dockerfile             # Configuracion Docker
├── requirements.txt       # Dependencias Python
└── README.md
```

## Instalacion

### Con Docker (Recomendado)

1. **Descargar y ejecutar la imagen Docker:**
```bash
docker run -d --name ckd-app -p 8080:8000 inigoarriazu/ckd-prediction-app:latest
```

2. **Abrir en el navegador:**
```
http://localhost:8080
```

3. **Comandos utiles de Docker:**
```bash
# Detener el contenedor
docker stop ckd-app

# Eliminar el contenedor
docker rm ckd-app

# Reiniciar con un puerto diferente (ejemplo: 9000)
docker run -d --name ckd-app -p 9000:8000 inigoarriazu/ckd-prediction-app:latest
```

### Instalacion Local

1. **Clonar el repositorio:**
```bash
git clone https://github.com/MBorge/SP_FinalProject.git
cd SP_FinalProject
```

2. **Crear entorno virtual (opcional pero recomendado):**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o en Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicacion:**
```bash
cd app
uvicorn mlapi:app --host 0.0.0.0 --port 8000
```

5. **Abrir en el navegador:**
```
http://localhost:8000
```

## Uso

1. Acceder a la interfaz web
2. Seleccionar el modelo de prediccion deseado
3. Introducir los valores clinicos del paciente
4. Hacer clic en "Predict" para obtener el resultado
5. El sistema mostrara si el paciente tiene probabilidad de CKD o no

## API Endpoints

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | `/` | Interfaz web principal |
| GET | `/models/` | Lista de modelos disponibles |
| GET | `/metrics/?model_name={nombre}` | Metricas del modelo seleccionado |
| POST | `/predict/` | Realizar prediccion con datos del paciente |

### Ejemplo de uso de la API

```bash
# Listar modelos disponibles
curl http://localhost:8000/models/

# Obtener metricas de un modelo
curl "http://localhost:8000/metrics/?model_name=knn_k5.pkl"

# Realizar una prediccion
curl -X POST http://localhost:8000/predict/ \
  -F "model_name=knn_k5.pkl" \
  -F "age=50" \
  -F "blood_pressure=80" \
  -F "glucose=120" \
  -F "urea=40" \
  -F "creatinine=1.2" \
  -F "sodium=140" \
  -F "potassium=4.5" \
  -F "hemoglobin=14" \
  -F "pcv=42" \
  -F "wbc=8000" \
  -F "rbc_count=5.0"
```

## Variables de Entrada

| Variable | Descripcion | Unidades/Rango Tipico |
|----------|-------------|----------------------|
| `age` | Edad del paciente | anos |
| `blood_pressure` | Presion arterial diastolica | mm/Hg |
| `glucose` | Glucosa en sangre | mg/dL |
| `urea` | Urea en sangre | mg/dL |
| `creatinine` | Creatinina serica | mg/dL |
| `sodium` | Sodio serico | mEq/L |
| `potassium` | Potasio serico | mEq/L |
| `hemoglobin` | Hemoglobina | g/dL |
| `pcv` | Volumen de celulas empaquetadas | % |
| `wbc` | Conteo de globulos blancos | cells/cumm |
| `rbc_count` | Conteo de globulos rojos | millions/cmm |

## Modelos

### KNN (K-Nearest Neighbors) con k=5
- **Accuracy**: 93.75%
- **Precision (CKD)**: 96%
- **Recall (CKD)**: 94%
- **F1-Score (CKD)**: 95%

El modelo utiliza normalizacion min-max (0-1) para las variables numericas. Los valores de normalizacion se guardan junto con el modelo para asegurar predicciones consistentes.

## Preprocesamiento de Datos

El pipeline de preprocesamiento incluye:

1. **Renombrado de columnas** - Nombres mas descriptivos
2. **Tratamiento de valores faltantes** - Conversion de "?" a NaN
3. **Conversion de tipos** - Columnas numericas a tipo numerico
4. **Limpieza de categorias** - Eliminacion de espacios en blanco
5. **Eliminacion de outliers** - Basado en analisis visual y conocimiento del dominio
6. **Imputacion numerica** - MICE (Multiple Imputation by Chained Equations)
7. **Imputacion categorica** - Estratificada por grupos de edad
8. **Eliminacion de columnas redundantes**
9. **Normalizacion** - Min-Max scaling (0-1)

## Tecnologias Utilizadas

- **Backend**: Python 3.12, FastAPI, Uvicorn
- **ML**: scikit-learn, joblib, NumPy
- **Data Processing**: Pandas, feature-engine
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Docker

## Equipo - Grupo M

Proyecto desarrollado para el curso de Scientific Programming del Master en Health Data Science (MHEDAS 2025-26).

## Licencia

Este proyecto es parte del trabajo academico del curso Scientific Programming (MHEDAS 2025-26).

---

**Nota**: Este proyecto es con fines educativos y de investigacion. No debe utilizarse como herramienta de diagnostico medico real sin la supervision de profesionales de la salud.
