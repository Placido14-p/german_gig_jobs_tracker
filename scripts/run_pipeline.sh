#!/bin/bash
cd /Users/placidopereira/german_gig_jobs_tracker
source venv/bin/activate

echo "=== Pipeline run: $(date) ===" >> logs/pipeline.log

python3 scripts/extract_jobs.py >> logs/pipeline.log 2>&1
python3 scripts/clean_jobs.py >> logs/pipeline.log 2>&1
psql german_gig_jobs -f sql/schema.sql >> logs/pipeline.log 2>&1
python3 scripts/load_to_db.py >> logs/pipeline.log 2>&1

echo "=== Pipeline run complete ===" >> logs/pipeline.log
