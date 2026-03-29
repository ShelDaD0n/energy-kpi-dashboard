# Energy KPI Dashboard
*By Sheldon Muriuki*
An automated data pipeline that fetches hourly electricity generation data from the U.S. Energy Information Administration (EIA) API, processes it, loads it into PostgreSQL, calculates energy KPIs, and generates dated reports with charts — on a daily schedule.

Built as a portfolio project targeting data engineering roles in the renewable energy sector.

---

## What it does

- Fetches real hourly net generation data for California's grid from the EIA API
- Cleans and transforms raw data using Pandas, engineering features like capacity factor, rolling averages, and daily totals
- Loads cleaned data into a PostgreSQL database using SQLAlchemy
- Calculates four energy KPIs: total MWh generated, average capacity factor, estimated revenue, and peak generation hour
- Auto-generates dated CSV reports and three charts using Matplotlib
- Runs the full pipeline in a single command, with an optional daily scheduler

---

## KPIs tracked

| KPI | Description |
|-----|-------------|
| Total generation (MWh) | Sum of hourly net generation per month |
| Avg capacity factor (%) | Average hourly output vs. peak observed output |
| Estimated revenue (USD) | Total MWh × $45/MWh market rate |
| Peak generation hour | Hour of day with highest average output |

---

## Sample output

**Q1 2024 — California Grid**

| Month | Total MWh | Avg Capacity Factor | Estimated Revenue |
|-------|-----------|-------------------|-------------------|
| January | 18,677,120 | 76.66% | $840,470,400 |
| February | 16,281,324 | 71.44% | $732,659,580 |
| March | 16,706,875 | 68.58% | $751,809,375 |

---

## Tech stack

- Python 3.12
- Pandas — data cleaning and feature engineering
- Requests — EIA API calls
- SQLAlchemy + psycopg2 — PostgreSQL integration
- Matplotlib — chart generation
- Schedule — pipeline automation
- PostgreSQL — data warehouse

---

## How to run

**1. Clone the repo**
```bash
git clone https://github.com/ShelDaD0n/energy-kpi-dashboard.git
cd energy-kpi-dashboard
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your EIA API key**

Create a `.env` file in the project root:
```
EIA_API_KEY=your_key_here
```
Get a free key at: https://www.eia.gov/opendata/register.php

**4. Create the database**
```bash
psql -c "CREATE DATABASE energy_db;"
```

**5. Run the pipeline**
```bash
python3 pipeline.py
```

**6. Run on a daily schedule**
```bash
python3 pipeline.py --schedule
```

Reports are saved to `data/reports/` with the date in the filename.

---

## Project structure
```
energy-kpi-dashboard/
├── fetch_data.py        # Pull hourly generation data from EIA API
├── clean_data.py        # Clean, transform, and engineer features
├── load_db.py           # Load data into PostgreSQL, run SQL queries
├── kpi_calculator.py    # Calculate KPIs and save to database
├── generate_report.py   # Generate charts and CSV reports
├── pipeline.py          # Run full pipeline, with optional scheduler
├── requirements.txt     # Python dependencies
└── data/
    ├── raw_generation.csv
    ├── cleaned_generation.csv
    ├── kpi_summary.csv
    └── reports/         # Dated chart PNGs and CSV reports
```