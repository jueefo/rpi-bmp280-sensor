import argparse
import RPi.GPIO as GPIO
import smbus2
import bme280
import time
from datetime import datetime

"""
pip install smbus2
pip install rpi.bme280
"""

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
address = 0x76
calibration_params = bme280.load_calibration_params(bus, address)


def get_sensor_data():
    try:
        data = bme280.sample(bus, address, calibration_params)
        temperature = data.temperature
        pressure = data.pressure
        return temperature, pressure
    except Exception as e:
        print(f"Error reading sensor data: {e}")
        return None, None


# # Sensing runtime in seconds
# runtime = 10
# # Polling interval in seconds
# interval = 1

# Start the run
start_time = time.time()
while args.runtime == 0 or time.time() - start_time < args.runtime:
    temperature, pressure = get_sensor_data()

    # Blink the LED
    GPIO.output(output_pin, GPIO.HIGH)

    time.sleep(args.interval/2)
    GPIO.output(output_pin, GPIO.LOW)
    time.sleep(args.interval/2)

    if temperature is not None and pressure is not None:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        temperature_formatted = f"{temperature:.2f}"
        pressure_formatted = f"{int(pressure)}"
        print(
            f"Time: {current_time}, Temperature: {temperature_formatted} °C, Pressure: {pressure_formatted} mbar")
    else:
        print("Sensor data not available due to error.")


# Clean up GPIO
GPIO.output(output_pin, GPIO.LOW)
GPIO.cleanup()
print("Kaikki toimii okej.")
