import sqlite3

conn = sqlite3.connect("db_temperature.db")
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS readings (
        device_id text NOT NULL,
        device_name text NOT NULL,
        reading_time int NOT NULL,
        reading_value real NOT NULL
    );
    """
)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS operational_data (
        key text PRIMARY KEY,
        value real
    );
    """
)
cursor.execute(
    """
    INSERT INTO operational_data(key, value)
    VALUES ('last_error_log', NULL) ON CONFLICT DO NOTHING;
    """
)

cursor.close()
conn.commit()
conn.close()
