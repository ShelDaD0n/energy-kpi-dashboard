import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

DB_URL = "postgresql+psycopg2://sheldadon@localhost/energy_db"

def load_data():
    print("Loading cleaned data...")
    df = pd.read_csv("data/cleaned_generation.csv")
    print(f"Loaded {len(df)} rows")

    print("Connecting to database...")
    engine = create_engine(DB_URL)

    print("Writing to generation table...")
    df.to_sql("generation", engine, if_exists="replace", index=False)
    print("Done — generation table created")

    # Verify it loaded correctly
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM generation"))
        count = result.scalar()
        print(f"Rows in database: {count}")

def run_queries():
    engine = create_engine(DB_URL)

    with engine.connect() as conn:
        print("\n--- Total MWh by month ---")
        result = conn.execute(text("""
            SELECT month, ROUND(SUM(generation_mwh)::numeric, 2) AS total_mwh
            FROM generation
            GROUP BY month
            ORDER BY month
        """))
        for row in result:
            print(f"  Month {row[0]}: {row[1]:,} MWh")

        print("\n--- Top 5 highest generation hours ---")
        result = conn.execute(text("""
            SELECT timestamp, generation_mwh
            FROM generation
            ORDER BY generation_mwh DESC
            LIMIT 5
        """))
        for row in result:
            print(f"  {row[0]}: {row[1]:,} MWh")

        print("\n--- Average capacity factor by month ---")
        result = conn.execute(text("""
            SELECT month, ROUND(AVG(capacity_factor_pct)::numeric, 2) AS avg_capacity_factor
            FROM generation
            GROUP BY month
            ORDER BY month
        """))
        for row in result:
            print(f"  Month {row[0]}: {row[1]}%")

if __name__ == "__main__":
    load_data()
    run_queries()