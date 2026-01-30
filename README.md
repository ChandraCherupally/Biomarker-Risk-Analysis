# 🩺 Health Risk Prediction & Biomarker Analysis

## 📌 Project Overview
This project analyzes a large-scale healthcare dataset containing diagnostic test results to assess and predict common health conditions using data-driven techniques. The dataset includes key clinical biomarkers related to **diabetes, hypertension, anemia, and cholesterol disorders**.

The goal is to perform **end-to-end exploratory data analysis (EDA)** and demonstrate how these biomarkers can be leveraged to:
- Understand disease patterns
- Support preventive healthcare research
- Build predictive and risk-scoring models
- Design a composite **Health Score system (similar to a CIBIL score)**

---

## 📊 Dataset Description

The dataset consists of **25,000 individual health records** with diagnostic measurements and a labeled health condition.

### Target Variable
- **Condition**:  
  `Fit`, `Anemia`, `Hypertension`, `Diabetes`, `High_Cholesterol`

### Independent Variables (Biomarkers)
- Blood Glucose
- HbA1C
- Systolic Blood Pressure
- Diastolic Blood Pressure
- LDL Cholesterol
- HDL Cholesterol
- Triglycerides
- Haemoglobin
- MCV (Mean Corpuscular Volume)

All biomarkers are numeric, and the target variable is categorical.

---

## 🧪 Clinical Reference Ranges

Clinical reference ranges were verified using **MedlinePlus (NIH)**, a government-backed and globally accepted medical reference source.

| Biomarker | Unit | Normal Range |
|---------|------|--------------|
| Blood Glucose (Fasting) | mg/dL | 70 – 99 |
| HbA1C | % | 4.0 – 5.6 |
| Systolic BP | mmHg | 90 – 120 |
| Diastolic BP | mmHg | 60 – 80 |
| LDL | mg/dL | < 100 (optimal) |
| HDL | mg/dL | ≥ 40 (men), ≥ 50 (women) |
| Triglycerides | mg/dL | < 150 |
| Haemoglobin | g/dL | 13.5–17.5 (men), 12.0–15.5 (women) |
| MCV | fL | 80 – 100 |

---

## 🔍 Exploratory Data Analysis (EDA)

### Key Findings
- Minimal missing data (~0.65%), handled using **median imputation**
- No duplicate records
- Several biomarkers show **right-skewed distributions**
- Significant outliers observed in:
  - Blood Glucose
  - HbA1C
  - Diastolic BP
  - Triglycerides
- Strong clinical correlations:
  - Blood Glucose ↔ HbA1C
  - Systolic BP ↔ Diastolic BP
- Clear separation between **Fit** and **Diabetes / Pre-Diabetes** groups
- Class imbalance present, with `Fit` being the majority class

---

## 📈 Statistical Validation

- **ANOVA and hypothesis testing** confirmed statistically significant differences in key biomarkers across health conditions.
- Post-hoc analysis supports the diagnostic relevance of Blood Glucose, HbA1C, and Blood Pressure measures.

---

## 🧠 Health Score System 

This project proposes a **composite Health Score system**, similar to a **CIBIL credit score**, to summarize an individual’s overall health risk.

### Health Score Characteristics
- Combines multiple biomarkers into a single score (e.g., 0–100)
- Risk-weighted biomarkers based on clinical importance
- Sensitive to extreme (outlier) values
- Generates condition-specific sub-scores:
  - Diabetes Risk
  - Cardiovascular Risk
  - Anemia Risk etc.

### Output Example
- Overall Health Score (Low / Moderate / High Risk)
- Disease risk flags
- Key contributing biomarkers
- Actionable health insights

---

## 🤖 Machine Learning Applications

This dataset can be used to:
- Build disease classification models
- Develop health risk scoring systems
- Perform anomaly detection for early disease identification

### Modeling Considerations
- Feature engineering (e.g., LDL/HDL ratio, pulse pressure)
- Robust outlier handling (log transform, Winsorization)
- Class imbalance correction (SMOTE, stratified sampling)
- Model evaluation with clinical interpretability in mind

---

## 🛠️ Tools & Technologies
- Python
- Pandas, NumPy
- Matplotlib, Seaborn
- SciPy, Statsmodels
- Scikit-learn
- Jupyter Notebook

---

## 📌 Use Cases
- Preventive healthcare analytics
- Clinical decision support
- Insurance underwriting
- Health dashboards and reporting
- Academic and ML research

---

## ⚠️ Disclaimer
This project is intended for **educational and analytical purposes only**.  
It does **not** provide medical diagnosis or treatment recommendations.

---

## 📬 Author
Developed as part of a healthcare analytics and machine learning study.

---

⭐ *If you find this project useful, feel free to star the repository.*
