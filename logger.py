from pathlib import Path
import sqlite3
import time

sensor_mapping={
	'28-3c01d6074879':'Speicher_Oben',
	'28-3c01d607152b':'Speicher_Mitte',
	'28-3c01d607cdd0':'Solar_VL',
	'28-3c01d6076837':'Solar_RL',
	'28-3c01d607b233':'Fußbodenheizung_VL_vM',
	'28-3c01d60753fe':'Fußbodenheizung_VL_nM',
	'28-3c01d607666e':'Fußbodenheizung_RL_vM',
	'28-3c01d6075bd4':'Fußbodenheizung_RL_nM',
	'28-3c01d6078f50':'Warmwasser_VL',
	'28-3c01d6070050':'Raumtemperatur',
}

def read_temp(device_id):
	sensor_output=Path(f'/sys/bus/w1/devices/{device_id}/w1_slave').read_text()
	sensor_temperature=int(sensor_output.split('t=')[1])/1000
	return sensor_temperature

def save_to_db(cursor, device_id, device_name, temperature):
	print(device_id, device_name, temperature)
	cursor.execute(f'''
	INSERT INTO readings(device_id, device_name, reading_time, reading_value)
	VALUES ('{device_id}','{device_name}',{int(time.time())},{temperature})
	''')

def main():
	conn = sqlite3.connect('db_temperature.db')
	cursor=conn.cursor()
	for device_id, device_name in sensor_mapping.items():
		save_to_db(cursor, device_id, device_name, read_temp(device_id))
	conn.commit()
	cursor.close()
	conn.close()

main()

