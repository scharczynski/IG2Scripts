CREATE SCHEMA IF NOT EXISTS ig2;

CREATE TABLE IF NOT EXISTS hour_meter
(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  time TIMESTAMP NOT NULL,
  analog REAL,
  int INTEGER,
  digital BOOLEAN,
  string TEXT,
  float_seq REAL[]
);
