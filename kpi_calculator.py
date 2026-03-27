import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

DB_URL = "postgresql+psycopg2://sheldadon@localhost/energy_db"

def calculate_kpis():
    engine = create_engine(DB_URL)

    with engine.connect() as conn:
        print("Calculating KPIs...\n")

        # KPI 1: Total energy generated per month
        total_mwh = conn.execute(text("""
            SELECT month,
                   ROUND(SUM(generation_mwh)::numeric, 2) AS total_mwh
            FROM generation
            GROUP BY month
            ORDER BY month
        """)).fetchall()

        # KPI 2: Average capacity factor per month
        avg_capacity = conn.execute(text("""
            SELECT month,
                   ROUND(AVG(capacity_factor_pct)::numeric, 2) AS avg_capacity_factor_pct
            FROM generation
            GROUP BY month
            ORDER BY month
        """)).fetchall()

        # KPI 3: Estimated revenue per month (assume $45 per MWh)
        revenue = conn.execute(text("""
            SELECT month,
                   ROUND((SUM(generation_mwh) * 45)::numeric, 2) AS estimated_revenue_usd
            FROM generation
            GROUP BY month
            ORDER BY month
        """)).fetchall()

        # KPI 4: Peak generation hour per month
        peak_hour = conn.execute(text("""
            SELECT month, hour, MAX(generation_mwh) AS peak_mwh
            FROM generation
            GROUP BY month, hour
            ORDER BY month, peak_mwh DESC
        """)).fetchall()

        # Build KPI summary dataframe
        kpi_rows = []
        for i in range(len(total_mwh)):
            month = total_mwh[i][0]
            peak = max(
                [r for r in peak_hour if r[0] == month],
                key=lambda x: x[2]
            )
            kpi_rows.append({
                "month": month,
                "total_mwh": total_mwh[i][1],
                "avg_capacity_factor_pct": avg_capacity[i][1],
                "estimated_revenue_usd": revenue[i][1],
                "peak_hour": peak[1],
                "peak_mwh": peak[2]
            })

        kpi_df = pd.DataFrame(kpi_rows)

        # Print KPI summary
        print("=== Energy KPI Summary — Q1 2024 (California) ===\n")
        for _, row in kpi_df.iterrows():
            print(f"Month {int(row['month'])}:")
            print(f"  Total generation:      {row['total_mwh']:,} MWh")
            print(f"  Avg capacity factor:   {row['avg_capacity_factor_pct']}%")
            print(f"  Estimated revenue:     ${row['estimated_revenue_usd']:,}")
            print(f"  Peak hour:             {int(row['peak_hour'])}:00 ({row['peak_mwh']:,} MWh)")
            print()

        # Save KPI summary to database
        kpi_df.to_sql("kpi_summary", engine, if_exists="replace", index=False)
        print("KPI summary saved to kpi_summary table in database")

        # Also save to CSV
        kpi_df.to_csv("data/kpi_summary.csv", index=False)
        print("KPI summary saved to data/kpi_summary.csv")

if __name__ == "__main__":
    calculate_kpis()