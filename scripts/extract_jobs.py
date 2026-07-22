import requests
import json
import time
from pathlib import Path
from datetime import datetime

BASE_URL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v6/jobs"
HEADERS = {"X-API-Key": "jobboerse-jobsuche"}

SEARCH_TERMS = ["Fahrer", "Lieferbote", "Kurier", "Lagerhelfer", "Reinigungskraft"]
LOCATION = "Berlin"
PAGE_SIZE = 25

def fetch_jobs_for_term(term, location):
    all_jobs = []
    page = 1

    while True:
        params = {
            "was": term,
            "wo": location,
            "page": page,
            "size": PAGE_SIZE
        }
        response = requests.get(BASE_URL, headers=HEADERS, params=params)

        if response.status_code != 200:
            print(f"Error fetching page {page} for '{term}': {response.status_code}")
            break

        data = response.json()
        jobs = data.get("ergebnisliste", [])

        if not jobs:
            break

        all_jobs.extend(jobs)
        print(f"  '{term}' - page {page}: got {len(jobs)} jobs (total so far: {len(all_jobs)})")

        max_results = data.get("maxErgebnisse", 0)
        if len(all_jobs) >= max_results or len(jobs) < PAGE_SIZE:
            break

        page += 1
        time.sleep(1)

    return all_jobs

def main():
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for term in SEARCH_TERMS:
        print(f"Fetching jobs for: {term}")
        jobs = fetch_jobs_for_term(term, LOCATION)

        filename = f"data/raw/{term}_{LOCATION}_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)

        print(f"Saved {len(jobs)} jobs to {filename}\n")

if __name__ == "__main__":
    main()
