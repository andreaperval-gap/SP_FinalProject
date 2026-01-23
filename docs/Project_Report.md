# **Scientific Programming Final Project Report**

## **Chronic Kidney Disease (CKD) Prediction System**

### **Group M \- MHEDAS 2025-26**

Participants:

* ARRIAZU GARCIA IÑIGO  
* BORGE DE PRADA MIGUEL  
* GARCIA I PUIG ORIOL  
* PEREZ VALLE ANDREA  
* POSTIGO JULIO CESAR  
* TORRES ZAMORA GABRIEL  
* TUNKARA ABDOULAHE

## **1\. Objective of the Project**

This project aims to develop a machine learning system to predict Chronic Kidney Disease (CKD) using clinical biomarkers. The workflow encompasses **data preprocessing** and **exploratory analysis** of a 400-patient dataset, implementation and validation of classification models (KNN, Random Forest, Decision Tree), API development using FastAPI and finally Containerization and deployment using Docker for easy distribution and reproducibility.

The goal is to provide healthcare professionals with a tool that predicts CKD based on 11 key numerical biomarkers, including blood pressure, creatinine, hemoglobin, and cell counts.

## **2\. Analysis and Key Results**

### **2.1 Data Preprocessing Pipeline**

The dataset contained 400 patient records with 25 variables, presenting several data quality challenges: cryptic column names, missing values encoded as "?" strings, and erroneous outliers.

The preprocessing pipeline, implemented in `preprocessing.py`, addresses these issues sequentially: column renaming to clinically meaningful terminology, conversion of "?" to `np.nan`, and type conversion for numerical columns.

For outlier handling, statistical outliers in biomarkers such as creatinine and urea were retained, as elevated values are clinically expected in CKD patients. However, visual inspection revealed three clearly erroneous values: sodium \= 4.5 mEq/L and potassium \= 39, 47 mEq/L. Threshold values were set empirically (sodium \< 5, potassium \> 20\) to remove these observations.

Missing numerical values were imputed using MICE (Multiple Imputation by Chained Equations) with Linear Regression. For categorical variables, we implemented stratified imputation by age groups (0-20, 21-40, 41-60, 61+) using the most frequent value within each stratum. Finally, the redundant "rbc" column was removed, and numerical features were normalized using Min-Max scaling to the \[0,1\] range.

### **2.2 Exploratory Data Analysis**

Outlier analysis revealed patterns consistent with CKD pathophysiology. Creatinine exhibited the highest outlier fraction (13.3%), followed by urea (10.0%) and glucose (9.6%)—biomarkers characteristically elevated in CKD patients. Electrolytes showed lower outlier proportions: sodium (5.1%) and potassium (1.3%), reflecting tighter physiological regulation.

Variability analysis showed creatinine with the highest coefficient of variation (CV \= 1.87), followed by urea (CV \= 0.88), while sodium exhibited the lowest (CV \= 0.076). Correlation analysis identified expected relationships: PCV and hemoglobin showed very high correlation (r \> 0.9), both correlating strongly with RBC count.

Q-Q plots confirmed non-normal distributions for several variables, guiding our choice of Min-Max normalization over z-score standardization.

### **2.3 Model Implementation and Comparison**

Three classification algorithms were evaluated:

**K-Nearest Neighbors (k=5)**: Using only 11 numerical biomarkers, achieved 93.75% test accuracy with precision of 0.96 and recall of 0.94 for CKD detection.

**Random Forest**: Achieved 99.17% test accuracy but showed clear overfitting, with cross-validation accuracy dropping to 94.93%.

**Decision Tree**: Achieved approximately 93% accuracy with higher variance across validation folds.

### **2.4 Validation Strategy**

The dataset was partitioned into 80% training and 20% testing using stratified sampling (random\_state=42). Additionally, 5-fold Stratified K-Fold cross-validation was performed on the training set:

| Metric | Mean | Std |
| :---- | :---- | :---- |
| Accuracy | 0.915 | ±0.042 |
| Precision | 0.953 | ±0.017 |
| Recall | 0.908 | ±0.070 |
| F1-Score | 0.929 | ±0.037 |

The low standard deviations indicate consistent performance across folds and good generalization capability.

### **2.5 Model Selection**

**Selected Model: KNN (k=5)**

Selection rationale: consistent generalization (unlike Random Forest's overfitting), interpretability for clinical stakeholders, deployment simplicity requiring only 11 numerical inputs, appropriate precision-recall balance for screening, and fast inference time.

### **2.6 API Implementation**

The prediction system uses FastAPI with four endpoints: root (`/`) serving the HTML interface, `/models/` listing available models, `/metrics/` returning performance metrics, and `/predict/` accepting clinical values and returning predictions.

Normalization parameters (min/max values) are stored alongside the model, allowing users to input raw clinical values that are automatically normalized before prediction.

### **2.7 Docker Deployment**

Containerization uses `python:3.12-slim` as base image. The container exposes port 8000 internally, mapped to 8080 on host, launched via Uvicorn.

**Dockerfile Configuration:**

```
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/mlapi.py .
COPY app/index.html .
COPY app/models/ ./models/
COPY app/img/ ./img/
EXPOSE 8000
CMD ["uvicorn", "mlapi:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Deployment Commands:**

```shell
# Pull and run the container
docker run -d --name ckd-app -p 8080:8000 inigoarriazu/ckd-prediction-app:latest

# Access the application
# Navigate to: http://localhost:8080
```

---

## **3\. Conclusions**

This project delivered an end-to-end machine learning system for CKD prediction, achieving 93.75% accuracy using 11 readily available clinical biomarkers.

**Technical Contributions**

The preprocessing pipeline handles real-world clinical data challenges through dual imputation strategies (MICE for numerical, age-stratified for categorical variables). The validation framework combining holdout testing with stratified cross-validation confirmed the model's generalization capability.

**Clinical Relevance**

The recall of 0.94 ensures most CKD cases are identified, while precision of 0.96 minimizes false positives. The required biomarkers are routinely collected in standard clinical assessments, enabling integration into existing workflows.

**Limitations and Future Work**

The dataset comprises only 400 patients from a single source, limiting external validity. The binary classification does not capture CKD staging (1-5). Future extensions include validation on external datasets, multi-class staging prediction, and integration of longitudinal data for progression modeling.

### **References:** 

**Repository**: [https://github.com/andreaperval-gap/SP\_FinalProject](https://github.com/andreaperval-gap/SP_FinalProject)   
**Docker Image**:   
`docker run -d --name ckd-app -p 8080:8000 inigoarriazu/ckd-prediction-app:latest`  
**Access URL**: [http://localhost:8080](http://localhost:8080) (after running Docker container)

