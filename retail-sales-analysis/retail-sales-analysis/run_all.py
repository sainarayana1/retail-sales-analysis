"""Run the whole pipeline:  python run_all.py"""
import subprocess, sys
steps = ["01_generate_data", "02_clean_data", "03_load_to_sqlite", "04_run_queries", "05_analysis_charts", "06_build_excel"]
import os
if os.path.exists("data/superstore_raw.csv") and "--regen" not in sys.argv:
    steps = steps[1:]; print("Found data/superstore_raw.csv - skipping data generation (use --regen to recreate)")
for s in steps:
    print(f"\n########## {s} ##########")
    if subprocess.run([sys.executable, f"scripts/{s}.py"]).returncode != 0:
        sys.exit(f"Step {s} failed")
print("\nDONE. Next: build the Power BI dashboard using powerbi/POWERBI_GUIDE.md")
