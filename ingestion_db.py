import pandas as pd
from sqlalchemy import create_engine
import logging
import time
from pathlib import Path


# --------------------------------------------------
# Project Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
DB_PATH = BASE_DIR / "data/Health_markers_datasets.db"


# Ensure required folders exist
LOG_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# Logging Configuration
# --------------------------------------------------
logger = logging.getLogger(__name__)

logging.basicConfig(
    filename=LOG_DIR / "ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)


# --------------------------------------------------
# Database Engine - Creating Bookings.db database
# --------------------------------------------------

engine = create_engine(f"sqlite:///{DB_PATH}")


# --------------------------------------------------
# Functions
# --------------------------------------------------

def ingest_db(df: pd.DataFrame, table_name: str, engine):
    """
    Ingest a dataframe into SQLite database.
    Replaces table if it already exists.
    """
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)


def load_raw_data():
    """
    Load all CSV files from data directory
    and ingest into SQLite database.
    """
    start = time.time()

    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data directory not found: {DATA_DIR}")

    for file_path in DATA_DIR.glob("*.csv"):
        try:
            df = pd.read_csv(file_path)
            logging.info(f"Ingesting {file_path.name} into DB")
            ingest_db(df, file_path.stem, engine)
        except Exception as e:
            logging.error(f"Failed processing {file_path.name}: {e}")

    end = time.time()

    total_time = round((end - start) / 60, 2)
    logging.info("------------- Ingestion Complete --------------------")
    logging.info(f"Total Time Taken: {total_time} minutes")

    print(f"Ingestion completed in {total_time} minutes")


# --------------------------------------------------
# Entry Point
# --------------------------------------------------

if __name__ == "__main__":
    load_raw_data()
