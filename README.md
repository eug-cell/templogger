# Templogger

RaspberryPi temperature logger

## Setup

Add to `/boot/config.txt`

```txt
dtoverlay=w1-gpio
gpiopin=4
pullup=on
```

To create a new database run following command: `python3 setup_db.py`
This is only necessary if no database exists previously or a new table is addded.

## Check Database Manually (sqlite3)

To check the database manually run following command: `sqlite3 db_temperature.db`
This will open the SQL console. In this you can run any SQL command. For example the following:

```txt
.headers on 
select * from readings;
```

## Setup Regular Execution

To run a script in a regular interval (e.g. every 5 min) we use the program `cron`.
To set this up run the following command: `crontab -e`
And paste following text if it does not exist already: `*/5 * * * * cd /home/pi/templogger && python3 logger.py`
