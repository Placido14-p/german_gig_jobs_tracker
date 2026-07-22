DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS locations;

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name TEXT UNIQUE NOT NULL
);

CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    plz TEXT,
    ort TEXT,
    strasse TEXT,
    UNIQUE (plz, ort, strasse)
);

CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,
    titel TEXT,
    firma TEXT,
    vollzeit BOOLEAN,
    verguetungsangabe TEXT,
    festgehalt NUMERIC,
    gehaltsspanne_von NUMERIC,
    gehaltsspanne_bis NUMERIC,
    veroeffentlicht_am DATE,
    eintritt_von DATE,
    entfernung_km NUMERIC,
    quereinstieg_geeignet BOOLEAN,
    category_id INTEGER REFERENCES categories(category_id),
    location_id INTEGER REFERENCES locations(location_id)
);
