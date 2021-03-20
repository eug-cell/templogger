# templogger

RaspberryPi temperature logger 

## setup

Add to `/boot/config.txt`

```txt
dtoverlay=w1-gpio
gpiopin=4
pullup=on
```

To creat a new database run following commands: `python3 setup_db.py`
This is only necessary if no database exists previously

## check database manually (sqlite3)

To check the database manually run following command: `sqlite3 db_temperature.db`
This will open the SQL console. In this you can run any SQL command. For example the following:

```txt
.headers on 
select * from readings;
```

## setup regular excecution

To run a script in a regualr interval (e.g. every 5 min) we use the programm `cron`.
To set this up run the following command: `crontab -e`
And paste following text if it doesn´t exist already: `*/5 * * * * cd /home/pi/templogger && python3 logger.py`
