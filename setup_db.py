import sqlite3

conn = sqlite3.connect('db_temperature.db')
cursor=conn.cursor()
cursor.execute('''

CREATE TABLE IF NOT EXISTS readings (
	device_id text NOT NULL,
	device_name text NOT NULL,
	reading_time int NOT NULL,
	reading_value real NOT NULL
);

''')

cursor.close()
conn.close()