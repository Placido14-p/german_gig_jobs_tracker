import json
import glob
import pandas as pd
from pathlib import Path

def load_all_raw_jobs():
    """Load and combine all raw JSON files from data/raw/"""
    all_jobs = []
    files = glob.glob("data/raw/*.json")
    print(f"Found {len(files)} raw files to process")

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            jobs = json.load(f)
            all_jobs.extend(jobs)

    print(f"Total raw job records loaded: {len(all_jobs)}")
    return all_jobs

def extract_fields(job):
    """Pull out the useful fields from one raw job record into a flat structure."""
    location = {}
    if job.get("stellenlokationen"):
        location = job["stellenlokationen"][0].get("adresse", {})

    return {
        "referenznummer": job.get("referenznummer"),
        "titel": job.get("stellenangebotsTitel"),
        "hauptberuf": job.get("hauptberuf"),
        "firma": job.get("firma"),
        "vollzeit": job.get("arbeitszeitVollzeit"),
        "verguetungsangabe": job.get("verguetungsangabe"),
        "festgehalt": job.get("festgehalt"),
        "gehaltsspanne_von": job.get("gehaltsspanneVon"),
        "gehaltsspanne_bis": job.get("gehaltsspanneBis"),
        "plz": location.get("plz"),
        "ort": location.get("ort"),
        "strasse": location.get("strasse"),
        "veroeffentlicht_am": job.get("datumErsteVeroeffentlichung"),
        "eintritt_von": job.get("eintrittszeitraum", {}).get("von"),
        "entfernung_km": job.get("entfernung"),
        "quereinstieg_geeignet": job.get("quereinstiegGeeignet"),
    }

def main():
    raw_jobs = load_all_raw_jobs()

    cleaned_records = [extract_fields(job) for job in raw_jobs]
    df = pd.DataFrame(cleaned_records)

    print(f"Rows before dedup: {len(df)}")
    df = df.drop_duplicates(subset="referenznummer")
    print(f"Rows after dedup: {len(df)}")

    df["veroeffentlicht_am"] = pd.to_datetime(df["veroeffentlicht_am"], errors="coerce")
    df["eintritt_von"] = pd.to_datetime(df["eintritt_von"], errors="coerce")

    Path("data/clean").mkdir(parents=True, exist_ok=True)
    output_path = "data/clean/gig_jobs_berlin.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved cleaned data to {output_path}")
    print(df.head())

if __name__ == "__main__":
    main()
