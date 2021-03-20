from pathlib import Path
import sqlite3
import time

sensor_mapping={
	'28-3c01d6074879':'Vorlauf_Solar',
	'28-3c01d6076837':'Rücklauf_Solar',
	'28-3c01d607b233':'Vorlauf_Speicher',  
	'28-3c01d60753fe':'Mitte_Speicher',   
	'28-3c01d6078f50':'Rücklauf_Speicher',    
	'28-3c01d607cdd0':'Vorlauf_Fußbodenheizung',  
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

