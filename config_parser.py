import os
import json
import sqlite3
from configparser import ConfigParser, MissingSectionHeaderError
from flask import Flask, jsonify, abort

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
CONFIG_PATH = "config.ini"          # path to the INI file
DB_PATH = "config_data.db"          # SQLite file
TABLE_NAME = "config_store"         # table that holds the JSON blob

# ----------------------------------------------------------------------
# Helper: initialise / connect to SQLite DB
# ----------------------------------------------------------------------
def init_db(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            json_data TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn

# ----------------------------------------------------------------------
# Helper: read and parse the INI file
# ----------------------------------------------------------------------
def parse_config(file_path: str = CONFIG_PATH) -> dict:
    """
    Returns a nested dict {section: {key: value, ...}, ...}
    Raises FileNotFoundError or ValueError on problems.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Configuration file '{file_path}' not found.")

    parser = ConfigParser()
    try:
        parser.read(file_path)
    except MissingSectionHeaderError as exc:
        raise ValueError(f"Invalid INI format: {exc}")

    config_dict = {section: dict(parser.items(section)) for section in parser.sections()}
    return config_dict

# ----------------------------------------------------------------------
# Helper: store JSON in SQLite
# ----------------------------------------------------------------------
def store_config(conn: sqlite3.Connection, data: dict) -> None:
    json_blob = json.dumps(data)
    # Replace any existing row (we keep only the latest config)
    conn.execute(f"DELETE FROM {TABLE_NAME}")
    conn.execute(f"INSERT INTO {TABLE_NAME} (json_data) VALUES (?)", (json_blob,))
    conn.commit()

# ----------------------------------------------------------------------
# Flask app – GET endpoint to fetch stored config as JSON
# ----------------------------------------------------------------------
app = Flask(__name__)

@app.route("/config", methods=["GET"])
def get_config():
    try:
        cur = app.config["DB_CONN"].cursor()
        cur.execute(f"SELECT json_data FROM {TABLE_NAME} LIMIT 1")
        row = cur.fetchone()
        if row is None:
            abort(404, description="No configuration stored in the database.")
        return jsonify(json.loads(row[0]))
    except Exception as exc:
        abort(500, description=str(exc))

# ----------------------------------------------------------------------
# Main routine – parse, store, then start the API
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # 1️⃣ Parse the configuration file
    try:
        config_data = parse_config()
        print("Configuration File Parser Results:")
        for sect, kv in config_data.items():
            print(f"{sect}:")
            for k, v in kv.items():
                print(f"  - {k}: {v}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        exit(1)

    # 2️⃣ Save JSON to SQLite
    try:
        db_conn = init_db()
        store_config(db_conn, config_data)
        print(f"\nConfiguration saved to SQLite database '{DB_PATH}'.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        exit(1)

    # 3️⃣ Attach DB connection to Flask app and run the server
    app.config["DB_CONN"] = db_conn
    print("\nStarting Flask API – GET http://localhost:5000/config")
    app.run(host="0.0.0.0", port=5000)