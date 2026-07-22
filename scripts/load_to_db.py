import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

DB_NAME = "german_gig_jobs"

def get_connection():
    return psycopg2.connect(dbname=DB_NAME)

def load_categories(df, cur):
    categories = df["hauptberuf"].dropna().unique().tolist()
    execute_values(
        cur,
        "INSERT INTO categories (category_name) VALUES %s ON CONFLICT DO NOTHING",
        [(c,) for c in categories]
    )
    print(f"Inserted {len(categories)} categories")

def load_locations(df, cur):
    locations = df[["plz", "ort", "strasse"]].drop_duplicates().values.tolist()
    execute_values(
        cur,
        "INSERT INTO locations (plz, ort, strasse) VALUES %s ON CONFLICT DO NOTHING",
        locations
    )
    print(f"Inserted {len(locations)} locations")

def load_jobs(df, cur):
    cur.execute("SELECT category_id, category_name FROM categories")
    category_map = {name: cid for cid, name in cur.fetchall()}

    cur.execute("SELECT location_id, plz, ort, strasse FROM locations")
    location_map = {}
    for lid, plz, ort, strasse in cur.fetchall():
        location_map[(plz, ort, strasse)] = lid

    job_rows = []
    for _, row in df.iterrows():
        cat_id = category_map.get(row["hauptberuf"])
        loc_key = (row["plz"], row["ort"], row["strasse"])
        loc_id = location_map.get(loc_key)
        job_rows.append((
            row["referenznummer"],
            row["titel"],
            row["firma"],
            row["vollzeit"] if pd.notna(row["vollzeit"]) else None,
            row["verguetungsangabe"],
            row["festgehalt"] if pd.notna(row["festgehalt"]) else None,
            row["gehaltsspanne_von"] if pd.notna(row["gehaltsspanne_von"]) else None,
            row["gehaltsspanne_bis"] if pd.notna(row["gehaltsspanne_bis"]) else None,
            row["veroeffentlicht_am"] if pd.notna(row["veroeffentlicht_am"]) else None,
            row["eintritt_von"] if pd.notna(row["eintritt_von"]) else None,
            row["entfernung_km"] if pd.notna(row["entfernung_km"]) else None,
            row["quereinstieg_geeignet"] if pd.notna(row["quereinstieg_geeignet"]) else None,
            cat_id,
            loc_id
        ))

    insert_sql = """INSERT INTO jobs (job_id, titel, firma, vollzeit, verguetungsangabe,
        festgehalt, gehaltsspanne_von, gehaltsspanne_bis, veroeffentlicht_am,
        eintritt_von, entfernung_km, quereinstieg_geeignet, category_id, location_id)
        VALUES %s ON CONFLICT (job_id) DO NOTHING"""
    execute_values(cur, insert_sql, job_rows)
    print(f"Inserted {len(job_rows)} jobs")

def main():
    df = pd.read_csv("data/clean/gig_jobs_berlin.csv")
    print(f"Loaded {len(df)} rows from CSV")

    conn = get_connection()
    cur = conn.cursor()

    load_categories(df, cur)
    conn.commit()

    load_locations(df, cur)
    conn.commit()

    load_jobs(df, cur)
    conn.commit()

    cur.close()
    conn.close()
    print("Done!")

if __name__ == "__main__":
    main()
