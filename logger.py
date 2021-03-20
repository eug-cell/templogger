from pathlib import Path

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



def main():
	print(read_temp('28-3c01d6074879'))

main()
