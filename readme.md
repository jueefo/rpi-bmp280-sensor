# Raspberry Pi Sensor Reader

Raspberry Pi Sensor Reader is a Python program that reads temperature and air pressure data from a BMP280 sensor and blinks an LED. If using a BME280 sensor, humidity is also measured. You can customize the measurement interval and runtime using command-line parameters.

## Installation

1. Clone this Git repository to your Raspberry Pi device:

```bash
git clone https://github.com/jueefo/rpi-bmp280-sensor
```

2. Navigate to the project's root directory:
```bash
cd rpi-bmp280-sensor
```

3. Install the necessary dependencies using the requirements.txt file:
```bash
pip install -r requirements.txt
```

## Usage

Using the program is straightforward from the command line. You can customize the measurement interval and runtime as follows:
```bash
python bmp280_sensor_reader.py --interval 2 --runtime 60
```
- `--interval` specifies the measurement interval in seconds.
- `--runtime` specifies the runtime in seconds. Set it to `0` to run the program indefinitely.

The program measures temperature and air pressure at the specified intervals and blinks the LED during each measurement cycle.

## SQLite Database Usage

The program stores sensor readings in an SQLite database (`sensor_data.db`).
- A table named `sensor_data` is created if it does not exist.
- Each measurement cycle records a new entry with:
  - `timestamp`: The time of the measurement.
  - `temperature`: Measured temperature in Celsius.
  - `pressure`: Measured air pressure in mbar.
  - `humidity`: Measured humidity percentage (only if using a BME280 sensor).
- The data is logged and stored automatically at each measurement interval.


## Troubleshooting

If you encounter issues with the program, consider the following:
- Ensure that the BMP280 sensor is correctly connected to the Raspberry Pi.
- Check the SQLite database (`sensor_data.db`) using an SQLite viewer or command-line tool to verify recorded data.

### I2C Speed Adjustment

To improve communication stability, the I2C bus speed has been reduced to 10 kHz (default is 100 kHz). To apply this setting, add the following line to the `/boot/config.txt` file:

```bash
dtparam=i2c_arm_baudrate=10000
```

After modifying the file, reboot your Raspberry Pi for the changes to take effect.
