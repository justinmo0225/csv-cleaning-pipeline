# CSV Cleaning Pipeline — Data Engineering ETL

This repository contains a small end-to-end ETL (Extract → Transform → Load) pipeline and visualization/reporting utilities built in Python. It's designed as a compact, production-minded example of data engineering best practices: clear stage separation, idempotent loading to a small SQLite warehouse, and automated report generation.

## Project layout

- `main.py` — orchestrates the pipeline and runs visualizations.
- `pipeline/` — ETL stage implementations:
  - `extract.py` — reads the raw CSV into a pandas DataFrame.
  - `transform.py` — normalizes column names, drops duplicates and missing rows.
  - `load.py` — writes the cleaned DataFrame into an SQLite database (`employee.db`) as table `employees`.
- `data/` — data and helpers:
  - `Messy_Employee_dataset.csv` — sample raw dataset used by the pipeline (input).
  - `download_data.py` — helper stub that demonstrates how the dataset could be downloaded from a remote source.
- `visualize.py` — reads the `employees` table from `employee.db`, creates two plots (salary histogram and avg salary by department), writes CSV reports to `reports/`, and produces a PDF report `reports/employee_report.pdf` using ReportLab.
- `reports/` — output artifacts (CSV summaries and generated PDF).
- `employee.db` — SQLite database written by the load stage.

## Data engineering contract

ETL stage contracts (functional, lightweight):

- extract(file_path: str) -> pd.DataFrame
  - Input: path to a CSV file (in this repo `data/Messy_Employee_dataset.csv`).
  - Output: raw DataFrame loaded with pandas.

- transform(df: pd.DataFrame) -> pd.DataFrame
  - Input: DataFrame from `extract`.
  - Behavior: normalizes column names to lowercase with underscores, drops duplicate rows and rows with any missing values.
  - Output: cleaned DataFrame ready to load.

- load(df: pd.DataFrame, db_name: str = "employee.db", table_name: str = "employees") -> None
  - Input: cleaned DataFrame.
  - Behavior: writes DataFrame to the specified SQLite database and table (replaces table if exists).

Success criteria: After running `main.py`, the SQLite DB contains a fully replaced `employees` table and the `reports/` folder contains:

- `cleaned_data.csv`
- `summary_stats.csv`
- `department_salary.csv`
- `status_distribution.csv`
- `employee_report.pdf`

## How to run (macOS / zsh)

1. Create and activate a Python 3.9+ virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies (see notes below for a minimal list):

```bash
pip install pandas matplotlib reportlab
```

3. Run the ETL + visuals by executing the orchestrator:

```bash
python main.py
```

Notes:
- `main.py` expects the CSV to exist at `data/messy_employee_dataset.csv` (case-insensitive in some OSs but keep the path exact). If you have the sample CSV named `Messy_Employee_dataset.csv`, either rename it or update `FILE_PATH` in `main.py`.
- On macOS, matplotlib's `plt.show()` will open a window. If running on a headless server, set the backend to a non-interactive backend (e.g., `Agg`) before importing `matplotlib.pyplot`.

## Dependencies

- Python 3.9+ (project was run in a 3.9 environment).
- pandas
- matplotlib
- reportlab

Optional (if you plan to pull data from Kaggle):
- `kaggle` or any dataset downloader; `data/download_data.py` contains an example stub.

You can create a `requirements.txt` with:

```text
pandas
matplotlib
reportlab
```

## Schema / columns

After `transform` the columns are normalized to lowercase/underscore format. Expected final columns (examples taken from the sample output):

- `employee_id`, `first_name`, `last_name`, `age`, `department_region`, `status`, `join_date`, `salary`, `email`, `phone`, `performance_score`, `remote_work`, `department`

Notes:
- `department` is inferred in `visualize.py` from `department_region` by splitting on `-` and taking the department prefix.

## Edge cases & assumptions

- The `transform` step drops any row with a missing value. That is a design choice for simplicity. In a production pipeline you may want to impute or only drop rows for critical fields.
- Duplicate rows are removed by `drop_duplicates()` — if you need deduplication logic based on keys prefer `drop_duplicates(subset=[...])`.
- Phone numbers in the sample look like malformed negative integers; the repository preserves the source numeric form but you may want to cast/format as strings and validate.
- `remote_work` in the raw CSV is a boolean-like column (`TRUE`/`FALSE`); after pandas parsing it becomes 1/0 or boolean depending on read behavior. `transform` currently doesn't coerce types beyond column name normalization.

## Quality gates & verification

Quick checks after running `main.py`:

- Confirm `employee.db` contains table `employees` (use `sqlite3 employee.db` → `.tables`).
- Open `reports/summary_stats.csv` to verify basic numerical summaries.
- Confirm `reports/employee_report.pdf` is generated.

Suggested automated checks to add:

- Unit tests for `pipeline.extract.extract`, `pipeline.transform.transform` and `pipeline.load.load` (use pytest and create small fixture CSVs).
- A smoke test that runs the pipeline on a small sample and asserts the DB table row count > 0 and report files were written.

## Troubleshooting

- FileNotFoundError for the CSV: check `main.py` FILE_PATH variable and confirm `data/` filename casing.
- ImportError for ReportLab or pandas: install dependencies into your active environment.
- SQLite locked error: ensure no other process is holding `employee.db` open (e.g., a DB browser). Close other clients and retry.

## Next steps / improvements (data-engineering focused)

- Add a small test suite (pytest) with unit and integration tests for the pipeline stages.
- Replace SQLite with a persistent warehouse (Postgres) or cloud object store + metadata for larger datasets.
- Add logging (structured) and observability: execution time per stage, row counts before/after transforms, error handling.
- Add schema validation (e.g., pandera or Great Expectations) before load to enforce types and ranges.
- Make the pipeline idempotent and configurable via CLI args or a lightweight config (path names, db settings, drop/append mode).
- Add streaming/batch support for larger datasets and chunked reads/writes.

## Contact / ownership

This repository is a compact demo of an ETL pipeline and reporting flow. If you want help extending the pipeline for production use (CI, tests, schema checks, deployment, or switching to Postgres/S3), open an issue or request specific changes.

---
