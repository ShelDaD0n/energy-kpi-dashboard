import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

DB_URL = "postgresql+psycopg2://sheldadon@localhost/energy_db"

REPORT_DATE = datetime.today().strftime("%Y-%m-%d")
REPORTS_DIR = "data/reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

def fetch_data(engine):
    with engine.connect() as conn:
        generation = pd.read_sql("SELECT * FROM generation", conn)
        kpis = pd.read_sql("SELECT * FROM kpi_summary", conn)
    return generation, kpis

def plot_monthly_generation(kpis):
    fig, ax = plt.subplots(figsize=(8, 5))
    months = ["January", "February", "March"]
    values = kpis["total_mwh"].astype(float).tolist()

    bars = ax.bar(months, values, color=["#2196F3", "#1976D2", "#0D47A1"], width=0.5)

    ax.set_title("Total Net Generation by Month — Q1 2024", fontsize=13, pad=15)
    ax.set_ylabel("Total Generation (MWh)", fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.set_ylim(0, max(values) * 1.2)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 100000,
                f"{val:,.0f}", ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    path = f"{REPORTS_DIR}/monthly_generation_{REPORT_DATE}.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")

def plot_capacity_factor(kpis):
    fig, ax = plt.subplots(figsize=(8, 5))
    months = ["January", "February", "March"]
    values = kpis["avg_capacity_factor_pct"].astype(float).tolist()

    ax.plot(months, values, marker="o", color="#2196F3", linewidth=2.5, markersize=8)
    ax.fill_between(months, values, alpha=0.1, color="#2196F3")

    ax.set_title("Average Capacity Factor by Month — Q1 2024", fontsize=13, pad=15)
    ax.set_ylabel("Capacity Factor (%)", fontsize=11)
    ax.set_ylim(0, 100)

    for i, val in enumerate(values):
        ax.text(i, val + 1.5, f"{val}%", ha="center", fontsize=9)

    plt.tight_layout()
    path = f"{REPORTS_DIR}/capacity_factor_{REPORT_DATE}.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")

def plot_hourly_profile(generation):
    fig, ax = plt.subplots(figsize=(10, 5))
    hourly = generation.groupby("hour")["generation_mwh"].mean().reset_index()

    ax.plot(hourly["hour"], hourly["generation_mwh"], color="#2196F3",
            linewidth=2.5, marker="o", markersize=5)

    ax.set_title("Average Hourly Generation Profile — Q1 2024", fontsize=13, pad=15)
    ax.set_xlabel("Hour of Day", fontsize=11)
    ax.set_ylabel("Avg Generation (MWh)", fontsize=11)
    ax.set_xticks(range(0, 24))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

    plt.tight_layout()
    path = f"{REPORTS_DIR}/hourly_profile_{REPORT_DATE}.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")

def save_csv_report(kpis):
    path = f"{REPORTS_DIR}/kpi_report_{REPORT_DATE}.csv"
    kpis.to_csv(path, index=False)
    print(f"Saved: {path}")

def generate_report():
    print(f"Generating report for {REPORT_DATE}...\n")
    engine = create_engine(DB_URL)
    generation, kpis = fetch_data(engine)

    plot_monthly_generation(kpis)
    plot_capacity_factor(kpis)
    plot_hourly_profile(generation)
    save_csv_report(kpis)

    print(f"\nReport complete — files saved to {REPORTS_DIR}/")

if __name__ == "__main__":
    generate_report()