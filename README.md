# German Gig Jobs Tracker

A data pipeline that extracts, cleans, and analyzes entry-level and gig-economy job postings in Berlin, using Germany's official job search API (Bundesagentur für Arbeit).

## Motivation

When I first arrived in Germany, I struggled to find openings for survival jobs (delivery, warehouse work, cleaning) despite these roles being in high demand. This project builds the tool I wish I'd had: a structured, queryable view into where these opportunities actually are.

## What it does

1. **Extract** - Pulls job postings across several entry-level categories (driver, courier, warehouse helper, cleaner) from the Bundesagentur fur Arbeit's Jobsuche API, handling pagination across thousands of listings.
2. **Clean** - Deduplicates and standardizes raw JSON into a structured dataset (pandas), handling messy/missing fields.
3. **Load** - Loads cleaned data into a normalized PostgreSQL database with three linked tables: jobs, categories, and locations.
4. **Analyze** - SQL queries answer real questions: which categories and districts have the most openings, pay ranges, full-time vs part-time split, career-changer friendliness, and posting trends over time.

## Tech stack

Python (requests, pandas, psycopg2), PostgreSQL, SQL

## Key findings

- Berufskraftfahrer/in (professional driver) is by far the most common entry-level category (654 postings), followed by cleaning roles (413).
- Postal code 10587 (Berlin-Charlottenburg) has the highest concentration of entry-level openings.
- Hourly pay is fairly consistent across categories (approx 14-16.50 EUR/hr), suggesting most of these roles sit near minimum wage.
- Only about 17% of postings are explicitly marked as open to career changers (Quereinstieg) - useful signal for newcomers without local experience.
- A single staffing agency (PerZukunft Arbeitsvermittlung) accounts for nearly half of all postings, highlighting how much of this market runs through intermediaries rather than direct employers.

## Data engineering challenges solved

- Silent join failure: location joins were returning 0 matches. Root cause was a float/string type mismatch - postal codes were stored as floats in the source data but as strings in the database, so identical values never matched during lookup. Fixed by enforcing consistent string typing before matching.
- Mixed pay units: hourly wages and annual salaries were stored in the same field, producing meaningless averages (e.g. 376 EUR/hour). Fixed by filtering analysis queries by the postings' actual pay-type field before aggregating.

## Project structure

- data/raw/ - Raw JSON pulled from the API
- data/clean/ - Cleaned, deduplicated CSV
- scripts/extract_jobs.py - API extraction with pagination
- scripts/clean_jobs.py - Cleaning and deduplication
- scripts/load_to_db.py - Loads cleaned data into PostgreSQL
- sql/schema.sql - Database schema (3 normalized tables)
- sql/analysis_queries.sql - Analysis queries answering key questions

## How to run it

1. Install dependencies: pip install -r requirements.txt
2. Create a PostgreSQL database: createdb german_gig_jobs
3. Run the pipeline in order:
   - python3 scripts/extract_jobs.py
   - python3 scripts/clean_jobs.py
   - psql german_gig_jobs -f sql/schema.sql
   - python3 scripts/load_to_db.py
4. Run the analysis: psql german_gig_jobs -f sql/analysis_queries.sql

## Data source

Bundesagentur fur Arbeit Jobsuche API (https://jobsuche.api.bund.dev/) - Germany's official federal employment agency job search service.
