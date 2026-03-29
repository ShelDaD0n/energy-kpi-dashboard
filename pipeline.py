import schedule
import time
import subprocess
import sys
from datetime import datetime

def run_step(script_name):
    print(f"\n--- Running {script_name} ---")
    result = subprocess.run(
        [sys.executable, script_name],
        capture_output=True,
        text=True
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"STDERR: {result.stderr}")
    if result.returncode != 0:
        print(f"ERROR: {script_name} failed with return code {result.returncode}")
        return False
    return True

def run_pipeline():
    start = datetime.now()
    print(f"========================================")
    print(f"Pipeline started at {start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"========================================")

    steps = [
        "fetch_data.py",
        "clean_data.py",
        "load_db.py",
        "kpi_calculator.py",
        "generate_report.py"
    ]

    for step in steps:
        success = run_step(step)
        if not success:
            print(f"\nPipeline stopped at {step}. Fix the error and re-run.")
            return

    end = datetime.now()
    duration = (end - start).seconds
    print(f"\n========================================")
    print(f"Pipeline complete at {end.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total runtime: {duration} seconds")
    print(f"========================================")

def schedule_pipeline():
    print("Scheduler started — pipeline will run daily at 08:00")
    print("Press Ctrl+C to stop\n")
    schedule.every().day.at("08:00").do(run_pipeline)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--schedule":
        schedule_pipeline()
    else:
        run_pipeline()