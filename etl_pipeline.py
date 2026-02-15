import sqlite3
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime

# ==================================================
# Project Paths
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
DB_PATH = DATA_DIR / "Health_markers_datasets.db"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# ==================================================
# Logging Configuration
# ==================================================

logging.basicConfig(
    filename=LOG_DIR / "etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

# ==================================================
# Clinical Validation Ranges
# ==================================================

CLINICAL_RANGES = {
    "Blood_glucose": (40, 500),
    "HbA1C": (3, 20),
    "Systolic_BP": (70, 250),
    "Diastolic_BP": (40, 150),
    "LDL": (20, 400),
    "HDL": (10, 150),
    "Triglycerides": (30, 1000),
    "Haemoglobin": (5, 25),
    "MCV": (50, 130)
}

NUMERIC_COLS = list(CLINICAL_RANGES.keys())

# ==================================================
# Extract
# ==================================================

def extract_table(conn):
    query = "SELECT * FROM Health_markers_dataset;"
    df = pd.read_sql_query(query, conn)
    logging.info(f"Extracted rows: {len(df)}")
    return df

# ==================================================
# Raw Preservation
# ==================================================

def preserve_raw_table(df, conn):
    df.to_sql(
        "health_markers_raw",
        con=conn,
        if_exists="append",
        index=False
    )
    logging.info("Raw table preserved")

# ==================================================
# Missing Report
# ==================================================

def calculate_missing_report(df):
    missing_report = (
        df.isnull()
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )
    missing_report.columns = ["Column", "Missing_Percentage"]
    logging.info(f"\nMissing % Report:\n{missing_report}")
    return missing_report

# ==================================================
# Clinical Range Validation
# ==================================================

def validate_clinical_ranges(df):

    for col, (min_val, max_val) in CLINICAL_RANGES.items():
        df[f"{col}_invalid"] = (
            (df[col] < min_val) | (df[col] > max_val)
        )

    df["invalid_count"] = df[
        [c for c in df.columns if c.endswith("_invalid")]
    ].sum(axis=1)

    return df

# ==================================================
# Outlier Detection
# ==================================================

def detect_outliers(df):

    for col in NUMERIC_COLS:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        df[f"{col}_outlier"] = (
            (df[col] < lower) | (df[col] > upper)
        )

    df["outlier_count"] = df[
        [c for c in df.columns if c.endswith("_outlier")]
    ].sum(axis=1)

    return df

# ==================================================
# Data Quality Scoring
# ==================================================

def calculate_quality_score(df):

    missing_score = df[NUMERIC_COLS].isnull().sum(axis=1)
    invalid_score = df["invalid_count"]
    outlier_score = df["outlier_count"]

    df["quality_score"] = (
        100
        - (missing_score * 5)
        - (invalid_score * 10)
        - (outlier_score * 3)
    ).clip(lower=0)

    return df

# ==================================================
# Clean + Transform
# ==================================================

def clean_dataframe(df):

    for col in NUMERIC_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["Condition"] = (
        df["Condition"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    calculate_missing_report(df)

    df = validate_clinical_ranges(df)
    df = detect_outliers(df)
    df = calculate_quality_score(df)

    return df

# ==================================================
# Create Analytics Layer (NO diagnostic columns)
# ==================================================

def create_analytics_layer(conn):

    analytics_query = """
    CREATE TABLE IF NOT EXISTS health_markers_analytics AS
    SELECT
        Blood_glucose,
        HbA1C,
        Systolic_BP,
        Diastolic_BP,
        LDL,
        HDL,
        Triglycerides,
        Haemoglobin,
        MCV,
        Condition
    FROM health_markers_curated
    WHERE quality_score >= 80;
    """

    conn.execute("DROP TABLE IF EXISTS health_markers_analytics;")
    conn.execute(analytics_query)
    conn.commit()

    logging.info("Analytics layer created")

# ==================================================
# Metadata Versioning
# ==================================================

def update_metadata(conn, rows_processed):

    metadata = pd.DataFrame([{
        "run_timestamp": datetime.now(),
        "rows_processed": rows_processed,
        "pipeline_version": "v1.0",
        "source_table": "Health_markers_dataset"
    }])

    metadata.to_sql(
        "etl_metadata",
        con=conn,
        if_exists="append",
        index=False
    )

# ==================================================
# Main ETL Flow
# ==================================================

if __name__ == "__main__":

    logging.info("=========== ETL STARTED ===========")

    conn = sqlite3.connect(DB_PATH)

    try:
        # 1. Extract
        df_extract = extract_table(conn)

        # 2. Preserve Raw
        preserve_raw_table(df_extract, conn)

        # 3. Clean + Quality Layer
        df_clean = clean_dataframe(df_extract)

        # 4. Load Curated Layer (WITH diagnostics)
        df_clean.to_sql(
            "health_markers_curated",
            con=conn,
            if_exists="replace",
            index=False
        )

        # 5. Create Analytics Layer (WITHOUT diagnostics)
        create_analytics_layer(conn)

        # 6.  Metadata
        update_metadata(conn, len(df_clean))

        logging.info("=========== ETL COMPLETED SUCCESSFULLY ===========")
        print("ETL completed successfully")

    except Exception as e:
        logging.error(f"ETL failed: {e}")
        print("ETL failed. Check logs.")

    finally:
        conn.close()
