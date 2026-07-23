# /// script
# requires-python = ">=3.10"
# dependencies = ["duckdb", "pyarrow"]
# ///
"""s3 — one-time prep over the downloaded open-jobs parquet.

1. Integrity check (row count, columns present).
2. data/company_job_counts.parquet — open-postings count per (ats, company);
   the "company small enough for a fractional CTO" guard used by s4.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib_common import DATA, say

import duckdb

PARQUET = DATA / "open-jobs.parquet"
COUNTS = DATA / "company_job_counts.parquet"


def main():
    if not PARQUET.exists():
        sys.exit("open-jobs.parquet not downloaded yet")
    con = duckdb.connect()
    cols = [r[0] for r in con.execute(
        f"DESCRIBE SELECT * FROM read_parquet('{PARQUET}')").fetchall()]
    need = {"id", "ats", "company", "url", "title", "jd_markdown",
            "title_embedding", "jd_embedding", "country_code", "level",
            "function", "company_does", "industry", "company_stage"}
    missing = need - set(cols)
    if missing:
        sys.exit(f"parquet missing expected columns: {missing}")
    n = con.execute(f"SELECT count(*) FROM read_parquet('{PARQUET}')").fetchone()[0]
    say(f"Dataset OK: {n:,} job rows, {len(cols)} columns")

    say("Counting open postings per company…")
    con.execute(f"""
        COPY (
            SELECT ats, company, count(*) AS open_jobs
            FROM read_parquet('{PARQUET}')
            GROUP BY ats, company
        ) TO '{COUNTS}' (FORMAT parquet)
    """)
    nc = con.execute(f"SELECT count(*) FROM read_parquet('{COUNTS}')").fetchone()[0]
    say(f"Done: {nc:,} companies counted -> {COUNTS.name}")


if __name__ == "__main__":
    main()
