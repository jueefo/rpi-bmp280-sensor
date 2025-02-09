import argparse
import RPi.GPIO as GPIO
import smbus2
import bme280
import time
from datetime import datetime
import sqlite3
import logging

# Set the logging level
logging.basicConfig(level=logging.INFO)

# Initialize argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--runtime", type=int, default=10,
                    help="Sensing runtime in seconds (default: 10). Set to 0 to run indefinitely.")
parser.add_argument("--interval", type=int, default=1,
                    help="Measurement interval in seconds (default: 1)")
args = parser.parse_args()

# Set the GPIO mode to GPIO.BOARD and setup for LED control
GPIO.setmode(GPIO.BOARD)
output_pin = 37
GPIO.setup(output_pin, GPIO.OUT)

# Initialize the I2C bus and open the BMP280 sensor
bus = smbus2.SMBus(1)
address = 0x77
calibration_params = bme280.load_calibration_params(bus, address)

# Initialize SQLite database
conn = sqlite3.connect('sensor_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
             id INTEGER PRIMARY KEY,
             timestamp TEXT,
             temperature REAL,
             pressure REAL,
             humidity REAL)''')
conn.commit()


def get_sensor_data():
    try:
        data = bme280.sample(bus, address, calibration_params)
        return data.temperature, data.pressure, data.humidity
    except Exception as e:
        logging.error(f"Error reading sensor data: {e}")
        return None, None, None


def save_to_db(timestamp, temperature, pressure, humidity):
    try:
        c.execute("INSERT INTO sensor_data (timestamp, temperature, pressure, humidity) VALUES (?, ?, ?, ?)",
                  (timestamp, temperature, pressure, humidity))
        conn.commit()
    except Exception as e:
        logging.error(f"Error saving data to database: {e}")


# Start the run
start_time = time.time()

try:
    while args.runtime == 0 or time.time() - start_time < args.runtime:
        temperature, pressure, humidity = get_sensor_data()

        # Blink the LED
        GPIO.output(output_pin, GPIO.HIGH)
        time.sleep(args.interval / 2)
        GPIO.output(output_pin, GPIO.LOW)
        time.sleep(args.interval / 2)

        if temperature is not None and pressure is not None and humidity is not None:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(
                f"Time: {current_time}, Temperature: {temperature:.2f} °C, Pressure: {int(pressure)} mbar, Humidity: {humidity:.2f}%")
            save_to_db(current_time, temperature, pressure, humidity)
        else:
            logging.warning("Sensor data not available due to error.")
except KeyboardInterrupt:
    logging.info("Program interrupted by user.")
finally:
    # Clean up GPIO and close the database connection
    GPIO.output(output_pin, GPIO.LOW)
    GPIO.cleanup()
    conn.close()
    logging.info("Cleaned up GPIO and closed the database connection.")
