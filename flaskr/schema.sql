DROP TABLE IF EXISTS location;

CREATE TABLE location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    total_properties INTEGER NOT NULL,
    average_rent INTEGER,
    rent_under_250 INTEGER NOT NULL,
    rent_250_to_500 INTEGER NOT NULL
);