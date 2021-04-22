import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sqlite3
import time

DB_PATH = "./db_temperature.db"
ERROR_LOG_PATH = "./error.log"

sensor_mapping = {
    "28-3c01d6074879": "Speicher_Oben",
    "28-3c01d607152b": "Speicher_Mitte",
    "28-3c01d607cdd0": "Solar_VL",
    "28-3c01d6076837": "Solar_RL",
    "28-3c01d607b233": "Fußbodenheizung_VL_vM",
    "28-3c01d60753fe": "Fußbodenheizung_VL_nM",
    "28-3c01d607666e": "Fußbodenheizung_RL_vM",
    "28-3c01d6075bd4": "Fußbodenheizung_RL_nM",
    "28-3c01d6078f50": "Warmwasser_VL",
    "28-3c01d6070050": "Raumtemperatur",
}

# add a logger that writes to a file that does not grow above 1MB
logger = logging.getLogger(__name__)
# delay=True avoids updating the "last modified time" of the log in case
# no errors happen
handler = RotatingFileHandler("error.log", maxBytes=1_000_000, backupCount=1, delay=True)
handler.setFormatter(
    logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
)
logger.addHandler(handler)


def read_temp(device_id):
    sensor_output = Path(f"/sys/bus/w1/devices/{device_id}/w1_slave").read_text()
    sensor_temperature = int(sensor_output.split("t=")[1]) / 1000
    return sensor_temperature


def save_temperature_to_db(cursor, device_id, device_name, temperature):
    print(device_id, device_name, temperature)
    cursor.execute(
        f"""
        INSERT INTO readings(device_id, device_name, reading_time, reading_value)
        VALUES ('{device_id}','{device_name}',{int(time.time())},{temperature})
        """
    )


def save_error_status_to_db(cursor):
    err_log = Path(ERROR_LOG_PATH)
    if not err_log.exists():
        err_log.touch()

    err_log_data = err_log.stat()
    print(
        f"The error log size {err_log_data.st_size:,} bytes large "
        f"and was last modified at {err_log_data.st_mtime}"
    )

    error_time = 0 if err_log_data.st_size == 0 else err_log_data.st_mtime
    cursor.execute(
        f"UPDATE operational_data SET value = {error_time} WHERE key = 'last_error_log'"
    )


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for device_id, device_name in sensor_mapping.items():
        save_temperature_to_db(cursor, device_id, device_name, read_temp(device_id))
        conn.commit()

    save_error_status_to_db(cursor)
    conn.commit()

    cursor.close()
    conn.close()


try:
    main()
except Exception as exc:
    logger.error(f"Exception: {exc}")
    raise
